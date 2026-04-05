from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time, datetime, timedelta
from typing import List, Optional


@dataclass
class User:
    username: str
    email: str
    pets: List["Pet"] = field(default_factory=list)
    preferences: dict[str, str] = field(default_factory=dict)

    def add_pet(self, pet: "Pet") -> None:
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner = self

    def remove_pet(self, pet: "Pet") -> None:
        if pet in self.pets:
            self.pets.remove(pet)
            pet.owner = None

    def update_preference(self, key: str, value: str) -> None:
        self.preferences[key] = value

    def get_pet_names(self) -> List[str]:
        return [pet.name for pet in self.pets]


@dataclass
class Pet:
    name: str
    species: str
    age_years: Optional[float] = None
    breed: Optional[str] = None
    owner: Optional[User] = None
    food_schedule: List["Food"] = field(default_factory=list)
    walks: List["Walk"] = field(default_factory=list)

    def add_food(self, food: "Food") -> None:
        if food not in self.food_schedule:
            self.food_schedule.append(food)
            food.pet = self

    def add_walk(self, walk: "Walk") -> None:
        if walk not in self.walks:
            self.walks.append(walk)
            walk.pet = self

    def upcoming_activities(self) -> List[str]:
        activities: List[str] = []
        for food in sorted(self.food_schedule):
            activities.append(food.summary())
        for walk in sorted(self.walks):
            activities.append(walk.summary())
        return activities


@dataclass(order=True)
class Food:
    meal_time: time
    title: str = "Meal"
    nutrition_details: str = ""
    quantity: str = ""
    recurrence: str = "daily"
    pet: Optional[Pet] = None
    notes: str = ""

    def summary(self) -> str:
        return (
            f"{self.title} at {self.meal_time.strftime('%H:%M')}"
            f" ({self.nutrition_details}, {self.quantity}, {self.recurrence})"
        )

    def schedule_text(self) -> str:
        pet_name = self.pet.name if self.pet else "pet"
        return f"Feed {pet_name}: {self.summary()}"


@dataclass(order=True)
class Walk:
    date: date
    start_time: time
    duration_minutes: int
    title: str = "Walk"
    pet: Optional[Pet] = None
    notes: str = ""

    def end_time(self) -> time:
        start_dt = datetime.combine(self.date, self.start_time)
        end_dt = start_dt + timedelta(minutes=self.duration_minutes)
        return end_dt.time()

    def summary(self) -> str:
        pet_name = self.pet.name if self.pet else "pet"
        return (
            f"{self.title} for {pet_name} on {self.date.isoformat()}"
            f" at {self.start_time.strftime('%H:%M')} for {self.duration_minutes} min"
        )
