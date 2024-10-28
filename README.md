# Gen AI for nursing - Data processor to assist in a student recovery plan
This repository is to handle the data for Professor Aboelela's Gen AI project. Data is sanitized and processed into a single file for use with an AI service to help guide student learning for at-risk students.

The process can be performed on your local computer following the instructions below:

## QUICK REFERENCE -- for after the initial setup
1. Replace old data from the `data` folder with the new data.
2. Open up a terminal and enter the following commands:
```
cd ~/Desktop/aboelela
python process.py
```
3. The resulting `processed.csv` will appear in the results folder.
    * This will overwrite the old `processed.csv` file if it is still present in the directory.

## Prerequisites and Set-up
At minimum you will need `Python` present in your computer. You can check this from your terminal using the command.
```
python --version
```
If no python version exists you will have to download python here: https://www.python.org/downloads/

### Download the repository from https://github.com/ccnmtl/aboelela
There are two main ways to handle the download:

#### Simple - `.zip` download
From the GitHub repository listed in the header above:

1. Click on `<> Code` &#8594; `Download ZIP`
2. Unzip the folder and move it to your desktop.
3. Open your computer's terminal and input the following instructions into the terminal:
```
cd ~/Desktop/aboelela
```

#### Comprehensive - `git clone`
```
git --version
```
1. Ensure that you have `git` downloaded on you computer using the above command: 
   * If git is not present, it  can be downloaded here: https://git-scm.com/downloads
2. From the GitHub repository listed in the header above: click on `<> Code` &#8594; `SSH` &#8594; Copy the git address 
3. Navigate to your Desktop from the terminal and clone the repository to your desktop:
```
cd ~/Desktop
git clone [the copied address from GitHub]
```
4. The new directory should appear on your desktop. Enter the new directory:
```
cd aboelela
```


## Populate the `data` folder
The finished file is the result of the `Results` and `Item` `.csv` files. Download the files and place them in the `data` folder.

***REMEMBER: Clear old  data from the folder before adding new data.***

## Process the data
Once the directory is set up and the data is in the proper folder you can run the following command from the terminal: 
```
python process.py
```
Retrieve the processed data from the `results` folder. The file will always be labeled as `processed.csv`
