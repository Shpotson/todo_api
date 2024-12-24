from datetime import datetime

import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from common.error import ValidationErrorResponse, NotFoundErrorResponse
from domain.tasks import TaskType, Task
from infrastructure.repositories.tasks.task_repository import TasksRepository, CommonRepositoryAnswers
from src.common.error import OptimisticConcurrencyErrorResponse

app = FastAPI()

tasks_repository = TasksRepository()

@app.get('/')
def root():
    data = "root"
    return PlainTextResponse(content=data, status_code = 200)

@app.get('/task/types')
def get_task_types():

    kinds = [TaskType.event, TaskType.regular, TaskType.deadline]

    json_data = jsonable_encoder(kinds)

    return JSONResponse(content=json_data, status_code = 200)

@app.get('/task')
def get_tasks_by_type(task_type:str):

    if not hasattr(TaskType, task_type):
        error_message = "Task type '" + task_type + "' not valid."
        return ValidationErrorResponse(error_message)

    tasks = tasks_repository.get_by_type(task_type)

    json_data = jsonable_encoder(tasks)

    return JSONResponse(content=json_data, status_code = 200)

@app.post('/task')
def add_task(type:str, name:str, description:str, to_date: datetime, from_date: datetime):

    if not hasattr(TaskType, type):
        error_message = "Task type '" + type + "' not valid."
        return ValidationErrorResponse(error_message)

    type_as_enum = TaskType(type)

    new_task = Task.create_new(
        name=name,
        description=description,
        to_date=to_date,
        from_date=from_date,
        task_type=type_as_enum
    )

    result = tasks_repository.upsert(new_task)

    if result == CommonRepositoryAnswers.optimistic_concurrency:
        return OptimisticConcurrencyErrorResponse()

    json_data = jsonable_encoder(new_task)

    return JSONResponse(content=json_data, status_code = 200)

@app.get('/task/{pk}')
def get_task_by_id(id:str):

    task = tasks_repository.get_by_id(id)

    if task is None:
        error_message = "Task with id '" + id + "' not found."
        return NotFoundErrorResponse(error_message)

    json_data = jsonable_encoder(task)

    return JSONResponse(content=json_data, status_code = 200)

@app.patch('/task')
def update_task(id:str, type:str, name:str, description:str, to_date: datetime, from_date: datetime | None):
    
    if not hasattr(TaskType, type):
        error_message = "Task type '" + type + "' not valid."
        return ValidationErrorResponse(error_message)

    type_as_enum = TaskType(type)

    task = tasks_repository.get_by_id(id)

    if task is None:
        error_message = "Task with pk '" + id + "' not found."
        return NotFoundErrorResponse(error_message)

    task.udpate(
        name=name,
        task_type=type_as_enum,
        description=description,
        to_date=to_date,
        from_date=from_date,
    )

    result = tasks_repository.upsert(task)

    if result == CommonRepositoryAnswers.optimistic_concurrency:
        return OptimisticConcurrencyErrorResponse()

    json_data = jsonable_encoder(task)

    return JSONResponse(content=json_data, status_code=200)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)