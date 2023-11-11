import sqlite3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QInputDialog

ball_count = 0


class Spravka(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('SpravkaWindow.ui', self)
        with open('text.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        self.label_2.setText(text)
        self.OkDialogButton.clicked.connect(self.closeSpravka)

    def closeSpravka(self):
        self.close()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MainWindow.ui', self)
        self.SpravkaButton.clicked.connect(self.openSpravka)
        self.LevelButton.clicked.connect(self.openLevel)
        self.HistoryButton.clicked.connect(self.openHistory)

    def openSpravka(self):
        spravka_dialog = Spravka()
        spravka_dialog.exec_()

    def openLevel(self):
        self.close()
        self.level_window = LevelWindow()
        self.level_window.show()

    def openHistory(self):
        self.history_window = HistoryWindow()

        self.history_window.show()


class LevelWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('LevelWindow.ui', self)
        self.ex = ex
        self.EasyButton.clicked.connect(self.open_first_level)
        self.NormalButton.clicked.connect(self.open_second_level)
        self.HardButton.clicked.connect(self.open_third_level)
        self.returnToMenu.clicked.connect(self.return_to_menu)

    def return_to_menu(self):
        self.close()
        self.ex.show()

    def open_first_level(self):
        self.close()
        self.first_level = FirstLevel(4)
        self.first_level.show()

    def open_second_level(self):
        self.close()
        self.second_level = SecondLevel()
        self.second_level.show()

    def open_third_level(self):
        self.close()
        self.third_level = ThirdLevel()
        self.third_level.show()


class FirstLevel(QMainWindow):
    def __init__(self, n):
        super().__init__()
        uic.loadUi('FirstLevel.ui', self)
        self.ex = ex
        self.label_list2 = [self.label_6, self.label_3, self.label_4, self.label_7]
        self.button_list2 = [self.pushButton, self.pushButton_5, self.pushButton_3, self.pushButton_2]
        self.counter1 = 0
        self.counter = 0
        self.opened_cards = 0
        self.max_opened_cards = 2
        self.right_image = []
        self.buttons = []
        self.i = []
        self.count3 = 0
        for btn in self.button_list2:
            btn.clicked.connect(self.open)

    def open(self):
        sender = self.sender()
        # if self.opened_cards == 0:
        if len(self.i) == 0 or len(self.i) == 1:
            sender.setVisible(False)
            self.buttons.append(sender)
            self.opened_cards += 1
            self.i.append(self.label_list2[self.button_list2.index(sender)])
        elif len(self.i) == 2:
            sender.setVisible(False)
            self.opened_cards = 0
            self.closeAllCards()
            self.i = []
            self.buttons = []
            self.buttons.append(sender)
            self.i.append(self.label_list2[self.button_list2.index(sender)])
        if all(not b.isVisible() for b in self.button_list2):
            name, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                                    "Введи имя чтобы сохранить резулььтат:")
            if ok_pressed:
                con = sqlite3.connect("results.sqlite")
                cur = con.cursor()
                r = cur.execute("SELECT id FROM res WHERE name = ? AND id_level = 1", (name,)).fetchone()
                print(r)
                if r:
                    cur.execute("""UPDATE res SET count = ? WHERE id = ?""", (self.count3 / 2 + 1, r))
                    con.commit()
                else:
                    cur.execute("""INSERT INTO res (name, count, id_level) VALUES (?, ?, ?)""",
                                (name, self.count3 / 2 + 1, 1))
                    con.commit()
                self.close()
                self.ex.show()

    def closeAllCards(self):
        if self.i[0].pixmap().toImage() == self.i[1].pixmap().toImage():
            self.counter += 1
        else:
            for button in self.buttons:
                button.setVisible(True)
        self.count3 += 2


class SecondLevel(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('SecondLevel.ui', self)
        self.ex = ex
        self.label_list2 = [self.label_3, self.label_4, self.label_7, self.label_6, self.label_8, self.label_9,
                            self.label_10, self.label_5]

        self.button_list2 = [self.pushButton, self.pushButton_2, self.pushButton_3, self.pushButton_4,
                             self.pushButton_5,
                             self.pushButton_6, self.pushButton_7, self.pushButton_8]
        self.counter2 = 0
        self.counter = 0
        self.opened_cards = 0
        self.max_opened_cards = 2
        self.right_image = []
        self.buttons = []
        self.i = []
        self.count3 = 0
        for btn in self.button_list2:
            btn.clicked.connect(self.open)

    def open(self):
        sender = self.sender()
        if len(self.i) == 0:
            sender.setVisible(False)
            self.buttons.append(sender)
            self.opened_cards += 1
            self.i.append(self.label_list2[self.button_list2.index(sender)])
        # elif self.opened_cards == 1:
        elif len(self.i) == 1:
            sender.setVisible(False)
            self.buttons.append(sender)
            self.opened_cards += 1
            self.i.append(self.label_list2[self.button_list2.index(sender)])
        # elif self.opened_cards == 2:
        elif len(self.i) == 2:
            sender.setVisible(False)
            self.opened_cards = 0
            self.closeAllCards()
            self.i = []
            self.buttons = []
            self.buttons.append(sender)
            self.i.append(self.label_list2[self.button_list2.index(sender)])
        if all(not b.isVisible() for b in self.button_list2):
            name, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                                    "Введи имя чтобы сохранить резулььтат:")
            if ok_pressed:
                con = sqlite3.connect("results.sqlite")
                cur = con.cursor()
                r = cur.execute("SELECT id FROM res WHERE name = ? AND id_level = 2", (name,)).fetchall()
                print(r)
                if r:
                    cur.execute(""" UPDATE res SET count = ? WHERE id = ?""", (self.count3 / 2 + 1, r))
                    con.commit()
                else:
                    cur.execute(""" INSERT INTO res (name, count, id_level) VALUES (?, ?, ?)""",
                                (name, self.count3 / 2 + 1, 2))
                    con.commit()
                self.close()
                self.ex.show()

    def closeAllCards(self):
        if self.i[0].pixmap().toImage() == self.i[1].pixmap().toImage():
            self.counter += 1
        else:
            for button in self.buttons:
                button.setVisible(True)
        self.count3 += 2


class ThirdLevel(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ThirdLevel.ui', self)
        self.ex = ex
        self.label_list2 = [self.label_2, self.label_13, self.label_12, self.label_11, self.label_7, self.label_8,
                            self.label_9, self.label_10, self.label_3, self.label_4, self.label_5, self.label_6, ]
        self.button_list2 = [self.pushButton, self.pushButton_12, self.pushButton_11, self.pushButton_10,
                             self.pushButton_9,
                             self.pushButton_8, self.pushButton_7, self.pushButton_6, self.pushButton_5,
                             self.pushButton_4,
                             self.pushButton_3, self.pushButton_2]
        self.counter = 0
        self.opened_cards = 0
        self.max_opened_cards = 2
        self.right_image = []
        self.buttons = []
        self.i = []
        self.count3 = 0

        for btn in self.button_list2:
            btn.clicked.connect(self.open)

    def open(self):
        sender = self.sender()
        # if self.opened_cards == 0:
        if len(self.i) == 0:
            sender.setVisible(False)
            self.buttons.append(sender)
            self.opened_cards += 1
            self.i.append(self.label_list2[self.button_list2.index(sender)])
        # elif self.opened_cards == 1:
        elif len(self.i) == 1:
            sender.setVisible(False)
            self.buttons.append(sender)
            self.opened_cards += 1
            self.i.append(self.label_list2[self.button_list2.index(sender)])

        # elif self.opened_cards == 2:
        elif len(self.i) == 2:
            sender.setVisible(False)
            self.opened_cards = 0
            self.closeAllCards()
            self.i = []
            self.buttons = []
            self.buttons.append(sender)
            self.i.append(self.label_list2[self.button_list2.index(sender)])

        if all(not b.isVisible() for b in self.button_list2):
            name, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                                    "Введи имя чтобы сохранить результат:")
            if ok_pressed:
                con = sqlite3.connect("results.sqlite")
                cur = con.cursor()
                r = cur.execute("SELECT id FROM res WHERE name = ? AND id_level = 3", (name,)).fetchall()
                print(r)
                if r:
                    cur.execute(""" UPDATE res SET count = ? WHERE id = ?""", (self.count3 / 2 + 1, r))
                    con.commit()
                else:
                    cur.execute(""" INSERT INTO res (name, count, id_level) VALUES (?, ?, ?)""",
                                (name, self.count3 / 2 + 1, 3))
                    con.commit()
                self.close()
                self.ex.show()

    def closeAllCards(self):
        if self.i[0].pixmap().toImage() == self.i[1].pixmap().toImage():
            self.counter += 1

        else:
            for button in self.buttons:
                button.setVisible(True)
        self.count3 += 2


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MainWindow.ui', self)

        self.SpravkaButton.clicked.connect(self.openSpravka)
        self.LevelButton.clicked.connect(self.openLevel)
        self.HistoryButton.clicked.connect(self.openHistory)

    def openSpravka(self):
        spravka_dialog = Spravka()
        spravka_dialog.exec_()

    def openLevel(self):
        self.close()
        self.level_window = LevelWindow()
        self.level_window.show()

    def openHistory(self):
        self.history_window = HistoryWindow()

        self.history_window.show()


class HistoryWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Hystory.ui', self)
        font = 20
        self.text_edit.setReadOnly(True)
        self.setCentralWidget(self.text_edit)
        style_sheet = f"font-size: {font}px;"
        self.text_edit.setStyleSheet(style_sheet)
        connection = sqlite3.connect('results.sqlite')
        cursor = connection.cursor()

        # Выполняем SQL-запрос для выборки данных из таблицы res
        cursor.execute('SELECT * FROM res')
        data = cursor.fetchall()

        # Закрываем соединение с базой данных
        connection.close()

        # Очищаем текстовое поле
        self.text_edit.clear()
        self.text_edit.appendPlainText('\n                         id            name     count    level')
        # Выводим данные в текстовое поле
        for row in data:
            row_str = '\t'.join(map(str, row))
            self.text_edit.appendPlainText('                         ' + row_str)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())