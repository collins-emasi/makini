import random
import threading

from kivy.animation import Animation
from kivy.clock import mainthread
from kivy.properties import StringProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import SlideTransition, NoTransition
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen


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
