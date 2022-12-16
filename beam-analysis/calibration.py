import numpy as np


def read_calibration_parameters(filename):
    return np.loadtxt(filename, delimiter=" ")

def linear_calibration(x, par):
    return (x - par[1]) / par[0]