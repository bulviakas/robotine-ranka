import RPi.GPIO as GPIO # type: ignore 
from time import sleep
from logger import get_logger
from config import *
logger = get_logger("Sequence Executor")

class SequenceExecutor:
    def __init__(self):

        self.pins = [
            FRIDGE_POS_PIN,
            TEST_POS_PIN,
            STRONG_SHAKE_PIN,
            SCAN_POS_PIN,
            LONG_PAUSE_PIN,
            END_POS_PIN,
            WEAK_SHAKE_PIN,
            SHORT_PAUSE_PIN,
            ERROR_LED_PIN,
            PASS_LED_PIN
        ]

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    # Internal helper
    def _run_action(self, pin, duration):
        GPIO.output(pin, GPIO.HIGH)
        sleep(duration)
        GPIO.output(pin, GPIO.LOW)

    # Robot actions
    def fridge_pos(self):
        self._run_action(FRIDGE_POS_PIN, 1)

    def test_pos(self):
        self._run_action(TEST_POS_PIN, 1)

    def strong_shake(self):
        self._run_action(STRONG_SHAKE_PIN, 3)

    def weak_shake(self):
        self._run_action(WEAK_SHAKE_PIN, 3)

    def scan_pos(self):
        self._run_action(SCAN_POS_PIN, 1)

    def long_pause(self):
        self._run_action(LONG_PAUSE_PIN, 5)

    def short_pause(self):
        self._run_action(SHORT_PAUSE_PIN, 3)

    def end_pos(self):
        self._run_action(END_POS_PIN, 1)

    def passed(self):
        self._run_action(PASS_LED_PIN, 5)

    def error(self):
        for i in range(3):
            self._run_action(ERROR_LED_PIN, 0.5)
            sleep(0.5)

    def right_sequence(self):
        """Runs the full correct robot workflow."""
        self.fridge_pos()
        self.test_pos()
        self.strong_shake()
        self.scan_pos()
        self.long_pause()
        self.end_pos()
        self.passed()

    def cleanup(self):
        """Cleanup GPIO state."""
        GPIO.cleanup()
        self.logger.info("GPIO cleanup done")

    def execute(self, sequence):
        for action in sequence:
            match action:
                case "fridge_pos":
                    self.fridge_pos()
                case "test_pos":
                    self.test_pos()
                case "strong_shake":
                    self.strong_shake()
                case "scan_pos":
                    self.scan_pos()
                case "long_pause":
                    self.long_pause()
                case "end_pos":
                    self.end_pos()
                case "weak_shake":
                    self.weak_shake()
                case "short_pause":
                    self.short_pause()
            self.passed()