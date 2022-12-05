from dataclasses import dataclass


@dataclass
class DataFormat:
    """Holds the structure of the .root file"""
    
    root_tree : str = "Data_R"
    
    channel   : str = "Channel"
    board     : str = "Board"
    flag      : str = "Flags"
    time      : str = "Timestamp"
    energy    : str = "Energy"
    
    @property
    def to_channel(self):
        return f"{self.root_tree}/{self.channel}"
    
    @property
    def to_board(self):
        return f"{self.root_tree}/{self.board}"
    
    @property
    def to_flag(self):
        return f"{self.root_tree}/{self.flag}"
    
    @property
    def to_time(self):
        return f"{self.root_tree}/{self.time}"
    
    @property
    def to_energy(self):
        return f"{self.root_tree}/{self.energy}"