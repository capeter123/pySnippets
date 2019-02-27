### pyinstaller pack .py to exe
```python
pyinstall -F -w exe.py
```

#### 运行方式
```
exe.exe text.txt
```
#### 减小exe文件
```
pyinstaller -F -w --upx-dir upx394w -i icon.ico xxx.py 
```
#### 多进程运行打包
```
pyinstaller -F -w --noconsole --upx-dir upx394w -i icon.ico helperAppTab.py
```