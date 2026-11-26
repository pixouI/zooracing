from stepper_motor import StepperMotor
from p_controller import PID
import _thread
from time import sleep_us

class DiffDrive:
    def __init__(self, motor1:StepperMotor, motor2:StepperMotor,PID : PID, pidDelay):
        self.motor1 = motor1
        self.motor2 = motor2
        self.motor1_accumulator = 0
        self.motor2_accumulator = 0
        self.phase1 = 0
        self.phase2 = 0
        self.pid = PID
        self.pidRunning = False
        self.pidDelay = pidDelay

    def driveInit(self):
        self.motor1.step_sequence
        self.motor2.step_sequence
        self.sequenceLength = len(self.motor1.step_sequence)
        if self.sequenceLength != len(self.motor2.step_sequence):
            raise ValueError("Motors have different step sequence lengths")
        self.pidRunning = True
        _thread.start_new_thread(self.pidLoop, ())

    def pidLoop(self):
        try:
            while self.pidRunning:
                self.pidOut = self.pid.findError()
                sleep_us(self.pidDelay)
        except Exception as e:
            print("PID thread died", e)

    def driver(self, sequence, sequenceLength):
        if self.motor1_accumulator >= 1.0:
            self.motor1_accumulator -= 1.0
            self.phase1 = (self.phase1 + 1) % sequenceLength
        
        if self.motor2_accumulator >= 1.0:
            self.motor2_accumulator -= 1.0
            self.phase2 = (self.phase2 + 1) % sequenceLength

        self.motor1.set_step(sequence[self.phase1])
        self.motor2.set_step(sequence[self.phase2])

    def driverdriver(self):
        self.motor1_accumulator += 1
        self.motor2_accumulator += 1
    
        self.driver(self.motor1.step_sequence, self.sequenceLength)

        if self.pidOut > 0:
            self.motor2_accumulator -= self.pidOut
        else:
            self.motor1_accumulator -= abs(self.pidOut)