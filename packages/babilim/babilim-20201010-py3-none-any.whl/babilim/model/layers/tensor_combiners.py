# AUTOGENERATED FROM: babilim/model/layers/tensor_combiners.ipynb

# Cell: 0
"""doc
# babilim.model.layers.tensor_combiners

> Ways of combining tensors.
"""

# Cell: 1
from babilim.core.annotations import RunOnlyOnce
from babilim.core.module_native import ModuleNative


# Cell: 2
class Stack(ModuleNative):
    def __init__(self, axis):
        """
        Stack layers along an axis.

        Creates a callable object with the following signature:
        * **tensor_list**: (List[Tensor]) The tensors that should be stacked. A list of length S containing Tensors.
        * **return**: A tensor of shape [..., S, ...] where the position at which S is in the shape is equal to the axis.

        Parameters of the constructor.
        :param axis: (int) The axis along which the stacking happens.
        """
        super().__init__()
        self.axis = axis
        
    @RunOnlyOnce
    def _build_pytorch(self, tensor_list):
        pass
        
    def _call_pytorch(self, tensor_list):
        import torch
        return torch.stack(tensor_list, dim=self.axis)
    
    @RunOnlyOnce
    def _build_tf(self, tensor_list):
        pass
        
    def _call_tf(self, tensor_list):
        import tensorflow as tf
        return tf.stack(tensor_list, axis=self.axis)


# Cell: 3
class Concat(ModuleNative):
    def __init__(self, axis):
        """
        Concatenate layers along an axis.

        Creates a callable object with the following signature:
        * **tensor_list**: (List[Tensor]) The tensors that should be stacked. A list of length S containing Tensors.
        * **return**: A tensor of shape [..., S * inp_tensor.shape[axis], ...] where the position at which S is in the shape is equal to the axis.

        Parameters of the constructor.
        :param axis: (int) The axis along which the concatenation happens.
        """
        super().__init__()
        self.axis = axis
        
    @RunOnlyOnce
    def _build_pytorch(self, tensor_list):
        pass
        
    def _call_pytorch(self, tensor_list):
        import torch
        return torch.cat(tensor_list, dim=self.axis)
    
    @RunOnlyOnce
    def _build_tf(self, tensor_list):
        pass
        
    def _call_tf(self, tensor_list):
        import tensorflow as tf
        return tf.concat(tensor_list, axis=self.axis)
