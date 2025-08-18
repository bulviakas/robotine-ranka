import logging
import sys

logging.getLogger("PIL").setLevel(logging.WARNING)

class ColorFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[90m",   # Gray
        "INFO": "\033[97m",    # White
        "WARNING": "\033[93m", # Yellow
        "ERROR": "\033[91m",   # Red
        "CRITICAL": "\033[31m" # Dark Red
    }

    LOGGER_COLORS = {
        "Main": "\033[32m",          # Dark Green
        "Pages": "\033[34m",         # Dark Blue
        "Block": "\033[92m",         # Bright green
        "Video Player": "\033[95m",  # Purple
        "Command Line": "\033[33m",   # Yellow
        "Language Handler": "\033[31m"
    }

    RESET = "\033[0m"

    def format(self, record):
        level_color = self.COLORS.get(record.levelname, "")
        logger_color = self.LOGGER_COLORS.get(record.name, "")
        
        if record.levelname == "DEBUG":
            # DEBUG: only level in gray, rest normal
            gray = self.COLORS["DEBUG"]
            return f"{gray}[{self.formatTime(record, '%H:%M:%S')}] [{record.name}] [{record.levelname}] {record.getMessage()}{self.RESET}"
        else:
            # Others: color logger name + message
            levelname = f"{level_color}{record.levelname}{self.RESET}"
            name = f"{logger_color}{record.name}{self.RESET}"
            msg = f"{logger_color}{record.getMessage()}{self.RESET}"

        return f"[{self.formatTime(record, '%H:%M:%S')}] [{name}] [{levelname}] {msg}"


# --- Logger Factory ---
def get_logger(name: str, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(ColorFormatter())
        logger.addHandler(handler)

    return logger


# --- Usage ---
log_main = get_logger("Main")
log_pages = get_logger("Pages")
log_block = get_logger("Block")
log_video = get_logger("Video Player")
log_cmd   = get_logger("Command Line")


# --- Example ---
if __name__ == "__main__":
    log_main.info("App started")
    log_pages.debug("video width: 683 height: 512")
    log_block.warning("Block misaligned")
    log_video.info("Video stopped")
    log_cmd.info("Clearing...")