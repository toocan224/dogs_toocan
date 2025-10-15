from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit

app = QApplication([])

# Главное окно
window = QWidget()
window.setWindowTitle("Пример с виджетами")

# Виджеты
label = QLabel("Введите текст и нажмите кнопку")
button = QPushButton("Нажми меня")
input_field = QLineEdit()
input_field.setPlaceholderText("Введите текст")

# Компоновка
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(input_field)
layout.addWidget(button)
window.setLayout(layout)

# Отображение окна
window.show()
app.exec()