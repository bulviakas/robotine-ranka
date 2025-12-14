#import RPi.GPIO as GPIO # type: ignore 
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

        self.current_position = "HOME"
        self.abort = False

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

        #GPIO.setmode(GPIO.BCM)
        #GPIO.setwarnings(False)

        #for pin in self.pins:
            #GPIO.setup(pin, GPIO.OUT)
            #GPIO.output(pin, GPIO.LOW)

    # Internal helper
    def _run_action(self, pin, duration):
        if self.abort:
            return
        #GPIO.output(pin, GPIO.HIGH)
        sleep(duration)
        #GPIO.output(pin, GPIO.LOW) # FIXME Set before sleeping when switching to relays

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
        logger.info("Sequence passed")
    
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
    
    def _execute_action(self, action):
        getattr(self, action)()

        if action in ROBOT_POSITIONS:
            self.current_position = ROBOT_POSITIONS[action]
            logger.debug(f"Position → {self.current_position}")


    def recover(self, reason):
        logger.error(f"Recovery triggered: {reason}")
        self.abort = True

        match self.current_position:
            case "FRIDGE":
                self.error_fridge()
                self.end_pos()
            case "TEST" | "SCAN":
                self.error_test()
                self.end_pos()
            case _:
                logger.warning("Unknown position → emergency stop")

        self.general_error()


    def execute(self, sequence, on_hard_error=None, on_soft_error=None):
        logger.info("Starting sequence execution")

        expected_index = 0
        soft_errors = []

        for action in sequence:
            expected = THE_CORRECT_SEQUENCE[expected_index]

            if action == "start_block":
                if expected_index != 0:
                    self.recover("Start block in invalid position")
                    if on_hard_error:
                        on_hard_error(
                            title="Sequence Error",
                            message="Start block can only appear at the beginning."
                        )
                    return

                logger.debug("Start block accepted")
                expected_index += 1
                continue

            # ---- HARD POSITIONAL CHECK ----
            if action in POSITIONAL_ACTIONS:
                if action != expected:
                    self.recover(
                        f"Expected {expected}, got {action}"
                    )
                    if on_hard_error:
                        on_hard_error(
                            title="Positional Error",
                            message=(
                                f"Invalid movement.\n\n"
                                f"Expected: {expected}\n"
                                f"Got: {action}\n\n"
                                f"Robot returned to HOME."
                            )
                        )
                    return
                expected_index += 1

            if action in {"strong_shake", "weak_shake"}:
                if self.current_position != "TEST":
                    logger.error(f"Shake attempted outside TEST zone at {self.current_position}")
                    self.recover(f"{action} attempted outside TEST zone")
                    if on_hard_error:
                        on_hard_error(
                            title="Hardware Safety Error",
                            message=(
                                f"{action} attempted outside TEST zone.\n"
                                f"Sequence aborted. Robot returned to HOME."
                            )
                        )
                    return

            # ---- SOFT CHECK ----
            if action in SOFT_ACTIONS:
                if action != THE_CORRECT_SEQUENCE[expected_index - 1]:
                    soft_errors.append(action)

            # ---- EXECUTION ----
            try:
                self._execute_action(action)
            except Exception as e:
                self.recover(str(e))
                on_hard_error(
                    title="Hardware Failure",
                    message="Hardware error detected. Robot recovered."
                )
                return

        # ---- FINAL RESULT ----
        if soft_errors:
            if on_soft_error:
                on_soft_error(
                    title="Faulty Result",
                    message=(
                        "Sequence completed, but issues were detected:\n\n"
                        + "\n".join(f"- {e}" for e in soft_errors)
                    )
                )
        else:
            self.passed()

