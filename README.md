# Whole Genome Sequencing quality check

## Table of contents
* [Description](#Description)
* [Technologies](#Dechnologies)
* [Installation](#Installation)
* [Data](#Data)
* [Examples](#Examples)


### 1. Description
The aim of the project was to create a tool for genome analysts to easly check quality, depth of coverage and other important statistics in Whole Genome Sequencing data by visualising it.

### 2. Technologies:
- Python 3.8 (Dash, SQLalchemy)
- PostgreSQL
- Docker

### 3. Installation
To run this project Python version >= 3.8 is required.
#### 3.1 Linux
1. Check your Python version
```
$ python --version
```
2. Change directory to project main directory
```
$ cd ~/wgsqc
```
or
```
$ cd <path_to_project>/wgsqc
```
3. Install required packages
```
$ pip install -r requirements.txt
```
4. If creating new database place your data in main directory and run inserts.py
```
$ mv <path_to_your_data> <path_to_project_main_directory>
$ cd <path_to_project_main_directory>/database/
$ python inserts.py
```
### 4. Data
### 5. Examples

