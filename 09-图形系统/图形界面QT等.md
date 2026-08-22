# 图形界面 QT 等

## 一、桌面环境与显示服务器

Qt 应用（以及整个桌面环境）都需要运行在显示服务器之上，而显示服务器是内核之上的第一个图形环节。

![图形系统架构](../images/image15.png)

![显示服务器与应用](../images/image16.png)

---

## 二、架构层次

```
应用层（Qt / GTK / 其他 GUI）
    ↓
显示服务器（X Server / Wayland Compositor）
    ↓
DRM / KMS（内核图形子系统）
    ↓
显示硬件（LCD / HDMI / MIPI-DSI）
```
