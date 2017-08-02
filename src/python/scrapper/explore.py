import pandas as pd

episode_lines = pd.DataFrame.from_csv("../../../data/episode_lines.csv", index_col=None)

oneEpisode = episode_lines[(episode_lines["season"] == 1) & (episode_lines["episode"] == 1)]

print(oneEpisode)