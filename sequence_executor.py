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

    def _run_action(self, pin, duration):
        if self.abort:
            return
        #GPIO.output(pin, GPIO.HIGH)
        sleep(duration)
        #GPIO.output(pin, GPIO.LOW) # FIXME Set before sleeping when switching to relays

    def fridge_pos(self):
        self.tasks_completed["fridge"] = True
        self._run_action(FRIDGE_POS_PIN, 1)

    def test_pos(self):
        self._run_action(TEST_POS_PIN, 1)
        self.tasks_completed["test"] = True

    def strong_shake(self):
        self._run_action(SHAKE_PIN, 3)

    def weak_shake(self):
        self._run_action(SHAKE_PIN, 3)

    def scan_pos(self):
        self._run_action(SCAN_POS_PIN, 1)
        self.tasks_completed["scan"] = True

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
            case "TEST":
                self.error_test()
            case "SCAN":
                self.end_pos()
            case _:
                logger.warning("Unknown position → emergency stop")

        self.general_error()
    
    def _record(self, event):
        self.events.append(event)

    def execute(self, sequence, on_hard_error=None, on_soft_error=None, on_incomplete_task=None):
        logger.info("Starting sequence execution")

        pos_index = 0
        soft_errors = []
        shake_performed = False
        self.tasks_completed = {
            "fridge": False,
            "test": False,
            "scan": False
        }

        for action in sequence:

            if action == "start_block":
                logger.debug("Start block accepted")
                continue

            if action in POSITIONAL_ACTIONS:
                expected = POSITIONAL_ACTIONS[pos_index]

                if action == "scan_pos" and not shake_performed:
                    logger.warning("Scan performed without prior shake")
                    soft_errors.append("Scan performed without shake")

                if action != expected:
                    self.recover(f"Expected {expected}, got {action}")
                    if on_hard_error:
                        on_hard_error(
                            title="Positional Error",
                            message=(
                                f"Invalid movement.\n\n"
                                f"Expected: {expected}\n"
                                f"Got: {action}\n\n"
                                f"Robot recovered safely."
                            )
                        )
                    return

                self._execute_action(action)
                pos_index += 1
                continue

            if action in {"strong_shake", "weak_shake"}:
                if self.current_position != "TEST":
                    self.recover("Shake outside TEST zone")
                    if on_hard_error:
                        on_hard_error(
                            title="Hardware Safety Error",
                            message="Shake attempted outside TEST zone."
                        )
                    return
                self._execute_action(action)
                shake_performed = True

                if action == "weak_shake":
                    logger.warning("Shake too weak")
                    soft_errors.append("Shake too weak")

                continue

            try:
                getattr(self, action)()
                if action in ROBOT_POSITIONS:
                    self.current_position = ROBOT_POSITIONS[action]
            except Exception as e:
                self.recover(str(e))
                if on_hard_error:
                    on_hard_error(
                        title="Hardware Error",
                        message="Hardware failure detected. Robot recovered."
                    )
                return
            
        missing_tasks = [
            name for name, done in self.tasks_completed.items() if not done
        ]
        if missing_tasks:
            if on_incomplete_task:
                on_incomplete_task(
                    title="Incomplete Tasks",
                    message=(
                        "The sequence finished, but not all required tasks were completed:\n\n"
                        + "\n".join(f"- {task.capitalize()} station not visited" for task in missing_tasks)
                    )
                )
            return


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