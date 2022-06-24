from kivy.lang import Builder

subjects = {
    "Mathematics": "Learn Addition, subtraction, multiplication...",
    "English": "Learn grammar, vocabularies, spelling, composition...",
    "Kiswahili": "Jifunze misamiati ya lugha, ngeli, mitungo...",
    "Science": "Learn about the world, how to make work easier...",
}

b = Builder

b.load_file("kivy-files/subjects/subject_list.kv")
b.load_file("kivy-files/math/start.kv")
