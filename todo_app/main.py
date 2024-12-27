from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import TodoItem as TodoItemModel

Base.metadata.create_all(bind=engine)

app = FastAPI()


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False


class TodoItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/item", response_model=TodoItem)
def create_item(item: TodoCreate, db: Session = Depends(get_db)):
    new_item = TodoItemModel(
        title=item.title,
        description=item.description,
        completed=item.completed
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/")
def get_information():
    return {
        "message": "Добро пожаловать в приложение для управления задачами.",
        "endpoints": [
            {
                "method": "GET",
                "path": "/",
                "description": "Информация о приложении"
            },
            {
                "method": "POST",
                "path": "/item",
                "description": "Создание новой задачи",
                "request_body": {
                    "title": "Название задачи (строка, обязательное)",
                    "description": "Описание задачи (строка, необязательное)",
                    "completed": "Статус завершения задачи (булево, необязательное, по умолчанию False)"
                }
            },
            {
                "method": "GET",
                "path": "/items",
                "description": "Получение списка всех задач"
            },
            {
                "method": "GET",
                "path": "/item/{item_id}",
                "description": "Получение информации о задаче по идентификатору"
            },
            {
                "method": "GET",
                "path": "/items/incomplete",
                "description": "Получение списка незавершённых задач"
            },
            {
                "method": "GET",
                "path": "/items/completed",
                "description": "Получение списка завершённых задач"
            },
            {
                "method": "GET",
                "path": "/items/stats",
                "description": "Получение статистики по задачам"
            },
            {
                "method": "GET",
                "path": "/items/search",
                "description": "Поиск задач по названию и/или описанию",
                "query_parameters": {
                    "title": "Название для поиска (строка, необязательное)",
                    "description": "Описание для поиска (строка, необязательное)"
                }
            },
            {
                "method": "PUT",
                "path": "/item/{item_id}",
                "description": "Обновление информации о задаче по идентификатору",
                "request_body": {
                    "title": "Новое название задачи (строка, обязательное)",
                    "description": "Новое описание задачи (строка, необязательное)",
                    "completed": "Новый статус завершения задачи (булево, необязательное)"
                }
            },
            {
                "method": "PATCH",
                "path": "/item/{item_id}/status",
                "description": "Обновление статуса завершения задачи по идентификатору",
                "query_parameters": {
                    "completed": "Статус завершения задачи (булево, обязательное)"
                }
            },
            {
                "method": "DELETE",
                "path": "/item/{item_id}",
                "description": "Удаление задачи по идентификатору"
            }
        ]
    }


@app.get("/items", response_model=List[TodoItem])
def get_items(db: Session = Depends(get_db)):
    items = db.query(TodoItemModel).all()
    return items


@app.get("/item/{item_id}", response_model=TodoItem)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/items/incomplete", response_model=List[TodoItem])
def get_incomplete_items(db: Session = Depends(get_db)):
    incomplete_items = db.query(TodoItemModel).filter(TodoItemModel.completed == False).all()
    return incomplete_items


@app.get("/items/completed", response_model=List[TodoItem])
def get_incomplete_items(db: Session = Depends(get_db)):
    incomplete_items = db.query(TodoItemModel).filter(TodoItemModel.completed == True).all()
    return incomplete_items


@app.get("/items/stats")
def get_stats(db: Session = Depends(get_db)):
    total_items = db.query(TodoItemModel).count()
    completed_items = db.query(TodoItemModel).filter(TodoItemModel.completed == True).count()
    return {
        "Всего": total_items,
        "Завершённых": completed_items,
        "Незавершённых": total_items - completed_items
    }


@app.get("/items/search", response_model=List[TodoItem])
def search_items(title: Optional[str] = None, description: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(TodoItemModel)

    if title:
        query = query.filter(TodoItemModel.title.ilike(f"%{title}%"))

    if description:
        query = query.filter(TodoItemModel.description.ilike(f"%{description}%"))

    items = query.all()
    return items


@app.put("/item/{item_id}", response_model=TodoItem)
def update_item(item_id: int, item: TodoCreate, db: Session = Depends(get_db)):
    db_item = db.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.title = item.title
    db_item.description = item.description
    db_item.completed = item.completed
    db.commit()
    db.refresh(db_item)
    return db_item


@app.patch("/item/{item_id}/status", response_model=TodoItem)
def update_item_status(item_id: int, completed: bool, db: Session = Depends(get_db)):
    db_item = db.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.completed = completed
    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/item/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(TodoItemModel).filter(TodoItemModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {
        "message": f"Задача с идентификатором {item_id} успешно удалена"
    }
