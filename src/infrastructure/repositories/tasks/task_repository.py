import sqlite3
from datetime import datetime
from enum import Enum

from domain.tasks import Task, TaskType


class CommonRepositoryAnswers(str, Enum):
    done = "done"
    optimistic_concurrency = "optimistic_concurrency"

class TasksRepository:
    def __init__(self):
        self.db_tasks: [] = []
        self.db_root = "../app/data/data.db"
        self.table_name = "tasks"
        self.migrate()


    def migrate(self):
        con = sqlite3.connect(self.db_root)
        cur = con.cursor()

        table_check_result = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")

        tables_exist = table_check_result.fetchall()

        for table in tables_exist:
            if table[0] == self.table_name:
                return

        cur.execute(
            "CREATE TABLE tasks(id UNIQUE, type, name, created_at, updated_at, description, to_date, from_date);"
        )

    def get_by_type(self, task_type):
        tasks_to_return = []

        con = sqlite3.connect(self.db_root)
        cur = con.cursor()

        get_result = cur.execute("SELECT * FROM tasks WHERE type = ?", (task_type,))

        answers = get_result.fetchall()

        for i in range(len(answers)):
            task_db = answers[i]
            if task_type == task_db[1]:
                task = Task.create_from_db(
                    task_id=task_db[0],
                    task_type=TaskType(task_db[1]),
                    name=task_db[2],
                    created_at=datetime.fromisoformat(task_db[3]),
                    updated_at=datetime.fromisoformat(task_db[4]),
                    description=task_db[5],
                    to_date=datetime.fromisoformat(task_db[6]),
                    from_date=datetime.fromisoformat(task_db[7]),
                )

                tasks_to_return.append(task)

        return tasks_to_return

    def get_by_id(self, id):
        con = sqlite3.connect(self.db_root)
        cur = con.cursor()

        get_result = cur.execute("SELECT * FROM tasks WHERE id = ?", (id,))

        answers = get_result.fetchall()

        for i in range(len(answers)):
            task_db = answers[i]
            if id == task_db[0]:
                task = Task.create_from_db(
                    task_id = task_db[0],
                    task_type = TaskType(task_db[1]),
                    name = task_db[2],
                    created_at = datetime.fromisoformat(task_db[3]),
                    updated_at = datetime.fromisoformat(task_db[4]),
                    description = task_db[5],
                    to_date = datetime.fromisoformat(task_db[6]),
                    from_date = datetime.fromisoformat(task_db[7]),
                )

                return task

        return None

    def upsert(self, task_updated):
        con = sqlite3.connect(self.db_root)
        cur = con.cursor()

        upsert_result = cur.execute(
            "INSERT INTO tasks(id,name,type,created_at,updated_at,description,to_date,from_date)" +
            " VALUES(" +
                    "'" + task_updated.Id + "',"
                    "'" + task_updated.Name + "',"
                    "'" + task_updated.Type.value + "',"
                    "'" + task_updated.CreatedAt.isoformat() + "',"
                    "'" + task_updated.UpdatedAt.isoformat() + "',"
                    "'" + task_updated.Description + "',"
                    "'" + task_updated.ToDate.isoformat() + "',"
                    "'" + task_updated.FromDate.isoformat() + "')"
            " ON CONFLICT(id) DO UPDATE" +
            " SET type         =excluded.type," +
                " name         =excluded.name," +
                " updated_at   =date('now')," +
                " description  =excluded.description," +
                " to_date      =excluded.to_date," +
                " from_date    =excluded.from_date" +
            " WHERE excluded.updated_at = updated_at" +
            " RETURNING id;")

        if upsert_result is None:
            con.rollback()
            return CommonRepositoryAnswers.optimistic_concurrency

        answer = upsert_result.fetchone()
        if  (upsert_result.rowcount != 1) | (answer[0] != task_updated.Id):
            con.rollback()
            print("Answer: " + str(answer))
            return CommonRepositoryAnswers.optimistic_concurrency

        con.commit()
        return CommonRepositoryAnswers.done
