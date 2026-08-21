# lLinux设备树的节点device_node

**N.parent** → 指向父节点

**N.child** → 指向"第一个子节点"

**N.sibling** → 指向"同级下一个节点"

**注意：**

struct device_node *sibling;

表示的是：

**当前节点在同一层级（同一个 parent 下）的下一个兄弟节点**

```c
struct device_node {
const char *name;
const char *type;
phandle phandle;
const char *full_name;
struct fwnode_handle fwnode;
struct property *properties;
struct property *deadprops;/* removed properties */
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