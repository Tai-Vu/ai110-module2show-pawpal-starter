from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


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

    def mark_task_complete(self, task: Task) -> None:
        """Mark a task complete."""
        task.mark_complete()

    def build_daily_plan(self, owner: Optional[Owner] = None) -> List[Task]:
        """Create a daily plan from pending tasks."""
        return self.organize_tasks(owner)


SchedulePlanner = Scheduler
