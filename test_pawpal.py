import pytest
from datetime import date, time
from pawpal_system import User, Pet, Food, Walk, PawPalSystem, Scheduler


# ── Fixtures ──────────────────────────────────────────────────────
@pytest.fixture
def pet():
    return Pet(name="Buddy", age=4, breed="Labrador")

@pytest.fixture
def user():
    return User(username="alex", email="alex@example.com")


# ── User & Pet Ownership ──────────────────────────────────────────
def test_user_add_and_remove_pet(user):
    pet = Pet(name="Buddy", age=4, breed="Labrador")
    user.add_pet(pet)
    assert pet in user.pets
    assert pet.owner is user
    assert user.get_pet_names() == ["Buddy"]

    user.remove_pet(pet)
    assert pet not in user.pets
    assert pet.owner is None


# ── Sorting Correctness ───────────────────────────────────────────
def test_sort_by_time_returns_chronological_order(pet):
    """Happy path: tasks added out of order should come back sorted."""
    walk_evening   = Walk(date=date(2026, 4, 5), start_time=time(18, 0), duration_minutes=45, title="Evening Walk")
    walk_morning   = Walk(date=date(2026, 4, 5), start_time=time(7,  0), duration_minutes=30, title="Morning Walk")
    walk_afternoon = Walk(date=date(2026, 4, 5), start_time=time(13, 0), duration_minutes=20, title="Afternoon Walk")

    pet.add_walk(walk_evening)    # added first but latest
    pet.add_walk(walk_morning)    # added second but earliest
    pet.add_walk(walk_afternoon)

    scheduler = Scheduler(pet)
    schedule = scheduler.sort_by_time()

    assert schedule[0] == walk_morning.summary()
    assert schedule[1] == walk_afternoon.summary()
    assert schedule[2] == walk_evening.summary()


def test_sort_by_time_empty_pet(pet):
    """Edge case: pet with no tasks should return an empty list."""
    scheduler = Scheduler(pet)
    assert scheduler.sort_by_time() == []


def test_sort_includes_food_and_walks(pet):
    """Happy path: food and walks are sorted together by time."""
    walk = Walk(date=date(2026, 4, 5), start_time=time(9, 0), duration_minutes=30, title="Morning Walk")
    food = Food(schedule_time=time(7, 30), title="Breakfast", quantity="1 cup", nutrition_details="dry food")

    pet.add_walk(walk)
    pet.add_food(food)

    scheduler = Scheduler(pet)
    schedule = scheduler.sort_by_time()

    assert schedule[0] == food.summary()   # 07:30 comes before 09:00
    assert schedule[1] == walk.summary()


# ── Recurrence Logic ──────────────────────────────────────────────
def test_daily_recurrence_creates_next_day_walk(pet):
    """Happy path: completing a daily walk adds one for the next day."""
    walk = Walk(
        date=date(2026, 4, 5),
        start_time=time(8, 0),
        duration_minutes=30,
        title="Morning Walk",
        recurrence="daily",
    )
    pet.add_walk(walk)
    pet.mark_walk_complete(walk)

    assert len(pet.walks) == 2
    next_walk = pet.walks[1]
    assert next_walk.date == date(2026, 4, 6)       # exactly +1 day
    assert next_walk.is_complete is False            # starts fresh
    assert next_walk.recurrence == "daily"           # recurrence carried forward


def test_weekly_recurrence_creates_next_week_walk(pet):
    """Happy path: completing a weekly walk adds one 7 days later."""
    walk = Walk(
        date=date(2026, 4, 5),
        start_time=time(10, 0),
        duration_minutes=60,
        title="Long Walk",
        recurrence="weekly",
    )
    pet.add_walk(walk)
    pet.mark_walk_complete(walk)

    assert len(pet.walks) == 2
    assert pet.walks[1].date == date(2026, 4, 12)   # exactly +7 days


def test_no_recurrence_does_not_create_new_walk(pet):
    """Edge case: non-recurring walk should not add a new entry."""
    walk = Walk(
        date=date(2026, 4, 5),
        start_time=time(8, 0),
        duration_minutes=30,
        title="One-off Walk",
        recurrence="none",
    )
    pet.add_walk(walk)
    pet.mark_walk_complete(walk)

    assert len(pet.walks) == 1                       # no new walk added
    assert walk.is_complete is True


# ── Conflict Detection ────────────────────────────────────────────
def test_conflict_detected_for_two_walks_at_same_time(pet):
    """Happy path: two walks at identical times triggers a warning."""
    walk1 = Walk(date=date(2026, 4, 5), start_time=time(8, 0), duration_minutes=30, title="Morning Walk")
    walk2 = Walk(date=date(2026, 4, 5), start_time=time(8, 0), duration_minutes=15, title="Vet Check-in")

    pet.add_walk(walk1)
    pet.add_walk(walk2)

    scheduler = Scheduler(pet)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "08:00" in warnings[0]


def test_conflict_detected_between_food_and_walk(pet):
    """Edge case: food and walk at same time should also conflict."""
    walk = Walk(date=date(2026, 4, 5), start_time=time(13, 0), duration_minutes=20, title="Afternoon Walk")
    food = Food(schedule_time=time(13, 0), title="Lunch", quantity="1 cup", nutrition_details="wet food")

    pet.add_walk(walk)
    pet.add_food(food)

    scheduler = Scheduler(pet)
    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "13:00" in warnings[0]


def test_no_conflict_when_times_are_unique(pet):
    """Edge case: all different times should return no warnings."""
    pet.add_walk(Walk(date=date(2026, 4, 5), start_time=time(7,  0), duration_minutes=30, title="Morning Walk"))
    pet.add_walk(Walk(date=date(2026, 4, 5), start_time=time(13, 0), duration_minutes=20, title="Afternoon Walk"))
    pet.add_walk(Walk(date=date(2026, 4, 5), start_time=time(18, 0), duration_minutes=45, title="Evening Walk"))

    scheduler = Scheduler(pet)
    assert scheduler.detect_conflicts() == []


# ── Completion Status ─────────────────────────────────────────────
def test_mark_complete_flips_status(pet):
    walk = Walk(date=date(2026, 4, 5), start_time=time(8, 0), duration_minutes=30, title="Morning Walk")
    assert walk.is_complete is False
    walk.mark_complete()
    assert walk.is_complete is True


def test_filter_by_completion(pet):
    walk1 = Walk(date=date(2026, 4, 5), start_time=time(7,  0), duration_minutes=30, title="Morning Walk")
    walk2 = Walk(date=date(2026, 4, 5), start_time=time(13, 0), duration_minutes=20, title="Afternoon Walk")

    pet.add_walk(walk1)
    pet.add_walk(walk2)
    walk1.mark_complete()

    scheduler = Scheduler(pet)
    assert scheduler.filter_by_completion(complete=True)  == [walk1]
    assert scheduler.filter_by_completion(complete=False) == [walk2]


def test_pet_task_count_increases_on_add(pet):
    assert len(pet.walks) == 0
    pet.add_walk(Walk(date=date(2026, 4, 5), start_time=time(9, 0), duration_minutes=20, title="Quick Walk"))
    assert len(pet.walks) == 1