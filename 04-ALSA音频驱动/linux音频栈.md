# Linux 音频栈

## 一、整体架构

```
用户态
  │
  ├── alsa-lib
  │
内核态
  │
  ├── ALSA Core
  │   ├── PCM Core
  │   ├── Control Core
  │   ├── Timer Core
  │   ├── RawMIDI
  │   └── HWDep
  │
  ├── ASoC Core
  │   ├── soc-core
  │   ├── soc-pcm
  │   ├── DAPM
  │   └── DAI
  │
  ├── CPU DAI driver
  ├── Codec driver
  └── Machine driver
```

---

## 二、核心文件

| 文件 | 作用 |
|------|------|
| `sound/core/sound.c` | `alsa_sound_init`，ALSA 核心初始化入口 |
