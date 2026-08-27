"""
USSD Session model — tracks menu navigation state.

Each time a user dials *123#, a session is created.
The session stores which screen they're on and accumulated input.
Sessions expire after 3 minutes of inactivity.
"""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, Text, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from .base import Base


class USSDSession(Base):
    __tablename__ = "ussd_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    session_id: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False,
        comment="Session ID from the USSD gateway"
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True,
        comment="Null if user hasn't registered yet"
    )
    phone_number: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True
    )

    # ── Menu State ──────────────────────────────────────────────────
    current_screen: Mapped[str] = mapped_column(
        String(50), default="main_menu",
        comment="Current USSD screen/menu"
    )
    accumulated_input: Mapped[str | None] = mapped_column(
        Text, nullable=True,
        comment="JSON string of accumulated user input across screens"
    )
    menu_depth: Mapped[int] = mapped_column(
        Integer, default=0,
        comment="How deep in the menu tree (0 = main menu)"
    )

    # ── Status ──────────────────────────────────────────────────────
    is_active: Mapped[bool] = mapped_column(default=True)
    last_request_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # ── Timestamps ──────────────────────────────────────────────────
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # ── Relationships ───────────────────────────────────────────────
    user: Mapped["User"] = relationship("User", back_populates="ussd_sessions")

    def __repr__(self) -> str:
        return f"<USSDSession {self.session_id[:8]} phone={self.phone_number} screen={self.current_screen}>"
