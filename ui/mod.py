from tkinter import ttk
import webbrowser
import tkinter as tk
from mcssd.mod.modutil import search_mods, get_mod_details, MCVersion

category_dict = {"全部": 0, "科技": 1, "魔法": 2, "冒险": 3, "农业": 4, "装饰": 5, "实用": 6, "辅助": 7, "魔改": 8, "lib": 9, "资源": 10, "世界": 11, "群系": 12, "结构": 13, "生物": 14, "能源": 15, "存储": 16, "物流": 17, "道具": 18, "安全": 19, "红石": 20, "食物": 21, "模型": 22, "关卡": 23, "指南": 24, "破坏": 25, "Meme": 26, "中式": 27, "日式": 28, "西式": 29, "恐怖": 30, "建材": 31, "生存": 32, "指令": 33, "优化": 34, "国创": 35}
mode_dict = {"全部": 0, "仅客户端": 1, "仅服务端": 2, "主客户端": 3, "主服务端": 4, "皆需安装": 5}
platform_dict = {"全部": 0, "Java版本": 1, "Bedrock版本": 2}
api_dict = {"全部": 0, "forge": 1, "fabric": 2, "quilt": 3, "neoforge": 4, "rift": 5, "liteloader": 6, "数据包": 7, "行为包": 8, "命令方块": 9, "文件覆盖": 10}
status_dict = {"全部": 0, "活跃": 1, "半弃坑": 2, "停更": 3}
sort_dict = {"全部": 0, "按收录时间": 1, "按最后编辑时间": 2}

