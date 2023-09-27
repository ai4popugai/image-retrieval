import time
from typing import Optional

import torch
from torch import nn

from nn_models.attention import MultiHeadAttention
from nn_models.utils import PositionWiseFeedForward


class TransformerEncoder(nn.Module):
    def __init__(self, hidden_size: int, d_ff: int, num_heads: int, dropout: float):
        if hidden_size % num_heads != 0:
            raise RuntimeError('hidden_size must be divisible by num_heads')
        super().__init__()
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.feed_forward = PositionWiseFeedForward(self.hidden_size, d_ff)
        self.self_attention = MultiHeadAttention(query_hidden_size=self.hidden_size,
                                                 keys_hidden_size=self.hidden_size,
                                                 values_hidden_size=self.hidden_size,
                                                 out_hidden_size=self.hidden_size,
                                                 hidden_size=self.hidden_size,
                                                 num_heads=self.num_heads)
        self.dropout = nn.Dropout(dropout)
        self.layer_norm_0 = nn.LayerNorm(self.hidden_size)
        self.layer_norm_1 = nn.LayerNorm(self.hidden_size)

    def forward(self, x: torch.Tensor, mask: Optional[torch.Tensor] = None):
        if x.shape[-1] != self.hidden_size:
            raise RuntimeError(f'Could not encode tensor with depth {x.shape[-1]}, '
                               f'only depth={self.hidden_size} allowed')
        attended, _ = self.self_attention(query=x, keys=x, values=x, mask=mask)
        x = self.layer_norm_0(x + self.dropout(attended))
        feed_forward_out = self.feed_forward(x)
        x = self.layer_norm_1(x + self.dropout(feed_forward_out))
        return x


class TransformerDecoder(nn.Module):
    def __init__(self, hidden_size: int, d_ff: int, num_heads: int, dropout: float):
        if hidden_size % num_heads != 0:
            raise RuntimeError('hidden_size must be divisible by num_heads')
        super().__init__()
        self.hidden_size = hidden_size
        self.num_heads = num_heads
        self.feed_forward = PositionWiseFeedForward(self.hidden_size, d_ff)
        self.self_attention = MultiHeadAttention(query_hidden_size=self.hidden_size,
                                                 keys_hidden_size=self.hidden_size,
                                                 values_hidden_size=self.hidden_size,
                                                 out_hidden_size=self.hidden_size,
                                                 hidden_size=self.hidden_size,
                                                 num_heads=self.num_heads)
        self.cross_attention = MultiHeadAttention(query_hidden_size=self.hidden_size,
                                                  keys_hidden_size=self.hidden_size,
                                                  values_hidden_size=self.hidden_size,
                                                  out_hidden_size=self.hidden_size,
                                                  hidden_size=self.hidden_size,
                                                  num_heads=self.num_heads)
        self.dropout = nn.Dropout(dropout)
        self.layer_norm_0 = nn.LayerNorm(self.hidden_size)
        self.layer_norm_1 = nn.LayerNorm(self.hidden_size)
        self.layer_norm_2 = nn.LayerNorm(self.hidden_size)




if __name__ == "__main__":
    # Example usage
    hs = 512
    d_ff = 2048
    num_heads = 4
    max_seq_length = 100

    # Create a random input tensor (batch_size, seq_length, hidden_size)
    batch_size = 32
    seq_length = 50
    encoder = TransformerEncoder(hidden_size=hs, d_ff=d_ff, num_heads=num_heads, dropout=0.2)
    input_tensor = torch.randn(batch_size, seq_length, hs)

    # Apply positional encoding to the input tensor
    start_time = time.perf_counter()
    output_tensor = encoder(input_tensor)
    print(time.perf_counter() - start_time)

    print("Input Tensor Shape:", input_tensor.shape)
    print("Output Tensor Shape:", output_tensor.shape)
