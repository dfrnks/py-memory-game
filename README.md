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
