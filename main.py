import os
import random
import threading
from os.path import join

from kivy.animation import Animation
from kivy.clock import mainthread, Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, NoTransition, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen

Window.size = (800, 480)
fn_path = join(os.getcwd(), 'assets', 'fonts')

Builder.load_file('kivy-files/subjects/subject_list.kv')
Builder.load_file("kivy-files/math/start.kv")
Builder.load_file("kivy-files/preloader/preloader.kv")
Builder.load_file('kivy-files/math/select_sign.kv')
Builder.load_file('kivy-files/math/quiz.kv')
Builder.load_file('kivy-files/math/final_score.kv')


class SubjectCard(MDCard):
    heading_text = StringProperty()
    description_text = StringProperty()


class SignButton(Button):
    bg_color = ListProperty([1, 1, 1, 1])


class OptionButton(Button):
    bg_color = ListProperty([1, 1, 1, 1])


class SubjectListScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SubjectListScreen, self).__init__(**kwargs)

    def subject_choice(self, choice):
        self.manager.current = choice


class PreloaderScreen(MDScreen):
    angle = 45/2

    @mainthread
    def change_screen(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'subjects'
        self.manager.transition = NoTransition()

    def loading(self, *args):
        anim = Animation(height=80, width=80, spacing=[10, 10], duration=0.25)
        anim += Animation(height=60, width=60, spacing=[5, 5], duration=0.25)
        anim += Animation(angle=self.angle, duration=0.25)
        anim.bind(on_complete=self.loading)
        anim.start(self.ids.loading)
        self.angle += 45/2

    def start_preloader(self):
        threading.Timer(4.0, self.change_screen).start()
        self.loading()


class SubjectScreen(MDScreen):
    pass


class MathStartScreen(MDScreen):
    pass


class SelectSignScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SelectSignScreen, self).__init__(**kwargs)
        self.answer = None
        self.selected_sign = ""

    def select_sign(self, sign):
        self.manager.current = 'quiz'
        self.selected_sign = sign
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        self.manager.get_screen('quiz').ids.question.text = f"{num1} {sign} {num2} = ?"
        if sign == "+":
            self.answer = str(num1 + num2)
        elif sign == "-":
            self.answer = str(num1 - num2)
        elif sign == "×":
            self.answer = str(num1 * num2)
        elif sign == "÷":
            self.answer = str(round((num1 / num2), 2))

        # option = [self.answer]
        # option_len = 1
        # while option_len < 4:
        #


class QuizScreen(MDScreen):
    pass


class FinalScoreScreen(MDScreen):
    pass


class MakiniApp(MDApp):
    def __init__(self, **kwargs):
        super(MakiniApp, self).__init__(**kwargs)
        self.preloader_screen = PreloaderScreen()
        self.screen_manager = ScreenManager(transition=NoTransition())

    def build(self):
        self.screen_manager.add_widget(self.preloader_screen)
        self.screen_manager.add_widget(SubjectListScreen())

        self.screen_manager.add_widget(MathStartScreen())
        self.screen_manager.add_widget(SelectSignScreen())
        self.screen_manager.add_widget(QuizScreen())
        self.screen_manager.add_widget(FinalScoreScreen())

        return self.screen_manager


    def on_start(self):
        self.preloader_screen.start_preloader()


if __name__ == "__main__":
    LabelBase.register(name='LuckiestGuy', fn_regular=join(fn_path, 'LuckiestGuy-Regular.ttf'))
    LabelBase.register(name='Andika', fn_regular=join(fn_path, 'Andika.ttf'))

    MakiniApp().run()
