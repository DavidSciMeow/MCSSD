import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import mcssd.util as util

# 保存文件
def file_save(url, file_name, progress_var):
    dest = filedialog.asksaveasfilename(defaultextension=".jar", initialfile=file_name, filetypes=[("JAR files", "*.jar")])
    if dest:
        progress_var.set(0)
        threading.Thread(target=util.download_file, args=(url, dest, progress_var)).start()
