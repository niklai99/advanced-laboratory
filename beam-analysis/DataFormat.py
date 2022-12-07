from dataclasses import dataclass
import glob
import numpy as np
import uproot


def read_data(file_name: str, detector: str):
    """function to read data from a .root file and return the energy and time data for a specific detector"""
    
    detectors = ["clyc_trap", "labr_b", "labr_a", "clyc_sum", "scint"]

    with uproot.open(file_name) as data_file:
        clyc_trap_energy = data_file[RootFileFormat().to_clyc_trap_energy].to_numpy()
        clyc_trap_time   = data_file[RootFileFormat().to_clyc_trap_time].to_numpy()
        labr_b_energy    = data_file[RootFileFormat().to_labr_b_energy].to_numpy()
        labr_b_time      = data_file[RootFileFormat().to_labr_b_time].to_numpy()
        labr_b_psd       = data_file[RootFileFormat().to_labr_b_psd].to_numpy()
        labr_b_psdvse    = data_file[RootFileFormat().to_labr_b_psdvse].to_numpy()
        labr_a_energy    = data_file[RootFileFormat().to_labr_a_energy].to_numpy()
        labr_a_time      = data_file[RootFileFormat().to_labr_a_time].to_numpy()
        labr_a_psd       = data_file[RootFileFormat().to_labr_a_psd].to_numpy()
        labr_a_psdvse    = data_file[RootFileFormat().to_labr_a_psdvse].to_numpy()
        clyc_sum_energy  = data_file[RootFileFormat().to_clyc_sum_energy].to_numpy()
        clyc_sum_time    = data_file[RootFileFormat().to_clyc_sum_time].to_numpy()
        clyc_sum_psd     = data_file[RootFileFormat().to_clyc_sum_psd].to_numpy()
        clyc_sum_psdvse  = data_file[RootFileFormat().to_clyc_sum_psdvse].to_numpy()
        scint_energy     = data_file[RootFileFormat().to_scint_energy].to_numpy()
        scint_time       = data_file[RootFileFormat().to_scint_time].to_numpy()
        scint_psd        = data_file[RootFileFormat().to_scint_psd].to_numpy()
        scint_psdvse     = data_file[RootFileFormat().to_scint_psdvse].to_numpy()

    energy_detector = dict(zip(detectors, [clyc_trap_energy, labr_b_energy, labr_a_energy, clyc_sum_energy, scint_energy]))
    time_detector   = dict(zip(detectors, [clyc_trap_time, labr_b_time, labr_a_time, clyc_sum_time, scint_time]))
    psd_detector    = dict(zip(detectors, [None, labr_b_psd, labr_a_psd, clyc_sum_psd, scint_psd]))
    psdvse_detector = dict(zip(detectors, [None, labr_b_psdvse, labr_a_psdvse, clyc_sum_psdvse, scint_psdvse]))

    return energy_detector[detector], time_detector[detector], psd_detector[detector], psdvse_detector[detector]



class Detector:
    """class to hold the data of a detector"""
    
    def __init__(self, name: str, target: str, runs: list[str]) -> None:
        self.name = name
        self.runs = np.array(runs)
        
        self.energy_dict = dict(zip(runs, [read_data(self.build_file_path(target, run), self.name)[0] for run in runs]))
        self.time_dict   = dict(zip(runs, [read_data(self.build_file_path(target, run), self.name)[1] for run in runs]))
        self.psd_dict    = dict(zip(runs, [read_data(self.build_file_path(target, run), self.name)[2] for run in runs]))
        self.psdvse_dict = dict(zip(runs, [read_data(self.build_file_path(target, run), self.name)[3] for run in runs]))
        
        self.histograms  = dict(zip(runs, [DataHistogram(self.energy_dict[run], self.time_dict[run], self.psd_dict[run], self.psdvse_dict[run]) for run in runs]))
    
    def build_file_path(self, target, run) -> str:
        return glob.glob(f"./data/beam-target{target}-run{run}.root")[0]
    
    def get_energy_histogram(self, run):
        return self.histograms[run].energy
    
    def get_time_histogram(self, run):
        return self.histograms[run].time
    
    def get_psd_histogram(self, run):
        return self.histograms[run].psd
    
    def get_psdvse_histogram(self, run):
        return self.histograms[run].psdvse
    
    def get_all_energy_histograms(self):
        e1, h1 = self.get_energy_histogram(self.runs[0])
        for run in self.runs[1:]:
            _, h2 = self.get_energy_histogram(run)
            h1 = np.sum([h1, h2], axis=0)
        return e1, h1
    

class DataHistogram:
    """Holds the structure of the detectors data"""
    
    def __init__(self, energy, time, psd, psdvse) -> None:
        self.e_edges        = energy[1]
        self.e_heights      = energy[0]
        self.t_edges        = time[1]
        self.t_heights      = time[0]
        self.psd_edges      = psd[1]
        self.psd_heights    = psd[0]
        self.psdvse_xedges  = psdvse[1]
        self.psdvse_yedges  = psdvse[2]
        self.psdvse_heights = psdvse[0]
        
    @property
    def energy(self):
        return self.e_edges, self.e_heights
    
    @property
    def time(self):
        return self.t_edges, self.t_heights
    
    @property
    def psd(self):
        return self.psd_edges, self.psd_heights
    
    @property
    def psdvse(self):
        return self.psdvse_xedges, self.psdvse_yedges, self.psdvse_heights.T
    
    
    
    

@dataclass
class RootFileFormat:
    """Holds the structure of the .root file"""
    
    # trees
    energy_tree : str = "Energy"
    time_tree   : str = "Time"
    psd_tree    : str = "PSD"
    psdve_tree  : str = "PSD_E"
    
    # name prefix
    energy_prefix : str = "_F_Energy"
    time_prefix   : str = "_F_Time"
    psd_prefix    : str = "_F_PSD"
    psdve_prefix  : str = "_F_PSDvsE"
    
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
    
    @property
    def to_labr_b_psd(self):
        return f"{self.psd_tree}/{self.psd_prefix}{self.labr_b}"
    
    @property
    def to_labr_a_psd(self):
        return f"{self.psd_tree}/{self.psd_prefix}{self.labr_a}"
    
    @property
    def to_clyc_sum_psd(self):
        return f"{self.psd_tree}/{self.psd_prefix}{self.clyc_sum}"
    
    @property
    def to_scint_psd(self):
        return f"{self.psd_tree}/{self.psd_prefix}{self.scint}"
    
    @property
    def to_labr_b_psdvse(self):
        return f"{self.psdve_tree}/{self.psdve_prefix}{self.labr_b}"
    
    @property
    def to_labr_a_psdvse(self):
        return f"{self.psdve_tree}/{self.psdve_prefix}{self.labr_a}"
    
    @property
    def to_clyc_sum_psdvse(self):
        return f"{self.psdve_tree}/{self.psdve_prefix}{self.clyc_sum}"
    
    @property
    def to_scint_psdvse(self):
        return f"{self.psdve_tree}/{self.psdve_prefix}{self.scint}"