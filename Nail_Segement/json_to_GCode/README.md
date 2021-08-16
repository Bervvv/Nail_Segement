使用说明：
## json2GCode_terminal
1. 相机拍下手指照片
2. 使用**精灵标注**手动标记指甲区域
3. 将标记好的照片导出成json
4. 使用该文件将json数据转换成G代码，空白json不会被处理.在命令行输入
  ```
  python json2GCode.py ouputs
  ```
  其中，json2GCode.py为该文件在本地路径，outputs为json所在文件夹的本地路径

5. G代码会生成在outputs中新生成的文件夹GCode。

## json2GCode_ide
方法同上。使用时，用IDE打开，拉到最后，替换PATH为json所在文件夹的本地路径。
```
args = r'PATH'
```

## 后记
在**transform**方法中更改**factor**即可改变输出的x，y比值。
