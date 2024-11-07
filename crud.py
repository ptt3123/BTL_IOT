from sqlalchemy import desc

from database import SessionLocal, Data, Action


def read_data(txt: str, pagesize: int, page: int, item: str = "", order: str = "") -> tuple[list[Data], int] :
    session = SessionLocal()

    if txt == "":
        query = session.query(Data)

    else:
        query = session.query(Data).filter(Data.tim.icontains(txt))

    total_count = query.count()

    if item == "tem":
        if order == "desc":
            result = query.order_by(desc(Data.tem))
        else:
            result = query.order_by(Data.tem)
    elif item == "hum":
        if order == "desc":
            result = query.order_by(desc(Data.hum))
        else:
            result = query.order_by(Data.hum)
    elif item == "lig":
        if order == "desc":
            result = query.order_by(desc(Data.lig))
        else:
            result = query.order_by(Data.lig)
    else:
        if order == "asc":
            result = query.order_by(Data.tim)
        else:
            result = query.order_by(desc(Data.tim))

    limit = pagesize
    offset = (page - 1) * pagesize
    result = result.offset(offset).limit(limit).all()
    session.close()
    return result, total_count


def create_data(data: dict) -> None:
    session = SessionLocal()
    new_data = Data(tem=data.get("tem"),hum=data.get("hum"),ws=data.get("ws"),
                    lig=data.get("lig"),tim=data.get("tim"))
    session.add(new_data)
    session.commit()
    session.close()
    return


def read_action(txt: str, pagesize: int, page: int, item: str, order: str) -> tuple[list[Action], int]:
    session = SessionLocal()

    if txt == "":
        query = session.query(Action)

    else:
        query = session.query(Action).filter(Action.tim.icontains(txt))

    if not item or not order:
        print("None")

    if item != "all":
        query = query.filter(Action.hw == item)

    if order != "all":
        query = query.filter(Action.act == order)

    total_count = query.count()
    limit = pagesize
    offset = (page - 1) * pagesize

    result = query.order_by(desc(Action.tim)).offset(offset).limit(limit).all()
    session.close()
    return result, total_count


def create_action(data: dict) -> None:
    session = SessionLocal()
    new_action = Action(hw=data.get("hw"),act=data.get("act"))
    session.add(new_action)
    session.commit()
    session.close()
    return


