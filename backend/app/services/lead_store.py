from dataclasses import dataclass
from datetime import datetime
from threading import Lock
from uuid import UUID

from app.models.lead import LeadCreate, LeadQualification


@dataclass(frozen=True)
class StoredLead:
    id: UUID
    data: LeadCreate
    received_at: datetime
    qualification: LeadQualification | None = None


class InMemoryLeadStore:
    """Temporary in-memory store; PostgreSQL can replace this later."""

    def __init__(self) -> None:
        self._leads: dict[UUID, StoredLead] = {}
        self._lock = Lock()

    def save(
        self,
        lead_id: UUID,
        data: LeadCreate,
        received_at: datetime,
        qualification: LeadQualification | None = None,
    ) -> None:
        with self._lock:
            self._leads[lead_id] = StoredLead(
                id=lead_id,
                data=data,
                received_at=received_at,
                qualification=qualification,
            )

    def count(self) -> int:
        with self._lock:
            return len(self._leads)

    def clear(self) -> None:
        with self._lock:
            self._leads.clear()


lead_store = InMemoryLeadStore()