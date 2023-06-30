#!/usr/bin/env python
import random
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PySide6.QtCore import QTimer


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memory Test")

        self.countdown_time = 4
        self.rounds = 4

        self.clicked = False
        self.letterAppeared = False
        self.verify = False

        self.correct = 0
        self.incorrect = 0
        self.missed = 0

        self.universalLetter = "nothing"
        self.first_letter = "nothing"
        self.second_letter = "nothing"

        self.center_button = QPushButton("START", self)
        self.center_button.setGeometry(50, 50, 200, 200)
        self.center_button.clicked.connect(self.on_click)

        self.correct_label = QLabel("Correct: 0", self)
        self.correct_label.setGeometry(50, 250, 200, 50)

        self.incorrect_label = QLabel("Incorrect: 0", self)
        self.incorrect_label.setGeometry(50, 275, 200, 50)

        self.missed_label = QLabel("Missed: 0", self)
        self.missed_label.setGeometry(50, 300, 200, 50)

        self.correct_label.setVisible(False)
        self.incorrect_label.setVisible(False)
        self.missed_label.setVisible(False)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

    def on_click(self):
        if self.countdown_time > 1:  # Initial Click
            print("letter didn't appear, start timer")

            self.center_button.setEnabled(False)
            self.correct_label.setVisible(False)
            self.incorrect_label.setVisible(False)
            self.missed_label.setVisible(False)

            self.correct = 0
            self.incorrect = 0
            self.missed = 0

            self.timer.start(1000)
        else:
            print("letter appeared")
            self.clicked = True

    def update(self):
        if self.countdown_time <= 1:  # Update when countdown finished/finishes
            self.center_button.setEnabled(True)
            self.timer.stop()
            if self.rounds >= 1:
                if not self.letterAppeared:  # Make Letter Appear
                    self.letterAppeared = True

                    self.provide_random_letter()
                    self.timer.start(2000)
                else:  # Make Letter Not Appear And Check
                    self.rounds -= 1
                    self.check()

                    print(self.verify)
                    if self.clicked and self.verify:
                        self.correct += 1
                        print("Correct!")
                    elif not self.clicked and self.verify:
                        self.missed += 1
                        print("MISSED!")
                    elif self.clicked and not self.verify:
                        self.incorrect += 1
                        print("Incorrect!")
                    else:
                        self.correct += 1
                        print("Correct!")

                    self.second_letter = self.first_letter
                    self.first_letter = self.universalLetter

                    self.letterAppeared = False
                    self.clicked = False

                    self.center_button.setText("")
                    self.timer.start(1000)
            else:
                self.letterAppeared = False
                self.results()
        else:  # Update countdown
            print("more than 0")
            self.countdown_time -= 1
            self.center_button.setText("{}".format(self.countdown_time))

    def provide_random_letter(self):
        letter = chr(random.randint(65, 65 + 7))
        self.universalLetter = letter
        self.center_button.setText(letter)

    def check(self):
        if (
            self.universalLetter == self.first_letter or
            self.universalLetter == self.second_letter
        ):
            self.verify = True
        else:
            self.verify = False

    def results(self):
        self.correct_label.setVisible(True)
        self.incorrect_label.setVisible(True)
        self.missed_label.setVisible(True)

        self.rounds = 10
        self.countdown_time = 4

        self.correct_label.setText("Correct: {}".format(self.correct))
        self.incorrect_label.setText("Incorrect: {}".format(self.incorrect))
        self.missed_label.setText("Missed: {}".format(self.missed))

        self.universalLetter = "nothing"
        self.first_letter = "nothing"
        self.second_letter = "nothing"

        self.center_button.setText("FINISHED, TRY AGAIN?")


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
