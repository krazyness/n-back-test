#!/usr/bin/env python
"""
MIT License

Copyright (c) 2023-2024 Brody Dai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import random
import sys
import os
import argparse
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

COUNTDOWN = 3


class MainWindow(QMainWindow):
    def my_font(self, size, bold):
        font = self.font()
        font.setPointSize(size)
        font.setBold(bold)
        return font

    def __init__(self, trials, matches, letter_duration, pause):
        super().__init__()
        self.TRIALS = trials
        self.MINIMUM_MATCHES = matches
        self.LETTER_DURATION = letter_duration
        self.PAUSE_DURATION = pause
        self.reset(2, trials, matches, True)

        self.setWindowTitle("Memory Test")
        self.resize(700, 500)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 0))
        self.setPalette(palette)
        self.correct_sound_output = QAudioOutput()
        self.correct_sound_output.setVolume(50)
        self.incorrect_sound_output = QAudioOutput()
        self.incorrect_sound_output.setVolume(50)
        fpath = os.path.dirname(__file__)
        self.correct_sound = QMediaPlayer()
        self.correct_sound.setAudioOutput(self.correct_sound_output)
        self.correct_sound.setSource(QUrl.fromLocalFile(
            f"{fpath}/RightChoice.wav"))
        self.incorrect_sound = QMediaPlayer()
        self.incorrect_sound.setAudioOutput(self.incorrect_sound_output)
        self.incorrect_sound.setSource(QUrl.fromLocalFile(
            f"{fpath}/WrongChoice.wav"))
        self.directory_button = QPushButton(
            'Choose a file to\nsave your results in', self)
        self.directory_button.setGeometry(250, 150, 200, 200)
        self.directory_button.setStyleSheet(
            'background-color: rgb(255, 255, 255);')
        self.directory_button.setFont(self.my_font(15, False))
        self.directory_button.setVisible(True)
        self.directory_button.clicked.connect(self.get_directory)
        self.center_button = QPushButton("Loading...", self)
        self.center_button.setGeometry(300, 200, 100, 100)
        self.center_button.setStyleSheet(
            'background-color: rgb(82, 200, 255);')
        self.center_button.setFont(self.my_font(15, False))
        self.center_button.setVisible(False)
        self.center_button.clicked.connect(lambda: self.check(True))
        self.practice_help1 = QPushButton("", self)
        self.practice_help1.setGeometry(175, 200, 100, 100)
        self.practice_help1.setFont(self.my_font(15, False))
        self.practice_help1.setVisible(False)
        self.practice_help1.setEnabled(False)
        self.practice_help2 = QPushButton("", self)
        self.practice_help2.setGeometry(50, 200, 100, 100)
        self.practice_help2.setFont(self.my_font(15, False))
        self.practice_help2.setVisible(False)
        self.practice_help2.setEnabled(False)

        self.infoTitle = QLabel("N-back working memory task", self)
        self.infoTitle.setGeometry(100, 50, 500, 50)
        self.infoTitle.setFont(self.my_font(20, True))
        self.infoTitle.setStyleSheet('color: white;')
        self.infoTitle.setVisible(False)
        self.info = QLabel(
            'In this task, you will see a sequence of letters.\n'
            'Each letter is shown for a few seconds. You need\n'
            'to decide if you saw the same letter 2 trials ago,\n'
            'that is, this is a n=2-back task.', self)
        self.info.setGeometry(100, -90, 500, 500)
        self.info.setFont(self.my_font(15, False))
        self.info.setStyleSheet('color: white;')
        self.info.setVisible(False)
        self.info2 = QLabel(
            'If you saw the same letter 2 trials ago, you click\n'
            'the window with the mouse.\n\n'
            'If correct, you will hear this sound:\n\n'
            'If incorrect, you will hear this sound:', self)
        self.info2.setGeometry(100, 50, 500, 500)
        self.info2.setFont(self.my_font(15, False))
        self.info2.setStyleSheet('color: white;')
        self.info2.setVisible(False)
        self.play_correct_button = QPushButton('PLAY', self)
        self.play_correct_button.setGeometry(425, 295, 250, 45)
        self.play_correct_button.setStyleSheet(
            'background-color: rgb(0, 255, 0);')
        self.play_correct_button.setVisible(False)
        self.play_incorrect_button = QPushButton('PLAY', self)
        self.play_incorrect_button.setGeometry(425, 350, 250, 45)
        self.play_incorrect_button.setStyleSheet(
            'background-color: rgb(0, 255, 0);')
        self.play_incorrect_button.setVisible(False)
        self.nextButton = QPushButton(
            'Click here for the next info screen', self)
        self.nextButton.setGeometry(100, 400, 250, 50)
        self.nextButton.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.nextButton.setFont(self.my_font(10, False))
        self.nextButton.setVisible(False)
        self.resultButton = QPushButton("Click here to continue", self)
        self.resultButton.setStyleSheet(
            'background-color: rgb(0, 255, 0);')
        self.resultButton.setGeometry(100, 325, 200, 50)
        self.resultButton.setFont(self.my_font(10, False))
        self.resultButton.setVisible(False)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)

    def reset(self, n_back, trials, matches, is_practice):
        self.n_back = n_back
        self.is_practice = is_practice
        self.trials_with_match_cnt = 0
        self.correct_cnt = 0
        self.missed_cnt = 0
        self.incorrect_cnt = 0
        self.countdown_cnt = 0
        self.rounds_cnt = 0
        self.is_letter_appeared = False
        self.clicks = []

        locations = random.sample(list(range(trials-n_back)), matches)
        locations = set(locations)
        a2z = list(map(chr, range(65, 91)))
        letters = random.choices(a2z, k=n_back)
        for i in range(trials-n_back):
            if i in locations:
                new = letters[i]
            else:
                new = random.choice(a2z)
            letters.append(new)
            if new == letters[i] and i in locations:
                self.trials_with_match_cnt += 1
            elif new == letters[i] and i not in locations:
                available_letters = set(a2z) - {new}
                letters[i] = random.choice(list(available_letters))
        self.random_letters_list = letters

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
                sys.exit(1)
        if self.file_path is not None:
            self.directory_button.setVisible(False)
            self.info_click()
        else:
            sys.exit(1)

    def info_click(self):
        self.infoTitle.setVisible(True)
        self.info.setVisible(True)
        self.info2.setVisible(True)
        self.play_correct_button.setVisible(True)
        self.play_correct_button.clicked.connect(self.correct_sound.play)
        self.play_incorrect_button.setVisible(True)
        self.play_incorrect_button.clicked.connect(self.incorrect_sound.play)
        self.nextButton.setVisible(True)
        self.nextButton.clicked.connect(self.info2_click)

    def info2_click(self):
        self.play_correct_button.setVisible(False)
        self.play_incorrect_button.setVisible(False)

        self.info.setText(
            'To help you learn this task, at first there is a very easy\n'
            'version. You will be reminded of the letters you saw the\n'
            'trials before. They come left from the letter in the middle\n'
            'of the screen. They are only there to help. Later on, they\n'
            'will not be shown anymore, and you will need to do it all\n'
            'based on your memory.')
        self.info.move(self.info.x(), self.info.y() + 15)

        self.info2.setText(
            'Tip: You can click outside of the box\n'
            'so your cursor doesn\'t block '
            'the displayed letter')

        self.nextButton.move(self.nextButton.x(), self.nextButton.y() - 50)
        self.nextButton.setText("Click here to begin your practice run!")
        self.nextButton.clicked.connect(self.on_next_button)

    def info3_click(self):
        self.infoTitle.setVisible(True)
        self.resultButton.setVisible(False)
        self.nextButton.setVisible(True)

        self.info.move(self.info.x(), self.info.y() - 35)
        self.info.setText(
            'Now that you have learned the n-back task, you need to\n'
            'do it purely based on your memory. Thus, click the letter\n'
            'if it is the same as 2 letters ago.')

        self.info2.setVisible(True)
        self.info2.move(self.info2.x(), self.info2.y() - 60)
        self.info2.setText(
            'Otherwise, do nothing.\n\n'
            'Concentrate, because this is not easy.')

        self.nextButton.setText("Click here to begin the 2-back test")
        self.nextButton.setGeometry(
            self.nextButton.x(), self.nextButton.y() + 10, 225, 50)

    def info4(self):
        self.info.move(self.info.x(), self.info.y() + 25)
        self.info.setText(
            'Congratulations on completing the 2-back test! Now,\n'
            'it\'s time to challenge yourself further with the 3-back test.\n'
            'In this task, you will be presented with a sequence of\n'
            'letters, similar to the previous test. This time, you need\n'
            'to determine if the current letter matches the one\n'
            'presented 3 trials ago.')

        self.info2.move(self.info2.x(), self.info2.y() + 60)
        self.info2.setText(
            'Concentrate, and try your best because this is not easy.')

        self.nextButton.setText("Click here to begin the 3-back test")
        self.nextButton.move(self.nextButton.x(), self.nextButton.y() + 80)

    def finish_screen(self):
        self.infoTitle.setText("You Finished!")
        self.info.setText(
            'Congratulations! You successfully completed the 2-back\n'
            'and 3-back test! You may now close the test window.')

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            if self.is_letter_appeared:
                self.check(True)

    def resizeEvent(self, event: QResizeEvent):
        for widget in self.findChildren(QWidget):
            if event.oldSize().width() <= 0:
                return
            old_centerx = event.oldSize().width() // 2 - widget.width() // 2
            old_centery = event.oldSize().height() // 2 - widget.height() // 2
            new_centerx = self.width() // 2 - widget.width() // 2
            new_centery = self.height() // 2 - widget.height() // 2
            distance_x = new_centerx - old_centerx
            distance_y = new_centery - old_centery
            widget.move(widget.x() + distance_x, widget.y() + distance_y)

    def on_next_button(self):
        self.center_button.setEnabled(False)
        self.center_button.setVisible(True)

        self.nextButton.setVisible(False)
        self.info.setVisible(False)
        self.infoTitle.setVisible(False)
        self.info2.setVisible(False)

        self.timer.start(1000)

    def update(self):
        if self.countdown_cnt < COUNTDOWN:
            self.center_button.setText(f"{COUNTDOWN-self.countdown_cnt}")
            self.countdown_cnt += 1
            return
        self.timer.stop()
        if self.rounds_cnt >= self.TRIALS:
            self.is_letter_appeared = False
            self.results()
            return
        if not self.is_letter_appeared:  # Make Letter Appear
            self.is_letter_appeared = True
            self.center_button.setVisible(True)
            self.center_button.setEnabled(True)
            self.center_button.setText(
                f"{self.random_letters_list[self.rounds_cnt]}")
            if self.is_practice:
                if self.rounds_cnt > 0:
                    self.practice_help1.setText(
                        f"{self.random_letters_list[self.rounds_cnt-1]}")
                    self.practice_help1.setVisible(True)
                if self.rounds_cnt > 1:
                    self.practice_help2.setText(
                        f"{self.random_letters_list[self.rounds_cnt-2]}")
                    self.practice_help2.setVisible(True)
            self.timer.start(self.LETTER_DURATION * 1000)
        else:  # Make Letter Not Appear And Check
            def updateTimerFunction():
                updateTimer.stop()
                self.is_letter_appeared = False
                self.check(False)
                self.rounds_cnt += 1
                self.timer.start((self.PAUSE_DURATION * 1000) * 2/7)
            updateTimer = QTimer()
            updateTimer.timeout.connect(updateTimerFunction)
            self.center_button.setVisible(False)
            self.practice_help1.setVisible(False)
            self.practice_help2.setVisible(False)
            updateTimer.start((self.PAUSE_DURATION * 1000) * 5/7)

    def check(self, clicked):
        if len(self.clicks) > self.rounds_cnt:
            return
        self.clicks.append(clicked)
        if self.rounds_cnt < self.n_back:
            return
        matched = self.random_letters_list[self.rounds_cnt] == \
            self.random_letters_list[self.rounds_cnt - self.n_back]
        if clicked:
            if matched:
                self.correct_sound.play()
                self.correct_cnt += 1
            else:
                self.incorrect_sound.play()
                self.incorrect_cnt += 1
        elif matched:
            self.incorrect_sound.play()
            self.missed_cnt += 1

    def results(self):
        self.center_button.setVisible(False)
        self.center_button.setText("Loading...")

        if self.is_practice:
            self.info.setText(
                f'There were {self.TRIALS} '
                'trials total in this block.'
                '\n\nTotal trials that had a '
                f'match: {self.trials_with_match_cnt}'
                '\n\nNumber of correctly matched '
                f'items: {self.correct_cnt}'
                f'\n\nNumber of missed items: {self.missed_cnt}'
                '\n\nNumber of false alarms: '
                f'{self.incorrect_cnt}')
            self.info.setVisible(True)

            self.reset(2, self.TRIALS, self.MINIMUM_MATCHES, False)

            self.resultButton.setVisible(True)
            self.resultButton.clicked.connect(self.info3_click)
        else:
            data = (f'Round Type: {self.n_back}-Back Test\n'
                    f'Number of Trials: {self.TRIALS}\n'
                    f'Trials With A Match: {self.trials_with_match_cnt}\n'
                    f'Number Of Correctly Matched Items: {self.correct_cnt}\n'
                    f'Number Of Missed Items: {self.missed_cnt}\n'
                    f'Number Of False Alarms: {self.incorrect_cnt}\n'
                    f'Letters Presented: {self.random_letters_list}\n'
                    f'Click Record: {self.clicks}\n')

            try:
                with open(self.file_path, "a") as file:
                    file.write(data)
                print("File saved")
            except IOError:
                print("An error occurred while saving the file.")

            if self.n_back == 2:
                self.reset(3, self.TRIALS, self.MINIMUM_MATCHES, False)
                self.info4()
                self.infoTitle.setVisible(True)
                self.nextButton.setVisible(True)
                self.info.setVisible(True)
                self.info2.setVisible(True)
            elif self.n_back == 3:
                self.finish_screen()
                self.infoTitle.setVisible(True)
                self.info.setVisible(True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--trials", help='sets '
        'the amount of trials given '
        'in test (default 25)', type=int, default=25)
    parser.add_argument(
        "--matches", help='sets '
        'the minimum amount of matches '
        'given in test (default 7)', type=int, default=7)
    parser.add_argument(
        "--letter-duration", help='sets '
        'the amount of time that the '
        'letter appears during the test '
        'in seconds (default 0.5)', type=float, default=0.5)
    parser.add_argument(
        "--pause", help='sets '
        'the interval between each letter '
        'appearing (default 2.5)', type=float, default=2.5)
    args = parser.parse_args()
    if args.trials <= args.matches+2:
        print(
            'ERR-01: cannot make trials less or equal to matches+2\n'
            f'Current #trials: {args.trials}\n'
            f'Current #matches: {args.matches}')
        sys.exit(1)
    app = QApplication([])
    window = MainWindow(
        args.trials,
        args.matches,
        args.letter_duration,
        args.pause)
    window.installEventFilter(window)
    window.show()
    app.exec()
