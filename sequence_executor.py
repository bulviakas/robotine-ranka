import RPi.GPIO as GPIO # type: ignore 
from time import sleep
from logger import get_logger
from config import *
logger = get_logger("Sequence Executor")


pins = [FRIDGE_POS_PIN, TEST_POS_PIN, STRONG_SHAKE_PIN, 
    SCAN_POS_PIN, LONG_PAUSE_PIN, END_POS_PIN, 
    WEAK_SHAKE_PIN, SHORT_PAUSE_PIN, ERROR_LED_PIN, PASS_LED_PIN]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for i in range(0, 10):
    GPIO.setup(pins[i], GPIO.OUT)

def right_sequence():
    fridge_pos()
    test_pos()
    strong_shake()
    scan_pos()
    long_pos()
    end_pos()
    passed()

def fridge_pos(): run_action(FRIDGE_POS_PIN, 1)
def test_pos(): run_action(TEST_POS_PIN, 1)
def strong_shake(): run_action(STRONG_SHAKE_PIN, 3)
def scan_pos(): run_action(SCAN_POS_PIN, 1)
def long_pos(): run_action(LONG_PAUSE_PIN, 5)
def end_pos(): run_action(END_POS_PIN, 1)
def weak_shake(): run_action(WEAK_SHAKE_PIN, 3)
def short_pause(): run_action(SHORT_PAUSE_PIN, 3)
def passed(): run_action(PASS_LED_PIN, 5)
def error():
    for i in range(0,3):
        run_action(ERROR_LED_PIN, 0.5)
        sleep(0.5)

def run_action(pin, duration):
    GPIO.output(pin, GPIO.HIGH)
    sleep(duration)
    GPIO.output(pin, GPIO.LOW)

right_sequence()

