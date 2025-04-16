from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Properties(Base):
    __tablename__ = 'properties'

    id = Column(Integer, primary_key=True)
    page_id = Column(String(50), nullable=False)
    scraping_date = Column(String, nullable=False)
    link = Column(String, nullable=False)
    operation = Column(String(50), nullable=False)
    size = Column(Integer, nullable=False)
    dorms = Column(Integer, nullable=False)
    toilets = Column(Integer, nullable=False)
    garage = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    additional_costs = Column(Integer, nullable=False)
    type = Column(String(255), nullable=False)
    street = Column(String(255), nullable=False)
    neighborhood = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

class PriceModels(Base):
    __tablename__ = 'price_models'

    id = Column(Integer, primary_key=True)
    operation = Column(String(50), unique=True, nullable=False)
    clusters_map = Column(String, nullable=False)  # Will store HTML content
    k_clusters = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=datetime.now, nullable=False)


