import RPi.GPIO as GPIO # type: ignore 
from time import sleep
from logger import get_logger
from config import *
logger = get_logger("Sequence Executor")

# All possible hardware paths:
# 1. Fridge - Home->fridge
# 2. Test   - Fridge->test
# 3. Shake  - Test->shake->test
# 4. Scan   - Test->scan
# 5. End    - Scan->home
# 6. Err_f  - Fridge->home
# 7. Err_t  - Test->home

class SequenceExecutor:
    def __init__(self):

        self.pins = [
            FRIDGE_POS_PIN,
            TEST_POS_PIN,
            SHAKE_PIN,
            SCAN_POS_PIN,
            ERR_FRIDGE_PIN,
            END_POS_PIN,
            ERR_TEST_PIN,
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
        GPIO.output(pin, GPIO.LOW) # FIXME Set before sleeping when switching to relays

    # Robot actions
    def fridge_pos(self):
        self._run_action(FRIDGE_POS_PIN, 1)

    def test_pos(self):
        self._run_action(TEST_POS_PIN, 1)

    def strong_shake(self):
        self._run_action(SHAKE_PIN, 3)

    def weak_shake(self):
        self._run_action(SHAKE_PIN, 3)

    def scan_pos(self):
        self._run_action(SCAN_POS_PIN, 1)

    def long_pause(self):
        sleep(3)

    def short_pause(self):
        sleep(1.5)

    def end_pos(self):
        self._run_action(END_POS_PIN, 1)

    def passed(self):
        self._run_action(PASS_LED_PIN, 3)
    
    def error_fridge(self):
        self._run_action(ERR_FRIDGE_PIN, 2)

    def error_test(self):
        self._run_action(ERR_TEST_PIN, 1)

    def general_error(self):
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
        logger.info("GPIO cleanup done")

    def execute(self, sequence):
        logger.info("Starting sequence execution...")
        for action in sequence:
            logger.debug(f"Executing {action}")
            match action:
                case "fridge_pos":
                    self.fridge_pos()
                    continue
                case "test_pos":
                    self.test_pos()
                    continue
                case "strong_shake":
                    self.strong_shake()
                    continue
                case "scan_pos":
                    self.scan_pos()
                    continue
                case "long_pause":
                    self.long_pause()
                    continue
                case "end_pos":
                    self.end_pos()
                    continue
                case "weak_shake":
                    self.weak_shake()
                    continue
                case "short_pause":
                    self.short_pause()
                    continue
                case _:
                    logger.error(f"Unknown action: {action}")
                    self.general_error()
                    return

        logger.info("Sequence executed successfully")
        self.passed()
        return
