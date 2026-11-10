
# Vi importerer time, så vi kan lave pauser mellem motorens steps.
# Math bruger vi til sin, cos og pi, og Pin/PWM bruges til at styre Picoens pins.
import time
import math
from machine import Pin, PWM


# Her opretter vi vores StepperMotor-klasse.
# Klassen samler alt det, motoren skal kunne.
class StepperMotor:

    # __init__ bliver kørt, når vi opretter en motor.
    # pins fortæller, hvilke pins vi bruger.
    # pwm_pct=0.15 betyder 15 % PWM.
    # frequency=18_000 betyder en frekvens på 18.000 Hz.
    def __init__(self, pins, pwm_pct=0.15, frequency=18_000):

        self.pins = pins
        self.pwm_pct = pwm_pct
        self.frequency = frequency

        # Holder styr på, hvor mange sekvenstrin motoren har kørt.
        self.total_steps = 0

        # Her gemmer vi PWM-udgangene.
        self.pwm_outputs = []

        # Opretter en PWM-udgang for hver pin.
        for pin in self.pins:
            self.pwm_outputs.append(PWM(Pin(pin)))

        # Indstiller frekvensen og slukker alle udgange.
        for pwm in self.pwm_outputs:
            pwm.freq(self.frequency)
            pwm.duty_u16(0)

        # Vi vælger full-step som standard.
        self.set_step_mode("full")

    # Denne funktion sender én tilstand fra vores step-sekvens ud til motoren.
    # state er en liste med værdier for de fire udgange.
    def apply_state(self, state):

        # zip parrer den første PWM-udgang med den første værdi osv.
        for pwm, value in zip(self.pwm_outputs, state):

            # PWM bruger tal fra 0 til 65535.
            pwm.duty_u16(int(value * 65535))

    # Denne funktion får motoren til at tage ét sekvenstrin.
    # direction = 1 betyder fremad i sekvensen.
    # direction = -1 betyder baglæns i sekvensen.
    def step(self, direction):

        # Vi accepterer kun de to retninger.
        if direction not in (1, -1):
            raise ValueError("direction must be 1 or -1")

        # Finder den næste tilstand i vores sekvens.
        # % sørger for, at vi bliver inden for listen.
        step_index = self.total_steps % len(self.step_seq)

        # Sender den valgte tilstand til motoren.
        self.apply_state(self.step_seq[step_index])

        # Opdaterer tælleren, så næste step fortsætter fra den nye position.
        self.total_steps += direction

    # Stop-funktionen sætter alle PWM-udgange til 0.
    def stop(self):
        for pwm in self.pwm_outputs:
            pwm.duty_u16(0)

    # Her vælger vi, om motoren skal bruge full, half eller microsteps.
    # microsteps bruges kun, når vi vælger micro.
    def set_step_mode(self, mode, microsteps=None):

        # Vi slukker motoren, før vi ændrer sekvensen.
        self.stop()

        self.mode = mode
        self.microsteps = microsteps

        # Full-step har fire tilstande.
        if self.mode == "full":
            step_seq = [
                [self.pwm_pct, self.pwm_pct, 0, 0],
                [0, self.pwm_pct, self.pwm_pct, 0],
                [0, 0, self.pwm_pct, self.pwm_pct],
                [self.pwm_pct, 0, 0, self.pwm_pct]
            ]

        # Half-step har otte tilstande.
        elif self.mode == "half":
            step_seq = [
                [self.pwm_pct, 0, 0, 0],
                [self.pwm_pct, self.pwm_pct, 0, 0],
                [0, self.pwm_pct, 0, 0],
                [0, self.pwm_pct, self.pwm_pct, 0],
                [0, 0, self.pwm_pct, 0],
                [0, 0, self.pwm_pct, self.pwm_pct],
                [0, 0, 0, self.pwm_pct],
                [self.pwm_pct, 0, 0, self.pwm_pct]
            ]

        # Microstep-sekvensen beregnes af funktionen nedenunder.
        elif self.mode == "micro":
            step_seq = self.generate_microstep_sequence(microsteps)

        # Hvis vi skriver en ugyldig mode, får vi en fejl.
        else:
            raise ValueError("mode must be full, half or micro")

        # Gemmer den valgte sekvens.
        self.step_seq = step_seq

        # Vi nulstiller sekvenstælleren ved skift af mode.
        # Det betyder ikke, at motorens fysiske position er nul.
        self.total_steps = 0

    # Denne funktion beregner vores microstep-sekvens.
    def generate_microstep_sequence(self, microsteps):

        # Antallet af microsteps skal være et positivt helt tal.
        if not isinstance(microsteps, int) or microsteps < 1:
            raise ValueError("microsteps must be a positive integer")

        sequence = []

        # Vi laver fire gange så mange tilstande som microsteps.
        for i in range(4 * microsteps):

            # Finder vinklen for den aktuelle tilstand.
            angle = i * 2 * math.pi / (4 * microsteps)

            # Beregner signalerne til de to faser.
            phase_a = math.cos(angle) * self.pwm_pct
            phase_b = math.sin(angle) * self.pwm_pct

            # Positive værdier sendes til plus-udgangen.
            # Negative værdier sendes til minus-udgangen.
            if phase_a >= 0:
                a_plus = phase_a
                a_minus = 0
            else:
                a_plus = 0
                a_minus = -phase_a

            if phase_b >= 0:
                b_plus = phase_b
                b_minus = 0
            else:
                b_plus = 0
                b_minus = -phase_b

            # Gemmer de fire signaler i den rigtige rækkefølge.
            sequence.append([
                a_plus,
                b_plus,
                a_minus,
                b_minus
            ])

        return sequence

    # Flytter motoren et bestemt antal steps.
    def move_stepper(self, steps, direction, delay=0.001):

        # Vi accepterer kun ikke-negative heltal.
        if not isinstance(steps, int) or steps < 0:
            raise ValueError("steps must be a non-negative integer")

        # Delay må ikke være mindre end 0.001 sekund.
        if delay < 0.001:
            delay = 0.001

        # Vi oversætter retningen til 1 eller -1.
        if direction == "forward":
            step_direction = 1
        elif direction == "backward":
            step_direction = -1
        else:
            raise ValueError("direction must be forward or backward")

        # try/finally sikrer, at motoren bliver stoppet.
        try:

            # Gentager bevægelsen det ønskede antal gange.
            for i in range(steps):

                # Tager ét step i den valgte retning.
                self.step(step_direction)

                # Venter, før næste step.
                time.sleep(delay)

        finally:
            # Stopper motoren, også hvis programmet afbrydes.
            self.stop()

    # Kører motoren kontinuerligt, indtil programmet afbrydes.
    def continuous_rotation(self, direction, delay=0.001):

        # Finder den ønskede retning.
        if direction == "forward":
            step_direction = 1
        elif direction == "backward":
            step_direction = -1
        else:
            raise ValueError("direction must be forward or backward")

        # Minimum delay.
        if delay < 0.001:
            delay = 0.001

        try:
            while True:

                # Tager ét step.
                self.step(step_direction)

                # Holder pause mellem hvert step.
                time.sleep(delay)

        except KeyboardInterrupt:
            # Når vi trykker Ctrl+C, forlader vi løkken.
            pass

        finally:
            # Slukker motorens udgange.
            self.stop()

