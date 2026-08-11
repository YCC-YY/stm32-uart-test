import serial
import time

def run_test():
    COM_PORT = "COM11"
    BAUD = 115200
    try:
        # 显式写全所有串口参数，和串口助手完全对齐
        ser = serial.Serial(
            port=COM_PORT,
            baudrate=BAUD,
            bytesize=serial.EIGHTBITS,  # 8位数据位
            parity=serial.PARITY_NONE,   # 无校验
            stopbits=serial.STOPBITS_ONE, # 1位停止位
            timeout=1,
            xonxoff=False,  # 关闭软件流控
            rtscts=False,   # 关闭硬件流控
            dsrdtr=False    # 关闭DTR流控
        )
    except Exception as e:
        print(f"❌串口异常:{e}")
        return

    print(f"✅串口打开成功 {COM_PORT}")
    time.sleep(1.5)
    # 先读开机打印，验证接收是否正常
    boot_msg = ser.read_all().decode("utf-8", errors="ignore")
    print(f"开机信息：{repr(boot_msg)}")


def send_cmd(ser, cmd: str) -> str:
    ser.reset_input_buffer()
    data = (cmd + "\n").encode("utf-8")   # 加上换行符
    for b in data:
        ser.write(bytes([b]))
        time.sleep(0.005)
    time.sleep(0.3)
    resp = ser.read_all()
    return resp.decode("utf-8", errors="ignore")

def run_test():
    COM_PORT = "COM11"
    BAUD = 115200
    try:
        ser = serial.Serial(
            port=COM_PORT,
            baudrate=BAUD,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.5,
            xonxoff=False,
            rtscts=False,
            dsrdtr=False
        )
    except Exception as e:
        print(f"❌串口异常:{e}")
        return

    print(f"✅串口打开成功 {COM_PORT}")
    # 等单片机复位启动完成
    time.sleep(2)
    ser.reset_input_buffer()
    ser.reset_output_buffer()

    print("\n==========开始执行串口自动化测试==========\n")

    test_cases = [
        ("led_on", "-->LED 打开"),
        ("led_off", "-->LED 关闭"),
        ("hello", "Hello from STM32")
    ]
    pass_cnt = 0
    fail_cnt = 0

    for cmd, expect in test_cases:
        print(f"发送命令：{cmd}")
        resp = send_cmd(ser, cmd)
        print(f"设备返回：{repr(resp)}")
        if expect in resp:
            print("👉结果：PASS ✔\n")
            pass_cnt += 1
        else:
            print(f"👉结果：FAIL ✘ 未检测到预期:{expect}\n")
            fail_cnt += 1
        # 每条命令间隔给单片机留余量
        time.sleep(0.5)

    print(f"==========测试结束==========")
    print(f"总用例:{len(test_cases)}  通过:{pass_cnt} 失败:{fail_cnt}")
    ser.close()

if __name__ == "__main__":
    run_test()