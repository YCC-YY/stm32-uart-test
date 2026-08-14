import pytest
from framework.serial_handler import SerialHandler
from framework.reporter import rep


@pytest.fixture(scope="module")
def dev():
    dev = SerialHandler(port="COM11", baud=115200)
    ok = dev.open()
    assert ok is True, "串口打开失败"
    yield dev
    dev.close()
    # 无论用例是否通过，都保存报告
    rep.save_json("report.json")


def test_led_on(dev):
    ret = dev.send_cmd("led_on")
    ok = "LED 打开" in ret
    rep.add_record("test_led_on", ok, ret)
    assert ok


def test_led_off(dev):
    ret = dev.send_cmd("led_off")
    ok = "LED 关闭" in ret
    rep.add_record("test_led_off", ok, ret)
    assert ok


def test_hello(dev):
    ret = dev.send_cmd("hello")
    ok = "Hello from STM32" in ret
    rep.add_record("test_hello", ok, ret)
    assert ok


def test_bad_cmd(dev):
    ret = dev.send_cmd("abc123456")
    print(f"\n[调试] 脚本收到返回内容：[{ret}]")
    ok = "ERR:unknown cmd" in ret
    rep.add_record("test_bad_cmd", ok, ret)
    assert ok
