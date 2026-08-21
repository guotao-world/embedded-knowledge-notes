# linux时钟

https://developer.aliyun.com/article/1324307

**✔ 基本判断：**

-   分频器 / 倍频器：通常是**clock provider**
-   时钟树末端外设（UART/SPI/I2C）：通常是**clock consumer**

**✔ 正确规则是：**

-   谁"注册 clk + 提供 clk_ops + 在 clk tree 中有节点"，谁就是 provider
-   谁"只通过 clk API 获取并使用 clk"，谁就是 consumer

**IMX6UL_CLK_UART1_IPG 是不是已经"展开过的"？**

**✔ 是的，但要分清"展开"的含义**

它不是在 DTS 里展开，而是：

👉 在**clock controller driver 初始化时（probe阶段）已经被 CCF 构建成 clock tree 节点**

也就是说：

-   DTS 只给"名字/ID引用"
-   真正的展开发生在**clock driver + CCF**

**❓2：只要 DTS 声明就可以用了吗？**

**✔ 基本是，但前提是：**

必须同时满足：

1.  clock provider driver 已注册（CCF 已建树）
2.  clks 节点 driver probe 完成
3.  of_clk_add_provider() 已执行

否则：

❌ DTS 写了也拿不到 clk

**示例：**

**<&clks IMX6UL_CLK_UART1_IPG>**

**合起来意思是：**

**👉 "去 clks 这个 clock controller 里，取第 IMX6UL_CLK_UART1_IPG 号 clock"**

clock-controller@... {
compatible = "vendor,clock-mux";
clocks = <&pll1>, <&pll2>, <&osc>;
clock-names = "pll1", "pll2", "osc";
#clock-cells = <1>;};
clock-controller@... { compatible = "vendor,clock-divider";
clocks = <&pll1>; clock-names = "parent";
#clock-cells = <0>;};