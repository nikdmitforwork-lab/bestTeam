#-------------------------------------------------------------------------------
# Name:        module3
# Purpose:     Окно с вопросами теста
# Author:      Студент
# Created:     29.10.2025
#-------------------------------------------------------------------------------

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QRadioButton, QPushButton, 
    QVBoxLayout, QHBoxLayout, QButtonGroup, QMessageBox
)
from win3 import ResultWin

# Константы
main_text = 'Тестирование "Списки и кортежи в Python"'
win_x, win_y = 200, 100
win_width, win_height = 1000, 600

# Вопросы и варианты ответов
QUESTIONS = [
    {
        'question': '1. Что такое список (list) в Python?',
        'options': [
            'Изменяемая упорядоченная коллекция элементов',
            'Неизменяемая упорядоченная коллекция элементов',
            'Неупорядоченная коллекция уникальных элементов',
            'Коллекция пар "ключ-значение"'
        ],
        'correct': 0
    },
    {
        'question': '2. Как создать пустой кортеж?',
        'options': [
            't = {}',
            't = []',
            't = ()',
            't = tuple()'
        ],
        'correct': 2
    },
    {
        'question': '3. Какой метод добавляет элемент в конец списка?',
        'options': [
            'insert()',
            'append()',
            'add()',
            'push()'
        ],
        'correct': 1
    },
    {
        'question': '4. Что вернет выражение: len([1, 2, 3, 4])?',
        'options': [
            '1',
            '4',
            '[1, 2, 3, 4]',
            'Ошибку'
        ],
        'correct': 1
    },
    {
        'question': '5. Как получить последний элемент списка my_list?',
        'options': [
            'my_list[0]',
            'my_list[-1]',
            'my_list[last]',
            'my_list[len(my_list)]'
        ],
        'correct': 1
    },
    {
        'question': '6. Какая операция НЕВОЗМОЖНА для кортежа?',
        'options': [
            'Конкатенация (сложение)',
            'Умножение на число',
            'Изменение элемента по индексу',
            'Получение среза'
        ],
        'correct': 2
    },
    {
        'question': '7. Как преобразовать список в кортеж?',
        'options': [
            'tuple(list)',
            'list(tuple)',
            'convert(list)',
            'list.to_tuple()'
        ],
        'correct': 0
    },
    {
        'question': '8. Что делает метод list.pop() без аргументов?',
        'options': [
            'Удаляет первый элемент',
            'Удаляет последний элемент и возвращает его',
            'Добавляет элемент в конец',
            'Очищает весь список'
        ],
        'correct': 1
    },
    {
        'question': '9. Что выведет код: print((1, 2) * 3)?',
        'options': [
            '(1, 2, 3)',
            '(3, 6)',
            '(1, 2, 1, 2, 1, 2)',
            'Ошибку'
        ],
        'correct': 2
    },
    {
        'question': '10. Какой из этих типов НЕИЗМЕНЯЕМ (immutable)?',
        'options': [
            'Список (list)',
            'Множество (set)',
            'Кортеж (tuple)',
            'Словарь (dict)'
        ],
        'correct': 2
    }
]

