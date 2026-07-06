# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What PawPal+ does

PawPal+ helps a pet owner manage care tasks for one or more pets with a simple scheduling system. The app combines a Streamlit interface with a Python scheduler that can:

- Organize tasks chronologically by scheduled time
- Prioritize higher-importance tasks when building a daily plan
- Flag overlapping schedules with conflict warnings
- Create new pending occurrences for recurring tasks such as daily, weekly, or monthly routines
- Filter tasks by pet or completion state for easier review

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Features

- Sorting by time: pending tasks are ordered by their scheduled time for a clean daily view.
- Priority-aware planning: the scheduler uses priority levels to keep essential tasks near the top of the plan.
- Conflict warnings: duplicate or overlapping times trigger a warning so scheduling conflicts are visible.
- Daily recurrence: completing a recurring task creates a fresh pending task for the next occurrence.
- Pet-specific filtering: tasks can be reviewed by pet name or completion status.

## 🧪 Testing PawPal+

Run the full test suite with:

```bash
python -m pytest
```

These tests cover the core scheduler behaviors, including chronological task ordering, recurring-task creation after completion, and conflict detection for duplicate scheduled times.

Successful test run output:

```text
============================= test session starts ==============================
platform win32 -- Python 3.14.5, pytest-9.0.3, pluggy-1.6.0
rootdir: C:\Users\taidu\ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 10 items

tests\test_pawpal.py ..........                                          [100%]

============================= 10 passed in 0.09s ==============================
```

Confidence Level: ★★★★★

## Demo Walkthrough

PawPal+ provides a simple dashboard for managing pet care tasks. A user can enter owner and pet information, add tasks with a scheduled time and priority, and immediately see how the scheduler organizes the day.

1. Open the Streamlit app and enter an owner name, pet name, and species.
2. Add one or more tasks such as a walk, feeding, or vet visit with a time and priority.
3. Review the task list and the scheduler's sorted pending tasks, which are displayed in chronological order.
4. If two tasks share the same scheduled time, the app shows a conflict warning so the user can adjust the plan.
5. When a recurring task is marked complete, the scheduler creates a new pending occurrence for the next cycle.

Example workflow:
- Add a pet named Mochi.
- Schedule a morning walk at 08:00 with high priority.
- Add a feeding task at 07:30.
- Generate the daily plan and view the sorted schedule.

Sample CLI output from running the main script:

```text
Today's Schedule
================
Sorted pending tasks:
- 07:30: Feed breakfast (high)
- 08:00: Morning walk (high)
- 14:00: Vet appointment (medium)

Mochi pending tasks:
- 07:30: Feed breakfast (high)
- 08:00: Morning walk (high)

Warning: overlapping tasks detected at 08:00 for Morning walk and Play session.

Created next occurrence:
- 08:00: Morning walk (high)
```
