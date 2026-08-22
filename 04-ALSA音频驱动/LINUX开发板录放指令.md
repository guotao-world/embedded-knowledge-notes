# LINUX 开发板录放指令

## 一、录音

```bash
arecord -D hw:0,0 -f S16_LE -r 16000 -c 2 -d 10 record.wav
```

或使用 plughw（自动做格式转换）：

```bash
arecord -D plughw:0,0 -f S16_LE -r 16000 -c 1 -d 10 record.wav
```

## 二、播放

```bash
aplay record.wav
```

## 三、音量调节

```bash
alsamixer
```

## 四、保存音量配置

```bash
alsactl store
```

---

## 五、参数说明

| 参数 | 含义 | 示例 |
|------|------|------|
| `-D` | 指定声卡设备 | `hw:0,0`（card0 device0） |
| `-f` | 采样格式 | `S16_LE`（16bit 小端） |
| `-r` | 采样率 | `16000`（16kHz） |
| `-c` | 声道数 | `2`（双声道） |
| `-d` | 录制时长（秒） | `10`（录 10 秒） |
