from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import numpy as np

# PROYECCIÓN DE DATOS
X = np.load("D:/rjru/Google Drive (rjruos@gmail.com)/dataset/dataX2.npy")
#X = np.load("D:/rjru/Google Drive (rjruos@gmail.com)/dataset/dataX2_sinDistancia.npy")
# PCA 
pca2 = PCA(n_components=2)
principalComponents = pca2.fit_transform(X)
np.save('D:/rjru/Google Drive (rjruos@gmail.com)/dataset/pca_2d_v2.npy', principalComponents)
# FIN PCA

# TSNE
tsne = TSNE(n_components=2, verbose=1, random_state=123)
tsne_res = tsne.fit_transform(X) 
np.save('D:/rjru/Google Drive (rjruos@gmail.com)/dataset/tsne_2d_v2.npy', tsne_res)
# FIN TSNE

