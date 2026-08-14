#include "uart_cmd.h"
#include "main.h"
#include "stdio.h"
#include "string.h"

// 处理串口完整一行命令
void UART_Cmd_Process(char *recv_buf)
{
    if(strcmp(recv_buf, "led_on") == 0)
    {
        HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_RESET);  // PA1 低电平点亮，与 main.c 原逻辑一致
        printf("LED 打开\r\n");
    }
    else if(strcmp(recv_buf, "led_off") == 0)
    {
        HAL_GPIO_WritePin(GPIOA, GPIO_PIN_1, GPIO_PIN_SET);
        printf("LED 关闭\r\n");
    }
    else if(strcmp(recv_buf, "hello") == 0)
    {
        printf("Hello from STM32\r\n");
    }
    else
    {
        // 未知命令返回错误，给脚本做断言
        printf("ERR:unknown cmd\r\n");
    }
}