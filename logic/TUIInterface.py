import os

from pygments.filter import Filter
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.widgets import Button, Header, Footer, Input
from LanguageQuizManager import Tester

class LanguageApp(App):
    CSS_PATH = "../language_app.tcss"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tester = Tester()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Filter languages...", id="filter_input")
        yield VerticalScroll(id="language_buttons")
        yield Footer()

    def on_mount(self) -> None:
        self.populate_language_buttons()

    def on_input_changed(self, event: Input.Changed) -> None:
        self.refresh_language_buttons()

    def refresh_language_buttons(self):
        filter_text = self.query_one("#filter_input").value.lower()
        language_buttons = self.query_one("#language_buttons")
        for button in language_buttons.children:
            if filter_text in button.label.plain.lower():
                button.visible = True
                button.display = True
            else:
                button.visible = False
                button.display=False


    def populate_language_buttons(self):
        filter_text = self.query_one("#filter_input").value.lower()

        timers = self.query("Button")
        [t.remove() for t in timers if t.id[0:4] == "lan_"]

        language_buttons = self.query_one("#language_buttons")


        all_button = Button(label="All", id="lan_all")
        language_buttons.mount(all_button)





        languages = self.tester.list_languages_with_full_names()
        for lang_code, lang_name in languages:
            if filter_text in lang_name.lower():
                button = Button(label=lang_name, id="lan_"+lang_code)
                language_buttons.mount(button)




    def on_button_pressed(self, event: Button.Pressed) -> None:

        if len(event.button.id)>4 and event.button.id[0:4] == "lan_":
            language = event.button.id[4:]
            if language == "all":
                self.tester.language = ""
            else:
                self.tester.language = language
            self.tester.play_audio()

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark

if __name__ == "__main__":
    app = LanguageApp()
    app.run()