class TestWin(QWidget):
    def __init__(self, fio, age):
        super().__init__()
        self.fio = fio
        self.age = age
        self.answers = [None] * len(QUESTIONS)  # Ответы пользователя
        self.current_question = 0
        self.set_appear()
        self.initUI()
        self.connects()
        self.update_question()

    def set_appear(self):
        self.setWindowTitle(main_text)
        self.resize(win_width, win_height)
        self.move(win_x, win_y)

    def initUI(self):
        # Панель навигации (номера вопросов)
        self.nav_buttons = []
        nav_layout = QHBoxLayout()
        for i in range(len(QUESTIONS)):
            btn = QPushButton(str(i + 1))
            btn.setFixedSize(40, 40)
            self.nav_buttons.append(btn)
            nav_layout.addWidget(btn)
        nav_layout.addStretch()
        
        # Отображение номера текущего вопроса
        self.question_counter = QLabel()
        self.question_counter.setAlignment(Qt.AlignCenter)
        self.question_counter.setStyleSheet("font-size: 14px; margin: 10px;")
        
        # Текст вопроса
        self.question_label = QLabel()
        self.question_label.setWordWrap(True)
        self.question_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 20px;")
        
        # Группа радиокнопок
        self.radio_group = QButtonGroup(self)
        self.radio_buttons = []
        
        radio_layout = QVBoxLayout()
        for i in range(4):
            rb = QRadioButton()
            rb.setStyleSheet("font-size: 14px; margin: 5px;")
            self.radio_buttons.append(rb)
            self.radio_group.addButton(rb, i)
            radio_layout.addWidget(rb)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        self.prev_button = QPushButton("← Назад")
        self.prev_button.setEnabled(False)
        
        self.next_button = QPushButton("Далее →")
        
        self.finish_button = QPushButton("Завершить тест")
        self.finish_button.setStyleSheet("background-color: #ff6b6b; color: white;")
        self.finish_button.hide()
        
        button_layout.addWidget(self.prev_button)
        button_layout.addStretch()
        button_layout.addWidget(self.finish_button)
        button_layout.addStretch()
        button_layout.addWidget(self.next_button)
        
        # Основной макет
        layout = QVBoxLayout()
        layout.addLayout(nav_layout)
        layout.addWidget(self.question_counter)
        layout.addWidget(self.question_label)
        layout.addLayout(radio_layout)
        layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def connects(self):
        # Подключение кнопок навигации
        for i, btn in enumerate(self.nav_buttons):
            btn.clicked.connect(lambda checked, idx=i: self.go_to_question(idx))
        
        # Подключение кнопок управления
        self.prev_button.clicked.connect(self.prev_question)
        self.next_button.clicked.connect(self.next_question)
        self.finish_button.clicked.connect(self.show_results)

    def go_to_question(self, index):
        self.save_current_answer()
        self.current_question = index
        self.update_question()

    def save_current_answer(self):
        checked_id = self.radio_group.checkedId()
        if checked_id != -1:
            self.answers[self.current_question] = checked_id

    def update_question(self):
        # Сброс выбора радиокнопок
        self.radio_group.setExclusive(False)
        for rb in self.radio_buttons:
            rb.setChecked(False)
        self.radio_group.setExclusive(True)
        
        # Обновление текста вопроса
        q_data = QUESTIONS[self.current_question]
        self.question_label.setText(q_data['question'])
        
        # Обновление вариантов ответов
        for i, option in enumerate(q_data['options']):
            self.radio_buttons[i].setText(f"{chr(65 + i)}) {option}")
        
        # Восстановление сохраненного ответа
        if self.answers[self.current_question] is not None:
            idx = self.answers[self.current_question]
            self.radio_buttons[idx].setChecked(True)
        
        # Обновление счетчика
        self.question_counter.setText(
            f"Вопрос {self.current_question + 1} из {len(QUESTIONS)}"
        )
        
        # Обновление навигационных кнопок
        for i, btn in enumerate(self.nav_buttons):
            if i == self.current_question:
                btn.setStyleSheet("background-color: #4d90fe; color: white; font-weight: bold;")
            elif self.answers[i] is not None:
                btn.setStyleSheet("background-color: #90ee90;")
            else:
                btn.setStyleSheet("")
        
        # Обновление кнопок управления
        self.prev_button.setEnabled(self.current_question > 0)
        
        if self.current_question == len(QUESTIONS) - 1:
            self.next_button.hide()
            self.finish_button.show()
        else:
            self.next_button.show()
            self.finish_button.hide()

    def prev_question(self):
        self.save_current_answer()
        if self.current_question > 0:
            self.current_question -= 1
            self.update_question()

    def next_question(self):
        self.save_current_answer()
        if self.current_question < len(QUESTIONS) - 1:
            self.current_question += 1
            self.update_question()

    def show_results(self):
        self.save_current_answer()
        
        # Проверка, все ли вопросы отвечены
        unanswered = [i+1 for i, ans in enumerate(self.answers) if ans is None]
        
        if unanswered:
            reply = QMessageBox.question(
                self, 'Не все вопросы отвечены',
                f'Вы не ответили на вопросы: {", ".join(map(str, unanswered))}\n'
                'Все равно завершить тест?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.No:
                return
        
        self.hide()
        self.result_win = ResultWin(self.fio, self.age, self.answers)
        self.result_win.show()