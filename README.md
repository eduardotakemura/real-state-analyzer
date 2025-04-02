# Real Estate Analyzer - Microservices Architecture

A sophisticated real estate analysis platform built using a microservices architecture, designed to scrape, analyze, and predict property prices while providing insights through an interactive web interface.

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

```
┌─────────────┐     ┌─────────────┐
│   React     │────▶│   FastAPI   │
│  Frontend   │◀────│  Backend    │
└─────────────┘     └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │  PostgreSQL  │
                    │  Database    │
                    └──────┬──────┘
                           │
                    ┌──────┴──────┐
                    │   RabbitMQ  │
                    │   Broker    │
                    └──────┬──────┘
                           │
     ┌──────────────┬─────┴────┬──────────────┐
     ▼              ▼          ▼              ▼
┌──────────┐  ┌──────────┐ ┌────────┐  ┌──────────┐
│ Scraper  │  │  Price   │ │  Data  │  │ Analysis │
│ Service  │  │  Model   │ │  API   │  │ Service  │
└──────────┘  └──────────┘ └────────┘  └──────────┘
```

## 🚀 Features

- **Real-time Property Data Collection**
  - Automated web scraping of property listings
  - Real-time data processing and storage
  - Robust error handling and retry mechanisms

- **Advanced Price Prediction**
  - Machine learning-based price prediction model
  - Historical price trend analysis
  - Feature importance analysis

- **Data Analysis and Insights**
  - Property market trends analysis
  - Neighborhood statistics
  - Investment opportunity identification

- **Interactive Web Interface**
  - Real-time property search and filtering
  - Interactive data visualizations
  - User-friendly dashboard

## 💻 Technology Stack

- **Frontend**:
  - React
  - Modern UI/UX design
  - Interactive data visualization libraries

- **Backend**:
  - FastAPI (Python)
  - PostgreSQL
  - SQLAlchemy ORM

- **Message Queue**:
  - RabbitMQ for asynchronous communication
  - Event-driven architecture

- **Machine Learning**:
  - Python-based ML pipeline
  - Scikit-learn
  - Data processing utilities

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
   git clone <repository-url>
   cd real-estate-analyzer
   ```

3. **Environment Setup**:
   ```bash
   cp .env.example .env
   # Configure your environment variables in .env
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

1. **Scraper Service** → publishes raw property data
2. **Analysis Service** → processes and enriches data
3. **Price Model Service** → generates price predictions
4. **API Service** → aggregates and serves data to frontend

## 📊 Data Flow

1. Property data is collected by the scraper service
2. Raw data is published to RabbitMQ
3. Analysis service processes and enriches the data
4. Price prediction model generates valuations
5. Processed data is stored in PostgreSQL
6. API serves data to the frontend application

## 🔐 Security

- Containerized services for isolation
- Environment-based configuration
- Secure database access
- API rate limiting
- Input validation and sanitization

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
- `react`: Frontend application
- `rabbitmq`: Message broker
- `price_model`: Price prediction service
- `scraper`: Data collection service
- `analyzer`: Data analysis service

## 📈 Scaling

The microservices architecture allows for independent scaling of components:

- Horizontal scaling of services
- Load balancing capabilities
- Independent deployment of services
- Isolated resource management 