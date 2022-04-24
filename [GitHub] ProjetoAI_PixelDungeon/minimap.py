from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, \
    QGridLayout
from PyQt5.QtGui import QPainter, QBrush, QPen, QPolygonF, QColor, QImage, QPixmap
from PyQt5.QtCore import Qt, QPointF, QTimer, QRect
import random
import gameControls
from main import tiles, fogOfWar, playerPos
from utils import *
#import tile_reader
#from tile_reader import *
#from fog_of_war import *
#from playerPos import *
#from item_reader import *
from gameControls import *
#from agent import *
import sys

# gameControls.initialize_game()

class Window(tiles, fogOfWar, playerPos, QWidget):
    # tilesvisitados = 0

    def __init__(self):
        super().__init__()
        self.title = "Minimap"
        self.top = 0
        self.left = 0
        self.width = 512
        self.height = 512
        #self._timer = QTimer(self)
        #self._timer.start(100)  # tempo entre ações
        #self._timer.timeout.connect(self._update)
        self.generalLayout = QGridLayout()
        self.centralWidget = QWidget(self)
        #self.InitWindow()

    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("ic_launcher.png"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def paintEvent(self, e):
        painter = QPainter(self)
        self.draw_tiles(painter)

    def draw_tiles(self, painter: QPainter):

        #tiles = read_tiles()
        #fogOfWar = read_fog_of_war()
        #playerPos = read_playerPos()
        #backpack = read_backpack()
        #dungeonDepth = read_depth()
        # state = np.concatenate((tiles, fogOfWar, playerPos))
        # print(state)

        # print(tiles_free, tiles_invisible, tiles_outofbounds, exploration_rate)

        pos = 0

        for row in range(32):
            for col in range(32):
                rgb = ColorMap[StaticTileType(tiles[pos]).name].value
                color = QColor(*rgb)
                row_offset = 16
                col_offset = 16
                col_start = col_offset * col
                row_start = row_offset * row


                if fogOfWar[pos] == 0:  # tiles visíveis no momento, aproveita pra desenhar o player e os inimigos
                    if playerPos[pos] == 1 or playerPos[pos] != 0:  # se o valor da célula for igual ao valor do pointer do player
                        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                        painter.setBrush(QBrush(QColor(255, 127, 39)))
                        painter.drawRect(col_start, row_start, 16, 16)
                        pos = pos + 1
                        # print(pos)
                    else:
                        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                        painter.setBrush(QBrush(color))
                        painter.drawRect(col_start, row_start, 16, 16)
                        pos = pos + 1

                elif fogOfWar[pos] == 1:  # "apaga" os tiles que o player não está enxergando
                    painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                    painter.setBrush(QBrush(color, 12))
                    painter.drawRect(col_start, row_start, 16, 16)
                    pos = pos + 1

                elif fogOfWar[pos] == 2 and tiles[pos] == 4:  # tiles invisiveis = preto
                    painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                    painter.setBrush(QBrush(QColor(0, 0, 0)))
                    painter.drawRect(col_start, row_start, 16, 16)
                    pos = pos + 1

                else:
                    pos = pos + 1

        # print(tilesvisitados)
        # return tilesvisitados

    def _update(self):
        # tilesvisitados = draw_tiles()
        #PDAgent.calcReward(self)
        # PDAgent.act(self.state) #move o tio
        # self.paintEvent(self) #isso fazia executar duas vezes
        self.update()

App = QApplication(sys.argv)
window = Window()
window.show()
App.processEvents()
#window.updatesEnabled()
#App.exec()
sys.exit(App.exec_())
App.quit()
#pass
#App.exec()
