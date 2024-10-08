from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from sqlalchemy import select, insert, delete, update

from models.models import breed
from breed.schemas import Breed, BreedAdd

router = APIRouter()

@router.get("/", summary="Возвращает все породы", response_model=list[Breed])
async def get_breed(session : AsyncSession = Depends(get_async_session)):
    query = select(breed)
    result = await session.execute(query)
    return result.all()

@router.post("/", summary="Добавить породу")
async def post_addbreed(data: BreedAdd, session : AsyncSession = Depends(get_async_session)):
    query = insert(breed).values(**data.model_dump())
    await session.execute(query)
    await session.commit()
    return {"status": "success"}

@router.delete("/{id}", summary="Удаляет породу по id")
async def delete_breed(id: int, session : AsyncSession = Depends(get_async_session)):
    query = delete(breed).where(breed.c.breedID == id)
    await session.execute(query)
    await session.commit()
    return {"status": "success"}