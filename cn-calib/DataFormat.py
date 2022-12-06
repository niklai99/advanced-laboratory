from dataclasses import dataclass
import glob
import numpy as np
import uproot


def read_data_from_sources(file_name: str, detector: str):
    """function to read data from a .root file and return the energy and time data for a specific detector"""
    
    detectors = ["clyc_trap", "labr_b", "labr_a", "clyc_sum", "scint"]

    with uproot.open(file_name) as data_file:
        clyc_trap_energy = data_file[RootFileFormat().to_clyc_trap_energy].to_numpy()
        clyc_trap_time   = data_file[RootFileFormat().to_clyc_trap_time].to_numpy()
        labr_b_energy    = data_file[RootFileFormat().to_labr_b_energy].to_numpy()
        labr_b_time      = data_file[RootFileFormat().to_labr_b_time].to_numpy()
        labr_a_energy    = data_file[RootFileFormat().to_labr_a_energy].to_numpy()
        labr_a_time      = data_file[RootFileFormat().to_labr_a_time].to_numpy()
        clyc_sum_energy  = data_file[RootFileFormat().to_clyc_sum_energy].to_numpy()
        clyc_sum_time    = data_file[RootFileFormat().to_clyc_sum_time].to_numpy()
        scint_energy     = data_file[RootFileFormat().to_scint_energy].to_numpy()
        scint_time       = data_file[RootFileFormat().to_scint_time].to_numpy()

    energy_detector = dict(zip(detectors, [clyc_trap_energy, labr_b_energy, labr_a_energy, clyc_sum_energy, scint_energy]))
    time_detector   = dict(zip(detectors, [clyc_trap_time, labr_b_time, labr_a_time, clyc_sum_time, scint_time]))

    return energy_detector[detector], time_detector[detector]



class Detector:
    """class to hold the data of a detector"""
    
    def __init__(self, name: str, sources: list[str]) -> None:
        self.name    = name
        self.sources = np.array(sources)
        
        self.energy_dict = dict(zip(sources, [read_data_from_sources(self.build_file_path(source), self.name)[0] for source in sources]))
        self.time_dict   = dict(zip(sources, [read_data_from_sources(self.build_file_path(source), self.name)[1] for source in sources]))
        
        self.histograms  = dict(zip(sources, [DataHistogram(self.energy_dict[source], self.time_dict[source]) for source in sources]))
        
        
    def build_file_name(self, source) -> str:
        return f"./data/HcompassF_{source}_calibration*"
    
    def build_file_path(self, source) -> str:
        return glob.glob(self.build_file_name(source))[0]
    
    def get_energy_histogram(self, source):
        return self.histograms[source].energy
    
    def get_time_histogram(self, source):
        return self.histograms[source].time
    
    

class DataHistogram:
    """Holds the structure of the detectors data"""
    
    def __init__(self, energy, time) -> None:
        self.e_binceters  = np.array(0.5 * (energy[1][1:] + energy[1][:-1]))
        self.e_binheights = energy[0]
        self.t_binceters  = np.array(0.5 * (time[1][1:] + time[1][:-1]))
        self.t_binhights  = time[0]
        
        
    @property
    def energy(self):
        return self.e_binceters, self.e_binheights
    
    @property
    def time(self):
        return self.t_binceters, self.t_binhights
    
    

@dataclass
class RootFileFormat:
    """Holds the structure of the .root file"""
    
    # trees
    energy_tree : str = "Energy"
    time_tree   : str = "Time"
    
    # name prefix
    energy_prefix : str = "_F_Energy"
    time_prefix   : str = "_F_Time"
    
    # boards
    board_1     : str = "V1725C_446"
    board_2     : str = "V1730B_281"
    
    # active channels
    clyc_trap = f"CH2@{board_1}" # clyc trapezio
    labr_b    = f"CH0@{board_2}" # labr b
    labr_a    = f"CH1@{board_2}" # labr a
    clyc_sum  = f"CH2@{board_2}" # clyc somma
    scint     = f"CH3@{board_2}" # liquid scintillator
    
    
    @property
    def to_clyc_trap_energy(self):
        return f"{self.energy_tree}/{self.energy_prefix}{self.clyc_trap}"
    
    @property
    def to_clyc_trap_time(self):
        return f"{self.time_tree}/{self.time_prefix}{self.clyc_trap}"
    
    @property
    def to_labr_b_energy(self):
        return f"{self.energy_tree}/{self.energy_prefix}{self.labr_b}"
    
    @property
    def to_labr_b_time(self):
        return f"{self.time_tree}/{self.time_prefix}{self.labr_b}"
    
    @property
    def to_labr_a_energy(self):
        return f"{self.energy_tree}/{self.energy_prefix}{self.labr_a}"
    
    @property
    def to_labr_a_time(self):
        return f"{self.time_tree}/{self.time_prefix}{self.labr_a}"
    
    @property
    def to_clyc_sum_energy(self):
        return f"{self.energy_tree}/{self.energy_prefix}{self.clyc_sum}"
    
    @property
    def to_clyc_sum_time(self):
        return f"{self.time_tree}/{self.time_prefix}{self.clyc_sum}"
    
    @property
    def to_scint_energy(self):
        return f"{self.energy_tree}/{self.energy_prefix}{self.scint}"
    
    @property
    def to_scint_time(self):
        return f"{self.time_tree}/{self.time_prefix}{self.scint}"