import uproot
import pandas as pd

def read_data(data_path, file_name, data_format):
    with uproot.open(f"{data_path}/{file_name}") as data_file:
        channels = data_file[data_format.to_channel].array().to_numpy()
        boards   = data_file[data_format.to_board].array().to_numpy()
        flags    = data_file[data_format.to_flag].array().to_numpy()
        time     = data_file[data_format.to_time].array().to_numpy()
        energy   = data_file[data_format.to_energy].array().to_numpy()
    return pd.DataFrame({"board": boards, "channel": channels, "flag": flags, "timestamp": time, "energy": energy})
