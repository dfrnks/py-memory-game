import copy
import torch

from torch import nn


class MemoryNet(nn.Module):
    """
    mini cnn structure
    """

    def __init__(self, input_dim, output_dim):
        super().__init__()

        h, w = input_dim

        if h != 16:
            raise ValueError(f"Expecting input height: 16, got: {h}")
        if w != 16:
            raise ValueError(f"Expecting input width: 16, got: {w}")

        # https://pytorch.org/docs/stable/nn.html#recurrent-layers
        # RNN - https://pytorch.org/docs/stable/generated/torch.nn.RNN.html
        # LSTM - https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html

        self.online = nn.Sequential(
            nn.Conv1d(in_channels=1, out_channels=16, kernel_size=1, stride=1),
            nn.ReLU(),
            nn.Conv1d(in_channels=16, out_channels=32, kernel_size=1, stride=1),
            nn.ReLU(),
            nn.Conv1d(in_channels=32, out_channels=64, kernel_size=1, stride=1),
            nn.ReLU(),
            nn.Conv1d(in_channels=64, out_channels=128, kernel_size=1, stride=1),
            nn.ReLU(),
            nn.Conv1d(in_channels=128, out_channels=2, kernel_size=1, stride=1),
            nn.ReLU(),
            nn.Flatten(),
            nn.Linear(32, 256),
            nn.ReLU(),
            nn.Linear(256, 16),
            nn.ReLU(),
            nn.Linear(16, output_dim),
        )

        device = "cuda" if torch.cuda.is_available() else "cpu"

        self.online = self.online.to(device=device)

        self.target = copy.deepcopy(self.online)

        # Q_target parameters are frozen.
        for p in self.target.parameters():
            p.requires_grad = False

    def forward(self, input, model):
        if model == "online":
            return self.online(input)
        elif model == "target":
            return self.target(input)
