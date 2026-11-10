from stepper_moterll import StepperMotor
import time


class DifferentialDrive:

    def __init__(self, left, right):
        # Her gemmer vi vores to motorer.
        # De skal være oprettet som hver deres StepperMotor-objekt i main.py.
        self.left = left
        self.right = right

        # Begge motorer skal starte slukket.
        self.stop()

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
