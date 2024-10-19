from PyQt5 import QtWidgets, QtCore
import mcssd.procedure.util as util
import mcssd.procedure.dl_procedure as dl
import ui.ui_util as ui_util
import global_vars

class ServerDLUI(QtWidgets.QWidget):
    def __init__(self, notebook):
        super().__init__()
        self.notebook = notebook
        self.layout = QtWidgets.QVBoxLayout(self)
        self.notebook.addTab(self, global_vars.lang.get('tab_svr_dl', 'Server Download'))

        # forge
        self.forge_versions = []
        self.forge_version_var = str()
        self.major_versions = []
        self.major_version_var = str()

        self.frame_forge_inner = QtWidgets.QWidget(self)
        self.layout_forge_inner = QtWidgets.QHBoxLayout(self.frame_forge_inner)
        self.layout.addWidget(self.frame_forge_inner)

        self.major_version_label = QtWidgets.QLabel(global_vars.lang.get('major_version', 'Maj. Version'), self.frame_forge_inner)
        self.layout_forge_inner.addWidget(self.major_version_label)

        self.major_version_combobox = QtWidgets.QComboBox(self.frame_forge_inner)
        self.major_version_combobox.addItems(self.major_versions)
        self.layout_forge_inner.addWidget(self.major_version_combobox)

        self.forge_version_label = QtWidgets.QLabel(global_vars.lang.get('specific_version', 'Specific Version'), self.frame_forge_inner)
        self.layout_forge_inner.addWidget(self.forge_version_label)

        self.forge_version_combobox = QtWidgets.QComboBox(self.frame_forge_inner)
        self.forge_version_combobox.addItems([v[0] for v in self.forge_versions])
        self.layout_forge_inner.addWidget(self.forge_version_combobox)

        self.forge_download_button = QtWidgets.QPushButton(global_vars.lang.get('download', 'Download'), self.frame_forge_inner)
        self.forge_download_button.clicked.connect(lambda: ui_util.file_save(lambda dest: dl.start_download_forge(self.forge_version_var, dest), "forge_version.jar"))
        self.layout_forge_inner.addWidget(self.forge_download_button)

        self.forge_progress_var = float()
        self.forge_progress_bar = QtWidgets.QProgressBar(self.frame_forge_inner)
        self.forge_progress_bar.setMaximum(100)
        self.layout_forge_inner.addWidget(self.forge_progress_bar)

        self.major_versions.extend(util.get_all_versions())
        self.major_version_combobox.addItems(self.major_versions)

        self.major_version_combobox.currentTextChanged.connect(self.on_major_version_selected)
        self.forge_version_combobox.currentTextChanged.connect(self.on_forge_search)

        # fabric
        self.fabric_versions = []
        self.fabric_version_var = str()

        self.frame_fabric_inner = QtWidgets.QWidget(self)
        self.layout_fabric_inner = QtWidgets.QHBoxLayout(self.frame_fabric_inner)
        self.layout.addWidget(self.frame_fabric_inner)

        self.fabric_version_label = QtWidgets.QLabel(global_vars.lang.get('fabric_version', 'Fabric Version'), self.frame_fabric_inner)
        self.layout_fabric_inner.addWidget(self.fabric_version_label)

        self.fabric_version_combobox = QtWidgets.QComboBox(self.frame_fabric_inner)
        self.fabric_version_combobox.addItems([v[0] for v in self.fabric_versions])
        self.layout_fabric_inner.addWidget(self.fabric_version_combobox)

        self.fabric_download_button = QtWidgets.QPushButton(global_vars.lang.get('download', 'Download'), self.frame_fabric_inner)
        self.fabric_download_button.clicked.connect(lambda: ui_util.file_save(lambda dest: dl.start_download_fabric(self.fabric_version_var, dest), "fabric_version.jar"))
        self.layout_fabric_inner.addWidget(self.fabric_download_button)

        self.fabric_versions.extend(util.get_fabric_versions())
        self.fabric_version_combobox.addItems([v[0] for v in self.fabric_versions])

        self.fabric_version_combobox.currentTextChanged.connect(self.on_fabric_search)

        self.fabric_progress_var = float()
        self.fabric_progress_bar = QtWidgets.QProgressBar(self.frame_fabric_inner)
        self.fabric_progress_bar.setMaximum(100)
        self.layout_fabric_inner.addWidget(self.fabric_progress_bar)

        # Vanilla
        self.versions = []
        self.version_var = str()

        self.frame_vanilla_inner = QtWidgets.QWidget(self)
        self.layout_vanilla_inner = QtWidgets.QHBoxLayout(self.frame_vanilla_inner)
        self.layout.addWidget(self.frame_vanilla_inner)

        self.version_label = QtWidgets.QLabel(global_vars.lang.get('van_version', 'Vanilla Version'), self.frame_vanilla_inner)
        self.layout_vanilla_inner.addWidget(self.version_label)

        self.version_combobox = QtWidgets.QComboBox(self.frame_vanilla_inner)
        self.version_combobox.addItems(self.versions)
        self.layout_vanilla_inner.addWidget(self.version_combobox)

        self.download_button = QtWidgets.QPushButton(global_vars.lang.get('download', 'Download'), self.frame_vanilla_inner)
        self.download_button.clicked.connect(lambda: ui_util.file_save(lambda dest: dl.start_download_Vanilla(self.version_var, dest), "vanilla_version.jar"))
        self.layout_vanilla_inner.addWidget(self.download_button)

        self.progress_var = float()
        self.progress_bar = QtWidgets.QProgressBar(self.frame_vanilla_inner)
        self.progress_bar.setMaximum(100)
        self.layout_vanilla_inner.addWidget(self.progress_bar)

        self.versions.extend(util.get_versions())
        self.version_combobox.addItems(self.versions)

        self.version_combobox.currentTextChanged.connect(self.on_search)

    def on_major_version_selected(self):
        selected_major_version = self.major_version_combobox.currentText()
        if selected_major_version:
            self.forge_versions.clear()
            self.forge_versions.extend(util.get_forge_versions(selected_major_version))
            self.forge_version_combobox.blockSignals(True)
            self.forge_version_combobox.clear()
            self.forge_version_combobox.addItems([v[0] for v in self.forge_versions])
            self.forge_version_combobox.blockSignals(False)

    def on_forge_search(self):
        search_term = self.forge_version_combobox.currentText().lower()
        filtered_versions = [v[0] for v in self.forge_versions if search_term in v[0].lower()]
        self.forge_version_combobox.blockSignals(True)
        self.forge_version_combobox.clear()
        self.forge_version_combobox.addItems(filtered_versions)
        self.forge_version_combobox.blockSignals(False)

    def on_fabric_search(self):
        search_term = self.fabric_version_combobox.currentText().lower()
        filtered_versions = [v[0] for v in self.fabric_versions if search_term in v[0].lower()]
        self.fabric_version_combobox.blockSignals(True)
        self.fabric_version_combobox.clear()
        self.fabric_version_combobox.addItems(filtered_versions)
        self.fabric_version_combobox.blockSignals(False)

    def on_search(self):
        search_term = self.version_combobox.currentText().lower()
        filtered_versions = [version for version in self.versions if search_term in version.lower()]
        self.version_combobox.blockSignals(True)
        self.version_combobox.clear()
        self.version_combobox.addItems(filtered_versions)
        self.version_combobox.blockSignals(False)

    def update_ui(self):
        self.notebook.setTabText(self.notebook.indexOf(self), global_vars.lang.get('tab_svr_dl', 'Server Download'))
        self.major_version_label.setText(global_vars.lang.get('major_version', 'Maj. Version'))
        self.forge_version_label.setText(global_vars.lang.get('specific_version', 'Specific Version:'))
        self.forge_download_button.setText(global_vars.lang.get('download', 'Download'))
        self.fabric_version_label.setText(global_vars.lang.get('fabric_version', 'Fabric Version'))
        self.fabric_download_button.setText(global_vars.lang.get('download', 'Download'))
        self.version_label.setText(global_vars.lang.get('van_version', 'Vanilla Version'))
        self.download_button.setText(global_vars.lang.get('download', 'Download'))

def ServerDL(notebook): return ServerDLUI(notebook)