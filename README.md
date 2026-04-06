# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Smart Scheduling
Smart scheduling means planning pet care in a way that balances priority, timing, and owner availability so every important task gets done without overwhelming the day. In a pet care app, that looks like automatically ordering meals, walks, and meds by urgency and time window, avoiding conflicts, and filling only the minutes the owner has available. It also means using preferences—like morning walks or quiet evening feedings—so the schedule feels natural, and explaining why each task was placed where it was. The result is a reliable daily plan that helps busy owners keep pets happy and healthy with less guesswork.

## Testing PawPal+

### Run the tests
```bash
python -m pytest -v
```

### What the tests cover
- **Sorting correctness** — tasks added out of order return in chronological order
- **Recurrence logic** — daily/weekly walks auto-create the next occurrence on completion
- **Conflict detection** — duplicate times trigger warnings (walk vs walk, food vs walk)
- **Completion filtering** — completed and incomplete walks are correctly separated
- **Edge cases** — empty pet schedule, non-recurring tasks, unique time slots

### Confidence Level
(4/5) — Core scheduling logic is well covered. 
Would increase to 5/5 with additional tests for multi-pet systems and Streamlit UI interactions.

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
