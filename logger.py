import logging

logging.getLogger("PIL").setLevel(logging.WARNING)

class LogColors:
    RESET = "\033[0m"
    GREY = "\033[90m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    BOLD_RED = "\033[1;31m"

class ColorFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG: LogColors.GREY + "%(asctime)s [DEBUG] %(name)s: %(message)s" + LogColors.RESET,
        logging.INFO: LogColors.GREEN + "%(asctime)s [INFO]  %(name)s: %(message)s" + LogColors.RESET,
        logging.WARNING: LogColors.YELLOW + "%(asctime)s [WARN]  %(name)s: %(message)s" + LogColors.RESET,
        logging.ERROR: LogColors.RED + "%(asctime)s [ERROR] %(name)s: %(message)s" + LogColors.RESET,
        logging.CRITICAL: LogColors.BOLD_RED + "%(asctime)s [CRIT]  %(name)s: %(message)s" + LogColors.RESET
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%H:%M:%S")
        return formatter.format(record)

def get_logger(name: str, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:  
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(ColorFormatter())
        logger.addHandler(ch)

    return logger