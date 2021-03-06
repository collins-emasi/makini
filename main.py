from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp

from classes import *
from settings import *


class MakiniApp(MDApp):
    def __init__(self, **kwargs):
        super(MakiniApp, self).__init__(**kwargs)
        self.preloader_screen = PreloaderScreen()
        self.screen_manager = ScreenManager(transition=NoTransition())

    def build(self):
        # Screen Preloader
        self.screen_manager.add_widget(self.preloader_screen)

        # Subject List
        self.screen_manager.add_widget(SubjectListScreen())

        # Mathematics
        self.screen_manager.add_widget(MathStartScreen())
        self.screen_manager.add_widget(SelectSignScreen())
        self.screen_manager.add_widget(QuizScreen())
        self.screen_manager.add_widget(FinalScoreScreen())

        # Science
        self.screen_manager.add_widget(ScienceStartScreen())
        self.screen_manager.add_widget(ScienceTopicsScreen())

        # English
        self.screen_manager.add_widget(EnglishStartScreen())

        # Kiswahili
        self.screen_manager.add_widget(KiswahiliStartScreen())

        return self.screen_manager

    def on_start(self):
        self.preloader_screen.start_preloader()


if __name__ == "__main__":
    LabelBase.register(name='LuckiestGuy', fn_regular=join(fn_path, 'LuckiestGuy-Regular.ttf'))
    LabelBase.register(name='Andika', fn_regular=join(fn_path, 'Andika.ttf'))

    MakiniApp().run()
