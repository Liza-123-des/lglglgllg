from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QHBoxLayout, 
                           QVBoxLayout, QGroupBox, QLabel, QRadioButton, 
                           QButtonGroup, QMessageBox)
import random

class Question:
    def __init__(self, question, right_answer, wrong1, wrong2, wrong3):
        self.question = question
        self.right_answer = right_answer
        self.wrong1 = wrong1
        self.wrong2 = wrong2
        self.wrong3 = wrong3

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.questions_list = [
            Question("2+2?", "4", "3", "5", "6"),
            Question("Столица России?", "Москва", "Санкт-Петербург", "Казань", "Сочи"),
            Question("Какой язык программирования мы изучаем?", "Python", "Java", "C++", "JavaScript")
        ]
        self.total_questions = len(self.questions_list)
        self.correct_answers = 0
        self.answered_questions = 0
        self.current_question = None
        self.setWindowTitle('Memory Card')
        self.resize(400, 300)
        self.lb_question = QLabel("Вопрос", alignment=Qt.AlignCenter)
        self.btn_answer = QPushButton("Ответить")
        self.RadioGroupBox = QGroupBox("Варианты ответов:")
        self.variant1 = QRadioButton()
        self.variant2 = QRadioButton()
        self.variant3 = QRadioButton()
        self.variant4 = QRadioButton()

        self.RadioGroup = QButtonGroup()
        self.RadioGroup.addButton(self.variant1)
        self.RadioGroup.addButton(self.variant2)
        self.RadioGroup.addButton(self.variant3)
        self.RadioGroup.addButton(self.variant4)

        v_layout = QVBoxLayout()
        h_layout1 = QHBoxLayout()
        h_layout2 = QHBoxLayout()
        
        h_layout1.addWidget(self.variant1)
        h_layout1.addWidget(self.variant2)
        h_layout2.addWidget(self.variant3)
        h_layout2.addWidget(self.variant4)
        
        v_layout.addLayout(h_layout1)
        v_layout.addLayout(h_layout2)
        self.RadioGroupBox.setLayout(v_layout)

        self.AnsGroupBox = QGroupBox("Результат:")
        self.lb_result = QLabel("Прав ты или нет?")
        self.lb_correct = QLabel("Правильный ответ")
        
        res_layout = QVBoxLayout()
        res_layout.addWidget(self.lb_result)
        res_layout.addWidget(self.lb_correct)
        self.AnsGroupBox.setLayout(res_layout)
        self.AnsGroupBox.hide()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.lb_question)
        main_layout.addWidget(self.RadioGroupBox)
        main_layout.addWidget(self.AnsGroupBox)
        main_layout.addWidget(self.btn_answer)
        self.setLayout(main_layout)
        self.btn_answer.clicked.connect(self.click_ok)
        self.next_question()
    
    def next_question(self):
        if self.answered_questions >= self.total_questions:
            if self.correct_answers == self.total_questions:
                self.show_congratulations()
            self.answered_questions = 0
            self.correct_answers = 0 
        self.current_question = random.choice(self.questions_list)
        self.ask(self.current_question)
        print(f"\nСтатистика: {self.correct_answers} из {self.total_questions}")
    
    def ask(self, q):
        self.lb_question.setText(q.question)
        answers = [q.right_answer, q.wrong1, q.wrong2, q.wrong3]
        random.shuffle(answers)
        self.variant1.setText(answers[0])
        self.variant2.setText(answers[1])
        self.variant3.setText(answers[2])
        self.variant4.setText(answers[3])
        self.correct_answer = q.right_answer
        self.lb_correct.setText(q.right_answer)
        self.show_question()
    
    def show_question(self):
        self.RadioGroupBox.show()
        self.AnsGroupBox.hide()
        self.btn_answer.setText("Ответить")
        self.RadioGroup.setExclusive(False)
        self.variant1.setChecked(False)
        self.variant2.setChecked(False)
        self.variant3.setChecked(False)
        self.variant4.setChecked(False)
        self.RadioGroup.setExclusive(True)
    
    def show_result(self):
        self.RadioGroupBox.hide()
        self.AnsGroupBox.show()
        self.btn_answer.setText("Следующий вопрос")
        self.answered_questions += 1
    
    def check_answer(self):
        selected = None
        for button in [self.variant1, self.variant2, self.variant3, self.variant4]:
            if button.isChecked():
                selected = button.text()
                break
        
        if selected == self.correct_answer:
            self.correct_answers += 1
            self.lb_result.setText("Правильно!")
        else:
            self.lb_result.setText("Неверно!")
        print(f"Рейтинг: {self.correct_answers/self.total_questions*100}%")
        self.show_result()
    
    def show_congratulations(self):
        msg = QMessageBox()
        msg.setWindowTitle("Поздравляем!")
        msg.setText("Вы ответили правильно на все вопросы!")
        msg.exec_()
    
    def click_ok(self):
        if self.btn_answer.text() == "Ответить":
            self.check_answer()
        else:
            self.next_question()


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()