import sys

from PyQt5.QtWidgets import QApplication

from mindpong.MainMenu import MainMenu
from mindpong.model.game import Game

def main():
  app = QApplication(sys.argv)
  

  update_data_callbacks = [
      lambda data: print('I am updating my data', data),
  ]
  game = Game(update_data_callbacks)
  game.start()

  menu = MainMenu(game)
  menu.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()