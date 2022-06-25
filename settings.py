import os
from os.path import join

from kivy.core.window import Window
from kivy.lang import Builder

# Define fonts path
fn_path = join(os.getcwd(), 'assets', 'fonts')

# Define Window size
Window.size = (800, 480)

# Load the kivy files
Builder.load_file('kivy-files/subjects/subject_list.kv')
Builder.load_file("kivy-files/math/start.kv")
Builder.load_file("kivy-files/preloader/preloader.kv")
Builder.load_file('kivy-files/math/select_sign.kv')
Builder.load_file('kivy-files/math/quiz.kv')
Builder.load_file('kivy-files/math/final_score.kv')

Builder.load_file("kivy-files/science/science_start.kv")
Builder.load_file("kivy-files/science/science_topics.kv")

Builder.load_file("kivy-files/english/english_start.kv")

Builder.load_file("kivy-files/kiswahili/kiswahili_start.kv")
