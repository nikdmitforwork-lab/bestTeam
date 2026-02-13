#-------------------------------------------------------------------------------
# Name:        module4
# Purpose:     Окно с результатами тестирования
# Author:      Студент
# Created:     29.10.2025
#-------------------------------------------------------------------------------

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QPushButton, 
    QHBoxLayout, QTableWidget, QTableWidgetItem, 
    QTextEdit, QHeaderView
)
import json
import os
from datetime import datetime
from win2_1 import QUESTIONS

# Глобальная переменная для истории всех попыток
ALL_RESULTS = []

class ResultWin(QWidget):
    def __init__(self, fio, age, answers):
        super().__init__()
        self.fio = fio
        self.age = age
        self.answers = answers
        self.score = 0
        self.calculate_score()
        
        # Сохранение результатов в историю
        result_data = {
            'fio': fio,
            'age': age,
            'answers': answers.copy(),
            'score': self.score,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'percentage': int((self.score / len(QUESTIONS)) * 100)
        }
        ALL_RESULTS.append(result_data)
        
        # Сохранение в файл
        self.save_to_file(result_data)
        
        self.set_appear()
        self.initUI()
        self.show()

    def calculate_score(self):
        for i, answer in enumerate(self.answers):
            if answer is not None and answer == QUESTIONS[i]['correct']:
                self.score += 1

    def save_to_file(self, result_data):
        try:
            # Создаем папку для результатов, если ее нет
            if not os.path.exists('results'):
                os.makedirs('results')
            
            filename = f"results/test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")

    def set_appear(self):
        self.setWindowTitle("Результаты тестирования")
        self.resize(900, 700)
        self.move(200, 50)

    def initUI(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel(f"Результаты теста: {self.fio}")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px;")
        layout.addWidget(title)
        
        # Общая статистика
        total = len(QUESTIONS)
        percentage = int((self.score / total) * 100)
        
        stats_text = f"""
        <div style='font-size: 16px;'>
        <b>Возраст:</b> {self.age}<br>
        <b>Правильных ответов:</b> {self.score} из {total}<br>
        <b>Процент выполнения:</b> {percentage}%<br>
        <b>Оценка:</b> {self.get_grade(percentage)}
        </div>
        """
        
        stats_label = QLabel(stats_text)
        stats_label.setAlignment(Qt.AlignCenter)
        stats_label.setTextFormat(Qt.RichText)
        layout.addWidget(stats_label)
        
        # Прогресс-бар (текстовый)
        progress_text = "[" + "█" * (percentage // 10) + "░" * (10 - percentage // 10) + "]"
        progress_label = QLabel(progress_text)
        progress_label.setAlignment(Qt.AlignCenter)
        progress_label.setStyleSheet("font-size: 24px; margin: 10px;")
        layout.addWidget(progress_label)
        
        # Детализация ответов
        details_label = QLabel("<b>Детализация по вопросам:</b>")
        details_label.setTextFormat(Qt.RichText)
        layout.addWidget(details_label)
        
        # Таблица с результатами
        table = QTableWidget(len(QUESTIONS), 4)
        table.setHorizontalHeaderLabels(["Вопрос", "Ваш ответ", "Правильный ответ", "Результат"])
        
        for i in range(len(QUESTIONS)):
            # Вопрос
            question_item = QTableWidgetItem(f"Вопрос {i+1}")
            
            # Ваш ответ
            user_answer = self.answers[i]
            if user_answer is not None:
                user_text = f"{chr(65 + user_answer)}) {QUESTIONS[i]['options'][user_answer]}"
            else:
                user_text = "Нет ответа"
            user_item = QTableWidgetItem(user_text)
            
            # Правильный ответ
            correct_idx = QUESTIONS[i]['correct']
            correct_text = f"{chr(65 + correct_idx)}) {QUESTIONS[i]['options'][correct_idx]}"
            correct_item = QTableWidgetItem(correct_text)
            
            # Результат
            if user_answer == correct_idx:
                result_item = QTableWidgetItem("✓ Верно")
                result_item.setForeground(Qt.darkGreen)
                user_item.setForeground(Qt.darkGreen)
            elif user_answer is None:
                result_item = QTableWidgetItem("✗ Нет ответа")
                result_item.setForeground(Qt.gray)
                user_item.setForeground(Qt.gray)
            else:
                result_item = QTableWidgetItem("✗ Неверно")
                result_item.setForeground(Qt.red)
                user_item.setForeground(Qt.red)
            
            table.setItem(i, 0, question_item)
            table.setItem(i, 1, user_item)
            table.setItem(i, 2, correct_item)
            table.setItem(i, 3, result_item)
        
        table.resizeColumnsToContents()
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setMaximumHeight(300)
        layout.addWidget(table)
        
        # Рекомендации
        recommendations = self.get_recommendations(percentage)
        rec_label = QLabel(f"<b>Рекомендации:</b><br>{recommendations}")
        rec_label.setWordWrap(True)
        rec_label.setTextFormat(Qt.RichText)
        rec_label.setStyleSheet("background-color: #f0f8ff; padding: 10px; border-radius: 5px;")
        layout.addWidget(rec_label)
        
        # История попыток (если есть)
        if len(ALL_RESULTS) > 1:
            history_label = QLabel("<b>История ваших попыток:</b>")
            history_label.setTextFormat(Qt.RichText)
            layout.addWidget(history_label)
            
            history_text = QTextEdit()
            history_text.setReadOnly(True)
            history_text.setMaximumHeight(100)
            
            history_content = ""
            for i, result in enumerate(ALL_RESULTS[-5:]):  # Последние 5 попыток
                history_content += (
                    f"{i+1}. {result['fio']} - {result['score']}/{len(QUESTIONS)} "
                    f"({result['percentage']}%) - {result['timestamp']}\n"
                )
            
            history_text.setText(history_content)
            layout.addWidget(history_text)
        
        # Кнопки
        button_layout = QHBoxLayout()
        
        restart_btn = QPushButton("Пройти тест заново")
        restart_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        
        theory_btn = QPushButton("Вернуться к теории")
        theory_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        
        close_btn = QPushButton("Завершить")
        close_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px;")
        
        button_layout.addWidget(restart_btn)
        button_layout.addWidget(theory_btn)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Подключение кнопок
        restart_btn.clicked.connect(self.restart_test)
        theory_btn.clicked.connect(self.return_to_theory)
        close_btn.clicked.connect(self.close)

    def get_grade(self, percentage):
        if percentage >= 90:
            return "5 (Отлично)"
        elif percentage >= 75:
            return "4 (Хорошо)"
        elif percentage >= 60:
            return "3 (Удовлетворительно)"
        elif percentage >= 40:
            return "2 (Неудовлетворительно)"
        else:
            return "1 (Плохо)"

    def get_recommendations(self, percentage):
        if percentage >= 90:
            return "Отличный результат! Вы прекрасно разбираетесь в списках и кортежах. Можете переходить к более сложным темам."
        elif percentage >= 75:
            return "Хороший результат! У вас есть прочные знания, но стоит повторить сложные моменты."
        elif percentage >= 60:
            return "Удовлетворительный результат. Рекомендуется повторить теорию и практиковаться с примерами."
        else:
            return "Нужно больше практики! Рекомендуется внимательно изучить теорию и выполнить практические задания."

    def restart_test(self):
        from win2 import TestWin
        self.hide()
        self.new_test = TestWin(self.fio, self.age)
        self.new_test.show()

    def return_to_theory(self):
        from win1 import TheoryWin
        self.hide()
        self.theory = TheoryWin(self.fio, self.age)
        self.theory.show()