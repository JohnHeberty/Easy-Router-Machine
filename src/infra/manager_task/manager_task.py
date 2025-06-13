import threading
import queue
import os

from src.infra.db.interfaces.connection_repository_interface import IDatabaseRepository
from src.infra.db.interfaces.manager_task_interface import IManagerTask

class Task:
    def __init__(self, query, return_):
        self.query = query
        self.return_ = return_
        self.result = None
        self.event = threading.Event()

    def set_result(self, result):
        self.result = result
        self.event.set()

class ManagerTask(IManagerTask):
    def __init__(self, database: IDatabaseRepository):
        self.Jobs_at_Queue = queue.Queue()
        self.InfoWorkers = {}
        self.database = database
        self.StartWorker()

    def add_task(self, query: str, return_: bool):
        task = Task(query, return_)
        self.Jobs_at_Queue.put(task)
        return task

    def StartWorker(self):
        for id in range(os.cpu_count() - 2):
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
        self.InfoWorkers[id]["OK"] = True
        while True:
            task = Jobs_at_Queue.get()
            if task.return_ == True:
                dataframe = self.database.run_query(task.query, task.return_)
                task.set_result(dataframe)
            else:
                status = self.database.run_query(task.query, task.return_)
                task.set_result(status)
   
