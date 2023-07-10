#!/usr/bin/env python
import random
import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

TRIALS = 25
MINIMUM_MATCHES = 7
COUNTDOWN = 3

LETTER_APPEAR_DURATION_SECONDS = 0.75
PAUSE_DURATION_SECONDS = 2


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memory Test")
        self.resize(700, 500)

        self.is_clicked = False
        self.is_letter_appeared = False
        self.is_practice = True
        self.n_back = 2

        self.debounce = False

        self.correct_cnt = 0
        self.incorrect_cnt = 0
        self.missed_cnt = 0
        self.trials_with_match_cnt = 0
        self.trials_with_no_match_cnt = 0

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

        self.directory_button = QPushButton('Choose a file to\nsave '
                                            'your results in', self)
        self.directory_button.setGeometry(250, 150, 200, 200)
        self.directory_button.setStyleSheet('background-color: '
                                            'rgb(0, 255, 0);')
        directory_buttonFont = QFont()
        directory_buttonFont.setPointSize(15)
        self.directory_button.setFont(directory_buttonFont)
        self.directory_button.setVisible(True)
        self.directory_button.clicked.connect(self.get_directory)

        self.center_button = QPushButton("Loading...", self)
        self.center_button.setGeometry(300, 200, 100, 100)
        self.center_button.setStyleSheet('background-color:'
                                         ' rgb(82, 200, 255);')
        center_buttonFont = QFont()
        center_buttonFont.setPointSize(15)
        self.center_button.setFont(center_buttonFont)
        self.center_button.setVisible(False)
        self.center_button.clicked.connect(self.on_click)

        self.practice_help1 = QPushButton("", self)
        self.practice_help1.setGeometry(175, 200, 100, 100)
        self.practice_help1.setFont(center_buttonFont)
        self.practice_help1.setVisible(False)
        self.practice_help1.setEnabled(False)

        self.practice_help2 = QPushButton("", self)
        self.practice_help2.setGeometry(50, 200, 100, 100)
        self.practice_help2.setFont(center_buttonFont)
        self.practice_help2.setVisible(False)
        self.practice_help2.setEnabled(False)

        self.rounds_cnt = 0
        self.countdown_cnt = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

    def get_directory(self):
        file_dialog = QFileDialog(self)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix("txt")

        self.file_path = None

        if file_dialog.exec() == QFileDialog.Accepted:
            self.file_path = file_dialog.selectedFiles()[0]

            try:
                with open(self.file_path, "w") as file:
                    file.write("")
            except IOError:
                print("An error occurred while creating/saving the file.")

        if self.file_path is not None:
            self.directory_button.setVisible(False)
            self.info_click()
        else:
            sys.exit()

    def info_click(self):
        self.infoTitle = QLabel("N-back working memory task", self)
        self.infoTitle.setGeometry(100, 50, 500, 50)
        infoTitleFont = QFont("Arial", 20)
        infoTitleFont.setBold(True)
        self.infoTitle.setFont(infoTitleFont)
        self.infoTitle.setVisible(True)

        self.info = QLabel('In this task, you will see a sequence '
                           'of letters.\nEach letter is shown for a '
                           'few seconds. You need\nto decide '
                           'if you saw the same letter '
                           '2 trials ago,\nthat is, '
                           'this is a n=2-back task.', self)
        self.info.setGeometry(100, -90, 500, 500)
        infoFont = QFont("Arial", 15)
        self.info.setFont(infoFont)
        self.info.setVisible(True)

        self.info2 = QLabel('If you saw the same letter 2 trials ago, '
                            'you click\nthe window with the mouse.'
                            '\n\nIf correct, you will hear this sound:'
                            '\n\nIf incorrect, you '
                            'will hear this sound:', self)
        self.info2.setGeometry(100, 40, 500, 500)
        info2Font = QFont("Arial", 15)
        self.info2.setFont(info2Font)
        self.info2.setVisible(True)

        self.play_correct_button = QPushButton('PLAY', self)
        self.play_correct_button.setGeometry(425, 275, 250, 45)
        self.play_correct_button.setStyleSheet('background-color:'
                                               ' rgb(0, 255, 0);')
        self.play_correct_button.setVisible(True)
        self.play_correct_button.clicked.connect(self.correct_sound.play)

        self.play_incorrect_button = QPushButton('PLAY', self)
        self.play_incorrect_button.setGeometry(425, 330, 250, 45)
        self.play_incorrect_button.setStyleSheet('background-color: '
                                                 'rgb(0, 255, 0);')
        self.play_incorrect_button.setVisible(True)
        self.play_incorrect_button.clicked.connect(self.incorrect_sound.play)

        self.nextButton = QPushButton('Click here for the '
                                      'next info screen', self)
        self.nextButton.setGeometry(100, 390, 250, 50)
        self.nextButton.setStyleSheet("background-color: rgb(0, 255, 0);")
        nextButtonFont1 = QFont()
        nextButtonFont1.setPointSize(10)
        self.nextButton.setFont(nextButtonFont1)
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

        self.info2.setText('Tip: You can click outside of the box\n'
                           'so your cursor doesn\'t block the letter')

        self.nextButton.setGeometry(100, 350, 250, 50)
        self.nextButton.setText("Click here to begin your practice run!")
        self.nextButton.clicked.connect(self.on_click)

    def info3_click(self):
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

        self.nextButton.setText("Click here to begin the 2-back test")
        self.nextButton.setGeometry(100, 310, 225, 50)
        self.nextButton.clicked.connect(self.on_click)

    def info4(self):
        self.info.setVisible(True)
        self.info.setGeometry(100, -75, 500, 500)
        self.info.setText('Congratulations on completing'
                          ' the 2-back test! '
                          'Now,\nit\'s time to challenge'
                          ' yourself further with the 3-back test.'
                          '\nIn this task, you will be presented '
                          'with a sequence of\nletters, similar '
                          'to the previous test. This time, '
                          'you need\nto determine if the '
                          'current letter matches the one'
                          '\npresented 3 trials ago.')

        self.info2.setVisible(True)
        self.info2.setGeometry(100, 20, 500, 500)
        self.info2.setText('Concentrate, and try '
                           'your best because this is '
                           'not easy.')

        self.nextButton.setText("Click here to begin the 3-back test")
        self.nextButton.setGeometry(100, 310, 225, 50)
        self.nextButton.clicked.connect(self.on_click)

    def finish_screen(self):
        self.infoTitle.setText("You Finished!")
        self.info.setText('Congratulations! You successfully completed '
                          'the 2-back\nand 3-back test! '
                          'You may now close the test window.')
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            if self.is_letter_appeared and not self.is_clicked:
                self.clicked_during_testing()
    
    def clicked_during_testing(self):
        self.is_clicked = True
        if self.check():
            self.correct_sound.play()
            self.correct_cnt += 1
        else:
            self.incorrect_sound.play()
            self.incorrect_cnt += 1

    def on_click(self):
        if not self.debounce:
            self.debounce = True
            if self.countdown_cnt < COUNTDOWN:
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

                self.get_random_letters(TRIALS, MINIMUM_MATCHES, self.n_back)
            else:
                self.clicked_during_testing()

    def update(self):
        if self.countdown_cnt >= COUNTDOWN:
            self.timer.stop()
            if self.rounds_cnt < TRIALS:
                if not self.is_letter_appeared:  # Make Letter Appear
                    self.is_letter_appeared = True
                    self.center_button.setVisible(True)
                    self.center_button.setEnabled(True)
                    self.debounce = False

                    self.center_button.setText(f"{self.random_letters_list[self.rounds_cnt]}")  

                    if self.is_practice:
                        if self.rounds_cnt > 0:
                            self.practice_help1.setText(f"{self.random_letters_list[self.rounds_cnt-1]}")
                            self.practice_help1.setVisible(True)
                        if self.rounds_cnt > 1:
                            self.practice_help2.setText(f"{self.random_letters_list[self.rounds_cnt-2]}")
                            self.practice_help2.setVisible(True)

                    self.timer.start(LETTER_APPEAR_DURATION_SECONDS * 1000)
                else:  # Make Letter Not Appear And Check
                    self.is_letter_appeared = False
                    self.center_button.setVisible(False)
                    
                    if not self.is_clicked:
                        if self.check():
                            self.missed_cnt += 1
                            self.incorrect_sound.play()

                    self.is_clicked = False
                    self.practice_help1.setVisible(False)
                    self.practice_help2.setVisible(False)

                    self.rounds_cnt += 1

                    self.timer.start(PAUSE_DURATION_SECONDS * 1000)
            else:
                self.is_letter_appeared = False
                self.results()
        else:  # Update countdown
            self.center_button.setText(f"{COUNTDOWN-self.countdown_cnt}")
            self.countdown_cnt += 1

    def get_random_letters(self, trials, matches, n_back):
        locations = random.sample(list(range(trials-n_back)), matches)
        locations = set(locations)
        # constant alphabet A-Z
        a2z = list(map(chr, range(65, 91)))
        # generate n_back letters
        letters = random.choices(a2z, k=n_back)
        # generate the rest letters
        for i in range(trials-n_back):
            if i in locations:
                letters.append(letters[i])
            else:
                letters.append(random.choice(a2z))
        self.random_letters_list = letters

    def check(self):
        if self.n_back == 3:
            if self.random_letters_list[self.rounds_cnt] == self.random_letters_list[self.rounds_cnt - 3]:
                self.trials_with_match_cnt += 1
                return True
            else:
                self.trials_with_no_match_cnt += 1
                return False
        elif self.n_back == 2:
            if self.random_letters_list[self.rounds_cnt] == self.random_letters_list[self.rounds_cnt - 2]:
                self.trials_with_match_cnt += 1
                return True
            else:
                self.trials_with_no_match_cnt += 1
                return False

    def results(self):
        self.center_button.setVisible(False)
        self.rounds_cnt = 0
        self.center_button.setText("Loading...")
        self.debounce = False

        if self.is_practice:
            self.info.setText(f'There were {TRIALS} '
                              'trials total in this block.'
                              '\n\nTotal trials that had a '
                              f'match: {self.trials_with_match_cnt}'
                              '\n\nTotal trials that had no '
                              f'match: {self.trials_with_no_match_cnt}'
                              '\n\nNumber of correctly matched '
                              f'items: {self.correct_cnt}'
                              f'\n\nNumber of missed items: {self.missed_cnt}'
                              '\n\nNumber of false alarms: '
                              f'{self.incorrect_cnt}')
            self.info.setVisible(True)

            self.trials_with_match_cnt = 0
            self.trials_with_no_match_cnt = 0
            self.correct_cnt = 0
            self.missed_cnt = 0
            self.incorrect_cnt = 0
            self.countdown_cnt = 0
            self.rounds_cnt = 0

            self.resultButton = QPushButton("Click here to continue", self)
            self.resultButton.setStyleSheet('background-color: '
                                            'rgb(0, 255, 0);')
            self.resultButton.setGeometry(100, 325, 200, 50)
            resultButtonFont = QFont()
            resultButtonFont.setPointSize(10)
            self.resultButton.setFont(resultButtonFont)
            self.resultButton.setVisible(True)
            self.resultButton.clicked.connect(self.info3_click)

            self.is_practice = False
        else:
            data = (f'Round Type: {self.n_back}-Back Test\n'
                    f'Number of Trials: {TRIALS}\n'
                    f'Trials With A Match: {self.trials_with_match_cnt}\n'
                    f'Trials With No Match: {self.trials_with_no_match_cnt}\n'
                    f'Number Of Correctly Matched Items: {self.correct_cnt}\n'
                    f'Number Of Missed Items: {self.missed_cnt}\n'
                    f'Number Of False Alarms: {self.incorrect_cnt}\n'
                    f'Letters Presented: {self.random_letters_list}\n')

            try:
                with open(self.file_path, "a") as file:
                    file.write(data)
                print("File saved")
            except IOError:
                print("An error occurred while saving the file.")
            
            self.trials_with_match_cnt = 0
            self.trials_with_no_match_cnt = 0
            self.correct_cnt = 0
            self.missed_cnt = 0
            self.incorrect_cnt = 0
            self.countdown_cnt = 0
            self.rounds_cnt = 0

            if self.n_back == 2:
                self.n_back = 3
                self.info4()
                self.infoTitle.setVisible(True)
                self.resultButton.setVisible(False)
                self.nextButton.setVisible(True)
            elif self.n_back == 3:
                self.finish_screen()
                self.infoTitle.setVisible(True)
                self.info.setVisible(True)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.installEventFilter(window)
    window.show()
    app.exec()
