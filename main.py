import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import threading
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup
from PIL import Image, ImageTk  # 用于加载GitHub图标
import logging
import mcssd.util as util
import mcssd.procedure.dl_procedure as dl
import pkg_resources
from PIL import Image
import io

# 配置日志记录
logging.basicConfig(filename='debug.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# 显示信息窗口
def show_info():
    info_window = tk.Toplevel(root)
    info_window.title("Info")
    info_window.geometry("300x150")
    
    info_label = tk.Label(info_window, text="DavidSciMeow")
    info_label.pack(pady=10)
    
    # 加载GitHub图标
    github_icon_data = pkg_resources.resource_string(__name__, 'github_icon.png')
    github_icon = Image.open(io.BytesIO(github_icon_data))
    github_icon = github_icon.resize((20, 20), Image.LANCZOS)
    github_icon = ImageTk.PhotoImage(github_icon)
    
    github_button = tk.Button(info_window, image=github_icon, text=" GitHub", compound=tk.LEFT, command=open_github)
    github_button.image = github_icon  # 保持引用，防止图像被垃圾回收
    github_button.pack(pady=10)

# 打开GitHub主页
def open_github():
    import webbrowser
    webbrowser.open("https://github.com/DavidSciMeow")

def file_save(url, file_name, progress_var):
    dest = filedialog.asksaveasfilename(defaultextension=".jar", initialfile=file_name, filetypes=[("JAR files", "*.jar")])
    if dest:
        progress_var.set(0)
        threading.Thread(target=util.download_file, args=(url, dest, progress_var)).start()


# 创建主窗口
root = tk.Tk()
root.title("Minecraft Server Downloader")
root.geometry("700x200")  # 初始窗口大小
root.minsize(700, 200)  # 设置最小尺寸

# 创建菜单栏
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# 添加“信息”菜单项
menu_bar.add_command(label="Info", command=show_info)

# 添加“调试”选项
debug_mode = tk.BooleanVar()
debug_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Debug", menu=debug_menu)
debug_menu.add_checkbutton(label="Enable Debug", variable=debug_mode)

# 创建Notebook
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill='both')

# 创建原版下载页面
frame_vanilla = tk.Frame(notebook)
notebook.add(frame_vanilla, text="Vanilla")

versions = []
version_var = tk.StringVar()

frame_vanilla_inner = tk.Frame(frame_vanilla)
frame_vanilla_inner.pack(pady=20, padx=20, fill='both', expand=True)

version_label = tk.Label(frame_vanilla_inner, text="Version:")
version_label.pack(side=tk.LEFT)

version_combobox = ttk.Combobox(frame_vanilla_inner, textvariable=version_var, values=versions, width=30)  # 固定宽度
version_combobox.pack(side=tk.LEFT, fill='x', expand=True)

download_button = tk.Button(frame_vanilla_inner, text="Download", command=lambda: file_save(dl.start_download_Vanilla(version_var.get(), progress_var)))
download_button.pack(side=tk.LEFT, padx=5)

def on_search(*args):
    search_term = version_var.get().lower()
    filtered_versions = [version for version in versions if search_term in version.lower()]
    version_combobox['values'] = filtered_versions

version_var.trace_add('write', on_search)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(frame_vanilla, variable=progress_var, maximum=100)
progress_bar.pack(side=tk.BOTTOM, fill='x')

# 创建Forge下载页面
frame_forge = tk.Frame(notebook)
notebook.add(frame_forge, text="Forge")

forge_versions = []
forge_version_var = tk.StringVar()
major_versions = []
major_version_var = tk.StringVar()

frame_forge_inner = tk.Frame(frame_forge)
frame_forge_inner.pack(pady=20, padx=20, fill='both', expand=True)

major_version_label = tk.Label(frame_forge_inner, text="Major Version:")
major_version_label.pack(side=tk.LEFT)

major_version_combobox = ttk.Combobox(frame_forge_inner, textvariable=major_version_var, values=major_versions, width=15)  # 固定宽度
major_version_combobox.pack(side=tk.LEFT, fill='x', expand=True)

