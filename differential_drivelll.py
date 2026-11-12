from stepper_moterll import StepperMotor
import time
import math


class DifferentialDrive:

    def __init__(self, left, right):
        # Her gemmer vi vores to motorer.
        # De skal være oprettet som hver deres StepperMotor-objekt i main.py.
        self.left = left
        self.right = right

        # Begge motorer skal starte slukket.
        self.stop()

        
    # Robotens mål i centimeter.
    wheel_diameter = 8.5
    wheel_distance = 24.5
    distance = 100
    
    # Antal half-steps pr. hjulomdrejning.
    steps_per_rotation = 400
    
    # Beregner hjulets omkreds.
    wheel_circumference = math.pi * wheel_diameter
    
    # Beregner antal steps for at køre 100 cm.
    def forward_steps(self, distance):

        if distance < 0:
            raise ValueError("Distance must be non-negative")

        return round(
            distance / self.wheel_circumference
            * self.steps_per_rotation
        )
    
    # Beregner hvor langt hvert hjul skal køre ved 90 graders drejning.
    def turn_steps(self, angle):

        # Afstand hvert hjul skal køre ved rotation på stedet.
        turn_distance = (
            math.pi * self.wheel_distance * abs(angle) / 360
        )

        return self.forward_steps(turn_distance)
   

    # Omregner drejningens distance til steps.
    turn_steps = round(
    turn_distance / wheel_circumference * steps_per_rotation
    )


    def stop(self):
        # Stopper begge motorer ved at sætte deres PWM-udgange til 0.
        self.left.stop()
        self.right.stop()

    def move(self, steps, left_direction, right_direction, delay=0.003):
        # Vi accepterer kun et helt antal steps fra 0 og opefter.
        if not isinstance(steps, int) or isinstance(steps, bool) or steps < 0:
            raise ValueError("steps must be a non-negative integer")

        # +1 betyder frem gennem motorens sekvens, -1 betyder tilbage.
        # Retningerne vælges hver for sig, så robotten også kan dreje.
        if left_direction not in (1, -1):
            raise ValueError("left_direction must be 1 or -1")
        if right_direction not in (1, -1):
            raise ValueError("right_direction must be 1 or -1")

        # Samme mindste pause som i StepperMotor.
        if delay < 0.001:
            delay = 0.001

        # finally sikrer, at begge motorer bliver slukket,
        # også hvis programmet afbrydes under kørslen.
        try:
            for i in range(steps):
                # Begge motorer tager ét sekvenstrin i samme løkke.
                # step() opdaterer selv motorens total_steps-tæller.
                self.left.step(left_direction)
                self.right.step(right_direction)

                # Først når begge motorer er opdateret, venter vi.
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

    # Drejer omkring ét hjul.
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

    # Starter en rotation uden at blokere programmet.
    def start_rotate(self, angle, delay=0.02):

        # Stopper eventuelle tidligere bevægelser.
        self.stop()

        self.remaining_steps = self.turn_steps(angle)

        if angle > 0:
            self.rotation_left_direction = 1
            self.rotation_right_direction = -1

        elif angle < 0:
            self.rotation_left_direction = -1
            self.rotation_right_direction = 1

        else:
            self.rotating = False
            return

        self.rotation_delay = max(delay, 0.001)
        self.last_step_time = time.ticks_us()
        self.rotating = True

    # Opdaterer motorerne ét step ad gangen.
    def update_rotation(self):

        if not self.rotating:
            return False

        current_time = time.ticks_us()

        # Kontrollerer om det er tid til næste step.
        if time.ticks_diff(current_time, self.last_step_time) >= self.rotation_delay * 1_000_000:

            # Tager ét step med hver motor.
            self.left.step(self.rotation_left_direction)
            self.right.step(self.rotation_right_direction)

            self.remaining_steps -= 1
            self.last_step_time = current_time

            # Stopper når rotationen er færdig.
            if self.remaining_steps <= 0:
                self.rotating = False
                self.stop()

        return self.rotating

    print("n")