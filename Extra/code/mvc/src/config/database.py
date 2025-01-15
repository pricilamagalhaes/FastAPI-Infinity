from sqlalchemy import create_engine
from sqlalchemy.orm import registry

engine = create_engine("sqlite:///books.db")
table_registry = registry()
    
