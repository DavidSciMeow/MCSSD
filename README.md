# MC_Server_Downloader
随便写的，练手的python项目，目标是下载原版/forge/fabric的服务器端
目前只是把服务端下载下来，自己运行java -jar然后服务端就能启动了

## 之后可能加点自动配置什么的，目前先写这么多
build使用如下指令：`pyinstaller --onefile --noconsole mc_dl.py`

目前打包了一份console的模组搜索器，仅支持搜索，会展示下载链接，在dist/mod_search.exe，linux用户可以自己打包modsearch.py即可。    
内部自己有帮助，使用-h --help就可以查看了
