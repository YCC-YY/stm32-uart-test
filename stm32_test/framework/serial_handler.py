import serial
import time

class SerialHandler:
    def __init__(self, port, baud, timeout=1):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.ser = None

    def open(self):
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baud,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=self.timeout,
                xonxoff=False,
                rtscts=False,
                dsrdtr=False
            )
            time.sleep(0.3)
            self.ser.reset_input_buffer()
            return True
        except Exception as e:
            print(f"串口打开失败:{e}")
            return False

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()

    def send_cmd(self, cmd: str) -> str:
        """发送命令，返回设备应答，增加异常保护"""
        if not (self.ser and self.ser.is_open):
            return "ERROR:串口未打开"
        try:
            self.ser.reset_input_buffer()
            self.ser.write((cmd + "\r\n").encode("utf-8"))
            resp = self.ser.read(512)
            return resp.decode("utf-8", errors="ignore").strip()
        except Exception as e:
            return f"ERROR:{str(e)}"