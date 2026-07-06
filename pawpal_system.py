from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Owner:
    name: str
    email: str = ""
    availability_start: str = "08:00"
    availability_end: str = "20:00"
    preferences: List[str] = field(default_factory=list)

    def add_preference(self, preference: str) -> None:
        """Add a new preference to the owner's profile."""
        pass

    def update_availability(self, start: str, end: str) -> None:
        """Update the owner's available time window."""
        pass

    def get_preferences(self) -> List[str]:
        """Return the owner's preferences."""
        return []


@dataclass
class Pet:
    name: str
    species: str
    age: str = ""
    care_needs: List[str] = field(default_factory=list)
    health_notes: str = ""

    def add_care_need(self, need: str) -> None:
        """Add a care need for the pet."""
        pass

    def update_profile(self, age: Optional[str] = None, health_notes: Optional[str] = None) -> None:
        """Update the pet profile information."""
        pass

    def get_care_needs(self) -> List[str]:
        """Return the pet's care needs."""
        return []


@dataclass
class Task:
    title: str
    category: str
    duration_minutes: int
    priority: str = "medium"
    frequency: Optional[str] = None
    time_window: Optional[str] = None

    def update_details(
        self,
        duration_minutes: Optional[int] = None,
        priority: Optional[str] = None,
        frequency: Optional[str] = None,
        time_window: Optional[str] = None,
    ) -> None:
        """Update task details."""
        pass

    def is_high_priority(self) -> bool:
        """Return whether the task is high priority."""
        return False

    def matches_preferences(self, preferences: List[str]) -> bool:
        """Check whether the task matches the owner's preferences."""
        return False


@dataclass
class SchedulePlanner:
    owner: Owner
    pet: Pet
    tasks: List[Task] = field(default_factory=list)
    daily_time_limit: int = 480

    def generate_plan(self) -> List[dict]:
        """Generate a daily plan from the current tasks."""
        return []

    def sort_tasks(self) -> List[Task]:
        """Sort tasks according to priority and duration."""
        return []

    def filter_conflicts(self, tasks: List[Task]) -> List[Task]:
        """Remove tasks that conflict with the daily time limits."""
        return []

    def explain_plan(self, plan: List[dict]) -> List[str]:
        """Explain why each scheduled task was chosen."""
        return []
