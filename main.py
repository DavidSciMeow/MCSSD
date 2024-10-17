import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import logging
from ui import forge, fabric, vanilla, mod

# 配置日志记录
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 创建主窗口
root = tk.Tk()
root.title("Minecraft Server Downloader")
root.geometry("1366x768")  # 初始窗口大小
root.minsize(1366, 768)  # 设置最小尺寸
# 创建菜单栏
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
# 创建Notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill='both')
# 创建TAB页
forge.cp_forge_search(notebook)
fabric.cp_fabric_search(notebook)
vanilla.cp_vanilla_search(notebook)
mod.cp_mod_search(notebook)

root.mainloop()