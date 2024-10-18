# MC_Server_Downloader
随便写的，练手的python项目，目标是下载原版/forge/fabric的服务器端

目前只是把服务端下载下来，自己运行java -jar然后服务端就能启动了

build使用如下指令：`pyinstaller --onefile --noconsole main.py`

FileStruct
|--lang (UI的语言文件)
|
|--mcssd (主要过程文件)
|....|--mod (模组搜索过程文件)
|....|--procedure (服务端下载过程文件)
|
|--ui (主程序的UI设计)
|....|-- **所有的UI设计**
|
|
|--main.py (主窗体)
|--mod_dl.py (模组下载链接搜索器 * 命令行)
|--mod_search.py (模组搜索器 * 命令行)


命令行的内部自己有帮助，使用`-h`或者`--help`就可以查看了
