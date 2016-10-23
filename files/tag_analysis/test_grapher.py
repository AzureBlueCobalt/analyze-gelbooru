import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def data_to_2d_heatmap(X):
	pca = PCA(n_components=2)
	pca.fit(X)
	X_simple = pca.transform(X)
	X_simple = np.array(X_simple)

	# print(X_simple)
	x_simple = X_simple[:,0]
	y_simple = X_simple[:,1]

	# fig, ax = plt.subplots()
	# ax.plot(x_simple, y_simple, 'o')
	# ax.set_title('Random data')
	# plt.show()

	heatmap, xedges, yedges = np.histogram2d(x_simple, y_simple, bins=32)
	extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
	plt.clf()
	# plt.imshow(heatmap, extent=extent, cmap="viridis")
	plt.imshow(heatmap, extent=extent, cmap="jet")
	plt.show()

num_samples, num_dimensions = 100000, 100
X = np.random.rand(num_samples, num_dimensions)
data_to_2d_heatmap(X)
