import torch
from torch import nn

from src.memory_game import MemoryGame

game = MemoryGame(8, 8, 0)
game.start()

obs = []
for i, v in enumerate(game.game_table):
    for j, l in enumerate(game.game_table[i]):
        obs.append(game.game_table[i][j])

device = torch.device('cpu')
if torch.cuda.is_available():
    device = torch.device('cuda')

pi_net = nn.Sequential(
    nn.Linear(64, 64),
    nn.Tanh(),
    nn.Linear(64, 64),
    nn.Tanh(),
    nn.Linear(64, 2),
    nn.ReLU(),
).to(device)

obs_tensor = torch.as_tensor(obs, dtype=torch.float32).to(device)
actions = pi_net(obs_tensor)
#
# i = torch.argmax(actions).item()
#
# print(i)

# ac = actions.cpu().detach().numpy()
#
# print(ac[0], min(round(ac[0] * 100), 7))
# print(ac[1], min(round(ac[1] * 100), 7))
#
# x = min(round(ac[0] * 100), 7)
# y = min(round(ac[1] * 100), 7)
#
# winning, table, pontos, acerto = game.next(x, y)
#
# print(winning, pontos, acerto)

