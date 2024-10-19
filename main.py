from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QTabWidget, QMessageBox
from PyQt5.QtCore import QFile, QTextStream
from PyQt5 import QtWidgets, QtCore, QtGui
import logging
import json
import global_vars
from ui import serdl, mod

# 配置日志记录
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

import global_vars
from ui import serdl, mod
import logging
from PyQt5.QtWidgets import QMainWindow, QTabWidget

# 配置日志记录
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(global_vars.lang.get('title', "Minecraft Server Downloader"))

        # 创建菜单栏
        menu_bar = self.menuBar()
        language_menu = menu_bar.addMenu(global_vars.lang.get('menu_language', 'Language'))

        # 创建标签页
        self.tabs = QTabWidget()
        self.server_dl_ui = serdl.ServerDLUI(self.tabs)
        self.tabs.addTab(self.server_dl_ui, global_vars.lang.get('tab_svr_dl', 'Server Download'))
        self.tabs.addTab(mod.ModSearchTab(), global_vars.lang.get('tab_mod', 'Mod Search'))
        self.setCentralWidget(self.tabs)

        self.update_ui_texts()

    def update_ui_texts(self):
        self.setWindowTitle(global_vars.lang.get('title', "Minecraft Server Downloader"))
        menu_bar = self.menuBar()
        language_menu = menu_bar.actions()[0].menu()
        language_menu.setTitle(global_vars.lang.get('menu_language', 'Language'))
        self.tabs.setTabText(0, global_vars.lang.get('tab_svr_dl', 'Server Download'))
        self.tabs.setTabText(1, global_vars.lang.get('tab_mod', 'Mod Search'))
        self.server_dl_ui.update_ui()  # Call update_ui on the instance

def load_language(lang_code):
    try:
        with open(f'lang/{lang_code}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading language file {lang_code}.json: {e}")
        return None

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    
    # 选择语言
    language_code = 'en'  # 默认语言
    global_vars.lang = load_language(language_code)
    if global_vars.lang is None:
        QMessageBox.critical(None, "Error", f"Error loading language file {language_code}.json")
        sys.exit(1)
    
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())