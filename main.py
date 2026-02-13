from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QPushButton, QWidget, QLabel, 
    QVBoxLayout, QLineEdit, QSpinBox, QHBoxLayout
)
from win1 import TheoryWin

# Константы
main_text = 'Тестирование "Списки и кортежи в Python"'
instr = 'Перед началом тестирования введите свои данные'
win_x, win_y = 200, 100
win_width, win_height = 1000, 600

class MainWin(QWidget):
    def __init__(self):
        super().__init__()
        self.set_appear()
        self.initUI()
        self.connects()
        self.show()

    def set_appear(self):
        self.setWindowTitle(main_text)
        self.resize(win_width, win_height)
        self.move(win_x, win_y)

    def initUI(self):
        self.instruction = QLabel(instr)
        self.instruction.setAlignment(Qt.AlignCenter)
        self.instruction.setStyleSheet("font-size: 16px; font-weight: bold; margin: 20px;")
        
        # ФИО
        self.lfio = QLabel("Ваше ФИО:")
        self.fio = QLineEdit()
        self.fio.setPlaceholderText("Введите фамилию, имя, отчество")
        
        # Возраст
        self.lage = QLabel("Ваш возраст:")
        self.age = QSpinBox()
        self.age.setRange(10, 100)
        self.age.setValue(18)
        
        # Кнопка
        self.button = QPushButton('Перейти к теории')
        self.button.setMinimumHeight(40)
        
        # Макет
        layout = QVBoxLayout()
        layout.addWidget(self.instruction)
        
        # ФИО
        fio_layout = QHBoxLayout()
        fio_layout.addWidget(self.lfio)
        fio_layout.addWidget(self.fio)
        layout.addLayout(fio_layout)
        
        # Возраст
        age_layout = QHBoxLayout()
        age_layout.addWidget(self.lage)
        age_layout.addWidget(self.age)
        layout.addLayout(age_layout)
        
        layout.addStretch()
        layout.addWidget(self.button, alignment=Qt.AlignCenter)
        layout.addStretch()
        
        self.setLayout(layout)

    def connects(self):
        self.button.clicked.connect(self.next_click)

    def next_click(self):
        fio = self.fio.text().strip()
        age = self.age.value()
        
        if fio and len(fio) > 2:
            self.hide()
            self.tw = TheoryWin(fio, age)
            self.tw.show()
        else:
            self.fio.setStyleSheet("border: 2px solid red;")
            self.lfio.setText("Ваше ФИО (обязательно!):")

if __name__ == "__main__":
    app = QApplication([])
    mw = MainWin()
    app.exec_()