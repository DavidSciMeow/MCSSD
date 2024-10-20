from PyQt5 import QtWidgets, QtGui, QtCore
import global_vars
import ui.ui_util as ui_util
import mcssd.downloader.util as util
from urllib.parse import urlparse

class VanillaTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)

        # Major version selection
        self.major_version_combobox = QtWidgets.QComboBox(self)
        self.major_version_combobox.addItem(global_vars.lang.get('select_major_version', 'Select Major Version'))
        self.major_version_combobox.addItems(util.get_versions())
        self.major_version_combobox.setCurrentIndex(0)  # Ensure placeholder text is shown
        self.layout.addWidget(self.major_version_combobox)

        # Download button
        self.download_button = QtWidgets.QPushButton(global_vars.lang.get('download', 'Download'), self)
        self.download_button.clicked.connect(self.start_download)
        self.layout.addWidget(self.download_button)

        # Progress bar
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.progress_bar)

        # Debug info (QListWidget)
        self.debug_info_listwidget = QtWidgets.QListWidget(self)
        self.layout.addWidget(self.debug_info_listwidget)

    def start_download(self):
        major_version = self.major_version_combobox.currentText()
        if major_version == global_vars.lang.get('select_major_version', 'Select Major Version'):
            self.add_debug_info("Please select a major version.")
            return
        
        url = util.start_download_Vanilla(major_version)
        
        # Extract the file name from the URL
        parsed_url = urlparse(url)
        file_name = parsed_url.path.split('/')[-1]
        
        ui_util.file_save(lambda dest: util.download_file(url, dest, self.progress_bar), file_name)
        self.add_debug_info(f"Started download for Vanilla version {major_version}")

    def add_debug_info(self, message):
        self.debug_info_listwidget.addItem(message)

class ForgeTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)

        # Major version selection
        self.major_version_combobox = QtWidgets.QComboBox(self)
        self.major_version_combobox.addItem(global_vars.lang.get('select_major_version', 'Select Major Version'))
        self.major_version_combobox.addItems(util.get_all_forge_majversions())
        self.major_version_combobox.setCurrentIndex(0)  # Ensure placeholder text is shown
        self.major_version_combobox.currentIndexChanged.connect(self.update_specific_versions)
        self.layout.addWidget(self.major_version_combobox)

        # Specific version selection
        self.specific_version_combobox = QtWidgets.QComboBox(self)
        self.specific_version_combobox.addItem(global_vars.lang.get('select_specific_version', 'Select Specific Version'))
        self.specific_version_combobox.setCurrentIndex(0)  # Ensure placeholder text is shown
        self.layout.addWidget(self.specific_version_combobox)

        # Download button
        self.download_button = QtWidgets.QPushButton(global_vars.lang.get('download', 'Download'), self)
        self.download_button.clicked.connect(self.start_download)
        self.layout.addWidget(self.download_button)

        # Progress bar
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.progress_bar)

        # Debug info (QListWidget)
        self.debug_info_listwidget = QtWidgets.QListWidget(self)
        self.layout.addWidget(self.debug_info_listwidget)

    def update_specific_versions(self):
        major_version = self.major_version_combobox.currentText()
        if major_version == global_vars.lang.get('select_major_version', 'Select Major Version'):
            return
        self.specific_versions = [version[0] for version in util.get_forge_versions(major_version)]
        self.specific_version_combobox.clear()
        self.specific_version_combobox.addItem(global_vars.lang.get('select_specific_version', 'Select Specific Version'))
        self.specific_version_combobox.addItems(self.specific_versions)
        self.specific_version_combobox.setCurrentIndex(0)  # Ensure placeholder text is shown

    def start_download(self):
        major_version = self.major_version_combobox.currentText()
        specific_version = self.specific_version_combobox.currentText()
        
        if major_version == global_vars.lang.get('select_major_version', 'Select Major Version'):
            self.add_debug_info("Please select a major version.")
            return
        
        if specific_version == global_vars.lang.get('select_specific_version', 'Select Specific Version'):
            self.add_debug_info("Please select a specific version for Forge.")
            return
        
        url = util.start_download_forge(specific_version)
        
        # Extract the file name from the URL
        parsed_url = urlparse(url)
        file_name = parsed_url.path.split('/')[-1]
        
        ui_util.file_save(lambda dest: util.download_file(url, dest, self.progress_bar), file_name)
        self.add_debug_info(f"Started download for Forge version {specific_version}")

    def add_debug_info(self, message):
        self.debug_info_listwidget.addItem(message)

class FabricTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)

        major_versions, loader_versions, installer_versions = util.get_fabric_versions()

        # Major version selection
        self.major_version_combobox = QtWidgets.QComboBox(self)
        self.major_version_combobox.addItem(global_vars.lang.get('select_major_version', 'Select Major Version'))
        self.major_version_combobox.addItems(major_versions)
        self.major_version_combobox.setCurrentIndex(0)  # Ensure placeholder text is shown
        self.layout.addWidget(self.major_version_combobox)

        # Fabric loader selection
        self.fabric_loader_combobox = QtWidgets.QComboBox(self)
        self.fabric_loader_combobox.addItem(global_vars.lang.get('select_loader_version', 'Select Loader Version'))
        self.fabric_loader_combobox.addItems(loader_versions)
        self.fabric_loader_combobox.setCurrentIndex(0)  # Ensure placeholder text is shown
        self.layout.addWidget(self.fabric_loader_combobox)

        # Fabric installer selection
        self.fabric_installer_combobox = QtWidgets.QComboBox(self)
        self.fabric_installer_combobox.addItem(global_vars.lang.get('select_installer_version', 'Select Installer Version'))
        self.fabric_installer_combobox.addItems(installer_versions)
        self.fabric_installer_combobox.setCurrentIndex(0)  # Ensure placeholder text is shown
        self.layout.addWidget(self.fabric_installer_combobox)

        # Download button
        self.download_button = QtWidgets.QPushButton(global_vars.lang.get('download', 'Download'), self)
        self.download_button.clicked.connect(self.start_download)
        self.layout.addWidget(self.download_button)

        # Progress bar
        self.progress_bar = QtWidgets.QProgressBar(self)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.progress_bar)

        # Debug info (QListWidget)
        self.debug_info_listwidget = QtWidgets.QListWidget(self)
        self.layout.addWidget(self.debug_info_listwidget)

    def start_download(self):
        major_version = self.major_version_combobox.currentText()
        loader_version = self.fabric_loader_combobox.currentText()
        installer_version = self.fabric_installer_combobox.currentText()
        
        if major_version == global_vars.lang.get('select_major_version', 'Select Major Version'):
            self.add_debug_info("Please select a major version.")
            return
        
        if loader_version == global_vars.lang.get('select_loader_version', 'Select Loader Version') or \
           installer_version == global_vars.lang.get('select_installer_version', 'Select Installer Version'):
            self.add_debug_info("Please select valid Fabric loader and installer versions before downloading.")
            return
        
        url = util.start_download_fabric(major_version, loader_version, installer_version)
        
        # Extract the file name from the URL
        parsed_url = urlparse(url)
        file_name = parsed_url.path.split('/')[-1]
        
        ui_util.file_save(lambda dest: util.download_file(url, dest, self.progress_bar), file_name)
        self.add_debug_info(f"Started download for Fabric version {major_version}")

    def add_debug_info(self, message):
        self.debug_info_listwidget.addItem(message)

class ServerDLUI(QtWidgets.QWidget):
    def __init__(self, notebook):
        super().__init__()
        self.notebook = notebook
        self.layout = QtWidgets.QVBoxLayout(self)
        self.notebook.addTab(self, global_vars.lang.get('tab_svr_dl', 'Server Download'))

        # Create tab widget
        self.tabs = QtWidgets.QTabWidget()
        self.layout.addWidget(self.tabs)

        # Add Vanilla tab
        self.vanilla_tab = VanillaTab()
        self.tabs.addTab(self.vanilla_tab, global_vars.lang.get('tab_vanilla', 'Vanilla'))

        # Add Forge tab
        self.forge_tab = ForgeTab()
        self.tabs.addTab(self.forge_tab, global_vars.lang.get('tab_forge', 'Forge'))

        # Add Fabric tab
        self.fabric_tab = FabricTab()
        self.tabs.addTab(self.fabric_tab, global_vars.lang.get('tab_fabric', 'Fabric'))

    def update_ui(self):
        # Update UI elements based on the current language
        self.notebook.setTabText(self.notebook.indexOf(self), global_vars.lang.get('tab_svr_dl', 'Server Download'))
        self.tabs.setTabText(self.tabs.indexOf(self.vanilla_tab), global_vars.lang.get('tab_vanilla', 'Vanilla'))
        self.tabs.setTabText(self.tabs.indexOf(self.forge_tab), global_vars.lang.get('tab_forge', 'Forge'))
        self.tabs.setTabText(self.tabs.indexOf(self.fabric_tab), global_vars.lang.get('tab_fabric', 'Fabric'))