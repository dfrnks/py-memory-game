import copy
import torch

from torch import nn


class MemoryNet(nn.Module):
    """
    mini cnn structure
    input -> (conv2d + relu) x 3 -> flatten -> (dense + relu) x 2 -> output
    """

    def __init__(self, input_dim, output_dim):
        super().__init__()

        h, w = input_dim

        if h != 16:
            raise ValueError(f"Expecting input height: 16, got: {h}")
        if w != 16:
            raise ValueError(f"Expecting input width: 16, got: {w}")

        self.online = nn.Sequential(
            # nn.Conv2d(in_channels=c, out_channels=32, kernel_size=8, stride=4),
            # nn.ReLU(),
            # nn.Conv2d(in_channels=32, out_channels=64, kernel_size=4, stride=2),
            # nn.ReLU(),
            # nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1),
            # nn.ReLU(),
            # nn.Flatten(),
            # nn.Linear(3136, 512),
            # nn.ReLU(),
            # nn.Linear(512, output_dim),

            nn.Linear(16, 128),
            nn.Tanh(),
            nn.Linear(128, 128),
            nn.Tanh(),
            nn.Linear(128, 16),
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
