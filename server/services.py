from models import Tank
from sqlalchemy import select

def create_tank(
        session,
        name,
        measurement_date,
        level_m,
        fuel_type,
        fuel_volume
):

    tank = Tank(
        name=name,
        measurement_date=measurement_date,
        level_m=level_m,
        fuel_type=fuel_type,
        fuel_volume=fuel_volume
    )

    try:
        session.add(tank)
        session.commit()
        session.refresh(tank)

        return tank

    except Exception:
        session.rollback()
        raise

def get_tanks(session, fuel_type=None, sort=None):
    statement = select(Tank)

    if fuel_type is not None:
        statement = statement.where(Tank.fuel_type == fuel_type)

    if sort == 'fuel_volume':
        statement = statement.order_by(Tank.fuel_volume)

    result = session.scalars(statement).all()

    return result

def get_tank_by_id(session, tank_id):
    statement = select(Tank).where(Tank.id == tank_id)

    tank = session.scalar(statement)

    return tank
    
def update_tank(
        session,
        tank_id,
        name,
        measurement_date,
        level_m,
        fuel_type,
        fuel_volume
):
    tank = session.scalar(
        select(Tank).where(Tank.id == tank_id)
    )

    if tank is None:
        return None

    tank.name = name
    tank.measurement_date = measurement_date
    tank.level_m = level_m
    tank.fuel_type = fuel_type
    tank.fuel_volume = fuel_volume

    try:
        session.commit()
        session.refresh(tank)

        return tank
    except Exception:
        session.rollback()
        raise

def delete_tank(
        session,
        tank_id
):
    tank = session.scalar(
        select(Tank).where(Tank.id == tank_id)
        )
    if tank is None:
        return False

    try:
        session.delete(tank)
        session.commit()

        return True
    
    except Exception:
        session.rollback()
        raise

