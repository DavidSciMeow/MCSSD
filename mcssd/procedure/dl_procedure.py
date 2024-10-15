from tkinter import ttk, filedialog, messagebox
import requests
import threading
from urllib.parse import urlparse, parse_qs
import logging
import mcssd.util as util


# 获取原版数据
def start_download_Vanilla(version, progress_var):
    '''
    start_download_Vanilla(version, progress_var) -> None\n\n
    Download the vanilla server jar file.\n\n
    version: The version of the server jar file.\n
    progress_var: The progress bar variable.
    '''
    url = f'https://launcher.mojang.com/v1/objects/{version}/server.jar'
    parsed_url = urlparse(url)
    file_name = parsed_url.path.split('/')[-1]
    return (url, file_name, progress_var)

# 获取Forge版数据
def start_download_forge(version, progress_var):
    '''
    start_download_forge(version, progress_var) -> None\n\n
    Download the forge server jar file.\n\n
    version: The version of the server jar file.\n
    progress_var: The progress bar variable.
    '''
    url = version[1]
    parsed_url = urlparse(url)
    file_name = parsed_url.path.split('/')[-1]
    return (url, file_name, progress_var)

# 获取Fabric版数据
def start_download_fabric(fabric_version, maven, progress_var):
    '''
    start_download_fabric(fabric_version, maven, progress_var) -> None\n\n
    Download the fabric server jar file.\n\n
    fabric_version: The version of the server jar file.\n
    maven: The maven link.\n
    progress_var: The progress bar variable.
    '''
    installer_url = "https://meta.fabricmc.net/v2/versions/installer"
    response = requests.get(installer_url)
    installer_data = response.json()
    url = installer_data[0]['url']
    file_name = urlparse(url).path.split('/')[-1]
    return (url, file_name, progress_var)