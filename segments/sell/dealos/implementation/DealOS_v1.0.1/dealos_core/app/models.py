import uuid
from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, Numeric, Boolean, JSON, ForeignKey, UniqueConstraint, Uuid
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

def uid(): return str(uuid.uuid4())
def now(): return datetime.now(timezone.utc)

class Organization(Base):
    __tablename__='organizations'
    id: Mapped[str]=mapped_column(Uuid(as_uuid=False),primary_key=True,default=uid)
    name: Mapped[str]=mapped_column(String,nullable=False)
    domain: Mapped[str|None]=mapped_column(String,unique=True)
    type: Mapped[str|None]=mapped_column(String)
    metadata_json: Mapped[dict]=mapped_column('metadata',JSON,default=dict)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,onupdate=now)

class Contact(Base):
    __tablename__='contacts'
    id: Mapped[str]=mapped_column(Uuid(as_uuid=False),primary_key=True,default=uid)
    organization_id: Mapped[str|None]=mapped_column(Uuid(as_uuid=False),ForeignKey('organizations.id'))
    email: Mapped[str|None]=mapped_column(String,unique=True)
    name: Mapped[str|None]=mapped_column(String)
    title: Mapped[str|None]=mapped_column(String)
    source: Mapped[str|None]=mapped_column(String)
    metadata_json: Mapped[dict]=mapped_column('metadata',JSON,default=dict)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,onupdate=now)

class Opportunity(Base):
    __tablename__='opportunities'
    __table_args__=(UniqueConstraint('source','external_id'),)
    id: Mapped[str]=mapped_column(Uuid(as_uuid=False),primary_key=True,default=uid)
    source: Mapped[str]=mapped_column(String,nullable=False)
    external_id: Mapped[str]=mapped_column(String,nullable=False)
    title: Mapped[str]=mapped_column(String,nullable=False)
    url: Mapped[str|None]=mapped_column(Text)
    description: Mapped[str|None]=mapped_column(Text)
    estimated_value_usd: Mapped[float|None]=mapped_column(Numeric)
    score: Mapped[float|None]=mapped_column(Numeric)
    risk_level: Mapped[str]=mapped_column(String,default='green')
    status: Mapped[str]=mapped_column(String,default='new')
    raw: Mapped[dict]=mapped_column(JSON,default=dict)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,onupdate=now)

class Deal(Base):
    __tablename__='deals'
    id: Mapped[str]=mapped_column(Uuid(as_uuid=False),primary_key=True,default=uid)
    opportunity_id: Mapped[str|None]=mapped_column(Uuid(as_uuid=False),ForeignKey('opportunities.id'))
    name: Mapped[str]=mapped_column(String,nullable=False)
    lane: Mapped[str|None]=mapped_column(String)
    stage: Mapped[str]=mapped_column(String,default='discovered')
    expected_value_usd: Mapped[float|None]=mapped_column(Numeric)
    recurring_monthly_usd: Mapped[float|None]=mapped_column(Numeric)
    probability: Mapped[float|None]=mapped_column(Numeric)
    risk_level: Mapped[str]=mapped_column(String,default='green')
    next_action: Mapped[str|None]=mapped_column(Text)
    metadata_json: Mapped[dict]=mapped_column('metadata',JSON,default=dict)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now,onupdate=now)

class Message(Base):
    __tablename__='messages'
    id: Mapped[str]=mapped_column(Uuid(as_uuid=False),primary_key=True,default=uid)
    deal_id: Mapped[str|None]=mapped_column(Uuid(as_uuid=False),ForeignKey('deals.id'))
    external_message_id: Mapped[str|None]=mapped_column(String,unique=True)
    thread_id: Mapped[str|None]=mapped_column(String)
    direction: Mapped[str]=mapped_column(String,nullable=False)
    sender: Mapped[str|None]=mapped_column(String)
    recipients: Mapped[list]=mapped_column(JSON,default=list)
    subject: Mapped[str|None]=mapped_column(Text)
    body_text: Mapped[str|None]=mapped_column(Text)
    classification: Mapped[dict]=mapped_column(JSON,default=dict)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class Outbox(Base):
    __tablename__='outbox'
    id: Mapped[str]=mapped_column(Uuid(as_uuid=False),primary_key=True,default=uid)
    deal_id: Mapped[str|None]=mapped_column(Uuid(as_uuid=False),ForeignKey('deals.id'))
    to_email: Mapped[str]=mapped_column(String,nullable=False)
    subject: Mapped[str|None]=mapped_column(Text)
    body_text: Mapped[str]=mapped_column(Text,nullable=False)
    reply_to_message_id: Mapped[str|None]=mapped_column(String)
    status: Mapped[str]=mapped_column(String,default='queued')
    risk_level: Mapped[str]=mapped_column(String,default='green')
    scheduled_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    sent_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict]=mapped_column('metadata',JSON,default=dict)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class Approval(Base):
    __tablename__='approvals'
    id: Mapped[str]=mapped_column(Uuid(as_uuid=False),primary_key=True,default=uid)
    deal_id: Mapped[str|None]=mapped_column(Uuid(as_uuid=False),ForeignKey('deals.id'))
    action_type: Mapped[str]=mapped_column(String,nullable=False)
    summary: Mapped[str]=mapped_column(Text,nullable=False)
    risk_level: Mapped[str]=mapped_column(String,default='orange')
    status: Mapped[str]=mapped_column(String,default='pending')
    payload: Mapped[dict]=mapped_column(JSON,default=dict)
    requested_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    decided_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    decided_by: Mapped[str|None]=mapped_column(String)

