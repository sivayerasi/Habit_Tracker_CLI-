from dataclasses import dataclass, field


VALID_STATUSES = {"done", "skipped"}


@dataclass
class Habit:
    id: str
    name: str
    description: str = ""
    created_at: str = ""

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Habit":
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            created_at=data.get("created_at", ""),
        )


@dataclass
class Log:
    habit_id: str
    date: str
    status: str  # "done" | "skipped"

    def __post_init__(self):
        if self.status not in VALID_STATUSES:
            raise ValueError(
                f"Invalid status '{self.status}'. Must be one of: {', '.join(VALID_STATUSES)}"
            )

    def to_dict(self) -> dict:
        return {
            "habit_id": self.habit_id,
            "date": self.date,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Log":
        return cls(
            habit_id=data["habit_id"],
            date=data["date"],
            status=data["status"],
        )
