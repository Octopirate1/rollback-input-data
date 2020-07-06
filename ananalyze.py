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


#[(0, 0.0), (1, 2827.629433595462), (2, 4691.011643572038), (3, 6291.606433117555), (4, 7637.1340298029245), (5, 8786.844957721642), (6, 9732.915019808921), (7, 10529.36251682242)]
#[(0, 0.0), (1, 2355.8458572787495), (2, 3748.2086601816095), (3, 4876.085161444655), (4, 5770.839040197697), (5, 6494.149319430279), (6, 7058.007428813435), (7, 7518.64456091589)]
#benchmarks for gang dataset with sum(~) and pow(sum(~^2),.5) respectively
