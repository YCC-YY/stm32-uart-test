# STM32 串口自动化测试框架

## 项目简介
基于 STM32F103 单片机实现串口命令交互；使用 Python + pytest 搭建分层自动化测试框架，实现 LED 外设自动回归测试。
框架将串口通信、测试报告生成封装成通用模块，测试用例与底层通信解耦，覆盖正常功能与异常指令场景。

## 硬件环境
- 主控：STM32F103C8T6
- 通信：USB-TTL 串口（USART1，PA9-TX / PA10-RX），波特率 115200，8N1
- 外设：板载 LED（PA1，低电平点亮）
- 开发：CLion + CMake + STM32 HAL 库（CubeMX 工程）

## 目录结构
```
proj
├── firmware                     # STM32 固件工程（CLion CMake）
│   └── Core
│       ├── Inc
│       │   └── uart_cmd.h       # 命令处理模块头文件
│       └── Src
│           ├── main.c           # 主函数、串口中断接收、printf重定向
│           └── uart_cmd.c       # 命令解析：led_on / led_off / hello / 非法命令
├── stm32_test                   # Python 自动化测试框架
│   ├── framework                # 通用框架层
│   │   ├── serial_handler.py    # 串口通信封装
│   │   └── reporter.py          # JSON 测试报告输出
│   ├── test_cases               # 测试用例目录
│   │   └── test_led.py          # LED 功能回归用例（4条）
│   └── requirements.txt         # 依赖清单
└── .github/workflows/ci.yml     # GitHub Actions 语法静态检查
```

## 固件构建与烧录
1. CLion 打开 `firmware/` 工程，重新加载 CMake
2. 构建（生成 `build/Debug/firmware.elf`），烧录到开发板
3. 串口助手（115200）验证：发送 `hello\r\n` 应返回 `Hello from STM32`

## 本地运行步骤
1. 创建并激活 Python 虚拟环境
```bash
python -m venv .venv
# Windows 激活
.venv\Scripts\Activate.ps1
pip install -r stm32_test/requirements.txt
```

2. 烧录 STM32 固件，修改 `stm32_test/test_cases/test_led.py` 中串口号为实际端口（默认 COM11）

3. 执行测试（须在 `stm32_test` 目录下运行）
```bash
pytest test_cases/test_led.py -v
```
运行结束自动生成 `report.json` 结构化测试报告（字段：`total` / `pass` / `data`）。

## 支持命令
| 命令      | 功能说明       |
|-----------|----------------|
| `led_on`  | 打开 LED       |
| `led_off` | 关闭 LED       |
| `hello`   | 返回问候信息   |
| 非法命令  | 返回 `ERR:unknown cmd` |

## 踩坑记录
1. 串口粘包问题：必须等待 `\r\n` 换行符，收到完整一行再解析命令
2. 字符串匹配前需去除缓冲区中的 `\r` / `\n`，否则 strcmp 匹配失败（当前实现：`'\n'` 触发整行、`'\r'` 直接忽略）
3. 脚本发送命令必须携带 `\r\n` 结束符，单片机才能识别完整指令
4. `printf` 必须重定向：syscalls.c 中 `__io_putchar` 是弱符号，若无强定义（main.c 中 `__io_putchar` 内部 `HAL_UART_Transmit`），printf 会跳空指针触发 HardFault
5. 固件新增源文件要加进根 `CMakeLists.txt` 的 `target_sources`，不要放 `cmake/stm32cubemx/CMakeLists.txt`（CubeMX 再生成会整体覆盖）
6. `requirements.txt` 必须保存为 UTF-8 编码，否则 pip 解析失败
7. pytest 中类名以 `Test` 开头会被误识别为测试类（`TestReporter` 类已加 `_` 前缀规避）
8. GitHub Actions 云端无物理串口，仅做 Python 语法静态检查，硬件测试本地执行

## CI 说明
GitHub Actions 仅执行 Python 语法静态检查（`compileall`）；硬件功能测试需本地连接开发板执行。
