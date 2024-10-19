from PyQt5 import QtWidgets, QtCore
import webbrowser
from mcssd.mod.modutil import search_mods, get_mod_details, MCVersion

category_dict = {"全部": 0, "科技": 1, "魔法": 2, "冒险": 3, "农业": 4, "装饰": 5, "实用": 6, "辅助": 7, "魔改": 8, "lib": 9, "资源": 10, "世界": 11, "群系": 12, "结构": 13, "生物": 14, "能源": 15, "存储": 16, "物流": 17, "道具": 18, "安全": 19, "红石": 20, "食物": 21, "模型": 22, "关卡": 23, "指南": 24, "破坏": 25, "Meme": 26, "中式": 27, "日式": 28, "西式": 29, "恐怖": 30, "建材": 31, "生存": 32, "指令": 33, "优化": 34, "国创": 35}
mode_dict = {"全部": 0, "仅客户端": 1, "仅服务端": 2, "主客户端": 3, "主服务端": 4, "皆需安装": 5}
platform_dict = {"全部": 0, "Java版本": 1, "Bedrock版本": 2}
api_dict = {"全部": 0, "forge": 1, "fabric": 2, "quilt": 3, "neoforge": 4, "rift": 5, "liteloader": 6, "数据包": 7, "行为包": 8, "命令方块": 9, "文件覆盖": 10}
status_dict = {"全部": 0, "活跃": 1, "半弃坑": 2, "停更": 3}
sort_dict = {"全部": 0, "按收录时间": 1, "按最后编辑时间": 2}

class ModSearchTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)

        search_frame = QtWidgets.QWidget()
        search_layout = QtWidgets.QGridLayout(search_frame)

        search_layout.addWidget(QtWidgets.QLabel("Keyword:"), 0, 0)
        self.keyword_entry = QtWidgets.QLineEdit()
        search_layout.addWidget(self.keyword_entry, 0, 1)

        self.fuzzy_check = QtWidgets.QCheckBox("Fuzzy Search")
        search_layout.addWidget(self.fuzzy_check, 0, 2)

        search_layout.addWidget(QtWidgets.QLabel("MC Version:"), 0, 3)
        self.mcver_entry = QtWidgets.QLineEdit()
        search_layout.addWidget(self.mcver_entry, 0, 4)

        search_button = QtWidgets.QPushButton("Search")
        search_button.clicked.connect(self.search_mod)
        search_layout.addWidget(search_button, 0, 5)

        layout.addWidget(search_frame)

        dropdown_frame = QtWidgets.QWidget()
        dropdown_layout = QtWidgets.QGridLayout(dropdown_frame)

        dropdown_layout.addWidget(QtWidgets.QLabel("Category:"), 0, 0)
        self.category_menu = QtWidgets.QComboBox()
        self.category_menu.addItems(category_dict.keys())
        dropdown_layout.addWidget(self.category_menu, 0, 1)

        dropdown_layout.addWidget(QtWidgets.QLabel("Mode:"), 0, 2)
        self.mode_menu = QtWidgets.QComboBox()
        self.mode_menu.addItems(mode_dict.keys())
        dropdown_layout.addWidget(self.mode_menu, 0, 3)

        dropdown_layout.addWidget(QtWidgets.QLabel("Platform:"), 0, 4)
        self.platform_menu = QtWidgets.QComboBox()
        self.platform_menu.addItems(platform_dict.keys())
        dropdown_layout.addWidget(self.platform_menu, 0, 5)

        dropdown_layout.addWidget(QtWidgets.QLabel("API:"), 0, 6)
        self.api_menu = QtWidgets.QComboBox()
        self.api_menu.addItems(api_dict.keys())
        dropdown_layout.addWidget(self.api_menu, 0, 7)

        dropdown_layout.addWidget(QtWidgets.QLabel("Status:"), 0, 8)
        self.status_menu = QtWidgets.QComboBox()
        self.status_menu.addItems(status_dict.keys())
        dropdown_layout.addWidget(self.status_menu, 0, 9)

        dropdown_layout.addWidget(QtWidgets.QLabel("Sort:"), 0, 10)
        self.sort_menu = QtWidgets.QComboBox()
        self.sort_menu.addItems(sort_dict.keys())
        dropdown_layout.addWidget(self.sort_menu, 0, 11)

        layout.addWidget(dropdown_frame)

        results_frame = QtWidgets.QWidget()
        results_layout = QtWidgets.QHBoxLayout(results_frame)

        self.search_results_listbox = QtWidgets.QListWidget()
        self.search_results_listbox.itemSelectionChanged.connect(self.display_mod_details)
        results_layout.addWidget(self.search_results_listbox)

        self.mod_details_frame = QtWidgets.QWidget()
        self.mod_details_layout = QtWidgets.QVBoxLayout(self.mod_details_frame)
        results_layout.addWidget(self.mod_details_frame)

        layout.addWidget(results_frame)

    def search_mod(self):
        keyword = self.keyword_entry.text()
        fuzzy = self.fuzzy_check.isChecked()
        category = self.category_menu.currentText()
        mode = self.mode_menu.currentText()
        platform = self.platform_menu.currentText()
        mcver_str = self.mcver_entry.text()
        mcver = MCVersion(mcver_str) if mcver_str else None
        api = self.api_menu.currentText()
        status = self.status_menu.currentText()
        sort = self.sort_menu.currentText()

        search_results = search_mods(keyword, fuzzy, category_dict[category], mode_dict[mode], platform_dict[platform], mcver, api_dict[api], status_dict[status], sort_dict[sort])

        self.search_results_listbox.clear()
        for mod in search_results['mods']:
            mod_name = f"{mod.get('name')} - {mod.get('ename')}"
            mod_id = mod.get('id')
            item = QtWidgets.QListWidgetItem(mod_name)
            item.setData(QtCore.Qt.UserRole, mod_id)
            self.search_results_listbox.addItem(item)

    def display_mod_details(self):
        selected_items = self.search_results_listbox.selectedItems()
        if not selected_items:
            return

        mod_id = selected_items[0].data(QtCore.Qt.UserRole)

        for i in reversed(range(self.mod_details_layout.count())):
            widget = self.mod_details_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        mod_details = get_mod_details(mod_id)

        mod_id_label = QtWidgets.QLabel(f"Mod ID: {mod_details['modid']}")
        self.mod_details_layout.addWidget(mod_id_label)

        mod_versions_label = QtWidgets.QLabel("Available Versions:")
        self.mod_details_layout.addWidget(mod_versions_label)

        mod_versions_list = QtWidgets.QListWidget()
        version_dict = {}
        for method in mod_details['operation_method']:
            for version in method['versions']:
                if version in version_dict:
                    version_dict[version].append(method['type'])
                else:
                    version_dict[version] = [method['type']]

        for version, types in version_dict.items():
            types_str = ', '.join(types).replace(":", "")
            mod_versions_list.addItem(f"{version} - {types_str}")
        mod_versions_list.setDisabled(True)
        self.mod_details_layout.addWidget(mod_versions_list)

        mod_relations_label = QtWidgets.QLabel("Mod Relations:")
        self.mod_details_layout.addWidget(mod_relations_label)

        mod_relations_frame = QtWidgets.QWidget()
        mod_relations_layout = QtWidgets.QVBoxLayout(mod_relations_frame)
        self.mod_details_layout.addWidget(mod_relations_frame)

        dependency_dict = {}
        expansion_dict = {}
        for relation in mod_details['mod_relations']:
            mod_type = relation["type"]
            for rel in relation["relations"]:
                description = rel["description"]
                if "依赖" in description:
                    for mod in rel["mods"]:
                        if mod in dependency_dict:
                            dependency_dict[mod].append(mod_type)
                        else:
                            dependency_dict[mod] = [mod_type]
                else:
                    for mod in rel["mods"]:
                        if mod in expansion_dict:
                            expansion_dict[mod].append(mod_type)
                        else:
                            expansion_dict[mod] = [mod_type]

        dependency_list = [f"{mod} - {', '.join(types)}" for mod, types in dependency_dict.items()]
        expansion_list = [f"{mod} - {', '.join(types)}" for mod, types in expansion_dict.items()]

        dependency_combobox = QtWidgets.QComboBox()
        dependency_combobox.addItems(dependency_list)
        dependency_combobox.setCurrentText("Dependency")
        mod_relations_layout.addWidget(dependency_combobox)

        expansion_combobox = QtWidgets.QComboBox()
        expansion_combobox.addItems(expansion_list)
        expansion_combobox.setCurrentText("Expansion")
        mod_relations_layout.addWidget(expansion_combobox)

        related_links = mod_details.get('related_links', [])
        download_url = mod_details['download_url']
        if download_url and download_url.startswith("/download/"):
            download_url = "https://www.mcmod.cn" + download_url
            related_links.append({'name': 'Download', 'url': download_url})

        related_links_values = [link['name'] for link in related_links]
        related_links_combobox = QtWidgets.QComboBox()
        related_links_combobox.addItems(related_links_values)
        related_links_combobox.setCurrentText("Download Links")
        related_links_combobox.activated.connect(lambda: self.open_related_link(related_links, related_links_combobox.currentText()))
        self.mod_details_layout.addWidget(related_links_combobox)

    def open_related_link(self, related_links, selected_name):
        for link in related_links:
            if link['name'] == selected_name:
                selected_url = f"https://{link['url'].lstrip('//')}"
                webbrowser.open_new(selected_url)
                break