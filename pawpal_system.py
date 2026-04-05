from dataclasses import dataclass

@dataclass
class Pet:
    name: str
    age: int
    breed: str
    owner: str

    def feed(self):
        pass

    def play(self):
        pass

    def groom(self):
        pass

@dataclass
class Task:
    description: str
    due_date: str
    priority: str
    pet: Pet

    def complete(self):
        pass

    def update(self):
        pass

class PawPalSystem:
    def __init__(self):
        self.pets = []
        self.tasks = []

    def add_pet(self, pet: Pet):
        pass

    def add_task(self, task: Task):
        pass

    def get_tasks_for_pet(self, pet: Pet):
        pass