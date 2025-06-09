# tests/conftest.py
import sys
import os

# Füge das Projektverzeichnis (Parent von tests/) zum sys.path hinzu
root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if root not in sys.path:
    sys.path.insert(0, root)
