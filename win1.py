#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:     Окно с теорией по спискам и кортежам
# Author:      Студент
# Created:     29.10.2025
#-------------------------------------------------------------------------------

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, 
    QScrollArea, QTextEdit
)
from win2 import TestWin

main_text = 'Тестирование "Списки и кортежи в Python"'
win_x, win_y = 200, 100
win_width, win_height = 1000, 600

class TheoryWin(QWidget):
    def __init__(self, fio, age):
        super().__init__()
        self.fio = fio
        self.age = age
        self.set_appear()
        self.initUI()
        self.connects()
        self.show()

    def set_appear(self):
        self.setWindowTitle(main_text)
        self.resize(win_width, win_height)
        self.move(win_x, win_y)

    def initUI(self):
        # Заголовок
        title = QLabel("Теория: Списки и кортежи в Python")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        
        # Текст теории
        theory_text = """
        <h2>Списки (Lists)</h2>
        <p><b>Список</b> - это изменяемая (mutable) упорядоченная коллекция элементов.</p>
        <ul>
            <li><b>Создание:</b> my_list = [1, 2, 3] или my_list = list()</li>
            <li><b>Изменение:</b> my_list[0] = 10</li>
            <li><b>Добавление:</b> my_list.append(4), my_list.insert(1, 5)</li>
            <li><b>Удаление:</b> my_list.remove(2), del my_list[0]</li>
            <li><b>Методы:</b> append(), extend(), insert(), remove(), pop(), sort(), reverse()</li>
        </ul>
        
        <h2>Кортежи (Tuples)</h2>
        <p><b>Кортеж</b> - это неизменяемая (immutable) упорядоченная коллекция элементов.</p>
        <ul>
            <li><b>Создание:</b> my_tuple = (1, 2, 3) или my_tuple = tuple([1, 2, 3])</li>
            <li><b>Особенности:</b> Нельзя изменить после создания</li>
            <li><b>Преимущества:</b> Быстрее списков, безопаснее (данные защищены от изменений)</li>
            <li><b>Использование:</b> Для хранения констант, ключей словарей, возврата нескольких значений из функции</li>
        </ul>
        
        <h2>Основные различия</h2>
        <table border="1" cellpadding="5">
            <tr><th>Характеристика</th><th>Список</th><th>Кортеж</th></tr>
            <tr><td>Изменяемость</td><td>✓ Изменяемый</td><td>✗ Неизменяемый</td></tr>
            <tr><td>Синтаксис</td><td>[] (квадратные скобки)</td><td>() (круглые скобки)</td></tr>
            <tr><td>Скорость</td><td>Медленнее</td><td>Быстрее</td></tr>
            <tr><td>Память</td><td>Больше</td><td>Меньше</td></tr>
            <tr><td>Использование</td><td>Для изменяемых данных</td><td>Для констант, ключей</td></tr>
        </table>
        
        <h2>Примеры операций</h2>
        <pre>
        # Списки
        fruits = ["apple", "banana", "cherry"]
        fruits.append("orange")  # Добавить элемент
        fruits[1] = "kiwi"      # Изменить элемент
        
        # Кортежи
        colors = ("red", "green", "blue")
        # colors[1] = "yellow"  # ОШИБКА! Нельзя изменить
        
        # Преобразования
        list_to_tuple = tuple([1, 2, 3])
        tuple_to_list = list((1, 2, 3))
        
        # Срезы (работают для обоих)
        my_data = [0, 1, 2, 3, 4, 5]
        print(my_data[1:4])    # [1, 2, 3]
        print(my_data[:3])     # [0, 1, 2]
        print(my_data[3:])     # [3, 4, 5]
        </pre>
        """
        
        # Область с прокруткой для теории
        scroll = QScrollArea()
        theory_widget = QWidget()
        theory_layout = QVBoxLayout()
        
        theory_label = QLabel()
        theory_label.setText(theory_text)
        theory_label.setWordWrap(True)
        theory_label.setTextFormat(Qt.RichText)
        
        theory_layout.addWidget(theory_label)
        theory_widget.setLayout(theory_layout)
        scroll.setWidget(theory_widget)
        scroll.setWidgetResizable(True)
        
        # Кнопка
        self.next_button = QPushButton('Начать тестирование')
        self.next_button.setMinimumHeight(40)
        
        # Основной макет
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(scroll)
        layout.addWidget(self.next_button)
        
        self.setLayout(layout)

    def connects(self):
        self.next_button.clicked.connect(self.next_click)

    def next_click(self):
        self.hide()
        self.tw = TestWin(self.fio, self.age)
        self.tw.show()