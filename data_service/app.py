from fastapi import FastAPI
from random import randint, choice
from pydantic import BaseModel
import datetime

app = FastAPI()

class DataRecord(BaseModel):
    id: int
    name: str
    value: float
    timestamp: datetime.datetime

NAMES = ["Гена", "Света", "Рома", "Даша", "Барон", "Толик", "Лена"]

@app.get("/data", response_model=DataRecord)
def get_random_data():
    """
    Генерирует рандомные данные.
    """
    record = DataRecord(
        id=randint(1, 1000),
        name=choice(NAMES),
        value=round(randint(10, 100) + randint(0, 99) / 100, 2),
        timestamp=datetime.datetime.now()
    )
    return record
