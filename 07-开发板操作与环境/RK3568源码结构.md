# RK3568 源码结构

## GPU / DRM 驱动目录

```
drivers/
└── gpu/
    └── drm/
        ├── drm_core.c
        ├── drm_ioctl.c
        ├── drm_plane.c
        ├── drm_crtc.c
        │
        └── rockchip/
            ├── rockchip_drm_drv.c
            ├── rockchip_vop.c
            ├── dw-mipi-dsi.c
            └── dw-hdmi.c
```

---

## 关键文件说明

| 文件 | 作用 |
|------|------|
| `drm_core.c` | DRM 核心框架 |
| `drm_ioctl.c` | DRM ioctl 接口 |
| `drm_plane.c` | 平面（Plane）管理 |
| `drm_crtc.c` | 显示控制器（CRTC）管理 |
| `rockchip_drm_drv.c` | Rockchip DRM 驱动入口 |
| `rockchip_vop.c` | Rockchip 显示输出处理器（VOP） |
| `dw-mipi-dsi.c` | DesignWare MIPI DSI 驱动 |
| `dw-hdmi.c` | DesignWare HDMI 驱动 |
