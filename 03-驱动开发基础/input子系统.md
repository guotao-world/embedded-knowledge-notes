# input 子系统

![input 子系统架构](../images/image32.png)

> input 子系统是 Linux 内核中统一管理输入设备（按键、鼠标、触摸屏、游戏手柄等）的框架。驱动通过 `input_report_key()` / `input_report_abs()` 等 API 上报事件，事件进入内核事件队列后，用户层通过 `/dev/input/eventX` 读取 `struct input_event` 数据。
