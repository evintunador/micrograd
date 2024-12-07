import random as r
from engine import Value
from nn import Module, Neuron, Linear, MLP

class Embedding(Module):
    def __init__(self, num_classes: int, dim: int):
        self.weight = [[Value(r.uniform(-1,1)) for _ in range(dim)] 
                       for _ in range(num_classes)]

    def __call__(self, x):
        assert isinstance(x, list), "x should be a list of integers"
        assert all(isinstance(idx, int) for idx in x), "All elements in x must be integers"
        # grab embedding assigned to each token
        out = [self.weight[idx] for idx in x]
        return out[0] if len(out) == 1 else out

    def __repr__(self):
        weights_repr = "\n".join(
            f"[{', '.join(str(p) for p in row)}]" for row in self.weight
        )
        return f"Embedding with weights:\n{weights_repr}"

    def parameters(self):
        return [p for c in self.weight for p in c]

def LayerNorm(x):
    '''
    Layer normalization module that only takes as input a single vector, 
    meaning you've gotta handle the tensor logic outside the call
    '''
    assert isinstance(x, list), "x should be a list of Value objects"
    assert all(isinstance(idx, Value) for idx in x), "All elements in x must be Value objects"

    n = len(x)
    # mean
    mean = Value(x[0].data / n, (x[0],)) # for some reason sum() gives me an error so i do the addition manually
    for xi in x[1:]: 
        mean = mean + (xi / n)
    # sd
    tot = (x[0] - mean)**2
    for xi in x[1:]:
        tot = tot + (xi - mean)**2
    sd = (tot / n) ** (-0.5)
    # normalization
    out = [None] * n
    for i in range(n):
        out[i] = (x[i] - mean) / sd

    return out

if __name__ == "__main__":
    ### test embedding
    E = Embedding(vocab_len, model_dim)
    print(E)
    print('\n')
    x = E([1,2,3])
    print(x)

    ### test layernorm
    # single vector
    x = [Value(r.uniform(-1,1)) for _ in range(model_dim)]
    print(x)
    y = LayerNorm(x)
    print(y)
    # tensor
    x = [[[Value(r.uniform(-1,1)) for _ in range(model_dim)]
          for _ in range(seq_len)]
         for _ in range(batch_size)]
    print(x)
    print('\n')
    y = [[LayerNorm(xi) for xi in seq] for seq in x]
    print(y)

    