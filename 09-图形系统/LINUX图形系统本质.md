# LINUX图形系统本质

**核心内容：**Linux图形系统本质上就是操作显示设备这类普通外设。内核提供显示硬件的驱动接口（例如 DRM），用户空间通过图形系统程序（如 X Server、Wayland Compositor）管理屏幕资源。各种GUI应用（Qt、GTK等）把自己要显示的内容提交给图形系统，由图形系统进行窗口管理、合成，最后通过显示驱动输出到屏幕。只是因为需要支持多窗口、多应用、动画、输入、GPU加速等功能，所以围绕显示设备发展出了非常复杂的软件生态。

-   DRM：Direct Rendering Manager 直接渲染管理器
-   渲染 = 把抽象的图形描述转换成最终像素。
-   DRM是从"GPU渲染管理"发展来的。
-   不是必须有显示服务器才能显示图形。显示服务器（X Server / Wayland Compositor）不是"显示图形的必要条件"，而是"管理多个图形应用的解决方案"。
-   DRM叫"直接渲染管理器"，是因为它最初的任务是管理多个程序安全、高效地直接使用GPU进行渲染。后来Linux把显示模式设置(KMS)、显示控制器管理也纳入DRM，所以今天的DRM已经不仅管理渲染，也管理整个显示输出链路。
-   DRM放在drivers/gpu下，是因为它诞生于GPU渲染管理；后来扩展成包含显示输出(KMS)的完整图形子系统，但源码目录沿用了历史结构。对于现代Linux来说，drivers/gpu/drm实际上代表的是整个图形/显示子系统，而不只是GPU。？？？？？？？

**RK3568源码结构：**

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