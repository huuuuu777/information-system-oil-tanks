from pydantic import BaseModel, ConfigDict

class TankBase(BaseModel):
    
    name: str
    measurement_date: str
    level_m: float
    fuel_type: str
    fuel_volume: float

class TankCreate(TankBase):
    pass

class TankUpdate(TankBase):
    pass

class TankRead(TankBase):
    id: int

    model_config = ConfigDict(from_attributes=True)