import sys

import pygame
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import random


class AlarmMiniGame(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('../ui_file/AR_mini_game.ui', self)
        self.stackedWidget.setCurrentIndex(0)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        qtimer = QTimer(self)
        qtimer.start(5000)
        qtimer.timeout.connect(self.mini_game)
        self.btn_count = 0
        self.egg_lbl.mousePressEvent = self.go_egg_event
        self.pushButton.clicked.connect(lambda x: self.close())
        self.play_alarm()

    def mini_game(self):
        """미니게임을 위한 좌표 세팅 함수"""
        x_value = random.randrange(0, 400)
        y_value = random.randrange(0, 500)
        self.egg_lbl.move(int(x_value), int(y_value))

    def go_egg_event(self, e):
        """미니게임 실행 함수(클릭에 성공했을때마다 카운트가 올라가며 10회 달성시 다음 페이지로 넘어감)"""
        self.btn_count += 1
        self.label_3.setText(f'{self.btn_count}/10')
        if self.btn_count == 3:
            self.egg_lbl.setPixmap(QPixmap('../ui_img/달걀2.png'))
        elif self.btn_count == 5:
            self.egg_lbl.setPixmap(QPixmap('../ui_img/달걀3.png'))
        elif self.btn_count == 8:
            self.egg_lbl.setPixmap(QPixmap('../ui_img/달걀4.png'))
        elif self.btn_count == 10:
            self.play_alarm()
            self.stackedWidget.setCurrentIndex(1)

    def play_alarm(self):
        """알람음 설정 / 다이얼로그가 켜지는 순간부터 미니게임 완료할때까지 무한재생"""
        pygame.init()
        sound_ = pygame.mixer.Sound('../sound/메이플스토리.mp3')
        sound_.play(-1)
        if self.btn_count == 10:
            pygame.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = AlarmMiniGame()
    myWindow.show()
    app.exec_()