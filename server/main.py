from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from database import Base, engine, get_session
from models import Tank
from services import (
    create_tank as create_tank_service, 
    get_tanks as get_tanks_service, 
    get_tank_by_id as get_tank_by_id_service,
    update_tank as update_tank_service,
    delete_tank as delete_tank_service)
from schemas import TankCreate, TankUpdate, TankRead

from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(engine)



@app.get('/')
def root():
    return {'message': 'Server is running'}

@app.get('/tanks', response_model=list[TankRead])
def get_tanks(
    fuel_type: str | None = None,
    sort: str | None = None,
    session: Session = Depends(get_session)
):
    return get_tanks_service(
        session,
        fuel_type=fuel_type,
        sort=sort
        )
    
@app.get('/tanks/{tank_id}', response_model=TankRead)
def get_tank(
    tank_id: int,
    session: Session = Depends(get_session)
):
    tank = get_tank_by_id_service(
        tank_id=tank_id,
        session=session
    )

    if tank is None:
        raise HTTPException(
            status_code=404,
            detail='Tank not found'
        )
    return tank

@app.post('/tanks', response_model=TankRead)
def create_tank(
    tank: TankCreate,
    session: Session = Depends(get_session)
    ):
    return create_tank_service(
        session=session,
        name=tank.name,
        measurement_date=tank.measurement_date,
        level_m=tank.level_m,
        fuel_type=tank.fuel_type,
        fuel_volume=tank.fuel_volume
    )


@app.put('/tanks/{tank_id}', response_model=TankRead)
def update_tank(
    tank_id: int,
    tank: TankUpdate,
    session: Session = Depends(get_session)
):
    update_tank = update_tank_service(
        session=session,
        tank_id=tank_id,
        name=tank.name,
        measurement_date=tank.measurement_date,
        level_m=tank.level_m,
        fuel_type=tank.fuel_type,
        fuel_volume=tank.fuel_volume
    )

    if update_tank is None:
        raise HTTPException(
            status_code=404,
            detail='Tank not found'
        )

    return update_tank

@app.delete('/tanks/{tank_id}', response_model=TankRead)
def delete_tank(
    tank_id: int,
    session: Session = Depends(get_session)
):
    deleted = delete_tank_service(
        session=session,
        tank_id=tank_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail='Tank not found'
        )

    return {'message': 'Tank deleted successfully'}
