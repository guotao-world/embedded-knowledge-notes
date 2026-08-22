# Secure Boot 的核心思想

启用 Secure Boot（RK2118 系列有 eFuse + RSA 验证公钥机制，防止未签名固件启动）

![Secure Boot](../images/image39.png)

> Secure Boot 通过在芯片 eFuse 中烧录公钥哈希，启动时 BootROM 用公钥验证固件签名，确保只有经过授权的固件才能启动，防止恶意固件注入。
