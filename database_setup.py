import sys
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
import sqlite3


engine = create_engine('sqlite:///restaurantmenu.db', echo = True)
Base = declarative_base()
Base.metadata.create_all(engine)

class Restaurant(Base):
	__tablename__ = 'restaurant'

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)


class MenuItem(Base):
	__tablename__ = 'menu_item'

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	description = Column(String(250))
	price = Column(String(10))
	course = Column(String(15))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'), nullable = False)
	restaurant_id = relationship('Restaurant')