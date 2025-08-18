from logger import get_logger
logger = get_logger("Language Manager")

class LanguageManager:
    def __init__(self, canvas, default_lang="EN"):
        self.canvas = canvas
        self.lang = default_lang

        # FIXME add all translations and transfer them to a json file
        self.translations = {
            "EN": {"start": "Start", "quit": "Quit", "tutorial": "Tutorial"},
            "LT": {"start": "Pradėti", "quit": "Išeiti", "tutorial": "Pamoka"},
        }
        self.items = []  # list of (item_id, key)
        self.widgets = []  # list of (widget, key, type)

    def register_text(self, item_id, key):
        """Register a canvas text item for automatic translation"""
        self.items.append((item_id, key))
        self.update_item(item_id, key)
        logger.debug(f"Text {key} registered")

    def register_widget(self, widget, key, widget_type="text", var=None):
        """
        Register a widget for automatic translation.
        - widget: the tk widget
        - key: translation key
        - widget_type: 'text' (Label/Button), 'option' (OptionMenu), 'var' (StringVar)
        - var: for option menus or StringVars
        """
        self.widgets.append((widget, key, widget_type, var))
        logger.debug(f"Widget {key} registered")
        self.update_widget(widget, key, widget_type, var)

    def set_language(self, lang):
        if lang not in self.translations:
            logger.warning(f"Language '{lang}' not available!")
            return
        self.lang = lang
        logger.info(f"Updating everything to {lang}")
        for item_id, key in self.items:
            self.update_item(item_id, key)
        for widget, key, widget_type, var in self.widgets:
            self.update_widget(widget, key, widget_type, var)
        logger.info(f"App language updated to {lang}")

    def update_item(self, item_id, key):
        text = self.translations[self.lang].get(key, key)
        self.canvas.itemconfig(item_id, text=text)
        logger.debug(f"Item {key} updated")

    def update_widget(self, widget, key, widget_type, var):
        text = self.translations[self.lang].get(key, key)

        if widget_type == "text":  # Label, Button, etc.
            widget.config(text=text)

        elif widget_type == "var":  # linked variable
            var.set(text)

        elif widget_type == "option":  # OptionMenu
            menu = widget["menu"]
            menu.delete(0, "end")
            for lang in self.translations.keys():
                menu.add_command(
                    label=self.translations[lang]["language"],
                    command=lambda l=lang: self.set_language(l)
                )
            var.set(self.translations[self.lang]["language"])
        logger.debug(f"Widget {key} updated")