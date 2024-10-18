import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import mcssd.procedure.util as util

# 保存文件
def file_save(argsx):
    dest = filedialog.asksaveasfilename(defaultextension=".jar", initialfile=argsx[1], filetypes=[("JAR files", "*.jar")])
    if dest:
        argsx[2].set(0)
        threading.Thread(target=util.download_file, args=(argsx[0], dest, argsx[2])).start()
