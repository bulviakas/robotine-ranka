import RPi.GPIO as GPIO
from time import sleep
from logger import get_logger
from config import *
logger = get_logger("Sequence Executor")
from dataclasses import dataclass
from typing import Literal, Optional

# All possible hardware paths:
# 1. Fridge - Home->fridge
# 2. Test   - Fridge->test
# 3. Shake  - Test->shake->test
# 4. Scan   - Test->scan
# 5. End    - Scan->home
# 6. Err_f  - Fridge->home
# 7. Err_t  - Test->home

@dataclass
class ExecutionResult:
    status: Literal["passed", "soft_error", "incomplete", "hard_error"]
    soft_errors: list[str]
    missing_tasks: list[str]
    hard_error_reason: Optional[str] = None

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

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)

    def _run_action(self, pin, duration):
        if self.abort:
            return
        GPIO.output(pin, GPIO.HIGH)
        sleep(0.3)
        GPIO.output(pin, GPIO.LOW)
        sleep(duration)

    def fridge_pos(self):
        self.tasks_completed["fridge"] = True
        logger.info("Moving to Fridge position...")
        self._run_action(FRIDGE_POS_PIN, TO_FRIDGE_DURATION)

    def test_pos(self):
        logger.info("Moving to Test position...")
        self._run_action(TEST_POS_PIN, TO_TEST_DURATION)
        self.tasks_completed["test"] = True

    def strong_shake(self):
        logger.info("Performing Strong Shake...")
        self._run_action(SHAKE_PIN, SHAKE_DURATION)

    def weak_shake(self):
        logger.info("Performing Weak Shake...")
        self._run_action(SHAKE_PIN, SHAKE_DURATION)

    def scan_pos(self):
        logger.info("Moving to Scan position...")
        self._run_action(SCAN_POS_PIN, TO_SCAN_DURATION)
        self.tasks_completed["scan"] = True

    def long_pause(self):
        logger.info("Initiating Long pause...")
        sleep(3)

    def short_pause(self):
        logger.info("Initiating Short pause...")
        sleep(1.5)

    def end_pos(self):
        logger.info("Moving to End position")
        self._run_action(END_POS_PIN, RECOVER_FROM_SCAN_DURATION)
        self.tasks_completed["end"] = True

    def passed(self, on_passed=None):
        #self._run_action(PASS_LED_PIN, 3)
        logger.info("Sequence passed")
        if on_passed:
            on_passed()
            return
    
    def error_fridge(self):
        logger.info("Homing from Fridge position...")
        self._run_action(ERR_FRIDGE_PIN, RECOVER_FROM_FRIDGE_DURATION)
        self.current_position = "HOME"

    def error_test(self):
        logger.info("Homing from Test Postion...")
        self._run_action(ERR_TEST_PIN, RECOVER_FROM_TEST_DURATION)
        self.current_position = "HOME"

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
            case "HOME":
                logger.info("Already homed.")
            case _:
                logger.warning("Unknown position → emergency stop")

        self.general_error()
    
    def _record(self, event):
        self.events.append(event)

    def execute(self, sequence, on_hard_error=None, on_soft_error=None, on_incomplete_task=None, on_passed=None):
        logger.info("Starting sequence execution")

        pos_index = 0
        soft_errors = []
        shake_performed = False
        self.abort = False
        self.tasks_completed = {
            "fridge": False,
            "test": False,
            "scan": False,
            "end": False
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
                    return ExecutionResult(
                        status="hard_error",
                        soft_errors=soft_errors,
                        missing_tasks=[],
                        hard_error_reason=f"{expected} → {action}"
                    )

                getattr(self, action)()
                if action in ROBOT_POSITIONS:
                    self.current_position = ROBOT_POSITIONS[action]
                    logger.debug(f"Position → {self.current_position}")
                pos_index += 1
                continue

            if action in {"strong_shake", "weak_shake"}:
                if self.current_position != "TEST":
                    self.recover("Shake outside TEST zone")
                    return ExecutionResult(
                        status="hard_error",
                        soft_errors=soft_errors,
                        missing_tasks=[],
                        hard_error_reason="shake_outside_test"
                    )
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
                        message="Hardware failure detected. Robot recovered."
                    )
                return
            
        missing_tasks = [
            name for name, done in self.tasks_completed.items() if not done
        ]
        if missing_tasks:
            return ExecutionResult(
                status="incomplete",
                soft_errors=soft_errors,
                missing_tasks=missing_tasks
            )


        if soft_errors:
            return ExecutionResult(
                status="soft_error",
                soft_errors=soft_errors,
                missing_tasks=[]
            )
        else:
            return ExecutionResult("passed", [], [])
