# LINUX 等待队列

## 一、队列一：条件驱动的"可重复等待机制"

### 基本 API

```c
wait_queue_head_t my_waitq;  // 等待队列头
init_waitqueue_head(&my_waitq);

wait_event_interruptible(my_waitq, condition);
wake_up_interruptible(&my_waitq);
```

### 注意事项

1. `wait_event_interruptible(queue, condition)` 如果 `condition == true`，则不会休眠，直接继续执行
2. `wait_event_interruptible(queue, condition)` 并不是"被 wake_up 唤醒就直接返回"，而是"**被唤醒后重新检查 condition，只有 condition 为真才真正返回**"
3. `wake_up = 敲门，condition = 门锁`

> 敲门了不代表你能进门：
> - 门锁没开（condition=false）→ 回去继续等
> - 门锁开了（condition=true）→ 才能继续执行

---

## 二、队列二：一次性"事件完成通知"（one-shot）

### 基本概念

completion 使用了 `wait_queue_head`，但它不是简单"封装"，而是：

```
completion = wait_queue + 状态(done) + 语义约束
```

### API

```c
DECLARE_COMPLETION_ONSTACK(done);

wait_for_completion(&done);
complete(&done);
```

### 与 wait_event 的区别

| 机制 | 特点 | 适用场景 |
|------|------|---------|
| `wait_event` | 条件驱动，可重复等待 | 等待某个条件持续成立 |
| `completion` | 一次性事件通知，有 done 状态 | 等待某个一次性事件完成 |
