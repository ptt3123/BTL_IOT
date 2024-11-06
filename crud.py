from sqlalchemy import desc

from database import SessionLocal, Data, Action


def read_data(txt: str, pagesize: int, page: int, item: str = "", order: str = "") -> tuple[list[Data], int] :
    session = SessionLocal()

    if txt == "":
        query = session.query(Data)
        total_count = query.count()

    else:
        query = session.query(Data).filter(Data.tim.icontains(txt))
        total_count = query.count()

    limit = pagesize
    offset = (page - 1) * pagesize
    if item == "tem":
        if order == "desc":
            result = query.order_by(desc(Data.tem)).offset(offset).limit(limit).all()
        else:
            result = query.order_by(Data.tem).offset(offset).limit(limit).all()
    elif item == "hum":
        if order == "desc":
            result = query.order_by(desc(Data.hum)).offset(offset).limit(limit).all()
        else:
            result = query.order_by(Data.hum).offset(offset).limit(limit).all()
    elif item == "lig":
        if order == "desc":
            result = query.order_by(desc(Data.lig)).offset(offset).limit(limit).all()
        else:
            result = query.order_by(Data.lig).offset(offset).limit(limit).all()
    else:
        if order == "desc":
            result = query.order_by(desc(Data.id)).offset(offset).limit(limit).all()
        else:
            result = query.order_by(Data.id).offset(offset).limit(limit).all()
    session.close()
    return result, total_count


def create_data(data: dict) -> None:
    session = SessionLocal()
    new_data = Data(tem=data.get("tem"),hum=data.get("hum"),lig=data.get("lig"),tim=data.get("tim"))
    session.add(new_data)
    session.commit()
    session.close()
    return


def read_action(txt: str, pagesize: int, page: int) -> tuple[list[Action], int]:
    session = SessionLocal()

    if txt == "":
        query = session.query(Action)
        total_count = query.count()

    else:
        query = session.query(Action).filter(Action.tim.icontains(txt))
        total_count = query.count()

    query = query.offset((page - 1) * pagesize).limit(pagesize)
    result = query.all()
    session.close()
    return result, total_count


def create_action(data: dict) -> None:
    session = SessionLocal()
    new_action = Action(hw=data.get("hw"),act=data.get("act"))
    session.add(new_action)
    session.commit()
    session.close()
    return