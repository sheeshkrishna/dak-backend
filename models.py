from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB



class Attachments(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    dak_id: Optional[uuid.UUID] = Field(default=None, foreign_key="dak_documents.id")
    file_name: str
    file_size: int
    file_type: str
    file_path: str
    uploaded_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)

class AuditLogs(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    table_name: str
    record_id: uuid.UUID
    action: str  # Check constraint: INSERT/UPDATE/DELETE (not supported in ORM)
    old_values: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    new_values: Optional[dict] = Field(default=None, sa_column=Column(JSONB))
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    ip_address: Optional[str] = None  # inet type in Postgres, use str
    user_agent: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Departments(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    code: str
    head_name: Optional[str] = None
    head_email: Optional[str] = None
    branch: str = Field(default="main")
    is_active: Optional[bool] = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Users(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    auth_user_id: Optional[uuid.UUID] = Field(default=None)  # FK but to auth module, may omit FK here
    name: str
    email: str
    role: str  # Check role values: admin, officer, clerk, viewer
    department_id: Optional[uuid.UUID] = Field(default=None, foreign_key="departments.id")
    branch: str = Field(default="main")
    is_active: Optional[bool] = True
    last_login: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class DakDocuments(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    dak_number: str
    reference_number: Optional[str] = None
    type: str  # Check values: inward/outward
    subject: str
    sender: str
    sender_address: Optional[str] = None
    receiver: Optional[str] = None
    receiver_address: Optional[str] = None
    department_id: Optional[uuid.UUID] = Field(default=None, foreign_key="departments.id")
    branch: str = Field(default="main")
    priority: str  # low, medium, high, urgent
    status: str  # received, under_process, forwarded, closed, escalated, draft, sent
    date_received: Optional[datetime] = Field(default_factory=datetime.utcnow)
    date_sent: Optional[datetime] = None
    due_date: Optional[datetime] = None
    content: Optional[str] = None
    remarks: Optional[str] = None
    created_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    assigned_to: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Escalations(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    dak_id: Optional[uuid.UUID] = Field(default=None, foreign_key="dak_documents.id")
    escalation_level: int = Field(default=1)
    escalated_to: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    escalated_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    reason: str
    status: str  # active, resolved, cancelled
    escalated_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None

class MovementLogs(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    dak_id: Optional[uuid.UUID] = Field(default=None, foreign_key="dak_documents.id")
    action: str
    from_department_id: Optional[uuid.UUID] = Field(default=None, foreign_key="departments.id")
    to_department_id: Optional[uuid.UUID] = Field(default=None, foreign_key="departments.id")
    from_user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    to_user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    remarks: Optional[str] = None
    action_by: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    action_at: datetime = Field(default_factory=datetime.utcnow)

class Notifications(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    dak_id: Optional[uuid.UUID] = Field(default=None, foreign_key="dak_documents.id")
    title: str
    message: str
    type: str  # info, warning, error, success
    is_read: Optional[bool] = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

