# linux音频栈

用户态

│

├── alsa-lib

│

内核态

│

├── ALSA Core

│ ├── PCM Core

│ ├── Control Core

│ ├── Timer Core

│ ├── RawMIDI

│ └── HWDep

│

├── ASoC Core

│ ├── soc-core

│ ├── soc-pcm

│ ├── DAPM

│ └── DAI

│

├── CPU DAI driver

├── Codec driver

└── Machine driver

**核心文件：**

sound/core/sound.c ： alsa_sound_init