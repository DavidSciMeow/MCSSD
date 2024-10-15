import requests
from bs4 import BeautifulSoup
import re
from enum import Enum

class MCVersion(Enum):
    VERSION_1_21_X = "1.21.x"
    VERSION_1_21_1 = "1.21.1"
    VERSION_1_21 = "1.21"
    VERSION_1_20_X = "1.20.x"
    VERSION_1_20_6 = "1.20.6"
    VERSION_1_20_5 = "1.20.5"
    VERSION_1_20_4 = "1.20.4"
    VERSION_1_20_3 = "1.20.3"
    VERSION_1_20_2 = "1.20.2"
    VERSION_1_20_1 = "1.20.1"
    VERSION_1_20 = "1.20"
    VERSION_1_19_X = "1.19.x"
    VERSION_1_19_4 = "1.19.4"
    VERSION_1_19_3 = "1.19.3"
    VERSION_1_19_2 = "1.19.2"
    VERSION_1_19_1 = "1.19.1"
    VERSION_1_19 = "1.19"
    VERSION_1_18_X = "1.18.x"
    VERSION_1_18_2 = "1.18.2"
    VERSION_1_18_1 = "1.18.1"
    VERSION_1_18 = "1.18"
    VERSION_1_17_X = "1.17.x"
    VERSION_1_17_1 = "1.17.1"
    VERSION_1_17 = "1.17"
    VERSION_1_16_X = "1.16.x"
    VERSION_1_16_5 = "1.16.5"
    VERSION_1_16_4 = "1.16.4"
    VERSION_1_16_3 = "1.16.3"
    VERSION_1_16_2 = "1.16.2"
    VERSION_1_16_1 = "1.16.1"
    VERSION_1_16 = "1.16"
    VERSION_1_15_X = "1.15.x"
    VERSION_1_15_2 = "1.15.2"
    VERSION_1_15_1 = "1.15.1"
    VERSION_1_15 = "1.15"
    VERSION_1_14_X = "1.14.x"
    VERSION_1_14_4 = "1.14.4"
    VERSION_1_14_3 = "1.14.3"
    VERSION_1_14_2 = "1.14.2"
    VERSION_1_14_1 = "1.14.1"
    VERSION_1_14 = "1.14"
    VERSION_1_13_X = "1.13.x"
    VERSION_1_13_2 = "1.13.2"
    VERSION_1_13_1 = "1.13.1"
    VERSION_1_13 = "1.13"
    VERSION_1_12_X = "1.12.x"
    VERSION_1_12_2 = "1.12.2"
    VERSION_1_12_1 = "1.12.1"
    VERSION_1_12 = "1.12"
    VERSION_1_11_X = "1.11.x"
    VERSION_1_11_2 = "1.11.2"
    VERSION_1_11_1 = "1.11.1"
    VERSION_1_11 = "1.11"
    VERSION_1_10_X = "1.10.x"
    VERSION_1_10_2 = "1.10.2"
    VERSION_1_10_1 = "1.10.1"
    VERSION_1_10 = "1.10"
    VERSION_1_9_X = "1.9.x"
    VERSION_1_9_4 = "1.9.4"
    VERSION_1_9 = "1.9"
    VERSION_1_8_X = "1.8.x"
    VERSION_1_8_9 = "1.8.9"
    VERSION_1_8_8 = "1.8.8"
    VERSION_1_8 = "1.8"
    VERSION_1_7_X = "1.7.x"
    VERSION_1_7_10 = "1.7.10"
    VERSION_1_7_9 = "1.7.9"
    VERSION_1_7_8 = "1.7.8"
    VERSION_1_7_5 = "1.7.5"
    VERSION_1_7_4 = "1.7.4"
    VERSION_1_7_2 = "1.7.2"
    VERSION_1_6_X = "1.6.x"
    VERSION_1_6_4 = "1.6.4"
    VERSION_1_6_2 = "1.6.2"
    VERSION_1_5_X = "1.5.x"
    VERSION_1_5_2 = "1.5.2"
    VERSION_1_4_X = "1.4.x"
    VERSION_1_4_7 = "1.4.7"
    VERSION_1_4_3 = "1.4.3"
    VERSION_1_4_2 = "1.4.2"
    VERSION_1_3_X = "1.3.x"
    VERSION_1_3_2 = "1.3.2"
    VERSION_1_2_X = "1.2.x"
    VERSION_1_2_5 = "1.2.5"
    EARLIER = "earlier"

