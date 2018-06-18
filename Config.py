class Config:
    def __init__(self, num_drones=10, com_range=105, move_consumption=.9, idle_consumption=.8, commConsumption=0.0):
        self.num_drones = num_drones
        self.com_range = com_range
        self.obstacles = []
        self.move_consumption = move_consumption
        self.idle_consumption = idle_consumption
        self.communicationConsumption = commConsumption

    