class Suppression(Base):
    __tablename__='suppressions'
    id: Mapped[str]=mapped_column(Uuid(as_uuid=False),primary_key=True,default=uid)
    email: Mapped[str]=mapped_column(String,nullable=False,unique=True)
    reason: Mapped[str]=mapped_column(String,nullable=False)
    source: Mapped[str|None]=mapped_column(String)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class ResearchJob(Base):
    __tablename__='research_jobs'
    id: Mapped[str]=mapped_column(Uuid(as_uuid=False),primary_key=True,default=uid)
    deal_id: Mapped[str|None]=mapped_column(Uuid(as_uuid=False),ForeignKey('deals.id'))
    opportunity_id: Mapped[str|None]=mapped_column(Uuid(as_uuid=False),ForeignKey('opportunities.id'))
    provider: Mapped[str]=mapped_column(String,default='openai')
    prompt: Mapped[str]=mapped_column(Text,nullable=False)
    structured_schema: Mapped[dict|None]=mapped_column(JSON)
    expected_value_usd: Mapped[float|None]=mapped_column(Numeric)
    status: Mapped[str]=mapped_column(String,default='queued')
    external_task_id: Mapped[str|None]=mapped_column(String)
    result: Mapped[dict|None]=mapped_column(JSON)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    submitted_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))

class ActionQueue(Base):
    __tablename__='action_queue'
    id: Mapped[str]=mapped_column(Uuid(as_uuid=False),primary_key=True,default=uid)
    deal_id: Mapped[str|None]=mapped_column(Uuid(as_uuid=False),ForeignKey('deals.id'))
    action_type: Mapped[str]=mapped_column(String,nullable=False)
    payload: Mapped[dict]=mapped_column(JSON,default=dict)
    risk_level: Mapped[str]=mapped_column(String,default='green')
    requires_approval: Mapped[bool]=mapped_column(Boolean,default=False)
    approval_id: Mapped[str|None]=mapped_column(Uuid(as_uuid=False),ForeignKey('approvals.id'))
    status: Mapped[str]=mapped_column(String,default='queued')
    result: Mapped[dict|None]=mapped_column(JSON)
    scheduled_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    completed_at: Mapped[datetime|None]=mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class AuditEvent(Base):
    __tablename__='audit_events'
    id: Mapped[str]=mapped_column(Uuid(as_uuid=False),primary_key=True,default=uid)
    actor: Mapped[str]=mapped_column(String,nullable=False)
    event_type: Mapped[str]=mapped_column(String,nullable=False)
    entity_type: Mapped[str|None]=mapped_column(String)
    entity_id: Mapped[str|None]=mapped_column(String)
    risk_level: Mapped[str|None]=mapped_column(String)
    payload: Mapped[dict]=mapped_column(JSON,default=dict)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)


class ModelUsage(Base):
    __tablename__='model_usage'
    id: Mapped[str]=mapped_column(Uuid(as_uuid=False),primary_key=True,default=uid)
    provider: Mapped[str]=mapped_column(String,nullable=False)
    model: Mapped[str|None]=mapped_column(String)
    task_type: Mapped[str|None]=mapped_column(String)
    input_tokens: Mapped[int|None]=mapped_column()
    output_tokens: Mapped[int|None]=mapped_column()
    estimated_cost_usd: Mapped[float|None]=mapped_column(Numeric)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
