
import math
import time


class DifferentialDrive:

    def __init__(self, left, right):
        # Gemmer vores to motorer.
        self.left = left
        self.right = right

        # Begge motorer starter slukket.
        self.stop()

    # Robotens mål i centimeter.
    wheel_diameter = 8.5
    wheel_distance = 24.5

    # Antal half-steps pr. hjulomdrejning.
    steps_per_rotation = 400

    # Beregner hjulets omkreds.
    wheel_circumference = math.pi * wheel_diameter

    # Beregner antal steps til en bestemt afstand.
    def forward_steps(self, distance):

        if distance < 0:
            raise ValueError("Distance must be non-negative")

        return round(
            distance / self.wheel_circumference
            * self.steps_per_rotation
        )

    # Beregner antal steps til en bestemt drejevinkel.
    def turn_steps(self, angle):

        # Afstand hvert hjul skal køre ved rotation på stedet.
        turn_distance = (
            math.pi * self.wheel_distance * abs(angle) / 360
        )

        return self.forward_steps(turn_distance)

    # Stopper begge motorer.
    def stop(self):
        self.left.stop()
        self.right.stop()

    # Flytter begge motorer et bestemt antal steps.
    def move(self, steps, left_direction, right_direction, delay=0.003):

        if not isinstance(steps, int) or isinstance(steps, bool) or steps < 0:
            raise ValueError("steps must be a non-negative integer")

        if left_direction not in (1, -1, 0):
            raise ValueError("Invalid left direction")

        if right_direction not in (1, -1, 0):
            raise ValueError("Invalid right direction")

        if delay < 0.001:
            delay = 0.001

        try:
            for i in range(steps):

                # Opdaterer venstre motor.
                if left_direction != 0:
                    self.left.step(left_direction)

                # Opdaterer højre motor.
                if right_direction != 0:
                    self.right.step(right_direction)

                time.sleep(delay)

        finally:
            self.stop()

    # Kører robotten fremad en bestemt afstand i cm.
    def forward(self, distance, delay=0.003):

        steps = self.forward_steps(distance)

        self.move(steps, 1, 1, delay)

    # Kører robotten baglæns en bestemt afstand i cm.
    def backward(self, distance, delay=0.003):

        steps = self.forward_steps(distance)

        self.move(steps, -1, -1, delay)

    # Roterer robotten på stedet med en bestemt vinkel.
    def rotate(self, angle, delay=0.003):

        steps = self.turn_steps(angle)

        if angle > 0:
            self.move(steps, 1, -1, delay)

        elif angle < 0:
            self.move(steps, -1, 1, delay)

    # Drejer omkring ét hjul. abs betyder at den retunere den absolutte værdi af et kompleks tal (n). I dette tilfælde vinklen divideret med 180.
    def pivot_turn(self, angle, stationary_side="left", delay=0.003):

        if stationary_side not in ("left", "right"):
            raise ValueError("stationary_side must be left or right")

        turn_distance = (
            math.pi * self.wheel_distance * abs(angle) / 180
        )

        steps = self.forward_steps(turn_distance)

        direction = 1 if angle > 0 else -1

        if stationary_side == "left":
            self.move(steps, 0, direction, delay)

        else:
            self.move(steps, direction, 0, delay)
