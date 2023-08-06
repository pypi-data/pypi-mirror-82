import os
import sys
import traceback
import warnings

import pytest
import numpy as np

import theano
import theano.tensor as tt

from theano import config, scalar
from theano.gof import Apply, Op, utils
from theano.tensor.basic import _allclose


# Used in TestComputeTestValue.test_no_perform
class IncOneC(Op):
    """
    An Op with only a C (c_code) implementation
    """

    __props__ = ()

    def make_node(self, input):
        input = scalar.as_scalar(input)
        output = input.type()
        return Apply(self, [input], [output])

    def c_code_cache_version(self):
        return (1,)

    def c_code(self, node, name, inputs, outputs, sub):
        (x,) = inputs
        (z,) = outputs
        return "%(z)s = %(x)s + 1;" % locals()


class TestComputeTestValue:
    @theano.change_flags(compute_test_value="raise")
    def test_variable_only(self):
        x = tt.matrix("x")
        x.tag.test_value = np.random.rand(3, 4).astype(config.floatX)
        y = tt.matrix("y")
        y.tag.test_value = np.random.rand(4, 5).astype(config.floatX)

        # should work
        z = tt.dot(x, y)
        assert hasattr(z.tag, "test_value")
        f = theano.function([x, y], z)
        assert _allclose(f(x.tag.test_value, y.tag.test_value), z.tag.test_value)

        # this test should fail
        y.tag.test_value = np.random.rand(6, 5).astype(config.floatX)
        with pytest.raises(ValueError):
            tt.dot(x, y)

    @theano.change_flags(compute_test_value="raise")
    def test_compute_flag(self):
        x = tt.matrix("x")
        y = tt.matrix("y")
        y.tag.test_value = np.random.rand(4, 5).astype(config.floatX)

        # should skip computation of test value
        theano.config.compute_test_value = "off"
        z = tt.dot(x, y)
        assert not hasattr(z.tag, "test_value")

        # should fail when asked by user
        theano.config.compute_test_value = "raise"
        with pytest.raises(ValueError):
            tt.dot(x, y)

        # test that a warning is raised if required
        theano.config.compute_test_value = "warn"
        warnings.simplefilter("error", UserWarning)
        try:
            with pytest.raises(UserWarning):
                tt.dot(x, y)
        finally:
            # Restore the default behavior.
            # TODO There is a cleaner way to do this in Python 2.6, once
            # Theano drops support of Python 2.4 and 2.5.
            warnings.simplefilter("default", UserWarning)

    @theano.change_flags(compute_test_value="raise")
    def test_string_var(self):
        x = tt.matrix("x")
        x.tag.test_value = np.random.rand(3, 4).astype(config.floatX)
        y = tt.matrix("y")
        y.tag.test_value = np.random.rand(4, 5).astype(config.floatX)

        z = theano.shared(np.random.rand(5, 6).astype(config.floatX))

        # should work
        out = tt.dot(tt.dot(x, y), z)
        assert hasattr(out.tag, "test_value")
        tf = theano.function([x, y], out)
        assert _allclose(tf(x.tag.test_value, y.tag.test_value), out.tag.test_value)

        def f(x, y, z):
            return tt.dot(tt.dot(x, y), z)

        # this test should fail
        z.set_value(np.random.rand(7, 6).astype(config.floatX))
        with pytest.raises(ValueError):
            f(x, y, z)

    @theano.change_flags(compute_test_value="raise")
    def test_shared(self):
        x = tt.matrix("x")
        x.tag.test_value = np.random.rand(3, 4).astype(config.floatX)
        y = theano.shared(np.random.rand(4, 6).astype(config.floatX), "y")

        # should work
        z = tt.dot(x, y)
        assert hasattr(z.tag, "test_value")
        f = theano.function([x], z)
        assert _allclose(f(x.tag.test_value), z.tag.test_value)

        # this test should fail
        y.set_value(np.random.rand(5, 6).astype(config.floatX))
        with pytest.raises(ValueError):
            tt.dot(x, y)

    @theano.change_flags(compute_test_value="raise")
    def test_ndarray(self):
        x = np.random.rand(2, 3).astype(config.floatX)
        y = theano.shared(np.random.rand(3, 6).astype(config.floatX), "y")

        # should work
        z = tt.dot(x, y)
        assert hasattr(z.tag, "test_value")
        f = theano.function([], z)
        assert _allclose(f(), z.tag.test_value)

        # this test should fail
        x = np.random.rand(2, 4).astype(config.floatX)
        with pytest.raises(ValueError):
            tt.dot(x, y)

    @theano.change_flags(compute_test_value="raise")
    def test_empty_elemwise(self):
        x = theano.shared(np.random.rand(0, 6).astype(config.floatX), "x")

        # should work
        z = (x + 2) * 3
        assert hasattr(z.tag, "test_value")
        f = theano.function([], z)
        assert _allclose(f(), z.tag.test_value)

    @theano.change_flags(compute_test_value="raise")
    def test_constant(self):
        x = tt.constant(np.random.rand(2, 3), dtype=config.floatX)
        y = theano.shared(np.random.rand(3, 6).astype(config.floatX), "y")

        # should work
        z = tt.dot(x, y)
        assert hasattr(z.tag, "test_value")
        f = theano.function([], z)
        assert _allclose(f(), z.tag.test_value)

        # this test should fail
        x = tt.constant(np.random.rand(2, 4), dtype=config.floatX)
        with pytest.raises(ValueError):
            tt.dot(x, y)

    @theano.change_flags(compute_test_value="raise")
    def test_incorrect_type(self):
        x = tt.fmatrix("x")
        # Incorrect dtype (float64) for test_value
        x.tag.test_value = np.random.rand(3, 4)
        y = tt.dmatrix("y")
        y.tag.test_value = np.random.rand(4, 5)

        with pytest.raises(TypeError):
            tt.dot(x, y)

    @theano.change_flags(compute_test_value="raise")
    def test_overided_function(self):
        # We need to test those as they mess with Exception
        # And we don't want the exception to be changed.
        x = tt.matrix()
        x.tag.test_value = np.zeros((2, 3), dtype=config.floatX)
        y = tt.matrix()
        y.tag.test_value = np.zeros((2, 2), dtype=config.floatX)
        with pytest.raises(ValueError):
            x.__mul__(y)

    @theano.change_flags(compute_test_value="raise")
    def test_scan(self):
        # Test the compute_test_value mechanism Scan.
        k = tt.iscalar("k")
        A = tt.vector("A")
        k.tag.test_value = 3
        A.tag.test_value = np.random.rand(5).astype(config.floatX)

        def fx(prior_result, A):
            return prior_result * A

        # Symbolic description of the result
        result, updates = theano.scan(
            fn=fx, outputs_info=tt.ones_like(A), non_sequences=A, n_steps=k
        )

        # We only care about A**k, but scan has provided us with A**1 through A**k.
        # Discard the values that we don't care about. Scan is smart enough to
        # notice this and not waste memory saving them.
        final_result = result[-1]
        assert hasattr(final_result.tag, "test_value")

    @theano.change_flags(compute_test_value="raise")
    def test_scan_err1(self):
        # This test should fail when building fx for the first time
        k = tt.iscalar("k")
        A = tt.matrix("A")
        k.tag.test_value = 3
        A.tag.test_value = np.random.rand(5, 3).astype(config.floatX)

        def fx(prior_result, A):
            return tt.dot(prior_result, A)

        # Since we have to inspect the traceback,
        # we cannot simply use self.assertRaises()
        try:
            theano.scan(fn=fx, outputs_info=tt.ones_like(A), non_sequences=A, n_steps=k)
            assert False
        except ValueError:
            # Get traceback
            tb = sys.exc_info()[2]
            frame_infos = traceback.extract_tb(tb)

            # We should be in the "fx" function defined above
            expected = "test_compute_test_value.py"
            assert any(
                (os.path.split(frame_info[0])[1] == expected and frame_info[2] == "fx")
                for frame_info in frame_infos
            ), frame_infos

    @theano.change_flags(compute_test_value="raise")
    def test_scan_err2(self):
        # This test should not fail when building fx for the first time,
        # but when calling the scan's perform()
        k = tt.iscalar("k")
        A = tt.matrix("A")
        k.tag.test_value = 3
        A.tag.test_value = np.random.rand(5, 3).astype(config.floatX)

        def fx(prior_result, A):
            return tt.dot(prior_result, A)

        with pytest.raises(ValueError):
            theano.scan(
                fn=fx, outputs_info=tt.ones_like(A.T), non_sequences=A, n_steps=k
            )

        # Since we have to inspect the traceback,
        # we cannot simply use self.assertRaises()
        try:
            theano.scan(
                fn=fx, outputs_info=tt.ones_like(A.T), non_sequences=A, n_steps=k
            )
            assert False
        except ValueError as e:
            assert str(e).startswith("could not broadcast input"), str(e)

    @theano.change_flags(compute_test_value="raise")
    def test_no_c_code(self):
        class IncOnePython(Op):
            """
            An Op with only a Python (perform) implementation
            """

            __props__ = ()

            def make_node(self, input):
                input = scalar.as_scalar(input)
                output = input.type()
                return Apply(self, [input], [output])

            def perform(self, node, inputs, outputs):
                (input,) = inputs
                (output,) = outputs
                output[0] = input + 1

        i = scalar.int32("i")
        i.tag.test_value = 3

        o = IncOnePython()(i)

        # Check that the c_code function is not implemented
        with pytest.raises((NotImplementedError, utils.MethodNotDefined)):
            o.owner.op.c_code(o.owner, "o", ["x"], "z", {"fail": ""})

        assert hasattr(o.tag, "test_value")
        assert o.tag.test_value == 4

    @pytest.mark.skipif(
        not theano.config.cxx, reason="G++ not available, so we need to skip this test."
    )
    @theano.change_flags(compute_test_value="raise")
    def test_no_perform(self):
        i = scalar.int32("i")
        i.tag.test_value = 3

        # Class IncOneC is defined outside of the TestComputeTestValue
        # so it can be pickled and unpickled
        o = IncOneC()(i)

        # Check that the perform function is not implemented
        with pytest.raises((NotImplementedError, utils.MethodNotDefined)):
            o.owner.op.perform(o.owner, 0, [None])

        assert hasattr(o.tag, "test_value")
        assert o.tag.test_value == 4

    @theano.change_flags(compute_test_value="raise")
    def test_disabled_during_compilation(self):
        # We test that it is disabled when we include deep copy in the code
        # This don't test that it is disabled during optimization, but the code do it.
        init_Mu1 = theano.shared(np.zeros((5,), dtype=config.floatX)).dimshuffle("x", 0)

        theano.function([], outputs=[init_Mu1])
