from generateDataBase import MeleeDataset, dataPoint
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

MAX_DEPTH = 8
def get_score(v1,v2):
   return min(abs(4*(v1-v2)),1)

def get_baseline(all_games, max_depth):
   accuracies_base = {i:[] for i in range(max_depth)} 
   accuracies_adv = {i:[] for i in range(max_depth)} 
   for game in all_games.keys():
      game_length = len(all_games[game]['L_trigger_data'])
      base_game_accuracies = {i:0 for i in range(max_depth)}
      for index in range(game_length):
         for d in range(min(max_depth, game_length-index)):
            #base_game_accuracies[d] += pow(sum(pow(get_score(v1,v2),2) for v1,v2 in zip([v[index] for v in all_games[game].values()], [v[index+d] for v in all_games[game].values()])),.5)
            base_game_accuracies[d] += sum(get_score(v1,v2) for v1,v2 in zip([v[index] for v in all_games[game].values()], [v[index+d] for v in all_games[game].values()]))
      for d in range(max_depth):
         accuracies_base[d].append(base_game_accuracies[d])
   return accuracies_base

response = open("meleePros.txt", 'rb') #change this to your dataset / create a dataset out of all your games
jsonResponse = json.loads(json.load(response))
jsonResponse = jsonResponse['sampleGames']

baseline_data = get_baseline(jsonResponse, MAX_DEPTH)
print([(i, sum(baseline_data[i])/len(baseline_data[i])) for i in baseline_data.keys()])

plt.violinplot(baseline_data.values(), [i for i in baseline_data.keys()], points=20, widths=0.3, showmeans=True, showextrema=True, showmedians=True)
plt.ylabel("Similarity Frame Score")
plt.xlabel("Frame Delay")
plt.title("Similarity Frame Score on Pro Dataset (lower is better)")
plt.show()

