from pathlib import Path

# ASSET PATHS
RESTART_BUTTON_PATH = Path("assets/restart_btn.svg")
SUBMIT_BUTTON_PATH = Path("assets/submit_btn.svg")
START_BLOCK_PATH = Path("assets/start_block.svg")
CMD_BLOCK_PATH = Path("assets/game_blocks.svg")
BLOCK_TEMPLATE_PATH = Path("assets/block_template.svg")
CMD_BLOCK_PATH = Path("assets/cmd_block.svg")
TT_ICON_PATH = Path("assets/tutorial_icon_thin.svg")
HOME_ICON_PATH = Path("assets/home_icon_thin.svg")
LNG_ICON_PATH = Path("assets/language_icon_thin.svg")
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

# Good fonts: Cascadia Code SemiBold, Segoe UI Black
MAIN_FONT = "Cascadia Code SemiBold"

BLOCK_COLOURS = [
    "#e74c3c", "#f39c12", "#27ae60", "#8e44ad", "#96d5ff",
    "#ff5f7f", "#f1c40f", "#2980b9"   # 8 pieces
]

BLOCK_LABELS = [
    "TESTAVIMO POZICIJA", "SILPNAS PAKRATYMAS", "STIPRUS PAKRATYMAS", "ŠALDYTUVO POZICIJA",
    "SKENAVIMO POZICIJA", "TRUMPA PAUZĖ", "ILGA PAUZĖ", "GALUTINĖ POZICIJA"
]

THE_CORRECT_SEQUENCE = [
    "ŠALDYTUVO POZICIJA", "TESTAVIMO POZICIJA", "STIPRUS PAKRATYMAS", "SKENAVIMO POZICIJA",
    "ILGA PAUZĖ", "TESTAVIMO POZICIJA", "GALUTINĖ POZICIJA", None
]

CONTEXT_VIDEO_SIZE = [480, 854] # Change when importing the actual video
INSTRUCTIONS_VIDEO_SIZE = [360, 480]

CONTEXT_TEXT = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed faucibus at sapien ac egestas. "
    "Morbi quis tellus ut mauris efficitur pellentesque ac luctus nisl. Pellentesque pharetra sapien dui. "
    "Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. "
    "Vivamus a tortor nec elit auctor sagittis eu at risus. Nulla ut ex eu justo luctus blandit ac non ipsum. "
    "Mauris sollicitudin fringilla eros, ac vulputate orci sagittis non. "
    "Donec a tortor vestibulum, blandit enim quis, convallis dolor. Curabitur laoreet justo quis rutrum pellentesque. "
    "Curabitur nisi ex, ornare eu blandit at, pulvinar eu eros. Proin sollicitudin massa sed nibh sollicitudin bibendum. "
)
