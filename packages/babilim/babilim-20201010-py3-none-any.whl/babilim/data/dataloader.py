# AUTOGENERATED FROM: babilim/data/dataloader.ipynb

# Cell: 0
"""doc
# babilim.data.dataloader

> A dataloader object loads the data to the gpu for training.
"""

# Cell: 1
import sys
import traceback
from typing import Iterable, Iterator, Any
from babilim.core.tensor import TensorWrapper


# Cell: 2
class Dataloader(Iterable):
    def __init__(self, native_dataloader, dataset):
        """
        The dataloader is a wrapper around native dataloaders.
        
        This API ensures that the data is on the GPU in babilim tensors and in a named tuple.
        
        You can iterate over the dataloader to get training samples.
        To get information about the original dataset you can use `self.dataset`.
        
        :param native_dataloader: The native dataloader, that should be wrapped.
        :param dataset: The original babilim dataset to allow a user getting information about it, if required.
        """
        self.dataset = dataset
        self._tensor_wrapper = TensorWrapper()
        self.native_dataloader = native_dataloader

    def __iter__(self) -> Iterator:
        class TensorDataloaderIterator(Iterator):
            def __init__(self, native_dataloader, tensor_wrapper):
                self._tensor_wrapper = tensor_wrapper
                self.native_dataloader_iter = iter(native_dataloader)

            def __next__(self) -> Any:
                # Print index errors, they probably were an error and not intentional.
                try:
                    x, y = next(self.native_dataloader_iter)
                    inp = dict(x._asdict())
                    outp = dict(y._asdict())
                    inp = self._tensor_wrapper.wrap(inp)
                    outp = self._tensor_wrapper.wrap(outp)
                    inp = type(x)(**inp)
                    outp = type(y)(**outp)
                    return inp, outp
                except IndexError as e:
                    traceback.print_exc(file=sys.stderr)
                    raise e
        return TensorDataloaderIterator(self.native_dataloader, self._tensor_wrapper)

    def __len__(self) -> int:
        return len(self.native_dataloader)
