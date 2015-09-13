import math

class reaction_simulator:
    def __init__(self, k_rate, reaction_list):
        self.k_rate = k_rate
        self.reactions = list()
        for reaction in reaction_list:
            