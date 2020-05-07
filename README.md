# Whole Genome Sequencing quality check

## Table of contents
  * [Description](#Description)
  * [Technologies](#Dechnologies)
  * [Installation](#Installation)
  * [Data](#Data)
  * [Examples](#Examples)


### Description
The aim of this project was to create a tool for genome analysts to easily check quality, depth of coverage and other important statistics in Whole Genome Sequencing data by visualising it.

### Technologies
- Python 3.8 (Dash, SQLalchemy)
- PostgreSQL
- Docker

### Installation
To run this project Docker version >= 18.09.9 and Python version >= 3.8 is required.

  #### Linux
  ##### Install Git and clone repository.
  ```
  $ cd ~/
  $ sudo apt-get install git
  $ git clone git@github.com:MNMdiagnostics/wgsqc.git
  $ cd ./wgsqc/
  ```

  ##### Prepare .env file with environment variables for database (example .env file is located in ./database/database.env)

  ##### Set up your Docker container and check if container is running
  ```
  $ docker run --name <POSTGRES_DB> -p <POSTGRES_PORT>:<POSTGRES_PORT> --env-file <env_file_path> -d postgres
  $ docker container ls
  ```

  ##### Check your Python version
  ```
  $ python --version
  ```

  ##### Install required packages
  ```
  $ pip install -r requirements.txt
  ```

  ##### If creating new database place your data in main directory and run inserts.py
  ```
  $ mv <path_to_your_data> .
  $ cd ./database/
  $ python inserts.py <path_to_root_data_directory>
  ```

  ##### Run app
  ```
  $ cd main/
  $ python app.py
  ```

### 4. Data

Current version allows user to create new database and insert user's files or connect to existing database and use it.
If inserting files, specific format is required.

```
  root_data_directory-
                     | - - - FOLDER1 - - - FILE1
                     |
                     | - - - FOLDER2 - - - FILE2
                     |
                     | - - - FOLDER3 - - - FILE3
                     |
                     | - - - FOLDER4 - - - FILE4
                     |
                     |...
```
Files should contain 6 tab-delimited columns:
  * Gene ID
  * Transcript ID
  * Mean coverage
  * Coverage X10
  * Coverage X20
  * Coverage X30


### 5. Examples
  1. Clone repo
  ```
  $ git clone git@github.com:MNMdiagnostics/wgsqc.git
  $ cd ./wgsqc/
  ```
  
  2. Set up .env file located in database/database.env
  ```
  POSTGRES_USER=test_user
  POSTGRES_PASSWORD=test
  POSTGRES_HOST=localhost
  POSTGRES_PORT=5432
  POSTGRES_DB=test_name
  ```
  
  3. Run docker container
  ```
  $ docker run --name test_name -p 5432:5432 --env-file database/database.env -d postgres
  $ docker container ls
  ```
  
  4. Install required packages
  ```
  $ pip install -r requirements.txt
  ```
  
  5. Move your data to project main directory and run inserts
  ```
  $ mv ~/wgsqc_data .
  $ cd database/
  $ python inserts.py ~/wgsqc_data
  $ cd ../main
  ```
  
  6. Run app
  ```
  $ python app.py
  ```
  
  7. Enter IP adress from terminal to your browser
  ![Enter IP adress](~/ip.png)
  
