from __future__ import annotations
from asyncio import tasks
from asyncio import tasks
import warnings
"""
PawPalSystem module defines a lightweight pet management system for tracking users, pets, food schedules, and walks.

Classes:
- User: represents an account with username, email, pet list, and preferences. Supports adding and removing pets and retrieving pet data.
- Pet: represents an animal with metadata, owner reference, food schedule, and walk schedule. Supports attaching food and walk entries and summarizing the combined schedule.
- Food: represents a timed meal or feeding event with nutrition details, quantity, recurrence, and an optional pet association.
- Walk: represents a scheduled walk with date, time, duration, completion state, and optional pet association.
- PawPalSystem: manages collections of users, pets, foods, and walks, ensuring bidirectional relationships are maintained and providing query methods for pet tasks and schedules.

This module is designed to support basic pet care workflow management with sortable schedules and simple ownership relationships.
"""

from ast import walk
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

    def get_pet_names(self) -> List[str]:
        return [pet.name for pet in self.pets]

    def get_pets(self) -> List["Pet"]:
        return list(self.pets)


@dataclass
class Pet:
    name: str
    age: int
    breed: str
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
            
    def mark_walk_complete(self, walk: "Walk") -> None:
        """Mark a walk complete and auto-schedule next if recurring."""
        next_walk = walk.mark_complete()   # returns new Walk or None
        if next_walk:
            self.add_walk(next_walk)

    def get_schedule(self) -> List[str]:
        schedule = [food.summary() for food in sorted(self.food_schedule)]
        schedule += [walk.summary() for walk in sorted(self.walks)]
        return schedule


@dataclass(order=True)
class Food:
    schedule_time: time
    title: str = "Meal"
    nutrition_details: str = ""
    quantity: str = ""
    recurrence: str = "daily"
    pet: Optional[Pet] = None
    notes: str = ""

    def summary(self) -> str:
        return (
            f"{self.title} at {self.schedule_time.strftime('%H:%M')}"
            f" ({self.quantity}, {self.nutrition_details}, {self.recurrence})"
        )


@dataclass(order=True)
class Walk:
    date: date
    start_time: time
    duration_minutes: int
    title: str = "Walk"
    pet: Optional[Pet] = None
    notes: str = ""
    is_complete: bool = False
    recurrence: str = "none"

    def mark_complete(self) -> Optional["Walk"]:
        self.is_complete = True
        if self.recurrence == "daily":
            next_date = self.date + timedelta(days=1)      # today + 1 day
        elif self.recurrence == "weekly":
            next_date = self.date + timedelta(weeks=1)     # today + 7 days
        else:
            return None   # no recurrence, nothing to create

        # Create and return the next occurrence
        return Walk(
            date=next_date,
            start_time=self.start_time,
            duration_minutes=self.duration_minutes,
            title=self.title,
            notes=self.notes,
            recurrence=self.recurrence,   # carry forward the recurrence
            is_complete=False,            # new task starts incomplete
        )
    def end_time(self) -> time:
        start_dt = datetime.combine(self.date, self.start_time)
        end_dt = start_dt + timedelta(minutes=self.duration_minutes)
        return end_dt.time()

    def summary(self) -> str:
        return (
            f"{self.title} on {self.date.isoformat()} at {self.start_time.strftime('%H:%M')}"
            f" for {self.duration_minutes} minutes"
        )


class PawPalSystem:
    def __init__(self):
        self.users: List[User] = []
        self.pets: List[Pet] = []
        self.foods: List[Food] = []
        self.walks: List[Walk] = []

    def add_user(self, user: User) -> None:
        if user not in self.users:
            self.users.append(user)

    def add_pet(self, pet: Pet) -> None:
        if pet not in self.pets:
            self.pets.append(pet)
            if pet.owner and pet not in pet.owner.pets:
                pet.owner.add_pet(pet)

    def add_food(self, food: Food) -> None:
        if food not in self.foods:
            self.foods.append(food)
            if food.pet:
                food.pet.add_food(food)

    def add_walk(self, walk: Walk) -> None:
        if walk not in self.walks:
            self.walks.append(walk)
            if walk.pet:
                walk.pet.add_walk(walk)

    def get_tasks_for_pet(self, pet: Pet) -> List[str]:
        return pet.get_schedule()

    def get_pets_for_user(self, user: User) -> List[Pet]:
        return user.get_pets()

    def get_upcoming_food_for_pet(self, pet: Pet) -> List[Food]:
        return sorted(pet.food_schedule)

    def get_upcoming_walks_for_pet(self, pet: Pet) -> List[Walk]:
        return sorted(pet.walks)
    
class Scheduler:
    """A scheduler class for managing and organizing a pet's food and walk schedules, including sorting tasks by time, filtering walks by completion status, and detecting time conflicts."""
        
    """Initialize the Scheduler with a pet object.
        Args:
            pet (Pet): The pet whose schedules are to be managed.
        """
    """Sort all tasks by time using a unified sort key. Cached for performance.
        Returns:
            List[str]: A list of task summaries sorted by their scheduled time.
        """
    """Return walks that match the given completion status.
        Args:
            complete (bool): True to filter completed walks, False for incomplete.
        Returns:
            List[Walk]: A list of Walk objects matching the completion status.
        """
    """Detect time conflicts using a hash map (O(n) instead of O(n²)).
        Returns:
            List[str]: A list of warning messages for conflicting time slots.
        """
    def __init__(self, pet: Pet):
        self.pet = pet
        self._cached_schedule = None

    def sort_by_time(self) -> List[str]:
        """Sort all tasks by time using a unified sort key. Cached for performance."""
        if self._cached_schedule is None:
            all_tasks = self.pet.food_schedule + self.pet.walks
            def sort_key(task):
                if hasattr(task, 'schedule_time'):
                    return task.schedule_time   # Food
                return task.start_time          # Walk

            self._cached_schedule = [task.summary() for task in sorted(all_tasks, key=sort_key)]
        return self._cached_schedule

    def filter_by_completion(self, complete: bool) -> List[Walk]:
        """Return walks that match the given completion status."""
        return [walk for walk in self.pet.walks if walk.is_complete == complete]

    def detect_conflicts(self) -> List[str]:
        """Detect time conflicts using a hash map (O(n) instead of O(n²))."""
        time_slots = {}
        # Group food and walks by time
        for food in self.pet.food_schedule:
            if food.schedule_time not in time_slots:
                time_slots[food.schedule_time] = []
            time_slots[food.schedule_time].append(("food", food.title))
    
        for walk in self.pet.walks:
            if walk.start_time not in time_slots:
                time_slots[walk.start_time] = []
            time_slots[walk.start_time].append(("walk", walk.title))
        # Flag slots with multiple tasks
        warnings = []
        for time_slot, tasks in time_slots.items():
            if len(tasks) > 1:
                task_names = ", ".join([f"{t[1]} ({t[0]})" for t in tasks])
                warnings.append(
                    f"⚠ Conflict at {time_slot.strftime('%H:%M')}: {task_names} for {self.pet.name}"
                    )
        return warnings
