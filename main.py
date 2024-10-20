import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QTabWidget, QMessageBox, QAction, QFontDialog
from PyQt5.QtCore import QFile, QTextStream
from PyQt5 import QtWidgets, QtCore, QtGui
import logging
import json
import global_vars
from ui import serdl, mod

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

        # 动态加载语言菜单项
        self.load_language_menu(language_menu)

        # 添加字体设置菜单
        settings_menu = menu_bar.addMenu(global_vars.lang.get('menu_settings', 'Settings'))
        font_action = QAction(global_vars.lang.get('menu_font', 'Set Font'), self)
        font_action.triggered.connect(self.set_font)
        settings_menu.addAction(font_action)

        # 创建标签页
        self.tabs = QTabWidget()
        self.server_dl_ui = serdl.ServerDLUI(self.tabs)
        self.tabs.addTab(self.server_dl_ui, global_vars.lang.get('tab_svr_dl', 'Server Download'))
        self.tabs.addTab(mod.ModSearchTab(), global_vars.lang.get('tab_mod', 'Mod Search'))
        self.setCentralWidget(self.tabs)

        # 设置默认字体为微软雅黑
        default_font = QtGui.QFont("Microsoft YaHei", 12)
        self.setFont(default_font)
        self.update_ui_fonts(default_font)

        self.update_ui_texts()

    def load_language_menu(self, language_menu):
        lang_dir = 'lang/'
        for filename in os.listdir(lang_dir):
            if filename.endswith('.json'):
                lang_code = filename.split('.')[0]
                try:
                    with open(os.path.join(lang_dir, filename), 'r', encoding='utf-8') as file:
                        lang_data = json.load(file)
                        lang_name = lang_data.get('menu_language_specific', lang_code)
                        lang_action = QAction(lang_name, self)
                        lang_action.triggered.connect(lambda checked, code=lang_code: self.change_language(code))
                        language_menu.addAction(lang_action)
                except Exception as e:
                    logging.error(f"Failed to load language file {filename}: {e}")

    def change_language(self, lang_code):
        # Load the new language file
        try:
            with open(f'lang/{lang_code}.json', 'r', encoding='utf-8') as file:
                new_lang = json.load(file)
                global_vars.lang.update(new_lang)
                self.update_ui_texts()
        except FileNotFoundError:
            logging.error(f"Language file for {lang_code} not found.")
            QMessageBox.warning(self, "Error", f"Language file for {lang_code} not found.")

    def set_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.setFont(font)
            self.update_ui_fonts(font)

    def update_ui_fonts(self, font):
        self.tabs.setFont(font)
        self.server_dl_ui.setFont(font)
        # 如果有其他需要更新字体的控件，可以在这里添加

    def update_ui_texts(self):
        self.setWindowTitle(global_vars.lang.get('title', "Minecraft Server Downloader"))
        self.tabs.setTabText(self.tabs.indexOf(self.server_dl_ui), global_vars.lang.get('tab_svr_dl', 'Server Download'))
        # 更新其他UI文本
        self.server_dl_ui.update_ui()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())