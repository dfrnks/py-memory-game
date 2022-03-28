import time


class PlayHistory:
    def __init__(self, save_dir):

        self.save_history = save_dir / "history.csv"

        with open(self.save_history, mode='w', encoding='utf-8') as f:
            f.write(
                f"id,width,height,action,reward,done,n_games,points,already_played,num_errors,time\n"
            )

    def record(self, games):
        with open(self.save_history, mode='a', encoding='utf-8') as f:
            f.write('\n'.join(','.join(g) for g in games) + '\n')
