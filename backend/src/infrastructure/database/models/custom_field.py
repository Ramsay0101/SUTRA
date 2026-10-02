import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from ....domain.models.enums import CustomFieldType
from ..session import Base


class CustomFieldDefinition(Base):
    __tablename__ = "custom_field_definitions"
    __table_args__ = (
        UniqueConstraint(
            "institution_id",
            "collection_id",
            "field_key",
            name="uq_institution_collection_field",
        ),
    )

    # -------------------------------------------------------------------------
    # Group 1: Primary Key & Tenant Isolation Anchors
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
    collection_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("entity_collections.id", ondelete="CASCADE"),
        nullable=True,
        index=True,  # Scoped to an Entity Table (None = global/master scope)
    )

    # -------------------------------------------------------------------------
    # Group 2: Field Metadata & Taxonomy
    # -------------------------------------------------------------------------
    field_key: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,  # e.g., 'roll_number', 'dorm_block', 'thesis_advisor_id'
    )
    label: Mapped[str] = mapped_column(
        String(128),
        nullable=False,  # e.g., 'Roll Number', 'Dormitory Block', 'Thesis Advisor'
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    field_type: Mapped[CustomFieldType] = mapped_column(
        Enum(CustomFieldType, name="custom_field_type"),
        nullable=False,
        index=True,
    )

    # -------------------------------------------------------------------------
    # Group 3: Dynamic Validation & Suite Governance
    # -------------------------------------------------------------------------
    validation_rules: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,  # e.g., {"required": true, "options": ["North", "South"], "min": 0}
    )
    visibility_suites: Mapped[list] = mapped_column(
        JSONB,
        default=lambda: ["command"],
        nullable=False,  # Suites permitted to view/edit (e.g. ["command", "instruction"])
    )

    # -------------------------------------------------------------------------
    # Group 4: Audit Timestamps
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
