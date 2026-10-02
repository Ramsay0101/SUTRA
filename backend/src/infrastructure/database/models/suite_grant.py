import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from ....domain.models.enums import SuiteCategory
from ..session import Base


class SuiteGrant(Base):
    __tablename__ = "suite_grants"
    __table_args__ = (
        CheckConstraint(
            "(collection_id IS NOT NULL AND user_id IS NULL) OR "
            "(collection_id IS NULL AND user_id IS NOT NULL)",
            name="chk_grant_target",
        ),
    )

    # -------------------------------------------------------------------------
    # Group 1: Primary Key & Tenant Isolation Anchor
    # -------------------------------------------------------------------------
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    institution_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("institutions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # -------------------------------------------------------------------------
    # Group 2: Capability Suite & Target Invariant
    # -------------------------------------------------------------------------
    suite: Mapped[SuiteCategory] = mapped_column(
        Enum(SuiteCategory, name="suite_category"),
        nullable=False,
        index=True,
    )

    # Target A: Table-Level Inheritance (Entire collection inherits this suite)
    collection_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("entity_collections.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    # Target B: Row-Level Direct User Grant (Explicit grant to single user)
    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    # -------------------------------------------------------------------------
    # Group 3: Audit Trail & Timestamps
    # -------------------------------------------------------------------------
    granted_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )