import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import mcssd.procedure.util as util
import mcssd.procedure.dl_procedure as dl
import ui.ui_util as ui_util
import global_vars

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import mcssd.procedure.util as util
import mcssd.procedure.dl_procedure as dl
import ui.ui_util as ui_util
import global_vars

class ServerDLUI:
    def __init__(self, notebook):
        self.notebook = notebook
        self.frame_server_dl = tk.Frame(notebook)
        self.notebook.add(self.frame_server_dl, text=global_vars.lang.get('tab_svr_dl', 'Server Download'))

        # forge
        self.forge_versions = []
        self.forge_version_var = tk.StringVar()
        self.major_versions = []
        self.major_version_var = tk.StringVar()

        self.frame_forge_inner = tk.Frame(self.frame_server_dl)
        self.frame_forge_inner.pack(pady=20, padx=20, fill='both')

        self.major_version_label = tk.Label(self.frame_forge_inner, text=global_vars.lang.get('major_version', 'Maj. Version'))
        self.major_version_label.pack(side=tk.LEFT)

        self.major_version_combobox = ttk.Combobox(self.frame_forge_inner, textvariable=self.major_version_var, values=self.major_versions, width=15)  # 固定宽度
        self.major_version_combobox.pack(side=tk.LEFT, fill='x')

        self.forge_version_label = tk.Label(self.frame_forge_inner, text=global_vars.lang.get('specific_version', 'Specific Version'))
        self.forge_version_label.pack(side=tk.LEFT)

        self.forge_version_combobox = ttk.Combobox(self.frame_forge_inner, textvariable=self.forge_version_var, values=[v[0] for v in self.forge_versions], width=30)  # 固定宽度
        self.forge_version_combobox.pack(side=tk.LEFT, fill='x')

        self.forge_download_button = tk.Button(self.frame_forge_inner, text=global_vars.lang.get('download', 'Download'), command=lambda: ui_util.file_save(dl.start_download_forge(self.forge_version_var.get(), self.forge_progress_var)))
        self.forge_download_button.pack(side=tk.LEFT, padx=5)

        self.forge_progress_var = tk.DoubleVar()
        self.forge_progress_bar = ttk.Progressbar(self.frame_forge_inner, variable=self.forge_progress_var, maximum=100)
        self.forge_progress_bar.pack(side=tk.TOP, fill='x')

        self.major_versions.extend(util.get_all_versions())
        self.major_version_combobox['values'] = self.major_versions

        def on_major_version_selected(*args):
            selected_major_version = self.major_version_var.get()
            if selected_major_version:
                self.forge_versions.clear()
                self.forge_versions.extend(util.get_forge_versions(selected_major_version))
                self.forge_version_combobox['values'] = [v[0] for v in self.forge_versions]

        self.major_version_var.trace_add('write', on_major_version_selected)

        def on_forge_search(*args):
            search_term = self.forge_version_var.get().lower()
            filtered_versions = [v[0] for v in self.forge_versions if search_term in v[0].lower()]
            self.forge_version_combobox['values'] = filtered_versions

        self.forge_version_var.trace_add('write', on_forge_search)


        # fabric
        self.fabric_versions = []
        self.fabric_version_var = tk.StringVar()

        self.frame_fabric_inner = tk.Frame(self.frame_server_dl)
        self.frame_fabric_inner.pack(pady=20, padx=20, fill='both')

        self.fabric_version_label = tk.Label(self.frame_fabric_inner, text=global_vars.lang.get('fabric_version', 'Fabric Version'))
        self.fabric_version_label.pack(side=tk.LEFT)

        self.fabric_version_combobox = ttk.Combobox(self.frame_fabric_inner, textvariable=self.fabric_version_var, values=[v[0] for v in self.fabric_versions], width=30)
        self.fabric_version_combobox.pack(side=tk.LEFT, fill='x')

        self.fabric_download_button = tk.Button(self.frame_fabric_inner, text=global_vars.lang.get('download', 'Download'), command=lambda: ui_util.file_save(dl.start_download_fabric(self.fabric_version_var.get(), self.fabric_progress_var)))
        self.fabric_download_button.pack(side=tk.LEFT, padx=5)

        self.fabric_versions.extend(util.get_fabric_versions())
        self.fabric_version_combobox['values'] = [v[0] for v in self.fabric_versions]

        def on_fabric_search(*args):
            search_term = self.fabric_version_var.get().lower()
            filtered_versions = [v[0] for v in self.fabric_versions if search_term in v[0].lower()]
            self.fabric_version_combobox['values'] = filtered_versions

        self.fabric_version_var.trace_add('write', on_fabric_search)

        self.fabric_progress_var = tk.DoubleVar()
        self.fabric_progress_bar = ttk.Progressbar(self.frame_fabric_inner, variable=self.fabric_progress_var, maximum=100)
        self.fabric_progress_bar.pack(side=tk.TOP, fill='x', expand=True)

        # Vanilla
        self.versions = []
        self.version_var = tk.StringVar()

        self.frame_vanilla_inner = tk.Frame(self.frame_server_dl)
        self.frame_vanilla_inner.pack(pady=20, padx=20, fill='both')

        self.version_label = tk.Label(self.frame_vanilla_inner, text=global_vars.lang.get('van_version', 'Vanilla Version'))
        self.version_label.pack(side=tk.LEFT)

        self.version_combobox = ttk.Combobox(self.frame_vanilla_inner, textvariable=self.version_var, values=self.versions, width=30)
        self.version_combobox.pack(side=tk.LEFT, fill='x')

        self.download_button = tk.Button(self.frame_vanilla_inner, text=global_vars.lang.get('download', 'Download'), command=lambda: ui_util.file_save(dl.start_download_Vanilla(self.version_var.get(), self.progress_var)))
        self.download_button.pack(side=tk.LEFT, padx=5)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.frame_vanilla_inner, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(side=tk.TOP, fill='x', expand=True)

        self.versions.extend(util.get_versions())
        self.version_combobox['values'] = self.versions

        def on_search(*args):
            search_term = self.version_var.get().lower()
            filtered_versions = [version for version in self.versions if search_term in version.lower()]
            self.version_combobox['values'] = filtered_versions

        self.version_var.trace_add('write', on_search)


    def update_ui(self):
        self.notebook.tab(self.notebook.index(self.frame_server_dl), text=global_vars.lang.get('tab_svr_dl', 'Server Download'))
        self.major_version_label.config(text=global_vars.lang.get('major_version', 'Maj. Version'))
        self.forge_version_label.config(text=global_vars.lang.get('specific_version', 'Specific Version:'))
        self.forge_download_button.config(text=global_vars.lang.get('download', 'Download'))
        self.fabric_version_label.config(text=global_vars.lang.get('fabric_version', 'Fabric Version'))
        self.fabric_download_button.config(text=global_vars.lang.get('download', 'Download'))
        self.version_label.config(text=global_vars.lang.get('van_version', 'Vanilla Version'))
        self.download_button.config(text=global_vars.lang.get('download', 'Download'))

def ServerDL(notebook): return ServerDLUI(notebook)


