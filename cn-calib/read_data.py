import uproot
import pandas as pd

def read_data(file_name, data_format):
    with uproot.open(file_name) as data_file:
        a_energy = data_file[data_format.to_a_energy].to_numpy()
        a_time   = data_file[data_format.to_a_time].to_numpy()
        b_energy = data_file[data_format.to_b_energy].to_numpy()
        b_time   = data_file[data_format.to_b_time].to_numpy()
        c_energy = data_file[data_format.to_c_energy].to_numpy()
        c_time   = data_file[data_format.to_c_time].to_numpy()
        d_energy = data_file[data_format.to_d_energy].to_numpy()
        d_time   = data_file[data_format.to_d_time].to_numpy()
        e_energy = data_file[data_format.to_e_energy].to_numpy()
        e_time   = data_file[data_format.to_e_time].to_numpy()
        
    return a_energy, a_time, b_energy, b_time, c_energy, c_time, d_energy, d_time, e_energy, e_time
