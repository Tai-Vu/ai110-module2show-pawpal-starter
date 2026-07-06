from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


RECURRING_FREQUENCIES = {"daily", "weekly", "monthly"}


@dataclass
class Task:
    description: str
    scheduled_time: str = "09:00"
    frequency: str = "once"
    completed: bool = False
    priority: str = "medium"

    def update_details(
        self,
        description: Optional[str] = None,
        scheduled_time: Optional[str] = None,
        frequency: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> None:
        """Update the task details."""
        if description is not None:
            self.description = description
        if scheduled_time is not None:
            self.scheduled_time = scheduled_time
        if frequency is not None:
            self.frequency = frequency
        if priority is not None:
            self.priority = priority

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def create_next_occurrence(self) -> "Task":
        """Create a new pending task for the next occurrence of a recurring task."""
        return Task(
            description=self.description,
            scheduled_time=self.scheduled_time,
            frequency=self.frequency,
            priority=self.priority,
        )

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completed = False

    def is_complete(self) -> bool:
        """Return whether the task is complete."""
        return self.completed

    def is_pending(self) -> bool:
        """Return whether the task is still pending."""
        return not self.completed

    def to_dict(self) -> Dict[str, object]:
        """Return the task as a dictionary."""
        return {
            "description": self.description,
            "scheduled_time": self.scheduled_time,
            "frequency": self.frequency,
            "completed": self.completed,
            "priority": self.priority,
        }

    def _time_to_minutes(self) -> int:
        """Convert the scheduled time into minutes for ordering."""
        try:
            hour_text, minute_text = self.scheduled_time.split(":")
            return int(hour_text) * 60 + int(minute_text)
        except ValueError:
            return 24 * 60


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[str] = None
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the pet."""
        if task not in self.tasks:
            self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        """Return tasks for the pet, optionally filtered by completion status."""
        if completed is None:
            return list(self.tasks)
        return [task for task in self.tasks if task.completed is completed]

    def get_pending_tasks(self) -> List[Task]:
        """Return pending tasks for the pet."""
        return self.get_tasks(completed=False)

    def get_completed_tasks(self) -> List[Task]:
        """Return completed tasks for the pet."""
        return self.get_tasks(completed=True)

    def update_profile(self, age: Optional[str] = None, species: Optional[str] = None) -> None:
        """Update the pet profile information."""
        if age is not None:
            self.age = age
        if species is not None:
            self.species = species


@dataclass
class Owner:
    name: str
    email: str = ""
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        if pet not in self.pets:
            self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from the owner."""
        if pet in self.pets:
            self.pets.remove(pet)

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Return a pet by name if it exists."""
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet
        return None

    def get_all_tasks(self, completed: Optional[bool] = None) -> List[Task]:
        """Return all tasks across the owner's pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks(completed=completed))
        return tasks

    def get_pending_tasks(self) -> List[Task]:
        """Return all pending tasks across the owner's pets."""
        return self.get_all_tasks(completed=False)

    def get_completed_tasks(self) -> List[Task]:
        """Return all completed tasks across the owner's pets."""
        return self.get_all_tasks(completed=True)


@dataclass
class Scheduler:
    owner: Optional[Owner] = None

    def set_owner(self, owner: Owner) -> None:
        """Set the owner for the scheduler."""
        self.owner = owner

    def get_all_tasks(self, owner: Optional[Owner] = None) -> List[Task]:
        """Return all tasks for the selected owner."""
        active_owner = owner or self.owner
        if active_owner is None:
            return []
        return active_owner.get_all_tasks()

    def get_pending_tasks(self, owner: Optional[Owner] = None) -> List[Task]:
        """Return pending tasks for the selected owner."""
        active_owner = owner or self.owner
        if active_owner is None:
            return []
        return active_owner.get_pending_tasks()

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks ordered by their scheduled time in minutes."""
        # How could this algorithm be simplified for better readability or performance?
        return sorted(tasks, key=lambda task: task._time_to_minutes())

    def organize_tasks(self, owner: Optional[Owner] = None) -> List[Task]:
        """Arrange pending tasks by time and priority."""
        tasks = self.get_pending_tasks(owner)
        priority_rank = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            tasks,
            key=lambda task: (
                task._time_to_minutes(),
                priority_rank.get(task.priority.lower(), 1),
                task.description.lower(),
            ),
        )

    def filter_tasks(
        self,
        tasks: List[Task],
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
        owner: Optional[Owner] = None,
    ) -> List[Task]:
        """Return a filtered subset of tasks by pet name and/or completion status."""
        active_owner = owner or self.owner
        filtered_tasks = list(tasks)

        if completed is not None:
            filtered_tasks = [task for task in filtered_tasks if task.completed is completed]

        if pet_name is not None:
            if active_owner is None:
                return []
            pet = active_owner.get_pet(pet_name)
            if pet is None:
                return []
            filtered_tasks = [task for task in filtered_tasks if task in pet.get_tasks()]

        return filtered_tasks

    def get_tasks_for_pet(self, pet_name: str, owner: Optional[Owner] = None, completed: Optional[bool] = None) -> List[Task]:
        """Return tasks for a specific pet, optionally filtered by completion state."""
        active_owner = owner or self.owner
        if active_owner is None:
            return []
        pet = active_owner.get_pet(pet_name)
        if pet is None:
            return []
        return pet.get_tasks(completed=completed)

    def get_recurring_tasks(self, owner: Optional[Owner] = None) -> List[Task]:
        """Return tasks that are marked as recurring such as daily or weekly tasks."""
        tasks = self.get_all_tasks(owner)
        return [task for task in tasks if task.frequency.lower() in RECURRING_FREQUENCIES]

    def detect_conflicts(self, tasks: List[Task]) -> List[tuple[Task, Task]]:
        """Detect tasks that share the same scheduled time."""
        conflicts: List[tuple[Task, Task]] = []
        for index, first_task in enumerate(tasks):
            for second_task in tasks[index + 1 :]:
                if first_task._time_to_minutes() == second_task._time_to_minutes():
                    conflicts.append((first_task, second_task))
        return conflicts

    def get_conflict_warning(self, owner: Optional[Owner] = None) -> Optional[str]:
        """Return a lightweight warning message when conflicting tasks are found."""
        try:
            active_owner = owner or self.owner
            if active_owner is None:
                return None

            all_tasks = active_owner.get_all_tasks()
            conflicts = self.detect_conflicts(all_tasks)
            if not conflicts:
                return None

            first_task, second_task = conflicts[0]
            return (
                f"Warning: overlapping tasks detected at {first_task.scheduled_time} "
                f"for {first_task.description} and {second_task.description}."
            )
        except Exception:
            return "Warning: could not check for task conflicts."

    def organize_tasks_by_pet(self, owner: Optional[Owner] = None) -> Dict[str, List[Task]]:
        """Group pending tasks by pet name."""
        active_owner = owner or self.owner
        if active_owner is None:
            return {}

        grouped_tasks: Dict[str, List[Task]] = {}
        for pet in active_owner.pets:
            grouped_tasks[pet.name] = pet.get_pending_tasks()
        return grouped_tasks

    def add_task_to_pet(self, pet_name: str, task: Task, owner: Optional[Owner] = None) -> bool:
        """Attach a task to a named pet for the selected owner."""
        active_owner = owner or self.owner
        if active_owner is None:
            return False
        pet = active_owner.get_pet(pet_name)
        if pet is None:
            return False
        pet.add_task(task)
        return True

    def mark_task_complete(
        self,
        task: Task,
        pet_name: Optional[str] = None,
        owner: Optional[Owner] = None,
    ) -> Optional[Task]:
        """Mark a task complete and create a new pending task for daily or weekly tasks."""
        task.mark_complete()
        if task.frequency.lower() in {"daily", "weekly"}:
            next_task = task.create_next_occurrence()
            active_owner = owner or self.owner
            if active_owner is not None and pet_name is not None:
                pet = active_owner.get_pet(pet_name)
                if pet is not None:
                    pet.add_task(next_task)
                    return next_task
            return next_task
        return None

    def build_daily_plan(self, owner: Optional[Owner] = None) -> List[Task]:
        """Create a daily plan from pending tasks."""
        return self.organize_tasks(owner)


SchedulePlanner = Scheduler
