set shell := ["C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", "-NoProfile", "-Command"]

build:
    python s2.py
    git add index.html
    git commit -m 'update index'
    git push
    [console]::beep(2000, 500)

clean:
    Remove-Item -Force index.html -ErrorAction SilentlyContinue

rebuild: clean build

csv:
    git add kildare_poi.csv
    git commit -m 'update csv'
    git push


validate:
    python validate_csv.py 

s2: 
    git add s2.py
    git commit -m 's2/news update'
    git push

news: s2 rebuild
