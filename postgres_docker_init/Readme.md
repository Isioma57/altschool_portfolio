# Dockerized PostgreSQL Setup & Python Database Interaction

<p align="center">
  <img alt="image" width="400" src="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*n_sEQRRWoRAikgtX9clAOg.png">
</p>

## 📕 Table Of Contents
* [Overview](#project-overview)
* [The Data](#the-data)
* [Project Structure](#project-structure)
* [How It Works](#how-it-works)
* [Installation and Setup](#installation-and-setup)
* [Configuration](#configuration)
* [How to Spin Up the Server](#how-to-spin-up-the-server)
* [Usage](#usage)
* [Troubleshooting](#troubleshooting)
* [License](#license)
 

# Overview
This project aims to establish a PostgreSQL server infrastructure using Docker and Docker Compose, facilitating seamless deployment and management. It includes tasks such as loading data of my choice into the database and implementing Python-based interactions utilizing psycopg2(a python database adapter). By leveraging Docker, the project ensures portability and reproducibility of the PostgreSQL environment, enhancing development efficiency and simplifying the process of setup and deployment.

Using psycopg2 offers several advantages:

- It provides a reliable and efficient way to connect and interact with PostgreSQL databases from Python.
- Supports advanced features like server-side cursors and asynchronous communication.
- Allows for straightforward execution of SQL commands, data retrieval, and transaction management.

# The Data
The data used in this project is sourced from [Kaggle](https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis) and consists of a CSV file named **```dataco_supply_chain```**. It provides insights into a smart supply chain for big data analysis. The choice of this dataset aligns with the project's objectives of simulating real-world data scenarios and showcasing practical database management.

# Project Structure

```plaintext
postgres_docker_init/
│
├── data/
│   └── dataco_supply_chain.csv    # Source data file
│
├── infra_script/
│   └── init.sql                   # SQL script for database initialization
│
├── src/
│   ├── db_manager.py              # Python script for database management functions
│   └── main.py                    # Main script demonstrating database interactions
│
├── .env                           # Environment variables file
├── docker-compose.yml             # Docker Compose configuration file
└── Readme.md                      # Project documentation

```

# How It Works

### Setup
The **```docker-compose.yml```** file defines a PostgreSQL service configured to run in a Docker container. Port 5434 on the local machine is mapped to Port 5432 in the Docker container to avoid conflicts with existing PostgreSQL installations.

### Initialization
The **```init.sql script```** creates a new schema, table, and loads data from the dataco_supply_chain.csv file into the PostgreSQL container upon startup.

### Python Interaction
The **```db_manager.py```** script provides functions to connect to the PostgreSQL database and execute queries. The **```main.py```** script demonstrates how to use these functions to perform operations such as counting the number of records in the database table.

# Installation and Setup

### Prerequisites

Ensure you have the following installed on your local machine:
- Docker
- Docker Compose
- Python

### Setup Instructions
- Clone the repository
```bash
git clone https://github.com/Isioma57/altschool_portfolio.git
```
- Navigate to the project directory
```bash
cd postgres_docker_init
```
- Create and activate a Python virtual environment using the following commands

For Window Users:
```bash
python -m venv venv
source venv/Scripts/activate
```
For Unix-based systems:
```bash
python3 -m venv venv
source venv/bin/activate
```
- Install Python dependencies using the:
```bash
pip install -r requirements.txt
```
# Configuration
Before running the scripts, you need to set the following environment variables:

    POSTGRES_USER: The username for the PostgreSQL database.
    POSTGRES_PASSWORD: The password for the PostgreSQL database.
    POSTGRES_DB: The name of the PostgreSQL database.
    POSTGRES_HOST: The hostname for the PostgreSQL database. (Optional, default is "localhost")
    POSTGRES_PORT: The port for the PostgreSQL database. (Optional, default is 5432)

You can set these environment variables in the .env file in the directory of the project with the following format:
```
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database
POSTGRES_HOST=your_host
POSTGRES_PORT=your_port
```

# How to Spin Up the Server

Once your .env file has been accurately set up with the necessary environment variables, simply run the following command in the project folder to start the PostgreSQL service:
```bash
docker-compose up
```

You can also run the command in detached mode with:
```bash
docker-compose up -d
```

# Usage

Once the container is up and running, navigate to the folder containing the Python script:
```bash
cd src
```
Execute the following command to interact with the database:
```bash
python main.py
```

For the purpose of this project, the Python script is written to count the total number of records in the dataset. Running python main.py will output:
```bash
$ python main.py
[(180519,)]
```
# Troubleshooting

### Character Encoding Issue

If you download or use the data straight from the source link indicated above, it is pertinent to note that it is encoded using the ISO-8859-1 character encoding rather than UTF-8. This could potentially cause issues when importing into a PostgreSQL database expecting UTF-8 encoding.

To check the encoding of the data, navigate to the folder containing the data and run this command:

```bash
file -i dataco_supply_chain.csv
```
To change it to UTF-8, run this command:
```bash
iconv -f ISO-8859-1 -t UTF-8 dataco_supply_chain.csv > dataco_supply_chain_utf8.csv
```
This will create a new copy of the data with the correct encoding. Rename the dataset if you wish.

### General Troubleshooting

If you encounter issues during setup or execution, consider the following:

- Ensure Docker and Docker Compose are running properly.
- Verify that the environment variables in the .env file are correctly set.
- Check the Docker container logs for any error messages.
- Ensure all Python dependencies are installed correctly.

# License

This project is licensed under the MIT License. See the LICENSE file for details.