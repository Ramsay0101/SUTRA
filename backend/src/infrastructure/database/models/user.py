import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..session import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("institution_id", "email", name="uq_institution_user_email"),
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
    # Group 2: Core Profile & Authentication
    # -------------------------------------------------------------------------
    custom_identifier: Mapped[str | None] = mapped_column(  # Institutional badge or roll number
        String(64),
        nullable=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )
    password_hash: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    auth_provider: Mapped[str] = mapped_column(
        String(32),
        default="local",  # "local", "google", "microsoft", "saml"
        nullable=False,
    )
    sso_subject_id: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )

    # -------------------------------------------------------------------------
    # Group 3: Security & Administrative Guardrails
    # -------------------------------------------------------------------------
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    is_superadmin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    must_change_password: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    is_mfa_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )
    mfa_secret: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )
    failed_login_attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    locked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    token_version: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    # -------------------------------------------------------------------------
    # Group 4: Extensible Metadata & Audit Timestamps
    # -------------------------------------------------------------------------
    metadata_: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
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