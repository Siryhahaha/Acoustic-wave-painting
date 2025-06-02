### T01

完成了np数组写入bin文件

#### 核心代码

写入代码

```python
    x.astype(np.float32).tofile('S1.bin')   #写入
```

读取代码

```python
    recovered_x = np.fromfile('S1.bin', dtype=np.float32)   #读取
```

stem是火柴，plot是连续

#### 想法

应该写一个简单的ui，统一输入范围，然后按键继续。

### T02

完成了wav文件写入bin文件

了解了简单wav音频知识

#### 核心代码

音频读取和保存，其中data是np数组，可以直接像T01一样写入bin

```
    rate, data = wav.read(wav_path)#采样率和数据
```



#### 简单wav知识

声道：体现在载入np数组的第二层是1还是2，可以通过`data = data[:, 0]`转化为单声道

采样率：可分析的最高频率，一般是44.1khz

其他：位深16bit

#### 问题

没有显示频率（但我也不会）

#### 想法

下一步试试导入🐎的代码

### T03

#### 核心代码

#### 简单wav知识

#### 问题

#### 想法