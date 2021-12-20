import numpy as np
from itertools import product

STOPS = (2, 50)
ENCODING = {'.': '0', '#': '1'}
TRANS = str.maketrans(ENCODING)
BACKTRANS = str.maketrans({val: key for key, val in ENCODING.items()})

with open('input') as f:
    enhancer = f.readline().strip().translate(TRANS)
    f.readline()
    rows = [row.strip().translate(TRANS) for row in f.readlines()]

def create_filler():
    """Generator for character to pad the infinite space around the board."""
    yield '0'   # first step is always blank
    initial = enhancer[0]
    altern = enhancer[int(initial * 9, 2)]
    while True:
        yield initial
        yield altern
        

filler = create_filler()
def enhance(in_array):
    """Applies the enhancement algorith, creating an expanding area around
    the given array."""
    pad = next(filler)
    pad_array = np.pad(in_array, 4, constant_values=pad)
    out_array = pad_array.copy()
    
    for i, j in product(range(1, pad_array.shape[0] - 1),
                        range(1, pad_array.shape[1] - 1)):
        neighbours = ''.join(pad_array[i-1:i+2, j-1:j+2].flatten().tolist())
        out_array[i,j] = enhancer[int(neighbours, 2)]
    
    out_array = out_array[2:-2, 2:-2]
    return out_array
    
def display(array):
    """Simple pretty-print for an array."""
    for row in array:
        print(''.join(row.tolist()).translate(BACKTRANS))

image = np.array([list(row) for row in rows])
iterations = 0
while iterations < max(STOPS):
    image = enhance(image)
    iterations += 1
    if iterations in STOPS:
        print(f'After {iterations} iterations:', sum(image.astype(int).flatten()))
