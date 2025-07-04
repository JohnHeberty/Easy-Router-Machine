import threading
import queue
import os

from src.infra.db.interfaces.connection_repository_interface import IDatabaseRepository
from src.infra.db.interfaces.manager_task_interface import IManagerTask

class Task:
    def __init__(self, query, return_, connection_id: int = 0):
        self.query = query
        self.return_ = return_
        self.connection_id = connection_id
        self.result = None
        self.event = threading.Event()

    def set_result(self, result):
        self.result = result
        self.event.set()

class ManagerTask(IManagerTask):
    def __init__(self, databases: IDatabaseRepository):
        self.Jobs_at_Queue = queue.Queue()
        self.InfoWorkers = {}
        self.databases = databases
        self.StartWorker()

    def add_task(self, query: str, return_: bool, connection_id: int = 0):
        task = Task(query, return_, connection_id)
        self.Jobs_at_Queue.put(task)
        return task

    def StartWorker(self):
        #for id in range(os.cpu_count() - 2):
        for id in range(1): # uma Thread
            self.InfoWorkers[id] = {}
            self.InfoWorkers[id]["Thread"] = threading.Thread(
                target=self.Worker,
                args=(
                    id,
                    self.Jobs_at_Queue,
                ),
                daemon=True,
            )
            self.InfoWorkers[id]["Thread"].start()
            while True:
                if "OK" in self.InfoWorkers[id]:
                    if self.InfoWorkers[id]["OK"]:
                        break

    def Worker(self, id, Jobs_at_Queue):
        db_routes = self.databases.get_connection_db_routes()
        db_locales = self.databases.get_connection_db_locales()

        self.InfoWorkers[id]["OK"] = True
        try:
            while True:
                task = Jobs_at_Queue.get()

                if task.connection_id == 0:
                    db_conn = db_routes
                elif task.connection_id == 1:
                    db_conn = db_locales

                if task.return_:
                    result = self.databases.run_query(db_conn, task.query, task.return_)
                    task.set_result(result)
                else:
                    status = self.databases.run_query(db_conn, task.query, task.return_)
                    task.set_result(status)

        finally:
            db_routes.close()
