import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import mcssd.util as util
import mcssd.procedure.dl_procedure as dl
import ui.ui_util as ui_util

def cp_forge_search(notebook):
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

    forge_download_button = tk.Button(frame_forge_inner, text="Download", command=lambda: ui_util.file_save(dl.start_download_forge(next(v for v in forge_versions if v[0] == forge_version_var.get()), forge_progress_var)))
    forge_download_button.pack(side=tk.LEFT, padx=5)

    major_versions.extend(util.get_all_versions())
    major_version_combobox['values'] = major_versions

    def on_major_version_selected(*args):
        selected_major_version = major_version_var.get()
        if selected_major_version:
            forge_versions.clear()
            forge_versions.extend(util.get_forge_versions(selected_major_version))
            forge_version_combobox['values'] = [v[0] for v in forge_versions]

    major_version_var.trace_add('write', on_major_version_selected)

    def on_forge_search(*args):
        search_term = forge_version_var.get().lower()
        filtered_versions = [v[0] for v in forge_versions if search_term in v[0].lower()]
        forge_version_combobox['values'] = filtered_versions

    forge_version_var.trace_add('write', on_forge_search)

    forge_progress_var = tk.DoubleVar()
    forge_progress_bar = ttk.Progressbar(frame_forge, variable=forge_progress_var, maximum=100)
    forge_progress_bar.pack(side=tk.BOTTOM, fill='x')
