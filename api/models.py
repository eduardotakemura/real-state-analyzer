from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

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


