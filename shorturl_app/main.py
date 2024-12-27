import string
import random
from typing import Optional
from fastapi import FastAPI, HTTPException, Request, Depends, APIRouter
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import URLItem


Base.metadata.create_all(bind=engine)

app = FastAPI()

urls_router_prefix = "/urls"
urls_router = APIRouter(prefix=urls_router_prefix)


class URLCreate(BaseModel):
    url: HttpUrl


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_short_id(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@app.post("/shorten")
def shorten_url(item: URLCreate, db: Session = Depends(get_db)):
    existing = db.query(URLItem).filter(URLItem.full_url == str(item.url)).first()
    if existing:
        return {"short_url": f"http://localhost:8000/{existing.short_id}"}
    else:
        for _ in range(10):
            short_id = generate_short_id()
            existing = db.query(URLItem).filter(URLItem.short_id == short_id).first()
            if not existing:
                new_item = URLItem(short_id=short_id, full_url=str(item.url))
                db.add(new_item)
                db.commit()
                db.refresh(new_item)
                return {"short_url": f"http://localhost:8000/{short_id}"}
        raise HTTPException(status_code=500, detail="Не удалось сгенерировать короткую ссылку")


@app.get("/")
def get_information():
    return {
        "message": "Добро пожаловать в приложение для сокращения ссылок.",
        "endpoints": [
            {
                "method": "GET",
                "path": "/",
                "description": "Информация о приложении"
            },
            {
                "method": "POST",
                "path": "/shorten",
                "description": "Создание короткой ссылки",
                "request_body": {
                    "url": "Полный URL-адрес для сокращения"
                }
            },
            {
                "method": "GET",
                "path": "/{short_id}",
                "description": "Перенаправление по короткой ссылке"
            },
            {
                "method": "GET",
                "path": "/stats/{short_id}",
                "description": "Получение статистики короткой ссылки"
            },
            {
                "method": "GET",
                "path": f"{urls_router_prefix}/all",
                "description": "Список всех созданных ссылок"
            },
            {
                "method": "DELETE",
                "path": "/delete/{short_id}",
                "description": "Удаление короткой ссылки"
            }
        ]
    }


@app.get("/{short_id}")
def redirect_to_full(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return RedirectResponse(url=url_item.full_url)


@app.get("/stats/{short_id}")
def get_stats(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return {
        "short_id": url_item.short_id,
        "full_url": url_item.full_url
    }


@app.delete("/delete/{short_id}")
def delete_url(short_id: str, db: Session = Depends(get_db)):
    url_item = db.query(URLItem).filter(URLItem.short_id == short_id).first()
    if not url_item:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    db.delete(url_item)
    db.commit()
    return {"message": f"Ссылка с идентификатором {short_id} успешно удалена"}


@urls_router.get("/all")
def get_all_urls(db: Session = Depends(get_db)):
    urls = db.query(URLItem).all()
    if not urls:
        return {"message": "Нет созданных ссылок"}
    else:
        return [
            {
                "short_id": url.short_id,
                "full_url": url.full_url
            }
            for url in urls
        ]


app.include_router(urls_router)
