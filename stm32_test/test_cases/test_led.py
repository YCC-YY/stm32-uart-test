import pytest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.append(str(BASE_DIR / "framework"))

from serial_handler import SerialHandler