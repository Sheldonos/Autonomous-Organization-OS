insert into audit_events(actor,event_type,entity_type,payload)
values ('system','schema_initialized','system','{"version":"1.0.0"}'::jsonb);
