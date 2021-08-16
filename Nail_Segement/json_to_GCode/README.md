使用说明：
1. 相机拍下手指照片
2. 使用**精灵标注**手动标记指甲区域
3. 将标记好的照片导出成json
4. 使用该文件将json数据转换成G代码，空白json不会被处理
  在命令行输入
  ‘python json2GCode.py ouputs'
  其中，json2GCode.py为该文件在本地路径，outputs为json所在文件夹的本地路径
5. G代码会生成在outputs中新生成的文件夹GCode。
