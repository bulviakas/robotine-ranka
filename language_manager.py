from logger import get_logger
logger = get_logger("Language Manager")
import tkinter as tk

class LanguageManager:
    def __init__(self, canvas, default_lang="EN"):
        self.canvas = canvas
        self.lang = default_lang

        # FIXME add all translations and transfer them to a json file
        self.translations = {
            "EN": {"start": "Start", "quit": "Quit", "tutorial": "Tutorial"},
            "LT": {"start": "Pradėti", "quit": "Išeiti", "tutorial": "Pamoka"},
        }

        self.widgets = []  # list of (widget, key, kwargs)

    def register_text(self, item_id, key):
        
        self.items.append((item_id, key))
        self.update_item(item_id, key)
        logger.debug(f"Text {key} registered")

    def register_widget(self, widget, key, **kwargs):
        """
        Register a widget with a translation key.
        kwargs may include 'text', 'item_id' (for canvas), etc.
        """
        self.widgets.append((widget, key, kwargs))
        logger.debug(f"Widget {key} registered")
        self.update_widget(widget, key, kwargs)

    def set_language(self, lang):
        if lang not in self.translations:
            logger.warning(f"Language '{lang}' not available")
            return
        self.lang = lang
        logger.info(f"Updating everything to {lang}")
        for widget, key, kwargs in self.widgets:
            self.update_widget(widget, key, kwargs)
        logger.info(f"App language updated to {lang}")

    def update_widget(self, widget, key, kwargs):
        text = self.translations.get(self.lang, {}).get(key, key)

        if isinstance(widget, tk.Canvas) and "item_id" in kwargs:
            widget.itemconfig(kwargs["item_id"], text=text)
            logger.debug(f"Canvas item {text} updated")

        elif hasattr(widget, "config"):
            widget.config(text=text)
            logger.debug(f"Widget {text} updated")

        else:
            logger.error(f"Unsupported widget type for {widget} with key {key}")