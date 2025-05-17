set shell := ["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", "-NoProfile", "-Command"]

build:
    python s2.py
    git add index.html
    git commit -m 'Update index'
    git push

clean:
    Remove-Item -Force index.html -ErrorAction SilentlyContinue

rebuild: clean build

csv:
    git add kildare_poi.csv
    git commit -m 'update csv'
    git push
