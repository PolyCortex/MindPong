import sys

from PyQt5.QtWidgets import QApplication

from mindpong.MainMenu import MainMenu

def main():
  app = QApplication(sys.argv)
  menu = MainMenu()
  menu.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()