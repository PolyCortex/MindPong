from pathlib import Path
import csv
import numpy as np
from mindpong.model.player import PlayerName


def get_available_games():
    p = Path("History/")
    if not p.is_dir():
        raise FileNotFoundError("The directory History does not exist")
    return [x for x in Path("History/").iterdir() if x.is_dir()]


def read_player_signal(game_name: str, player_name: PlayerName):
    file_path = Path('History/%s/%s' %
                     (game_name, player_name.value[0])).with_suffix('.csv')
    signals = [[] for _ in range(6)]
    headers = []
    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(list(reader)):
            if i is not 0:
                for j in range(1, len(row)):
                    signals[j-1].append(row[j])
            else:
                headers = row[1:-1]
        signals = [np.array(signal).astype(np.float) for signal in signals]
    return {headers[i]: signals[i] for i in range(len(headers))}
