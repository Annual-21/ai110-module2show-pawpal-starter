import pytest
from datetime import date, time
from pawpal_system import User, Pet, Food, Walk, PawPalSystem

def test_user_add_and_remove_pet():
    user = User(username="alex", email="alex@example.com")
    pet = Pet(name="Buddy", age=4, breed="Labrador")

    user.add_pet(pet)

    assert pet in user.pets
    assert pet.owner is user
    assert user.get_pet_names() == ["Buddy"]
    assert user.get_pets() == [pet]

    user.remove_pet(pet)

    assert pet not in user.pets
    assert pet.owner is None
    assert user.get_pet_names() == []


def test_pet_add_food_and_walk_schedule():
    pet = Pet(name="Buddy", age=4, breed="Labrador")

    food_morning = Food(
        schedule_time=time(7, 30),
        title="Breakfast",
        nutrition_details="dry food",
        quantity="1 cup",
        recurrence="daily",
    )
    food_evening = Food(
        schedule_time=time(18, 0),
        title="Dinner",
        nutrition_details="wet food",
        quantity="1 cup",
        recurrence="daily",
    )
    walk_morning = Walk(date=date(2026, 4, 1), start_time=time(8, 0), duration_minutes=30, title="Morning Walk")
    walk_afternoon = Walk(date=date(2026, 4, 1), start_time=time(16, 0), duration_minutes=45, title="Afternoon Walk")

    pet.add_food(food_evening)
    pet.add_food(food_morning)
    pet.add_walk(walk_afternoon)
    pet.add_walk(walk_morning)

    assert food_morning.pet is pet
    assert food_evening.pet is pet
    assert walk_morning.pet is pet
    assert walk_afternoon.pet is pet

    assert pet.get_schedule() == [
        food_morning.summary(),
        food_evening.summary(),
        walk_morning.summary(),
        walk_afternoon.summary(),
    ]


def test_food_summary_output():
    food = Food(
        schedule_time=time(12, 15),
        title="Lunch",
        nutrition_details="protein rich",
        quantity="2 cups",
        recurrence="daily",
    )

    assert food.summary() == "Lunch at 12:15 (2 cups, protein rich, daily)"


def test_walk_end_time_and_summary():
    walk = Walk(date=date(2026, 4, 1), start_time=time(23, 30), duration_minutes=90, title="Late Walk")

    assert walk.end_time() == time(1, 0)
    assert walk.summary() == "Late Walk on 2026-04-01 at 23:30 for 90 minutes"


def test_pawpal_system_add_and_query_methods():
    system = PawPalSystem()
    user = User(username="mia", email="mia@example.com")
    pet = Pet(name="Luna", age=2, breed="Beagle", owner=user)
    user.add_pet(pet)

    system.add_user(user)
    system.add_pet(pet)

    assert user in system.users
    assert pet in system.pets
    assert system.get_pets_for_user(user) == [pet]
    assert system.get_pets_for_user(user)[0].owner is user

    food = Food(
        schedule_time=time(12, 0),
        title="Lunch",
        quantity="2 cups",
        nutrition_details="wet food",
        recurrence="daily",
        pet=pet,
    )
    walk = Walk(
        date=date(2026, 4, 2),
        start_time=time(15, 0),
        duration_minutes=20,
        title="Afternoon Walk",
        pet=pet,
    )

    system.add_food(food)
    system.add_walk(walk)

    assert food in system.foods
    assert walk in system.walks
    assert food in pet.food_schedule
    assert walk in pet.walks
    assert system.get_upcoming_food_for_pet(pet) == [food]
    assert system.get_upcoming_walks_for_pet(pet) == [walk]

def test_task_mark_complete():
    walk = Walk(date=date(2026, 4, 1), start_time=time(8, 0), duration_minutes=30, title="Morning Walk")

    assert walk.is_complete is False     # default from dataclass field

    walk.mark_complete()

    assert walk.is_complete is True      # mark_complete() flips the bool


def test_pet_task_count_increases_on_add():
    pet = Pet(name="Buddy", age=4, breed="Labrador")

    assert len(pet.walks) == 0           # pet.walks starts as empty list (your dataclass default)

    walk = Walk(date=date(2026, 4, 1), start_time=time(9, 0), duration_minutes=20, title="Quick Walk")
    pet.add_walk(walk)                   # your existing add_walk() method

    assert len(pet.walks) == 1           # list grew by 1
    assert walk in pet.walks     # correct walk was appended