# Real Estate Analyzer

Multi container app that scrap data from web pages, extract insights from the data, elaborate reports and predict real estate prices.  
(Hosted demo app available soon)

## 🏗️ Architecture Overview

The project is built using a modern microservices architecture with Docker containers, featuring:

- **Frontend**: React-based web application
- **Backend API**: FastAPI service
- **Database**: PostgreSQL for data persistence
- **Message Broker**: RabbitMQ for inter-service communication
- **Specialized Services**:
  - Property Scraper Service
  - Price Prediction Model Service
  - Data Analysis Service

### System Architecture Diagram

![architecture diagram](architecture.png)

## 🚀 How It Works

- **FastAPI – The Project's Central Hub**
  - Acts as the core that connects all microservices  
  - Serves data to the frontend  
  - Dispatches tasks to microservices via RabbitMQ  
  - Serves as the single access point to the database  

- **React Frontend – Modern & Responsive UX**
  - Subscribes to real-time updates via webhooks  
  - Offers a responsive dashboard with dynamic queue updates  

- **PostgreSQL – Scalable & Reliable Database**
  - Open-source, robust, and scalable relational database solution  

- **RabbitMQ – Asynchronous Message Broker**
  - Reliable message queue system to handle multiple asynchronous requests across services  

- **ETL Pipeline – Extract, Transform, Load for Insightful Data**
  - Extracts (scrapes) data from real estate websites  
  - Preprocesses raw data (cleansing and normalization)  
  - Enhances data with additional features (e.g., latitude and longitude)  
  - Loads processed data into the database  

- **Price Prediction Model – Intelligent Price Estimation**
  - Deep learning-based ANN model for training and inference  
  - Predicts property prices based on up-to-date data  

- **Data Analyzer – Insight Generation from Data**
  - Includes tools for exploratory data analysis  
  - Generates visualizations like heatmaps, summary tables, and cluster maps

## 💻 Technology Stack

- **Frontend**:
  - React
  - Nginx serving

- **API**:
  - FastAPI (Python)
  - SQLAlchemy ORM

- **Storage**:
  - PostgreSQL (Database)
  - Pickle (Models)
  - csv (Temp data)

- **Web Scraping/Automation**:
  - Selenium
  - Beautiful Soup

- **Message Queue**:
  - RabbitMQ for asynchronous communication
  - Event-driven architecture

- **Deep Learning**:
  - Python-based pipeline
  - TensorFlow/Keras

- **Data Analysis**:
  - Pandas
  - Numpy
  - Scikit-learn
  - Matplotlib
  - Folium

- **Infrastructure**:
  - Docker containerization
  - Docker Compose orchestration
  - Volume management for data persistence

## 🛠️ Setup and Installation

1. **Prerequisites**:
   - Docker and Docker Compose
   - Git

2. **Clone the repository**:
   ```bash
   git clone https://github.com/eduardotakemura/real-state-analyzer.git
   cd real-estate-analyzer
   ```

3. **Environment Setup**:
   ```bash
   cp .env
   # Configure your environment variables in .env such as:
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=postgres
    DB_PASSWORD=postgres
    DB_NAME=real_estate_db
    RABBITMQ_DEFAULT_USER=guest
    RABBITMQ_DEFAULT_PASS=guest
    LOCATION_IQ_API_KEY=<your locationIQ api key> # Register your API key for free in https://my.locationiq.com/register, we're limited to 5000/request day
   ```

4. **Launch the application**:
   ```bash
   docker-compose up -d
   ```

5. **Access the services**:
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - RabbitMQ Management: http://localhost:15672

## 🔄 Service Communication

The system uses an event-driven architecture with RabbitMQ:

1. **Scraper Service** → receive task, run ETL script and query API to load data into the database, publish success message
2. **Analysis Service** → receive task, fetch dataset from API and publish results
3. **Price Model Service (Training)** → receive task, fetch data from API, run training pipeline and store models in .pkl format, publish results
4. **Price Model Service (Prediction)** → receive task, load models.pkl and run inference, publish results
5. **API Service** → serves data to frontend, single access point to database, and push services tasks to queue
6. **Database Service** → accessible only through API
7. **Frontend Service** → query API through HTTP requests, subscribe to results through web-hooks

## 📝 API Documentation

The API documentation is available at `http://localhost:8000/docs` when running the application locally. It provides:

- Interactive API documentation
- Request/response examples
- Authentication details
- Schema information

## 🐳 Container Management

Each service is containerized and managed via Docker Compose:

- `database`: PostgreSQL database
- `api`: FastAPI backend service
- `react`: React frontend application
- `rabbitmq`: Message broker
- `price_model`: Price prediction service
- `scraper`: Web scraper service
- `analyzer`: Data analysis service

## 📈 Scaling

The microservices architecture allows for independent scaling of components:

- Horizontal scaling of services
- Load balancing capabilities
- Independent deployment of services
- Isolated resource management 