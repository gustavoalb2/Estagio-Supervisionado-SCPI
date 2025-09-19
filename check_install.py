import sys
import subprocess
import os

print("Python executable:", sys.executable)
print("Python version:", sys.version)
print("Python path:", sys.path)

try:
    import reportlab
    print("ReportLab is installed at:", reportlab.__file__)
except ImportError:
    print("ReportLab is not installed.")

try:
    import openpyxl
    print("openpyxl is installed at:", openpyxl.__file__)
except ImportError:
    print("openpyxl is not installed.")

# Get the directory of the current Python executable
python_dir = os.path.dirname(sys.executable)

# Construct the path to pip
pip_path = os.path.join(python_dir, "Scripts", "pip.exe")

# Install reportlab and openpyxl
if os.path.exists(pip_path):
    print(f"Installing packages using {pip_path}...")
    subprocess.call([pip_path, "install", "reportlab"])
    subprocess.call([pip_path, "install", "openpyxl"])
else:
    print(f"Pip not found at {pip_path}")