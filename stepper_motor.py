# Name: Jeppe Nielsen
# Email: jepni26@student.sdu.dk

from machine import Pin, PWM
import time

class StepperMotor:
    def __init__(self, pins, pwm_pct=0.30, frequency=18_000):
        self.step_index = 0 # instantiate vars for move_stepper function
        self.total_steps = 0

        self.pwm_pct = pwm_pct # assign parameters to object via .self
        self.pins = pins
        self.outputs = [] # Instantiate self.outputs (the list of output pins and their frequencies)

        for pin in self.pins: # For every pin:
            output = PWM(Pin(pin)) # Make output pin PWM
            output.freq(frequency) # Set frequency of pin to given value
            output.duty_u16(0) # Set duty cycle of pin to 0
            self.outputs.append(output) # Add pin to final list

        # Store each step sequence under a separate mode name.
        p = self.pwm_pct # assign pwm_pct to p to make sequence tables more readable

        self.step_sequences = {
            "full": [
                [p, p, 0, 0],
                [0, p, p, 0],
                [0, 0, p, p],
                [p, 0, 0, p],
            ]
        }

        for sequence in self.step_sequences:
            self.step_sequences[sequence] = [
                [int(p * 65535) for p in step] for step in self.step_sequences[sequence]
            ]

        self.step_sequence = self.step_sequences["full"] # make default mode full-step

    def stop(self): # Function to stop all outputs
        for pin in self.outputs:
            pin.duty_u16(0) # Set duty cycle of every pin to 0         

    def move_stepper(self, steps, direction, delay = 0.001): # Pin to actually move motor using chosen mode
        increment = 0 # var added to index and total steps to keep track of wheel's rotation
        if direction == "forward": # positive if going forward, negative if going backward
            increment = 1
        elif direction == "backward":
            increment = -1
        else: 
            raise ValueError("Invalid direction")

        sequence_length = len(self.step_sequence) # save number of steps in sequence
        self.step_index = 0
        for i in range(steps): # For loop 
            step = self.step_sequence[self.step_index] # get current step
            self.step_index = (self.step_index + increment) % sequence_length # move to next position in sequence. modulo to keep track regardless of num of rotations
            self.set_step(step)
            self.total_steps += increment # update total steps
            time.sleep(delay) # wait [delay] until next step

    def set_step(self, step): # Function to set the step sequence directly
            for pin, duty in zip(self.outputs, step): # for every pin:
                pin.duty_u16(duty) # apply pwm value to pin