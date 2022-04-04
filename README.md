# py-memory-game

Projeto de TCC

O projeto consiste em criar um jogo da memoria e passar para uma Deep Q-Learning jogar.

Para instalar na sua maquina instale os pacotes do python
```
pip install -r requirements.txt
```


Para jogar o jogo rode:
```
python main.py --manually
```

Para jogar o jogo randomicamente pelo computador rode:
```
python main.py --random
```

Para jogar o jogo pela rede rode:
```
python main.py --network
```


Para abrir o tensorboard para visualizar alguns graficos rode:

```
tensorboard --logdir=runs
```

## Network

    Input -> 
    nn.Linear(16, 128),
    nn.ReLU(),
    nn.Linear(128, 64),
    nn.ReLU(),
    nn.Linear(64, 32),
    nn.ReLU(),
    nn.Linear(32, output_dim)
    -> Output

## Hiperpameters

    lr=0.00025,
    max_memory_size=100000,
    batch_size=32,
    gamma=0.9,
    exploration_rate=1,
    exploration_rate_decay=0.99999975,
    exploration_rate_min=0.1,
    save_every=5e5,
    burnin=1e4,
    learn_every=3,
    sync_every=1e4,