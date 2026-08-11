

# STM32 串口自动化测试项目
> 嵌入式测试实战：STM32F103 + CMake + CLion + Python串口自动化测试

## 项目简介
基于STM32F103C8T6开发板，实现UART串口中断收发；
使用pyserial编写Python脚本，做上位机自动化收发测试。
整套工程使用CMake构建，不依赖Keil/IAR。

## 硬件
- STM32F103C8T6
- USB‑TTL模块
- ST‑Link下载器

## 环境
- arm‑none‑eabi‑gcc 交叉编译器
- CLion + CMake + Ninja
- OpenOCD（调试）
- Python3 + pyserial

## 目录结构
- firmware/：STM32固件源码（CubeMX生成CMake工程）
- stm32_test/：Python串口自动化测试脚本

## 功能
1. USART1 中断接收，收到数据回显
2. CMake一键编译生成elf/hex固件
3. Python脚本自动发送指令、校验串口返回数据

## 使用
1. CMake编译工程
2. ST‑Link烧录hex固件
3. 接USB‑TTL，运行python脚本进行自动化测试

