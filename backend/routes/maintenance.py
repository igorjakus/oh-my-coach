from fastapi import APIRouter, Depends
from sqlmodel import Session, delete

from backend.config import engine
from backend.models import Goal, PersonalisedAgent, Task

maintenance_router = APIRouter()


def get_session():
    with Session(engine) as session:
        yield session


@maintenance_router.delete("/clear-database")
async def clear_database(session: Session = Depends(get_session)):
    """Clear all data from the database"""
    session.exec(delete(Task))
    session.exec(delete(Goal))
    session.exec(delete(PersonalisedAgent))
    session.commit()
    return {"ok": True}