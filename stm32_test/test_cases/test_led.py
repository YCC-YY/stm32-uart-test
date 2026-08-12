import pytest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR))

from framework import SerialHandler
@pytest.fixture(scope="module")
def ser():
    s = SerialHandler("COM11", 115200)
    yield s
    s.close()

@pytest.mark.parametrize("cmd,expected", [
    ("led_on", "-->LED 打开"),
    ("led_off", "-->LED 关闭"),
])
def test_led(ser, cmd, expected):
    resp = ser.send_cmd(cmd)
    assert expected in resp