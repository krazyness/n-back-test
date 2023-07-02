#!/usr/bin/env python
import random
import time
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memory Test")
        self.resize(700, 500)

        self.countdown_time = 4
        self.rounds = 4

        self.clicked = False
        self.letterAppeared = False
        self.verify = False
        self.practiceRunCheck = True

        self.correct = 0
        self.incorrect = 0
        self.missed = 0
        self.trialsWithMatch = 0
        self.trialsWithNoMatch = 0

        self.universalLetter = "nothing"
        self.first_letter = "nothing"
        self.second_letter = "nothing"

        self.beginInfo = QPushButton("Click to start", self)
        self.beginInfo.setGeometry(200, 100, 300, 300)
        self.beginInfoFont = QFont()
        self.beginInfoFont.setPointSize(14)
        self.beginInfo.setFont(self.beginInfoFont)
        self.beginInfo.clicked.connect(self.info_click)

        self.center_button = QPushButton("Loading...", self)
        self.center_button.setGeometry(300, 200, 100, 100)
        self.center_buttonFont = QFont()
        self.center_buttonFont.setPointSize(15)
        self.center_button.setFont(self.center_buttonFont)
        self.center_button.clicked.connect(self.on_click)
        self.center_button.setVisible(False)

        self.practice_help1 = QPushButton("1", self)
        self.practice_help1.setGeometry(175, 200, 100, 100)
        self.practice_help1.setFont(self.center_buttonFont)
        self.practice_help1.setVisible(False)
        self.practice_help1.setEnabled(False)

        self.practice_help2 = QPushButton("2", self)
        self.practice_help2.setGeometry(50, 200, 100, 100)
        self.practice_help2.setFont(self.center_buttonFont)
        self.practice_help2.setVisible(False)
        self.practice_help2.setEnabled(False)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

    def info_click(self):
        print("info1 appeared")
        self.beginInfo.setVisible(False)

        self.infoTitle = QLabel("N-back working memory task", self)
        self.infoTitle.setGeometry(100, 50, 500, 50)
        self.infoTitleFont = QFont("Arial", 20)
        self.infoTitleFont.setBold(True)
        self.infoTitle.setFont(self.infoTitleFont)
        self.infoTitle.setVisible(True)

        self.info = QLabel("In this task, you will see a sequence of letters.\nEach letter is shown for a few seconds. You need\nto decide if you saw the same letter 2 trials ago,\nthat is, this is a n=2-back task.", self)
        self.info.setGeometry(100, -90, 500, 500)
        self.infoFont = QFont("Arial", 15)
        self.info.setFont(self.infoFont)
        self.info.setVisible(True)

        self.info2 = QLabel("If you saw the same letter 2 trials ago, you click\nit with the mouse.", self)
        self.info2.setGeometry(100, 10, 500, 500)
        self.info2Font = QFont("Arial", 15)
        self.info2.setFont(self.info2Font)
        self.info2.setVisible(True)

        self.nextButton = QPushButton("Click here for the next info screen", self)
        self.nextButton.setGeometry(100, 325, 200, 50)
        self.nextButtonFont1 = QFont()
        self.nextButtonFont1.setPointSize(10)
        self.nextButton.setFont(self.nextButtonFont1)
        self.nextButton.setVisible(True)

        self.nextButton.clicked.connect(self.info2_click)
    
    def info2_click(self):
        print("Info2 appeared")
        self.info2.setVisible(False)

        self.info.setText("To help you learn this task, at first there is a very easy\nversion. You will be reminded of the letters you saw the\ntrials before. They come left from the letter in the middle\nof the screen. They are only there to help. Later on, they\nwill not be shown anymore, and you will need to do it all\nbased on your memory.")
        self.info.setGeometry(100, -75, 500, 500)

        self.nextButton.setGeometry(100, 260, 225, 50)
        self.nextButton.setText("Click here to begin your practice run!")
        self.nextButton.clicked.connect(self.on_click)
    
    def info3_click(self):
        print("Info3 appeared")
        self.trialsWithMatch = 0
        self.trialsWithNoMatch = 0
        self.correct = 0
        self.missed = 0
        self.incorrect = 0

        self.infoTitle.setVisible(True)
        self.resultButton.setVisible(False)
        self.nextButton.setVisible(True)

        self.info.setGeometry(100, -75, 500, 500)
        self.info.setText("Now that you have learned the n-back task, you need to\ndo it purely based on your memory. Thus, click the letter\nif it is the same as 2 letters ago.")

        self.info2.setVisible(True)
        self.info2.setText("Otherwise, do nothing.\n\nConcentrate, because this is not easy.")

        self.nextButton.setText("Click here to begin the actual test")
        self.nextButton.setGeometry(100, 310, 225, 50)
        self.nextButton.clicked.connect(self.on_click)

    def on_click(self):
        print("clicked")
        if self.countdown_time > 1:  # Initial Click
            self.center_button.setEnabled(False)
            self.center_button.setVisible(True)

            self.nextButton.setVisible(False)
            self.info.setVisible(False)
            self.infoTitle.setVisible(False)
            self.info2.setVisible(False)

            self.correct = 0
            self.incorrect = 0
            self.missed = 0

            self.timer.start(1000)
        else:
            self.clicked = True

    def update(self):
        if self.countdown_time <= 1:  # Update when countdown finished/finishes
            self.center_button.setEnabled(True)
            self.timer.stop()
            if self.rounds >= 1:
                if not self.letterAppeared:  # Make Letter Appear
                    self.letterAppeared = True

                    self.provide_random_letter()
                    self.timer.start(750)
                else:  # Make Letter Not Appear And Check
                    self.rounds -= 1
                    self.check()

                    if self.clicked and self.verify:
                        self.correct += 1
                    elif not self.clicked and self.verify:
                        self.missed += 1
                    elif self.clicked and not self.verify:
                        self.incorrect += 1

                    self.second_letter = self.first_letter
                    self.first_letter = self.universalLetter

                    self.letterAppeared = False
                    self.clicked = False

                    self.center_button.setVisible(False)
                    self.practice_help1.setVisible(False)
                    self.practice_help2.setVisible(False)

                    self.timer.start(2000)
            else:
                self.letterAppeared = False
                self.results()
        else:  # Update countdown
            self.countdown_time -= 1
            self.center_button.setText("{}".format(self.countdown_time))

    def provide_random_letter(self):
        letter = chr(random.randint(65, 65 + 7))
        self.universalLetter = letter
        self.center_button.setText(letter)

        if self.practiceRunCheck:
            self.practiceRunFunc()

        self.center_button.setVisible(True)
    
    def practiceRunFunc(self):
        if self.first_letter != "nothing":
            self.practice_help1.setText("{}".format(self.first_letter))
            self.practice_help1.setVisible(True)
        if self.second_letter != "nothing":
            self.practice_help2.setText("{}".format(self.second_letter))
            self.practice_help2.setVisible(True)

    def check(self):
        if self.universalLetter == self.second_letter:
            self.verify = True
            self.trialsWithMatch += 1
        else:
            self.verify = False
            self.trialsWithNoMatch += 1

    def results(self):
        self.center_button.setVisible(False)

        self.rounds = 4
        self.countdown_time = 4

        self.universalLetter = "nothing"
        self.first_letter = "nothing"
        self.second_letter = "nothing"
        self.center_button.setText("Loading...")
        
        self.info.setText("There were 25 trials total in this block.\n\nTotal trials that had a match: {}\n\nTotal trials that had no match: {}\n\nNumber of correctly matched items: {}\n\nNumber of missed items: {}\n\nNumber of false alarms: {}".format(self.trialsWithMatch, self.trialsWithNoMatch, self.correct, self.missed, self.incorrect))
        self.info.setVisible(True)

        self.resultButton = QPushButton("Click here to continue", self)
        self.resultButton.setGeometry(100, 325, 200, 50)
        self.resultButtonFont = QFont()
        self.resultButtonFont.setPointSize(10)
        self.resultButton.setFont(self.resultButtonFont)
        self.resultButton.setVisible(True)
        self.resultButton.clicked.connect(self.info3_click)

        self.practiceRunCheck = False


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
