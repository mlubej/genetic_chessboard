import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import MultiPoint, Polygon

from .utils import transform


def plot_chromosome(individual, initial_polygons, board_size, filename=''):
    """
    Function to plot the final configuration for a given chromosome. The plot can be saved if the filename argument
    is specified.
    :param individual: an individual class, containing information about the pieces order and placement
    :param initial_polygons: original definition of polygons
    :param board_size: size of chessboard
    :param filename: name of the file to save the image to
    """
    new_polys = []
    for poly in initial_polygons:
        pts = np.array(poly.checkers)[:, :-1]
        checkers = np.array(poly.checkers)[:, -1]
        pts = pts[checkers == 1]
        poly = poly.difference(MultiPoint(pts + 0.5).buffer(0.2))
        new_polys.append(poly)

    new_polys = np.array(new_polys)
    new_polys = [transform(p, *s) for p, s in zip(new_polys[individual.chromosome],
                                                  individual.placements) if s is not None]
    indices = [individual.chromosome[idx] for idx, s in enumerate(individual.placements) if s is not None]
    canvas = Polygon([[0, 0], [board_size, 0], [board_size, board_size], [0, board_size]])
    gdf = gpd.GeoDataFrame({'idx': indices}, geometry=new_polys)

    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    ax.plot(*canvas.exterior.xy, 'k')
    gdf.plot(ax=ax, column='idx', edgecolor='black', alpha=0.75, vmin=0, vmax=len(initial_polygons))
    ax.set_ylim([-0.1, board_size + 0.1])
    ax.set_xlim([-0.1, board_size + 0.1])
    ax.set_title(f'[{",".join(individual.chromosome.astype(str))}]', fontsize=20)
    ax.set_xlabel(f'Fitness score: {int(individual.fitness)}', fontsize=20)
    ax.set_xticks([])
    ax.set_yticks([])

    if filename != '':
        fig.savefig(filename)


# TODO: fix
def plot_process(data, filename=''):
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    ax.plot(data[:, 0], data[:, 1], 'r*-')
    ax.set_title('Evolution process', fontsize=20)
    ax.set_xlabel('Generations', fontsize=20)
    ax.set_ylabel('Score', fontsize=20)
    if filename != '':
        fig.savefig(filename)
