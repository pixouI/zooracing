# sensorVals = [10000,15535,15535,17000,26000]
# sensorThreshold = 25000
# sensorWeights = [-2,-1,0,1,2]
# binaryValues = [0,0,0,0,0]
# activeSensors = 0
# rightMotorDelay = 0
# leftMotorDelay = 0
# rightPWM = 50
# leftPWM = 50
# k = 25

class PID:
    def __init__(self, Kp, sensor1, sensor2, sensor3):
        self.Kp = Kp
        self.sensorPins = [sensor1, sensor2, sensor3]
    
    def getSensorVals(self):
        for i in range(len(self.sensorPins)):
            self.sensorData = []
            self.sensorData.append(self.sensorPins[i].read_u16()) # evt. bitshift m. >> 6 
        
    def findError(self):   
        total = sum(self.sensorData)
        if total > 0:
            error = (self.sensorData[0] * -1 + self.sensorData[1] * 0 + self.sensorData[2] * 1) / total
        else:
            error = 0
        return self.Kp * error