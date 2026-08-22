# Linux 设备树的节点 device_node

## 一、节点关系指针

| 指针 | 含义 |
|------|------|
| `N.parent` | 指向父节点 |
| `N.child` | 指向"第一个子节点" |
| `N.sibling` | 指向"同级下一个节点" |

> `struct device_node *sibling;` 表示的是：当前节点在同一层级（同一个 parent 下）的下一个兄弟节点。

---

## 二、device_node 结构体

```c
struct device_node {
    const char *name;
    const char *type;
    phandle phandle;
    const char *full_name;
    struct fwnode_handle fwnode;

    struct property *properties;
    struct property *deadprops;    /* removed properties */

    struct device_node *parent;
    struct device_node *child;
    struct device_node *sibling;

    struct kobject kobj;
    unsigned long _flags;
    void *data;

#if defined(CONFIG_SPARC)
    const char *path_component_name;
    unsigned int unique_id;
    struct of_irq_controller *irq_trans;
#endif
};
```

---

## 三、节点树结构示意

```
        root (/)
         │
    ┌────┴────┐
    │         │
  node A    node B
    │
 ┌──┴──┐
 │     │
 A1    A2
```

- `root.child` → node A
- `node A.sibling` → node B
- `node A.child` → A1
- `A1.sibling` → A2
- `A1.parent` → node A
