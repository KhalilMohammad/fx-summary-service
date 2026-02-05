from typing import List, Optional
from pydantic import BaseModel


class DailyRate(BaseModel):
    date: str
    rate: float
    percent_change: float


class SummaryResponse(BaseModel):
    start_rate: float
    end_rate: float
    total_percent_change: float
    mean_rate: float
    daily: Optional[List[DailyRate]] = None
