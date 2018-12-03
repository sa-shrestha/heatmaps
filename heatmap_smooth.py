# Libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import kde
import re
import csv
import matplotlib.colors as clr

file_in = "/Users/samanashrestha/Sites/heatmaps/soc_data.csv"
file_out = "/Users/samanashrestha/Sites/heatmaps/out.txt"

xoffset = 1960 # xrange min
# data_range_x = [[1960, 2017], 58]
# data_range_y = [[5, 86], 58]


def get_data(file_in):
    with open(file_in) as f:
        ncols = len(f.readline().split(','))
    
    a = np.loadtxt(file_in, int, delimiter=',', skiprows=1, usecols=range(1,ncols))
    return a

print(get_data(file_in))


def init_heatmap_mat(rows, cols):

    # out = [[0]*cols]*rows
    out = [[0.0]*cols for _ in range(rows)]

    return out

def create_heatmap_mat():

    soc_data = get_data(file_in)

    out = [[], []]

    for i in range(len(soc_data)):

        for j in range(len(soc_data[0]) - 15):
        # for j in range(1):

            # print("i, j, soc_data[i][j]", i, j, soc_data[i][j])
            out[0].append(i)
            out[1].append(soc_data[i][j])
            # print("out[", i, "]", out[i], "soc_data[i][j]", soc_data[i][j])

    return out

heatmap_xylist = create_heatmap_mat()


# x, y = data (list of lists: xpoints list and y points list)
x, y = heatmap_xylist

# fig with 2 plot areas
fig, axes = plt.subplots(ncols=2, nrows=1, figsize=(21, 5))
 

#custom cmap
cmap = clr.LinearSegmentedColormap.from_list('custom seagreen', 
                                             [(0,    '#ffffff'),
                                              (1,    '#68B925')], N=256)

# Everything sarts with a Scatterplot
axes[0].set_title('Scatterplot')
axes[0].plot(x, y, 'ko')
# As you can see there is a lot of overplottin here!
 
# # Thus we can cut the plotting window in several hexbins
nbins = 20
# axes[1].set_title('Hexbin')
# axes[1].hexbin(x, y, gridsize=nbins, cmap=plt.cm.BuGn_r)
 
# # 2D Histogram
# axes[2].set_title('2D Histogram')
# axes[2].hist2d(x, y, bins=nbins, cmap=plt.cm.BuGn_r)
 
# Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents
k = kde.gaussian_kde(heatmap_xylist)
xi, yi = np.mgrid[min(x):max(x):nbins*1j, min(y):max(y):nbins*1j]
zi = k(np.vstack([xi.flatten(), yi.flatten()]))
 
# # plot a density
# axes[3].set_title('Calculate Gaussian KDE')
# axes[3].pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=plt.cm.BuGn_r)
 
# add shading
axes[1].set_title('2D Density with shading')

axes[1].pcolormesh(xi, yi, zi.reshape(xi.shape), edgecolor='none', shading='gouraud', cmap=cmap)




 
# # contour

# axes[5].set_title('Contour')
# axes[5].pcolormesh(xi, yi, zi.reshape(xi.shape), shading='gouraud', cmap=plt.cm.BuGn_r)
# axes[5].contour(xi, yi, zi.reshape(xi.shape) )

# plt.show()

fig.savefig('foo.png', transparent=True)