def search_mods(keyword=None, fuzzy=False, category=0, mode=0, platform=0, mcver=None, api=0, status=0, sort=0):
    """
    搜索Minecraft模组。

    参数:
    keyword (str): 搜索关键词, 可空。
    fuzzy (bool): 是否进行模糊匹配。默认值为False。
    category (int): 搜索类别。默认值为0, 不添加类别参数。
        1: 科技, 2: 魔法, 3: 冒险, 4: 农业, 5: 装饰, 6: 实用, 7: 辅助, 8: 魔改, 9: lib, 10: 资源,
        11: 世界, 12: 群系, 13: 结构, 14: 生物, 15: 能源, 16: 存储, 17: 物流, 18: 道具, 19: 安全,
        20: 红石, 21: 食物, 22: 模型, 23: 关卡, 24: 指南, 25: 破坏, 26: Meme, 27: 中式, 28: 日式,
        29: 西式, 30: 恐怖, 31: 建材, 32: 生存, 33: 指令, 34: 优化, 35: 国创
    mode (int): 搜索模式。默认值为0, 不添加模式参数。
        1: 仅客户端, 2: 仅服务端, 3: 主客户端, 4: 主服务端, 5: 皆需安装
    platform (int): 平台。默认值为0, 不添加平台参数。
        1: Java版本, 2: Bedrock版本
    mcver (MCVersion): Minecraft版本。默认值为None, 不添加版本参数。
    api (int): API类型。默认值为0, 不添加API参数。
        1: forge, 2: fabric, 3: quilt, 4: neoforge, 5: rift, 6: liteloader, 7: 数据包, 8: 行为包, 9: 命令方块, 10: 文件覆盖
    status (int): 状态。默认值为0, 不添加状态参数。
        1: 活跃, 2: 半弃坑, 3: 停更
    sort (int): 排序方式。默认值为0, 不添加排序参数。
        1: 按收录时间, 2: 按最后编辑时间

    返回:
    dict: 包含模组详情、当前页数、总页数和总条目数的字典。
    """
    base_url = "https://www.mcmod.cn"
    search_url = f"{base_url}/modlist.html"

    params = []
    if keyword:
        params.append(f"key={keyword}")
    if fuzzy:
        params.append("nlp=ngram")
    if category != 0:
        params.append(f"category={category}")
    if mode != 0:
        params.append(f"mode={mode}")
    if platform != 0:
        params.append(f"platform={platform}")
    if mcver is not None:
        params.append(f"mcver={mcver.value}")
    if api != 0:
        params.append(f"api={api}")
    if status != 0:
        params.append(f"status={status}")
    if sort == 1:
        params.append("sort=createtime")
    elif sort == 2:
        params.append("sort=lastedittime")

    if params:
        search_url += "?" + "&".join(params)
    
    response = requests.get(search_url)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 提取模组列表
    mod_list_frame = soup.find('div', class_='modlist-list-frame')
    if not mod_list_frame:
        print("No mods found")
        return
    
    mods = mod_list_frame.find_all('div', class_='modlist-block')
    mod_details = []
    for mod in mods:
        if 'modlist-ad' in mod.get('class', []) or 'modlist-pages-block' in mod.get('class', []):
            continue
            
        title_div = mod.find('div', class_='title')
        name = title_div.find('p', class_='name').text.strip()
        ename = title_div.find('p', class_='ename').text.strip()
        
        cover_div = mod.find('div', class_='cover')
        url = base_url + cover_div.find('a')['href']
        
        # 提取URL中的数字部分
        match = re.search(r'/(\d+)\.html', url)
        if match:
            id = match.group(1)
        else:
            id = None
        
        mod_details.append({
            'name': name,
            'ename': ename,
            'url': url,
            'id': id
        })
    
    # 提取页数信息
    try:
        pages_block = soup.find('div', class_='modlist-pages-block')
        pages_text = pages_block.find('ul').text.strip()
        # 解析页数信息
        match = re.search(r'当前 (\d+) / (\d+) 页，共计 (\d+) 条。', pages_text)
        if match:
            current_page = int(match.group(1))
            total_pages = int(match.group(2))
            total_items = int(match.group(3))
        else:
            current_page = 1
            total_pages = 1
            total_items = len(mod_details)
    except AttributeError:
        current_page = 1
        total_pages = 1
        total_items = len(mod_details)
    
    return {
        'mods': mod_details,
        'current_page': current_page,
        'total_pages': total_pages,
        'total_items': total_items
    }