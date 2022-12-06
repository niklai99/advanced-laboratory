import numpy as np
from scipy.optimize import curve_fit

def gaussian(x, a, b, c):
    return a * np.exp(-(x - b)**2 / (2 * c**2))

def fit_peak(func, x, y, err_y, e_fit, p0):
    par, cov = curve_fit(func, x[e_fit], y[e_fit], sigma=err_y[e_fit], p0=p0, absolute_sigma=True)
    err = np.sqrt(np.diag(cov))
    return par, np.abs(err)


def build_parameter_string(par, err):
    parameter_names = ["A", "$\mu$", "$\sigma$"]
    par_str = ""
    for i in range(len(par)):
        par_str += f"{parameter_names[i]} = {par[i]:.3f} +/- {err[i]:.3f}"
        if i < len(par) - 1:
            par_str += "\n"
    return par_str


def save_parameters(par, err, name):
    parameter_names = ["A", "mu", "sigma"]
    with open(f"./calib-parameters/{name}_parameters.txt", "w") as f:
        for i in range(len(par)):
            f.write(f"{parameter_names[i]} {par[i]} {err[i]}\n")