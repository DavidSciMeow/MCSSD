import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
import json
import os
import global_vars
from ui import serdl, mod

# 配置日志记录
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 加载语言文件
def load_language(lang_code):
    try:
        with open(f'lang/{lang_code}.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading language file {lang_code}.json: {e}")
        return None

# 更新UI文本
def update_ui_texts():
    root.title(global_vars.lang.get('title',"Minecraft Server Downloader"))
    #file_menu.entryconfig(0, label=lang['menu_file'])
    #edit_menu.entryconfig(0, label=lang['menu_edit'])
    #help_menu.entryconfig(0, label=lang['menu_help'])
    menu_bar.entryconfig(language_menu_index, label=global_vars.lang.get('menu_language','Language'))  # 更新菜单的标签名
    notebook.tab(0, text=global_vars.lang.get('tab_svr_dl', 'Server Download'))
    notebook.tab(1, text=global_vars.lang.get('tab_mod','Mod Serach'))
    dlpg.update_ui()  # 更新下载页面的UI文本

# 选择语言
language_code = 'en'  # 默认语言
lang = load_language(language_code)
if lang is None:
    lang = load_language('en')  # 如果默认语言文件加载失败，尝试加载英文语言文件

# 创建主窗口
root = tk.Tk()
root.title(global_vars.lang.get('title',"Minecraft Server Downloader"))
root.geometry("1366x768")  # 初始窗口大小
root.minsize(1366, 768)  # 设置最小尺寸

# 创建菜单栏
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# 创建菜单项
#file_menu = tk.Menu(menu_bar, tearoff=0)
#file_menu.add_command(label=lang['menu_file'])
#menu_bar.add_cascade(label=lang['menu_file'], menu=file_menu)

#edit_menu = tk.Menu(menu_bar, tearoff=0)
#edit_menu.add_command(label=lang['menu_edit'])
#menu_bar.add_cascade(label=lang['menu_edit'], menu=edit_menu)

#help_menu = tk.Menu(menu_bar, tearoff=0)
#help_menu.add_command(label=lang['menu_help'])
#menu_bar.add_cascade(label=lang['menu_help'], menu=help_menu)

# 创建语言菜单
language_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label=global_vars.lang.get('menu_language','Language'), menu=language_menu)
language_menu_index = menu_bar.index("end")  # 获取语言菜单的索引

# 扫描语言文件目录并动态生成菜单项
language_files = [f for f in os.listdir('lang') if f.endswith('.json')]
for lang_file in language_files:
    lang_code = os.path.splitext(lang_file)[0]
    lang_data = load_language(lang_code)
    if lang_data:
        language_menu.add_command(
                    label=lang_data['menu_language_specific'],
                    command=lambda lc=lang_code: (lambda new_lang: global_vars.lang.update(new_lang) or update_ui_texts() if new_lang else None)(load_language(lc))
                )
# 创建Notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill='both')

# 创建TAB页
dlpg = serdl.ServerDL(notebook)
mod.cp_mod_search(notebook)

root.mainloop()