from datetime import datetime, date
from decimal import Decimal
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator


class PosPayment(BaseModel):
    payment_id: int
    payment_type: str
    amount: Decimal


class PosSale(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    date: datetime
    payment_type: str
    product: str
    product_reference: str | None = None
    pos_name: str
    sale_reference: str
    pos_session: str
    payments: list[PosPayment] = Field(default_factory=list)
    quantity: Decimal
    price: Decimal


class DailySalesReportConfig(BaseModel):
    start_date: date
    end_date: date | None = None
    output_path: Path

    @model_validator(mode="after")
    def validate_date_range(self) -> "DailySalesReportConfig":
        if self.end_date is not None and self.end_date < self.start_date:
            raise ValueError("end_date no puede ser anterior a start_date")
        return self
