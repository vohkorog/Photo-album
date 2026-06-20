import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Base
from database import engine

class db:
    @staticmethod
    def create_model():
        Base.metadata.create_all(engine)

    @staticmethod
    def delete_model():
        Base.metadata.drop_all(engine)