create extension if not exists pgcrypto;
create extension if not exists vector;

create table if not exists organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  domain text,
  type text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create unique index if not exists organizations_domain_uq on organizations(lower(domain)) where domain is not null;

create table if not exists contacts (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid references organizations(id) on delete set null,
  email text,
  name text,
  title text,
  source text,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create unique index if not exists contacts_email_uq on contacts(lower(email)) where email is not null;

create table if not exists opportunities (
  id uuid primary key default gen_random_uuid(),
  source text not null,
  external_id text not null,
  title text not null,
  url text,
  description text,
  response_deadline timestamptz,
  estimated_value_usd numeric,
  score numeric,
  risk_level text not null default 'green',
  status text not null default 'new',
  raw jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(source, external_id)
);
create index if not exists opportunities_status_score_idx on opportunities(status, score desc);

create table if not exists deals (
  id uuid primary key default gen_random_uuid(),
  opportunity_id uuid references opportunities(id) on delete set null,
  organization_id uuid references organizations(id) on delete set null,
  name text not null,
  lane text,
  stage text not null default 'discovered',
  expected_value_usd numeric,
  recurring_monthly_usd numeric,
  probability numeric check(probability is null or (probability >= 0 and probability <= 1)),
  risk_level text not null default 'green',
  next_action text,
  next_action_at timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists deals_stage_idx on deals(stage);

create table if not exists messages (
  id uuid primary key default gen_random_uuid(),
  deal_id uuid references deals(id) on delete set null,
  external_message_id text,
  thread_id text,
  direction text not null check(direction in ('inbound','outbound')),
  sender text,
  recipients jsonb not null default '[]'::jsonb,
  subject text,
  body_text text,
  classification jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);
create unique index if not exists messages_external_uq on messages(external_message_id) where external_message_id is not null;

create table if not exists outbox (
  id uuid primary key default gen_random_uuid(),
  deal_id uuid references deals(id) on delete set null,
  to_email text not null,
  subject text,
  body_text text not null,
  reply_to_message_id text,
  status text not null default 'queued',
  risk_level text not null default 'green',
  scheduled_at timestamptz not null default now(),
  sent_at timestamptz,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);
create index if not exists outbox_dispatch_idx on outbox(status, scheduled_at);

create table if not exists approvals (
  id uuid primary key default gen_random_uuid(),
  deal_id uuid references deals(id) on delete set null,
  action_type text not null,
  summary text not null,
  risk_level text not null default 'orange',
  status text not null default 'pending',
  payload jsonb not null default '{}'::jsonb,
  requested_at timestamptz not null default now(),
  decided_at timestamptz,
  decided_by text,
  expires_at timestamptz
);
create index if not exists approvals_pending_idx on approvals(status, requested_at);

create table if not exists suppressions (
  id uuid primary key default gen_random_uuid(),
  email text not null,
  reason text not null,
  source text,
  created_at timestamptz not null default now()
);
create unique index if not exists suppressions_email_uq on suppressions(lower(email));

create table if not exists research_jobs (
  id uuid primary key default gen_random_uuid(),
  deal_id uuid references deals(id) on delete set null,
  opportunity_id uuid references opportunities(id) on delete set null,
  provider text not null default 'openai',
  prompt text not null,
  structured_schema jsonb,
  expected_value_usd numeric,
  status text not null default 'queued',
  external_task_id text,
  result jsonb,
  created_at timestamptz not null default now(),
  submitted_at timestamptz,
  completed_at timestamptz
);
create index if not exists research_queue_idx on research_jobs(provider, status, created_at);

create table if not exists action_queue (
  id uuid primary key default gen_random_uuid(),
  deal_id uuid references deals(id) on delete set null,
  action_type text not null,
  payload jsonb not null default '{}'::jsonb,
  risk_level text not null default 'green',
  requires_approval boolean not null default false,
  approval_id uuid references approvals(id) on delete set null,
  status text not null default 'queued',
  result jsonb,
  scheduled_at timestamptz not null default now(),
  completed_at timestamptz,
  created_at timestamptz not null default now()
);
create index if not exists action_queue_idx on action_queue(status, scheduled_at);

create table if not exists knowledge_facts (
  id uuid primary key default gen_random_uuid(),
  subject_type text not null,
  subject_id text not null,
  predicate text not null,
  value jsonb not null,
  source_uri text,
  confidence numeric,
  valid_until timestamptz,
  created_at timestamptz not null default now()
);
create index if not exists knowledge_subject_idx on knowledge_facts(subject_type, subject_id, predicate);

create table if not exists audit_events (
  id uuid primary key default gen_random_uuid(),
  actor text not null,
  event_type text not null,
  entity_type text,
  entity_id text,
  risk_level text,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);
create index if not exists audit_events_time_idx on audit_events(created_at desc);

create table if not exists model_usage (
  id uuid primary key default gen_random_uuid(),
  provider text not null,
  model text,
  task_type text,
  input_tokens bigint,
  output_tokens bigint,
  estimated_cost_usd numeric,
  created_at timestamptz not null default now()
);
