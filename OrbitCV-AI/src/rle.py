import numpy as np

def rle_decode(rle,shape):
    mask = np.zeros(shape[0] * shape[1], dtype=np.uint8)

    if not isinstance(rle, str) or rle.strip() == "":
        return mask.reshape(shape, order="F")
    
    parts = rle.split()
    values = np.asarray(parts, dtype=int)

    starts = values[0::2] - 1

    lengths = values[1::2]

    ends = starts + lengths

    for start, end in zip(starts, ends):
        mask[start:end] = 1

    return mask.reshape(shape, order="F")
