from chainer import cuda
from chainer import function
from chainer import utils
from chainer.utils import type_check


class SquaredDifference(function.Function):
    """Squared difference of input variables."""

    def check_type_forward(self, in_types):
        type_check.expect(in_types.size() == 2)
        type_check.expect(
            in_types[0].dtype.kind == 'f',
            in_types[0].dtype == in_types[1].dtype,
            in_types[0].shape == in_types[1].shape
        )

    def forward(self, inputs):
        xp = cuda.get_array_module(*inputs)
        x1, x2 = inputs
        self.difference = x1 - x2
        y = xp.square(self.difference)
        return utils.force_array(y),

    def backward(self, inputs, grads):
        x1, x2 = inputs
        gy, = grads
        gx = gy * self.difference * 2
        gx = utils.force_array(gx)
        return gx, -gx

def squared_difference(x1, x2):
    """Squared difference of input variables.

    Args:
        x1 (~chainer.Variable): Input variables to be compared.
        x2 (~chainer.Variable): Input variables to be compared.

    Returns:
        ~chainer.Variable: ``(x1 - x2) ** 2`` element-wise.
    """
    return SquaredDifference()(x1, x2)
