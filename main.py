from datetime import date, time
from pawpal_system import User, Pet, Food, Walk, PawPalSystem, Scheduler

user = User(username="alex", email="alex@example.com")
pet = Pet(name="Buddy", age=4, breed="Labrador")
user.add_pet(pet)

# 2. Add walks OUT OF ORDER
walk_evening   = Walk(date=date(2026, 4, 5), start_time=time(18, 0), duration_minutes=45, title="Evening Walk", recurrence="daily")
walk_morning   = Walk(date=date(2026, 4, 5), start_time=time(7, 0),  duration_minutes=30, title="Morning Walk", recurrence="daily")
walk_afternoon = Walk(date=date(2026, 4, 5), start_time=time(13, 0), duration_minutes=20, title="Afternoon Walk")

# 3. Add TWO tasks at the SAME time to trigger conflict
walk_conflict  = Walk(date=date(2026, 4, 5), start_time=time(7, 0),  duration_minutes=15, title="Vet Check-in")
food_conflict  = Food(schedule_time=time(13, 0), title="Lunch", quantity="1 cup", nutrition_details="dry food", recurrence="daily")

pet.add_walk(walk_evening)
pet.add_walk(walk_morning)
pet.add_walk(walk_afternoon)
pet.add_walk(walk_conflict)    # same time as walk_morning  → conflict
pet.add_food(food_conflict)    # same time as walk_afternoon → conflict

# 4. Sort and print schedule
scheduler = Scheduler(pet)

print("=== Sorted Schedule ===")
for item in scheduler.sort_by_time():
    print(f"  - {item}")

# 5. Detect and print conflicts
print("\n=== Conflict Detection ===")
warnings = scheduler.detect_conflicts()
if warnings:
    for warning in warnings:
        print(f"  {warning}")
else:
    print("  No conflicts found.")

# 6. Filter by completion
walk_morning.mark_complete()

print("\n=== Completed Tasks ===")
for walk in scheduler.filter_by_completion(complete=True):
    print(f"  ✓ {walk.summary()}")

print("\n=== Incomplete Tasks ===")
for walk in scheduler.filter_by_completion(complete=False):
    print(f"  ✗ {walk.summary()}")