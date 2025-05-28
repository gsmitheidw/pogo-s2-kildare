
build:
    python s2.py
    git add index.html
    git commit -m 'Update index'
    git push
    [console]::beep(2000, 500)

clean:
    rm -f index.html -ErrorAction SilentlyContinue

rebuild: clean build

csv:
    git add kildare_poi.csv
    git commit -m 'update csv'
    git push


validate:
    python validate_csv.py 
