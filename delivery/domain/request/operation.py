from pydantic import BaseModel
from datetime import time
from domain.data.enums.week import DayOfWeek

class Operation(BaseModel):
    timeout: time
    timein: time
    day: DayOfWeek