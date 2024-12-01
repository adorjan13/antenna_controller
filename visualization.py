import numpy
from config import  STEPS_PER_DEGREE

# Koordináták kiszámítása
def calculate_coordinates(azimuth, elevation):

    r = 1
    x = r * numpy.cos(numpy.radians(elevation)) * numpy.cos(numpy.radians(azimuth))
    y = r * numpy.cos(numpy.radians(elevation)) * numpy.sin(numpy.radians(azimuth))
    z = r * numpy.sin(numpy.radians(elevation))
    return x, y, z

# Azimut és eleváció  értékek lépésekké alakítása
def azimuth_elevation_to_steps(azimuth, elevation):

    azimuth_steps = int(azimuth * STEPS_PER_DEGREE)
    elevation_steps = int(elevation * STEPS_PER_DEGREE)
    return azimuth_steps, elevation_steps

# "Földgömb" kirajzolása
def plot_globe(ax):

    u = numpy.linspace(0, 2 * numpy.pi, 100)
    v = numpy.linspace(0, numpy.pi, 100)
    x = numpy.outer(numpy.cos(u), numpy.sin(v))
    y = numpy.outer(numpy.sin(u), numpy.sin(v))
    z = numpy.outer(numpy.ones(numpy.size(u)), numpy.cos(v))

    ax.plot_surface(x, y, z, color='lightblue', alpha=0.6)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.grid(False)