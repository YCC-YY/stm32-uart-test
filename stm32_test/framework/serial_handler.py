import serial
import time

class SerialHandler:
    def __init__(self, port, baud=115200, timeout=0.5):
        self.ser = serial.Serial(port, baud, timeout=timeout)
        time.sleep(2)
        self.ser.reset_input_buffer()

    def send_cmd(self, cmd: str, wait=0.3) -> str:
        self.ser.reset_input_buffer()
        self.ser.write((cmd + "\n").encode("utf-8"))
        time.sleep(wait)
        return self.ser.read_all().decode("utf-8", errors="ignore")

    def close(self):
        self.ser.close()