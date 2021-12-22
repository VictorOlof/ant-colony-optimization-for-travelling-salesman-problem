import numpy as np
from scipy import spatial
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('victor.csv')
distances = [i for i in df["Distance"]]

n = 3
chunked_dist = [distances[i:i + n] for i in range(0, len(distances), n)]
pc = np.matrix(chunked_dist)

points_coordinate = pc
distance_matrix = spatial.distance.cdist(points_coordinate, points_coordinate, metric='euclidean')


def cal_total_distance(routine):
    num_points, = routine.shape
    return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])



from sko.ACA import ACA_TSP

aca = ACA_TSP(func=cal_total_distance, n_dim=n,
              size_pop=50, max_iter=150,
              distance_matrix=distance_matrix)

best_x, best_y = aca.run()

# %% Plot
fig, ax = plt.subplots(1, 2)
best_points_ = np.concatenate([best_x, [best_x[0]]])
best_points_coordinate = points_coordinate[best_points_, :]
ax[0].plot(best_points_coordinate[:, 0], best_points_coordinate[:, 1], 'o-r')
pd.DataFrame(aca.y_best_history).cummin().plot(ax=ax[1])
plt.show()
