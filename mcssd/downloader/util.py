import requests
from urllib.parse import urlparse, parse_qs
from bs4 import BeautifulSoup

# 获取Minecraft版本列表
def get_versions():
    response = requests.get('https://launchermeta.mojang.com/mc/game/version_manifest.json')
    response.raise_for_status()
    return [version['id'] for version in response.json()['versions']]

# 获取所有Forge版本号列表
def get_all_versions():
    response = requests.get('https://files.minecraftforge.net/net/minecraftforge/forge/')
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'lxml')
    
    # 找到左侧的版本号列表
    sidebar = soup.find('div', class_='sidebar-left sidebar-sticky')
    if not sidebar:
        raise ValueError("Could not find sidebar")
    
    version_list = []
    
    # 解析所有版本号
    for li in sidebar.find_all('li', class_='li-version-list'):
        version_text = li.find('a', class_='elem-text toggle-collapsible').text.strip()
        sub_versions = li.find_all('a', href=True)
        for sub_version in sub_versions:
            version_list.append(sub_version.text.strip())
    
    return version_list
    
def get_forge_versions(game_version):
    # 构建URL以获取特定游戏版本的Forge版本信息
    url = f'https://files.minecraftforge.net/net/minecraftforge/forge/index_{game_version}.html'
    
    # 发送HTTP GET请求以获取网页内容
    response = requests.get(url)
    response.raise_for_status()  # 如果请求失败，则引发HTTPError异常
    
    # 使用BeautifulSoup解析网页内容
    soup = BeautifulSoup(response.content, 'lxml')
    
    # 查找包含下载信息的容器
    download_container = soup.find('div', class_='download-container')
    if not download_container:
        raise ValueError("Could not find download container")  # 如果找不到下载容器，则引发ValueError异常
    
    # 查找下载列表表格
    download_list = download_container.find('table', class_='download-list')
    if not download_list:
        raise ValueError("Could not find download list")  # 如果找不到下载列表，则引发ValueError异常
    
    versions = []
    
    # 遍历下载列表中的每一行
    for row in download_list.find('tbody').find_all('tr'):
        cols = row.find_all('td')
        if len(cols) > 1:
            # 查找包含下载链接的<a>标签
            a_tags = cols[2].find_all('a')
            for a_tag in a_tags:
                # 查找包含"Installer"的<i>标签
                i_tag = a_tag.find('i', class_='classifier-installer')
                if i_tag and 'Installer' in a_tag.text:
                    href = a_tag['href']
                    parsed_url = urlparse(href)
                    url_param = parse_qs(parsed_url.query).get('url', [None])[0]
                    if url_param:
                        # 提取版本ID并添加到版本列表中
                        version_id = url_param.split('/')[-2]
                        versions.append((version_id, url_param))
    
    return versions

# 获取Fabric版本列表
def get_fabric_versions():
    url = "https://meta.fabricmc.net/v2/versions/installer"
    response = requests.get(url)
    data = response.json()
    versions = [(version['version'], version['maven']) for version in data if 'version' in version and 'maven' in version]
    return versions

# 下载文件
def download_file(url, dest, progress_var):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    with open(dest, 'wb') as file:
        for data in response.iter_content(1024):
            file.write(data)
            progress_var.set(progress_var.get() + len(data) / total_size * 100)

# 获取原版数据
def start_download_Vanilla(version): return f'https://launcher.mojang.com/v1/objects/{version}/server.jar'
# 获取Forge版数据
def start_download_forge(version): return f"https://maven.minecraftforge.net/net/minecraftforge/forge/{version}/forge-{version}-installer.jar"
# 获取Fabric版数据
def start_download_fabric(version): return next((item['url'] for item in requests.get("https://meta.fabricmc.net/v2/versions/installer").json() if item['version'] == version), None)
    
    