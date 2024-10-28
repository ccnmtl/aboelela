After sanitizing and processing the data a processed file will be generated in this folder. If an older file named `processed.csv` is in this directory when
```
python process.py
```
is run in the terminal then the old file will be replaced with a new file made from the data in the data directory

The file is formatted with the following headers:
| UNI (ID) | Category | Max Score | Student Score | % Correct |
| -------- | -------- | --------- | ------------- | --------- |