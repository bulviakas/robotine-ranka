from pathlib import Path

BLACK = "#161316"
WHITE = "#F5F5F5"

# ASSET PATHS
RESTART_BUTTON_PATH = Path("assets/restart_btn.svg")
SUBMIT_BUTTON_PATH = Path("assets/submit_btn.svg")
START_BLOCK_PATH = Path("assets/start_block.svg")
CMD_BLOCK_PATH = Path("assets/game_blocks.svg")
BLOCK_TEMPLATE_PATH = Path("assets/block_template.svg")
CMD_BLOCK_PATH = Path("assets/cmd_block.svg")
TT_ICON_PATH = Path("assets/tutorial_icon.svg")
HOME_ICON_PATH = Path("assets/home_icon.svg")
START_BTN_PATH = Path("assets/start_btn.svg")
CONTEXT_VIDEO_PATH = Path("assets/Fish-spinning.mp4")
INSTRUCTIONS_VIDEO_PATH = Path("assets/roach.gif")

# CONSTANTS
OVERLAP_FRAC        = 0.2
CMD_BAR_HEIGHT_FRAC = 1.7
TOP_PAD_FRAC        = 0.19
MID_PAD_FRAC        = 0.05   # vertical gap between cmd bar & button
BOT_PAD_FRAC        = 0.1
SIDE_GAP_FRAC       = 0.02   # side padding for menu
GAP_BETWEEN_BTNS    = 3
BLOCK_SIZE_COEF     = 0.02
CMD_SIDE_PAD        = 32
CMD_H_PAD           = 16
MENU_TOP_FRAC       = 0.08
GAP_FROM_VIDEO      = 24 #px

# TODO: import better fonts

# Good default fonts: Cascadia Code SemiBold, Segoe UI Black
MAIN_FONT = "Cascadia Code SemiBold"

COLOUR_PALETTE = [
    "#e74c3c", "#f39c12", "#27ae60", "#8e44ad", "#96d5ff",
    "#ff5f7f", "#f1c40f", "#2980b9"   # 8 pieces
]

BLOCK_LABELS = [
    "test_pos", "weak_shake", "strong_shake", "fridge_pos",
    "scan_pos", "short_pause", "long_pause", "end_pos"
]

THE_CORRECT_SEQUENCE = [
    "start_pos",
    "fridge_pos", "test_pos", "strong_shake", "scan_pos",
    "long_pause", "end_pos", None
]

POSITIONAL_ACTIONS = [
    "fridge_pos",
    "test_pos",
    "scan_pos",
    "end_pos"
]

OPTIONAL_ACTIONS = {
    "strong_shake",
    "weak_shake",
    "long_pause",
    "short_pause"
}

ROBOT_POSITIONS = {
    "fridge_pos": "FRIDGE",
    "test_pos": "TEST",
    "scan_pos": "SCAN",
    "end_pos": "HOME",
}

CONTEXT_VIDEO_SIZE = [480, 854] # Change when importing the actual video
INSTRUCTIONS_VIDEO_SIZE = [360, 480]

LANGUAGES = ["LT", "EN"]

# PIN LAYOUT
FRIDGE_POS_PIN  = 26
TEST_POS_PIN    = 6
SHAKE_PIN       = 5
SCAN_POS_PIN    = 16
ERR_FRIDGE_PIN  = 25
END_POS_PIN     = 24
ERR_TEST_PIN    = 22
ERROR_LED_PIN   = 27
PASS_LED_PIN    = 17

ROBOT_SPEED = 0.25 # from 0 to 1

# HARDWARE ACTION DURATIONS
TO_FRIDGE_DURATION              = 3.8 / ROBOT_SPEED
RECOVER_FROM_FRIDGE_DURATION    = 2.3 / ROBOT_SPEED
TO_TEST_DURATION                = 4.8 / ROBOT_SPEED
SHAKE_DURATION                  = 15.1 / ROBOT_SPEED
RECOVER_FROM_TEST_DURATION      = 2.2 / ROBOT_SPEED
TO_SCAN_DURATION                = 3.8 / ROBOT_SPEED
RECOVER_FROM_SCAN_DURATION      = 2.3 / ROBOT_SPEED