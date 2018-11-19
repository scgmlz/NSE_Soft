import pytest
import mieze_python
from mieze_python.mieze import Mieze

def test_launch_version():
    assert(mieze_python.__version__== '0.0.1')
        