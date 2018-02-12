# CompressedImage

### 利用TinyPNG自动压缩图片

#### 原因
在App开发过程中会在项目中添加图片，假如把UI设计师的图片(未压缩)直接放到工程中，会增加包的大小。在开发过程中不能保证每一个开发者在添加图片时都经压缩处理。基于此原因我们可以通过git log来获取提交记录再过滤出Add、Modify的图片，进行压缩。

#### 如何使用

1.首先利用邮箱申请TinyPNG的key ，但是免费压缩图片数为500张  [TinyPNG](https://tinypng.com/developers);

2.把startCompress.py、compressPng.py、startDate.txt三个文件放到工程目录下;

3.cd 到工程目录下
执行如下命令即可

```python
python startCompress.py
```
备注:startCompress.py 是入口脚本，compressPng.py 真正的压缩脚本(包含过滤git提交记录) startDate.txt 记录压缩时间的文件。

#### 适用平台

iOS & Android


