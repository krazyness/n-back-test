#!/usr/bin/env python
import random
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

TRIALS = 25
COUNTDOWN = 3

LETTER_APPEAR_DURATION_SECONDS = 0.75
PAUSE_DURATION_SECONDS = 2
REPEAT_PROBABILITY = 0.4  # Probability of match


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memory Test")
        self.resize(700, 500)

        self.is_clicked = False
        self.is_letter_appeared = False
        self.is_practice = True

        self.correct_cnt = 0
        self.incorrect_cnt = 0
        self.missed_cnt = 0
        self.trials_with_match_cnt = 0
        self.trials_with_no_match_cnt = 0

        self.universal_letter = None
        self.first_letter = None
        self.second_letter = None

        self.correct_sound_output = QAudioOutput()
        self.correct_sound_output.setVolume(50)

        self.incorrect_sound_output = QAudioOutput()
        self.incorrect_sound_output.setVolume(50)

        self.correct_sound = QMediaPlayer()
        self.correct_sound.setAudioOutput(self.correct_sound_output)
        self.correct_sound.setSource(QUrl.fromLocalFile("RightChoice.wav"))

        self.incorrect_sound = QMediaPlayer()
        self.incorrect_sound.setAudioOutput(self.incorrect_sound_output)
        self.incorrect_sound.setSource(QUrl.fromLocalFile("WrongChoice.wav"))

        self.beginInfo = QPushButton("Click this button to start", self)
        self.beginInfo.setGeometry(200, 100, 300, 300)
        self.beginInfo.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.beginInfoFont = QFont()
        self.beginInfoFont.setPointSize(16)
        self.beginInfo.setFont(self.beginInfoFont)
        self.beginInfo.clicked.connect(self.info_click)

        self.center_button = QPushButton("Loading...", self)
        self.center_button.setGeometry(300, 200, 100, 100)
        self.center_button.setStyleSheet('background-color:'
                                         ' rgb(82, 200, 255);')
        self.center_buttonFont = QFont()
        self.center_buttonFont.setPointSize(15)
        self.center_button.setFont(self.center_buttonFont)
        self.center_button.clicked.connect(self.on_click)
        self.center_button.setVisible(False)

        self.practice_help1 = QPushButton("", self)
        self.practice_help1.setGeometry(175, 200, 100, 100)
        self.practice_help1.setFont(self.center_buttonFont)
        self.practice_help1.setVisible(False)
        self.practice_help1.setEnabled(False)

        self.practice_help2 = QPushButton("", self)
        self.practice_help2.setGeometry(50, 200, 100, 100)
        self.practice_help2.setFont(self.center_buttonFont)
        self.practice_help2.setVisible(False)
        self.practice_help2.setEnabled(False)

        self.rounds_cnt = 0
        self.countdown_cnt = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

    def info_click(self):
        self.beginInfo.setVisible(False)

        self.infoTitle = QLabel("N-back working memory task", self)
        self.infoTitle.setGeometry(100, 50, 500, 50)
        self.infoTitleFont = QFont("Arial", 20)
        self.infoTitleFont.setBold(True)
        self.infoTitle.setFont(self.infoTitleFont)
        self.infoTitle.setVisible(True)

        self.info = QLabel('In this task, you will see a sequence '
                           'of letters.\nEach letter is shown for a '
                           'few seconds. You need\nto decide '
                           'if you saw the same letter '
                           '2 trials ago,\nthat is, '
                           'this is a n=2-back task.', self)
        self.info.setGeometry(100, -90, 500, 500)
        self.infoFont = QFont("Arial", 15)
        self.info.setFont(self.infoFont)
        self.info.setVisible(True)

        self.info2 = QLabel('If you saw the same letter 2 trials ago, '
                            'you click\nit with the mouse.'
                            '\n\nIf correct, you will hear this sound:'
                            '\n\nIf incorrect, you '
                            'will hear this sound:', self)
        self.info2.setGeometry(100, 40, 500, 500)
        self.info2Font = QFont("Arial", 15)
        self.info2.setFont(self.info2Font)
        self.info2.setVisible(True)

        self.play_correct_button = QPushButton('Click here to play'
                                               ' CORRECT sound', self)
        self.play_correct_button.setGeometry(410, 275, 250, 45)
        self.play_correct_button.setStyleSheet('background-color:'
                                               ' rgb(0, 255, 0);')
        self.play_correct_button.setVisible(True)
        self.play_correct_button.clicked.connect(self.correct_sound.play)

        self.play_incorrect_button = QPushButton('Click here to play'
                                                 ' INCORRECT sound', self)
        self.play_incorrect_button.setGeometry(425, 330, 250, 45)
        self.play_incorrect_button.setStyleSheet('background-color: '
                                                 'rgb(252, 61, 61);')
        self.play_incorrect_button.setVisible(True)
        self.play_incorrect_button.clicked.connect(self.incorrect_sound.play)

        self.nextButton = QPushButton('Click here for the '
                                      'next info screen', self)
        self.nextButton.setGeometry(100, 390, 250, 50)
        self.nextButton.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.nextButtonFont1 = QFont()
        self.nextButtonFont1.setPointSize(10)
        self.nextButton.setFont(self.nextButtonFont1)
        self.nextButton.setVisible(True)

        self.nextButton.clicked.connect(self.info2_click)

    def info2_click(self):
        self.play_correct_button.setVisible(False)
        self.play_incorrect_button.setVisible(False)

        self.info.setText('To help you learn this task, '
                          'at first there is a very easy\nversion. '
                          'You will be reminded of the letters '
                          'you saw the\ntrials before. They come left '
                          'from the letter in the middle\nof the screen. '
                          'They are only there to help. '
                          'Later on, they\nwill not be shown anymore, '
                          'and you will need to do it all '
                          '\nbased on your memory.')
        self.info.setGeometry(100, -75, 500, 500)

        self.info2.setText('Tip: Keep your cursor at '
                           'the center button\nso that '
                           'you won\'t miss a click.')

        self.nextButton.setGeometry(100, 350, 250, 50)
        self.nextButton.setText("Click here to begin your practice run!")
        self.nextButton.clicked.connect(self.on_click)

    def info3_click(self):
        self.trials_with_match_cnt = 0
        self.trials_with_no_match_cnt = 0
        self.correct_cnt = 0
        self.missed_cnt = 0
        self.incorrect_cnt = 0

        self.countdown_cnt = 0
        self.rounds_cnt = 0

        self.infoTitle.setVisible(True)
        self.resultButton.setVisible(False)
        self.nextButton.setVisible(True)

        self.info.setGeometry(100, -95, 500, 500)
        self.info.setText('Now that you have learned '
                          'the n-back task, you need to '
                          '\ndo it purely based on your memory. '
                          'Thus, click the letter\nif it '
                          'is the same as 2 letters ago.')

        self.info2.setVisible(True)
        self.info2.setGeometry(100, -10, 500, 500)
        self.info2.setText('Otherwise, do nothing.'
                           '\n\nConcentrate, because this is not easy.')

        self.nextButton.setText("Click here to begin the actual test")
        self.nextButton.setGeometry(100, 310, 225, 50)
        self.nextButton.clicked.connect(self.on_click)

    def on_click(self):
        if self.countdown_cnt < COUNTDOWN:  # Initial Click
            self.center_button.setEnabled(False)
            self.center_button.setVisible(True)

            self.nextButton.setVisible(False)
            self.info.setVisible(False)
            self.infoTitle.setVisible(False)
            self.info2.setVisible(False)

            self.correct_cnt = 0
            self.incorrect_cnt = 0
            self.missed_cnt = 0

            self.timer.start(1000)
        else:
            self.is_clicked = True

    def update(self):
        if (
            self.countdown_cnt >= COUNTDOWN
        ):  # Update when countdown finished/finishes
            self.center_button.setEnabled(True)
            self.timer.stop()
            if self.rounds_cnt < TRIALS:
                if not self.is_letter_appeared:  # Make Letter Appear
                    self.is_letter_appeared = True

                    self.provide_random_letter()
                    self.timer.start(LETTER_APPEAR_DURATION_SECONDS * 1000)
                else:  # Make Letter Not Appear And Check
                    self.rounds_cnt += 1
                    self.center_button.setVisible(False)

                    if self.check():
                        if self.is_clicked:
                            self.correct_cnt += 1
                            self.correct_sound.play()
                        elif not self.is_clicked:
                            self.incorrect_cnt += 1
                            self.incorrect_sound.play()
                    else:
                        if self.is_clicked:
                            self.incorrect_cnt += 1
                            self.incorrect_sound.play()
                        elif not self.is_clicked:
                            pass

                    self.second_letter = self.first_letter
                    self.first_letter = self.universal_letter

                    self.is_letter_appeared = False
                    self.is_clicked = False
                    self.practice_help1.setVisible(False)
                    self.practice_help2.setVisible(False)

                    self.timer.start(PAUSE_DURATION_SECONDS * 1000)
            else:
                self.is_letter_appeared = False
                self.results()
        else:  # Update countdown
            self.center_button.setText(f"{COUNTDOWN-self.countdown_cnt}")
            self.countdown_cnt += 1

    def provide_random_letter(self):
        letter = chr(random.randint(65, 65 + 7))
        if (
            self.first_letter == self.second_letter and
            self.first_letter is not None
        ):
            while True:
                if letter == self.first_letter:
                    letter = chr(random.randint(65, 65 + 7))
                else:
                    self.universal_letter = letter
                    self.center_button.setText(letter)
                    break
        elif self.second_letter is not None:
            if random.random() <= REPEAT_PROBABILITY:
                self.universal_letter = self.second_letter
                self.center_button.setText(self.second_letter)
            else:
                self.universal_letter = letter
                self.center_button.setText(letter)
        else:
            self.universal_letter = letter
            self.center_button.setText(letter)

        if self.is_practice:
            if self.first_letter is not None:
                self.practice_help1.setText(f"{self.first_letter}")
                self.practice_help1.setVisible(True)
            if self.second_letter is not None:
                self.practice_help2.setText(f"{self.second_letter}")
                self.practice_help2.setVisible(True)

        self.center_button.setVisible(True)

    def check(self):
        if self.universal_letter == self.second_letter:
            self.trials_with_match_cnt += 1
            return True
        else:
            self.trials_with_no_match_cnt += 1
            return False

    def results(self):
        self.center_button.setVisible(False)

        self.rounds_cnt = 0

        self.universal_letter = None
        self.first_letter = None
        self.second_letter = None
        self.center_button.setText("Loading...")

        self.info.setText(f'There were {TRIALS} trials total in this block.'
                          '\n\nTotal trials that had a '
                          f'match: {self.trials_with_match_cnt}'
                          '\n\nTotal trials that had no '
                          f'match: {self.trials_with_no_match_cnt}'
                          '\n\nNumber of correctly matched '
                          f'items: {self.correct_cnt}'
                          f'\n\nNumber of missed items: {self.missed_cnt}'
                          f'\n\nNumber of false alarms: {self.incorrect_cnt}')
        self.info.setVisible(True)

        self.resultButton = QPushButton("Click here to continue", self)
        self.resultButton.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.resultButton.setGeometry(100, 325, 200, 50)
        self.resultButtonFont = QFont()
        self.resultButtonFont.setPointSize(10)
        self.resultButton.setFont(self.resultButtonFont)
        self.resultButton.setVisible(True)
        self.resultButton.clicked.connect(self.info3_click)

        self.is_practice = False


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
