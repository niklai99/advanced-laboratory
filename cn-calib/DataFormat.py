from dataclasses import dataclass
import numpy as np

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
    a = f"CH2@{board_1}"
    b = f"CH0@{board_2}"
    c = f"CH1@{board_2}"
    d = f"CH2@{board_2}"
    e = f"CH3@{board_2}"
    
    
    @property
    def to_a_energy(self):
        return f"{self.energy_tree}/{self.energy_prefix}{self.a}"
    
    @property
    def to_a_time(self):
        return f"{self.time_tree}/{self.time_prefix}{self.a}"
    
    @property
    def to_b_energy(self):
        return f"{self.energy_tree}/{self.energy_prefix}{self.b}"
    
    @property
    def to_b_time(self):
        return f"{self.time_tree}/{self.time_prefix}{self.b}"
    
    @property
    def to_c_energy(self):
        return f"{self.energy_tree}/{self.energy_prefix}{self.c}"
    
    @property
    def to_c_time(self):
        return f"{self.time_tree}/{self.time_prefix}{self.c}"
    
    @property
    def to_d_energy(self):
        return f"{self.energy_tree}/{self.energy_prefix}{self.d}"
    
    @property
    def to_d_time(self):
        return f"{self.time_tree}/{self.time_prefix}{self.d}"
    
    @property
    def to_e_energy(self):
        return f"{self.energy_tree}/{self.energy_prefix}{self.e}"
    
    @property
    def to_e_time(self):
        return f"{self.time_tree}/{self.time_prefix}{self.e}"