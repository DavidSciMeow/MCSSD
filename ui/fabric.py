import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from urllib.parse import urlparse, parse_qs
import mcssd.procedure.dl_procedure as dl
import ui.ui_util as ui_util
import mcssd.util as util

def cp_fabric_search(notebook):
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

    fabric_download_button = tk.Button(frame_fabric_inner, text="Download", command=lambda: ui_util.file_save(dl.start_download_fabric(fabric_version_var.get(), next(v[1] for v in fabric_versions if v[0] == fabric_version_var.get()), fabric_progress_var)))
    fabric_download_button.pack(side=tk.LEFT, padx=5)

    fabric_versions.extend(util.get_fabric_versions())
    fabric_version_combobox['values'] = [v[0] for v in fabric_versions]

    def on_fabric_search(*args):
        search_term = fabric_version_var.get().lower()
        filtered_versions = [v[0] for v in fabric_versions if search_term in v[0].lower()]
        fabric_version_combobox['values'] = filtered_versions

    fabric_version_var.trace_add('write', on_fabric_search)

    fabric_progress_var = tk.DoubleVar()
    fabric_progress_bar = ttk.Progressbar(frame_fabric, variable=fabric_progress_var, maximum=100)
    fabric_progress_bar.pack(side=tk.BOTTOM, fill='x')