forge_version_label = tk.Label(frame_forge_inner, text="Specific Version:")
forge_version_label.pack(side=tk.LEFT)

forge_version_combobox = ttk.Combobox(frame_forge_inner, textvariable=forge_version_var, values=[v[0] for v in forge_versions], width=30)  # 固定宽度
forge_version_combobox.pack(side=tk.LEFT, fill='x', expand=True)

forge_download_button = tk.Button(frame_forge_inner, text="Download", command=lambda: file_save(dl.start_download_forge(next(v for v in forge_versions if v[0] == forge_version_var.get()), forge_progress_var)))
forge_download_button.pack(side=tk.LEFT, padx=5)

def on_major_version_selected(*args):
    selected_major_version = major_version_var.get()
    if selected_major_version:
        forge_versions.clear()
        forge_versions.extend(util.get_forge_versions(selected_major_version))
        forge_version_combobox['values'] = [v[0] for v in forge_versions]
        if debug_mode.get():
            logging.debug("Major versions loaded: %s", major_versions)

major_version_var.trace_add('write', on_major_version_selected)

def on_forge_search(*args):
    search_term = forge_version_var.get().lower()
    filtered_versions = [v[0] for v in forge_versions if search_term in v[0].lower()]
    forge_version_combobox['values'] = filtered_versions

forge_version_var.trace_add('write', on_forge_search)

forge_progress_var = tk.DoubleVar()
forge_progress_bar = ttk.Progressbar(frame_forge, variable=forge_progress_var, maximum=100)
forge_progress_bar.pack(side=tk.BOTTOM, fill='x')

# 创建Fabric下载页面
frame_fabric = tk.Frame(notebook)
notebook.add(frame_fabric, text="Fabric")

fabric_versions = []
fabric_version_var = tk.StringVar()

frame_fabric_inner = tk.Frame(frame_fabric)
frame_fabric_inner.pack(pady=20, padx=20, fill='both', expand=True)

fabric_version_label = tk.Label(frame_fabric_inner, text="Version:")
fabric_version_label.pack(side=tk.LEFT)

fabric_version_combobox = ttk.Combobox(frame_fabric_inner, textvariable=fabric_version_var, values=[v[0] for v in fabric_versions], width=30)  # 固定宽度
fabric_version_combobox.pack(side=tk.LEFT, fill='x', expand=True)

fabric_download_button = tk.Button(frame_fabric_inner, text="Download", command=lambda: file_save(dl.start_download_fabric(fabric_version_var.get(), next(v[1] for v in fabric_versions if v[0] == fabric_version_var.get()), fabric_progress_var)))
fabric_download_button.pack(side=tk.LEFT, padx=5)

def on_fabric_search(*args):
    search_term = fabric_version_var.get().lower()
    filtered_versions = [v[0] for v in fabric_versions if search_term in v[0].lower()]
    fabric_version_combobox['values'] = filtered_versions

fabric_version_var.trace_add('write', on_fabric_search)

fabric_progress_var = tk.DoubleVar()
fabric_progress_bar = ttk.Progressbar(frame_fabric, variable=fabric_progress_var, maximum=100)
fabric_progress_bar.pack(side=tk.BOTTOM, fill='x')

# 切换标签页时加载版本列表
def on_tab_changed(event):
    selected_tab = event.widget.tab(event.widget.index("current"))["text"]
    if selected_tab == "Vanilla" and not versions:
        versions.extend(util.get_versions())
        version_combobox['values'] = versions
        if debug_mode.get():
            logging.debug("Vanilla versions loaded: %s", versions)
    elif selected_tab == "Forge" and not major_versions:
        major_versions.extend(util.get_all_versions())
        major_version_combobox['values'] = major_versions
        if debug_mode.get():
            logging.debug("Major versions loaded: %s", major_versions)
    elif selected_tab == "Fabric" and not fabric_versions:
        fabric_versions.extend(util.get_fabric_versions())
        fabric_version_combobox['values'] = [v[0] for v in fabric_versions]
        if debug_mode.get():
            logging.debug("Fabric versions loaded: %s", fabric_versions)

notebook.bind("<<NotebookTabChanged>>", on_tab_changed)

root.mainloop()