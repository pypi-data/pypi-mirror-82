# AUTOGENERATED FROM: babilim/core/device.ipynb

# Cell: 0
"""doc
# babilim.core.device

> Controll on what device code is executed.
"""

# Cell: 1
# MIT License
#
# Copyright (c) 2019 Michael Fuerst
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import List
import babilim
from babilim import PYTORCH_BACKEND, TF_BACKEND


# Cell: 2
_device_stack = ["gpu:0"]

def get_current_device() -> str:
    """
    Get a string specifying the currently selected default device.
    
    When you manually assign a device, you should always use this device.
    """
    return _device_stack[-1]

def get_current_device_native_format() -> str:
    """
    Get a string specifying the currently selected default device in the backend specific native format.
    
    When you manually assign a device, you should always use this device.
    """
    name = _device_stack[-1]
    if babilim.is_backend(TF_BACKEND):
        return "/" + name
    elif babilim.is_backend(PYTORCH_BACKEND):
        import torch
        if torch.cuda.is_available():
            return name.replace("gpu", "cuda")
        else:
            return "cpu"
    else:
        raise RuntimeError("No implementation for this backend was found. (backend={})".format(babilim.get_backend()))


# Cell: 3
class Device(object):
    def __init__(self, name: str):
        """
        Set the default device for babilim in a with statement.
        
        ```python
        with Device("gpu:1"):
            # All tensors of MyModule are on gpu 1 automatically.
            mymodule = MyModule()
        ```
        
        When there is nested with-device statements, the innermost overwrites all others.
        By default gpu:0 is used.
        
        Only works for tensors which are at some point wrapped by a babilim module (Lambda, Tensor, etc.).
        
        :param name: The name of the device. ("cpu", "gpu:0", "gpu:1", etc.)
        """
        self.name = name
        self.native_device = None

    def __enter__(self):
        _device_stack.append(self.name)
        if babilim.is_backend(TF_BACKEND):
            import tensorflow as tf
            self.native_device = tf.device(get_current_device_native_format())
            self.native_device.__enter__()
        elif babilim.is_backend(PYTORCH_BACKEND):
            pass
        else:
            raise RuntimeError("No implementation for this backend was found. (backend={})".format(babilim.get_backend()))
        return self

    def __exit__(self, type, value, traceback):
        _device_stack.pop()
        if babilim.is_backend(TF_BACKEND):
            self.native_device.__exit__()
            self.native_device = None
        elif babilim.is_backend(PYTORCH_BACKEND):
            pass
        else:
            raise RuntimeError("No implementation for this backend was found. (backend={})".format(babilim.get_backend()))
