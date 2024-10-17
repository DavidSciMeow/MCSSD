import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import mcssd.procedure.dl_procedure as dl
import ui.ui_util as ui_util
import mcssd.util as util


def cp_vanilla_search(notebook):
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

    download_button = tk.Button(frame_vanilla_inner, text="Download", command=lambda: ui_util.file_save(dl.start_download_Vanilla(version_var.get(), progress_var)))
    download_button.pack(side=tk.LEFT, padx=5)

    versions.extend(util.get_versions())
    version_combobox['values'] = versions

    def on_search(*args):
        search_term = version_var.get().lower()
        filtered_versions = [version for version in versions if search_term in version.lower()]
        version_combobox['values'] = filtered_versions

    version_var.trace_add('write', on_search)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(frame_vanilla, variable=progress_var, maximum=100)
    progress_bar.pack(side=tk.BOTTOM, fill='x')
