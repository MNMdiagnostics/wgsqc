# Whole Genome Sequencing quality check

## Table of contents
* [Description](#Description)
* [Technologies](#Dechnologies)
* [Installation](#Installation)
* [Data](#Data)
* [Examples](#Examples)


### 1. Description
The aim of this project was to create a tool for genome analysts to easily check quality, depth of coverage and other important statistics in Whole Genome Sequencing data by visualising it.

### 2. Technologies
- Python 3.8 (Dash, SQLalchemy)
- PostgreSQL
- Docker

### 3. Installation
To run this project Docker version >= 18.09.9 and Python version >= 3.8 is required.
#### 3.1 Linux
1. Install Git and clone repository.
```
$ cd ~/
$ sudo apt-get install git
$ git clone git@github.com:MNMdiagnostics/wgsqc.git
$ cd ./wgsqc/
```
2. Prepare .env file with environment variables for database (example .env file is located in ./database/database.env)
3. Set up your Docker container and check if container is running
```
$ docker run --name <POSTGRES_DB> -p <POSTGRES_PORT>:<POSTGRES_PORT> --env-file <env_file_path> -d postgres
$ docker container ls
```
4. Check your Python version
```
$ python --version
```
5. Install required packages
```
$ pip install -r requirements.txt
```
6. If creating new database place your data in main directory and run inserts.py
```
$ mv <path_to_your_data> .
$ cd ./database/
$ python inserts.py
```
### 4. Data
### 5. Examples

