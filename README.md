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
### 5. Examples

