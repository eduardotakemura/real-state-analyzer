# Real Estate Analyzer
The Real Estate Analyzer is a data-driven application designed to fully extract, analyze, and model real estate data. 
It consists of an ETL pipeline module, for web scraping, data preprocessing, and database management,
along with a front-end and back-end system that allows users to filter, 
analyze, and predict real estate prices based on current market.

## Table of Contents
1. [Overview](#overview)
2. [Project Architecture](#project-architecture)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Libraries](#libraries)
6. [Features](#features)
7. [Contributing](#contributing)
8. [License](#license)

## Overview
The Real Estate Analyzer automates the process of gathering and analyzing real estate data. It scrapes property listings from real estate websites, 
processes the data, and stores it in a SQL database. The application provides an API for querying the data and includes a machine learning model to predict 
rental and selling prices based on user-defined filters. The app has a React front-end for user interaction, a Flask back-end to serve the data, and integrated 
tools for analysis and modeling.

## Project Architecture
![architecture](architecture.png)
### ETL (Extract, Transform, Load) Pipeline
1. **Scrapper Module**:
   - This module scrapes real estate data from web pages using **Selenium**.
   - It collects data such as property prices, locations, descriptions, and other relevant details from real estate listings.
     
2. **Preprocessor Module**:
   - After the data is scrapped, this module cleans, formats, and transforms the raw data into a structured format, ensuring it is suitable for storage and later analysis.
   - Common tasks include handling missing values, normalizing data, and removing duplicates.
     
3. **Loader Module**:
   - The preprocessed data is then loaded into a **SQL** database.
   - This database acts as the centralized storage for all real estate data, making it easy to query and retrieve specific subsets of information based on user requirements.

### API
4. **API**:
   - The DB is accessible through an API built with Flask.
   - The API allows for filtering and querying the data based on various criteria such as location, price range, and property size.
   - It serves as the bridge between the DB and the application.
  
### Application Components
5. **React Frontend**:
   - The front-end of the application is built with React. Initially, the user is presented with a simple form to input filters such as location, price, and property type.
   - Upon submitting the form, the React Frontend fetch data from the Flask Backend, which query the API server to retrieve the corresponding real estate data.
     
6. **Data Analysis (Analyzer Module)**:
   - Once the data is fetched from the API, it is passed to the **Analyzer Module**.
   - This module performs various data analysis tasks on the filtered real estate data, generating visual reports in the form of charts and tables.
   - It helps users gain insights from the data by summarizing trends and patterns in the real estate market.
     
7. **Price Prediction (Price Model Module)**:
   - The Modeller Module is a machine learning model that is trained on historical real estate data.
   - Its primary purpose is to predict renting or selling prices.
   - On the app, the model is loaded and used for inference after the data is analyzed, offering users a forecast of property values.
   - In the project there's also a ModelProcessor module, which goal is to prepare the data for the model training.
     
8. **Flask Backend**:
   - The Flask backend serves the React frontend, handling requests and communicating with the API, Analyzer and Price Model Modules.
   - It ensures the seamless flow of data (connection) between the Frontend and Backend, allowing users to interact with the real estate data in real-time.

## Installation
Instructions on how to install the project locally.

```bash
# Clone this repository
$ git clone https://github.com/eduardotakemura/real-estate-analyzer.git

# Go into the repository
$ cd real-estate-analyzer

# Install dependencies
$ pip install -r requirements.txt # Python
$ cd app/react npm install # React
```

## Usage
### ETL Pipeline
Since I'm not providing data on this repository, you need to:
- Initialize the local database;
- Create the properties table, which will hold the data;
- Then run the ETL pipeline script, which will scrap, preprocess and load the gathering data into your DB table.

```bash
# Initialize DB and create the properties table
$ set FLASK_APP=__init__:create_api
$ cd api
$ flask db init
$ flask db migrate -m "Create properties table"
$ flask db upgrade

# Run the ETL pipeline script
# Scrapper will pop browser windows if the headless option is off
# Several logs will be printed on console, so you can check the script progress
$ python etl_main.py
```
### Running the Application
After gather and successfully load the data into the DB, 
we need to run individually the App (Flask backend), API and React Frontend instances.

```bash
# Run the API
$ cd ./.. # cd back to main folder
$ python api_main.py

# Run the Flask Backend
$ python app_main.py

# Run the React Frontend
$ cd app/react
$ npm start
```
With this, each instance will listen in the following ports:
- Frontend: 3000;
- API: 4000;
- Backend: 5000;

### Using the Application
The Frontend can be accessed through http://localhost:3000/. 
- You can then select the desired filters and submit the form to get a full report for this dataset;
- At the page end, you can use the price prediction model by selecting and submitting the form;

## Libraries
The project relies most on the following libraries:
- **Flask**: Backend serving.
- **React.js**: Frontend user interface.
- **Selenium**: Web scrapping data tool.
- **Pandas/Numpy**: Data preprocessing and manipulation.
- **SQLAlchemy**: For handling the database.
- **PostgreSQL**: Data Storage.
- **Scikit-learn**: Machine learning tools.
- **Matplotlib/Seaborn**: For visualizing data and charts in reports.
- **Kneed**: Clustering Analysis tools.
- **Folium**: Interactive maps.
- **TensorFlow/Keras**: Deep Learning Model Outlining, Compiling, Saving and Loading.

## Features
- **Web Scraping**: Automatically scrapes real estate listings from multiple websites.
- **Data Preprocessing**: Cleans and processes the scraped data for analysis.
- **SQL Database**: Stores preprocessed real estate data for fast querying.
- **Filters**: Allows users to filter real estate data by price, location, size, etc.
- **Data Analysis**: Performs data analysis on queried data, displaying charts and tables.
- **Price Prediction**: Predicts renting and selling prices using pre-trained machine learning models.
- **API Integration**: The backend provides API endpoints for querying the database and returning results.
- **Interactive Frontend**: A React-based frontend where users can input filters and receive analysis reports.

## Contributing
Contributions are welcome! Please read the contributing guidelines first.

1. Fork the repo
2. Create a new branch (git checkout -b feature/feature-name)
3. Commit your changes (git commit -m 'Add some feature')
4. Push to the branch (git push origin feature/feature-name)
5. Open a pull request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
