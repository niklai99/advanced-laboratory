import numpy as np


def read_calibration_parameters(file_name: str):
    """function to read the calibration parameters from a .txt file"""
    
    with open(file_name, "r") as file:
        p = file.readlines()[0].split(" ")
        return float(p[0]), float(p[1])
    
    
def calibrate(energy: np.ndarray, slope: float, intercept: float) -> np.ndarray:
    """function to calibrate the energy of a detector"""
    
    return (energy - intercept) / slope