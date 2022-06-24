import random
import threading

from kivy.animation import Animation
from kivy.clock import mainthread
from kivy.properties import StringProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.screenmanager import SlideTransition, NoTransition
from kivymd.uix.card import MDCard
from kivymd.uix.screen import MDScreen


######################################
#          MDElements                #
######################################

class SubjectCard(MDCard):
    heading_text = StringProperty()
    description_text = StringProperty()


class SignButton(Button):
    bg_color = ListProperty([1, 1, 1, 1])


class OptionButton(Button):
    bg_color = ListProperty([1, 1, 1, 1])


#########################################
#           MDScreens                   #
#########################################

class EnglishStartScreen(MDScreen):
    def __init__(self, **kwargs):
        super(EnglishStartScreen, self).__init__(*kwargs)
        self.name = 'english_start'


class SubjectScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SubjectScreen, self).__init__(**kwargs)
        self.name = 'subjects'


class MathStartScreen(MDScreen):
    def __init__(self, **kwargs):
        super(MathStartScreen, self).__init__(**kwargs)
        self.name = 'math_start'


class ScienceStartScreen(MDScreen):
    def __init__(self, **kwargs):
        super(ScienceStartScreen, self).__init__(**kwargs)
        self.name = 'science_start'


class FinalScoreScreen(MDScreen):
    def __init__(self, **kwargs):
        super(FinalScoreScreen, self).__init__(**kwargs)
        self.name = 'final_score'


class SubjectListScreen(MDScreen):
    def __init__(self, **kwargs):
        super(SubjectListScreen, self).__init__(**kwargs)
        self.name = 'subject_list'

    def subject_choice(self, choice):
        self.manager.current = choice


class PreloaderScreen(MDScreen):
    angle = 45/2

    @mainthread
    def change_screen(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'subject_list'
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


class SelectSignScreen(MDScreen):
    pass


class QuizScreen(MDScreen):
    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)
        self.answer = None
        self.selected_sign = ""
        self.correct = 0
        self.wrong = 0

    def select_sign(self, sign):
        self.manager.current = 'quiz'
        self.selected_sign = sign
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        self.manager.get_screen('quiz').ids.question.text = f"{num1} {sign} {num2} = ?"

        if sign == "+":
            self.answer = str(num1 + num2)
        elif sign == "–":
            self.answer = str(num1 - num2)
        elif sign == "×":
            self.answer = str(num1 * num2)
        elif sign == "÷":
            self.answer = str(round((num1 / num2), 2))

        option_list = [self.answer]
        option_len = 1
        while option_len < 4:
            option = 0
            if sign == "+":
                option = random.randint(1, 20)
            elif sign == "–":
                option = random.randint(-10, 10)
            elif sign == "×":
                option = random.randint(1, 100)
            elif sign == "÷":
                option = str(round(random.uniform(1, 10), 2))
            if option not in option_list:
                option_list.append(option)
            else:
                option_len -= 1
            option_len += 1

        random.shuffle(option_list)
        for i in range(1, 5):
            self.manager.get_screen('quiz').ids[f"option_{i}"].text = str(option_list[i - 1])

    def get_id(self, instance):
        for id, widget in enumerate(reversed(instance.parent.children), start=1):
            if widget.__self__ == instance:
                return f"option_{id}"

    def quiz(self, option, instance):
        if option == self.answer:
            self.ids[self.get_id(instance)].bg_color = [0, 1, 0, 1]
            option_id_list = [f"option_{i}" for i in range(1, 5)]
            option_id_list.remove(self.get_id(instance))
            for option_id in option_id_list:
                self.ids[option_id].disabled = True
            self.correct += 1
        else:
            for i in range(1, 5):
                if self.ids[f"option_{i}"].text == self.answer:
                    self.ids[f"option_{i}"].bg_color = [0, 1, 0, 1]
                else:
                    self.ids[f"option_{i}"].disabled = True
            self.ids[self.get_id(instance)].bg_color = [1, 0, 0, 1]
            self.ids[self.get_id(instance)].disabled_color = [1, 1, 1, 1]
            self.wrong += 1

    def next_question(self):
        self.select_sign(self.selected_sign)
        for i in range(1, 5):
            self.ids[f"option_{i}"].disabled = False
            self.ids[f"option_{i}"].bg_color = (40/255, 6/255, 109/255, 1)
            self.ids[f"option_{i}"].disabled_color = (1, 1, 1, .3)

    def replay(self):
        self.correct = 0
        self.wrong = 0
        self.manager.current = 'select_sign'

    def final_score(self):
        if self.correct == 0 and self.wrong == 0:
            self.manager.current = 'select_sign'
        else:
            for i in range(1, 5):
                self.ids[f"option_{i}"].disabled = False
                self.ids[f"option_{i}"].bg_color = (40 / 255, 6 / 255, 109 / 255, 1)
                self.ids[f"option_{i}"].disabled_color = (1, 1, 1, .3)
            percentage_score = round((self.correct/(self.correct + self.wrong)) * 100)
            final_score_screen = self.manager.get_screen('final_score')
            final_score_screen.correct.text = f"{self.correct} - Correct"
            final_score_screen.wrong.text = f"{self.wrong} - Wrong"
            final_score_screen.percentage_score.text = f"{percentage_score}% Correct"
            self.manager.current = 'final_score'