def cp_mod_search(notebook):
    # 创建Mod搜索页面
    frame_mod_search = ttk.Frame(notebook)
    notebook.add(frame_mod_search, text="Mod Search")

    frame_mod_search_inner = ttk.Frame(frame_mod_search)
    frame_mod_search_inner.pack(pady=2, fill='x', expand=True)

    # 搜索框
    search_frame = tk.Frame(frame_mod_search_inner)
    search_frame.grid(row=0, column=0, sticky='w')

    tk.Label(search_frame, text="Keyword:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    keyword_entry = tk.Entry(search_frame, width=20)
    keyword_entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

    fuzzy_var = tk.BooleanVar()
    fuzzy_check = tk.Checkbutton(search_frame, text="Fuzzy Search", variable=fuzzy_var)
    fuzzy_check.grid(row=0, column=2, padx=5, pady=5, sticky='w')

    tk.Label(search_frame, text="MC Version:").grid(row=0, column=3, padx=5, pady=5, sticky='w')
    mcver_entry = tk.Entry(search_frame, width=10)
    mcver_entry.grid(row=0, column=4, padx=5, pady=5, sticky='w')

    # Search Button
    search_button = tk.Button(search_frame, text="Search", command=lambda: search_mod())
    search_button.grid(row=0, column=5, padx=5, pady=5, sticky='w')

    # 下拉框
    dropdown_frame = tk.Frame(frame_mod_search_inner)
    dropdown_frame.grid(row=0, column=1, sticky='w')

    tk.Label(dropdown_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
    category_menu = ttk.Combobox(dropdown_frame, values=list(category_dict.keys()), width=10)
    category_menu.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    category_menu.set("全部")

    tk.Label(dropdown_frame, text="Mode:").grid(row=0, column=2, padx=5, pady=5, sticky='w')
    mode_menu = ttk.Combobox(dropdown_frame, values=list(mode_dict.keys()), width=10)
    mode_menu.grid(row=0, column=3, padx=5, pady=5, sticky='w')
    mode_menu.set("全部") 

    tk.Label(dropdown_frame, text="Platform:").grid(row=0, column=4, padx=5, pady=5, sticky='w')
    platform_menu = ttk.Combobox(dropdown_frame, values=list(platform_dict.keys()), width=10)
    platform_menu.grid(row=0, column=5, padx=5, pady=5, sticky='w')
    platform_menu.set("全部")

    tk.Label(dropdown_frame, text="API:").grid(row=0, column=6, padx=5, pady=5, sticky='w')
    api_menu = ttk.Combobox(dropdown_frame, values=list(api_dict.keys()), width=10)
    api_menu.grid(row=0, column=7, padx=5, pady=5, sticky='w')
    api_menu.set("全部")

    tk.Label(dropdown_frame, text="Status:").grid(row=0, column=8, padx=5, pady=5, sticky='w')
    status_menu = ttk.Combobox(dropdown_frame, values=list(status_dict.keys()), width=10)
    status_menu.grid(row=0, column=9, padx=5, pady=5, sticky='w')
    status_menu.set("全部")

    tk.Label(dropdown_frame, text="Sort:").grid(row=0, column=10, padx=5, pady=5, sticky='w')
    sort_menu = ttk.Combobox(dropdown_frame, values=list(sort_dict.keys()), width=10)
    sort_menu.grid(row=0, column=11, padx=5, pady=5, sticky='w')
    sort_menu.set("全部")



    def search_mod():
        keyword = keyword_entry.get()
        fuzzy = fuzzy_var.get()
        category = category_menu.get()
        mode = mode_menu.get()
        platform = platform_menu.get()
        mcver_str = mcver_entry.get()
        mcver = MCVersion(mcver_str) if mcver_str else None
        api = api_menu.get()
        status = status_menu.get()
        sort = sort_menu.get()

        # 检查下拉列表是否选择了有效的选项
        if category not in category_dict:
            print("Please select a valid category.")
            return
        if mode not in mode_dict:
            print("Please select a valid mode.")
            return
        if platform not in platform_dict:
            print("Please select a valid platform.")
            return
        if api not in api_dict:
            print("Please select a valid API.")
            return
        if status not in status_dict:
            print("Please select a valid status.")
            return
        if sort not in sort_dict:
            print("Please select a valid sort option.")
            return

        search_results = search_mods(keyword, fuzzy, category_dict[category], mode_dict[mode], platform_dict[platform], mcver, api_dict[api], status_dict[status], sort_dict[sort])
        
        search_results_listbox.delete(0, tk.END)
        for mod in search_results['mods']:
            mod_name = f"{mod.get('name')} - {mod.get('ename')}"
            mod_id = mod.get('id')
            search_results_listbox.insert(tk.END, (mod_name, mod_id))

        search_results_listbox.bind('<<ListboxSelect>>', lambda e: display_mod_details(search_results_listbox.get(search_results_listbox.curselection())[1]))

    def display_mod_details(mod_id):
        mod_details = get_mod_details(mod_id)
        mod_id_label.config(text=f"Mod ID: {mod_details['modid']}")
        
        for widget in mod_versions_frame.winfo_children():
            widget.destroy()
        for widget in mod_relations_frame.winfo_children():
            widget.destroy()

        for method in mod_details['operation_method']:
            label = tk.Label(mod_versions_frame, text=method['type'])
            label.pack(anchor='w')
            combobox = ttk.Combobox(mod_versions_frame, values=method['versions'], state='readonly')
            combobox.pack(anchor='w', fill='x')

        # 清除现有的控件
        for widget in mod_versions_frame.winfo_children():
            widget.destroy()
        for widget in mod_relations_frame.winfo_children():
            widget.destroy()

        # 填充操作方法
        for method in mod_details['operation_method']:
            label = tk.Label(mod_versions_frame, text=method['type'])
            label.pack(anchor='w')
            combobox = ttk.Combobox(mod_versions_frame, values=method['versions'], state='readonly')
            combobox.pack(anchor='w', fill='x')

        # 解析mod_relations数据
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

        # 将数据转换为所需的格式
        dependency_list = [f"{mod} - {', '.join(types)}" for mod, types in dependency_dict.items()]
        expansion_list = [f"{mod} - {', '.join(types)}" for mod, types in expansion_dict.items()]

        # 创建下拉框
        dependency_label = tk.Label(mod_relations_frame, text="dependency:")
        dependency_label.pack(anchor='w', padx=5, pady=5)
        dependency_combobox = ttk.Combobox(mod_relations_frame, values=dependency_list, width=50, state='readonly')
        dependency_combobox.pack(anchor='w', padx=5, pady=5, fill='x')

        expansion_label = tk.Label(mod_relations_frame, text="expansion:")
        expansion_label.pack(anchor='w', padx=5, pady=5)
        expansion_combobox = ttk.Combobox(mod_relations_frame, values=expansion_list, width=50, state='readonly')
        expansion_combobox.pack(anchor='w', padx=5, pady=5, fill='x')



        # for relation in mod_details['mod_relations']:
        #     label = tk.Label(mod_relations_frame, text=relation['type'])
        #     label.pack(anchor='w')
        #     for rel in relation['relations']:
        #         desc_label = tk.Label(mod_relations_frame, text=rel['description'])
        #         desc_label.pack(anchor='w')
        #         combobox = ttk.Combobox(mod_relations_frame, values=rel['mods'], state='readonly')
        #         combobox.pack(anchor='w', fill='x')

        download_url = mod_details['download_url']
        if download_url and download_url.startswith("/download/"):
            download_url = "https://www.mcmod.cn" + download_url
        mod_download_label.config(text=f"Download Links: {download_url}")

    # 搜索结果和详细信息展示框
    results_frame = tk.Frame(frame_mod_search)
    results_frame.pack(pady=2, padx=10, fill='both', expand=True)

    search_results_frame = tk.Frame(results_frame)
    search_results_frame.pack(side='left', fill='both', expand=True, padx=10)

    search_results_listbox = tk.Listbox(search_results_frame)
    search_results_listbox.pack(fill='both', expand=True)

    mod_details_frame = tk.Frame(results_frame)
    mod_details_frame.pack(side='right', fill='both', expand=True, padx=10)

    mod_id_label = tk.Label(mod_details_frame, text="Mod ID:")
    mod_id_label.pack(anchor='w')

    mod_download_label = tk.Label(mod_details_frame, text="Download Links:")
    mod_download_label.pack(anchor='w')
    mod_download_label.bind("<Button-1>", lambda e: webbrowser.open_new(mod_download_label.cget("text").split(": ")[1]) if mod_download_label.cget("text").split(": ")[1].startswith("http") else None)

    mod_versions_label = tk.Label(mod_details_frame, text="Available Versions:")
    mod_versions_label.pack(anchor='w')
    mod_versions_frame = tk.Frame(mod_details_frame)
    mod_versions_frame.pack(anchor='w', fill='x')

    mod_relations_label = tk.Label(mod_details_frame, text="Mod Relations:")
    mod_relations_label.pack(anchor='w')
    mod_relations_frame = tk.Frame(mod_details_frame)
    mod_relations_frame.pack(anchor='w', fill='x')

    