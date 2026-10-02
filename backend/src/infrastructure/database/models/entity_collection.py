import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Index, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..session import Base


class EntityCollection(Base):
    __tablename__ = "entity_collections"
    __table_args__ = (
        UniqueConstraint("institution_id", "table_key", name="uq_institution_entity_table"),
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
    # Group 2: Collection Metadata & Identifiers
    # -------------------------------------------------------------------------
    table_key: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,  # e.g., "students", "faculty", "guardians", "visiting_scholars"
    )
    display_name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,  # e.g., "Undergraduate Students", "Faculty & Lecturers"
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # -------------------------------------------------------------------------
    # Group 3: Audit Timestamps
    # -------------------------------------------------------------------------
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


class EntityMembership(Base):
    __tablename__ = "entity_memberships"
    __table_args__ = (
        UniqueConstraint("user_id", "collection_id", name="uq_user_collection"),
        Index("idx_entity_memberships_attributes", "custom_attributes", postgresql_using="gin"),
    )

    # -------------------------------------------------------------------------
    # Group 1: Primary Key & Relational Anchors
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
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    collection_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("entity_collections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # -------------------------------------------------------------------------
    # Group 2: Dynamic Custom Fields (Indexed JSONB Container)
    # -------------------------------------------------------------------------
    custom_attributes: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Group 3: Audit Timestamps
    # -------------------------------------------------------------------------
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
