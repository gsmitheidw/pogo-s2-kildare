set shell := ["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", "-NoProfile", "-Command"]

build:
    python s2.py

clean:
    Remove-Item -Force index.html -ErrorAction SilentlyContinue

rebuild: clean build

