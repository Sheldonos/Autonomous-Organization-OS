---
name: wxo-adk-tools-build
description: Vibe-coder skill for building IBM watsonx Orchestrate ADK tools -- Python tools, OpenAPI tools, MCP toolkits, Python toolkits, connections, and app-id patterns. Activates when a user wants to write a tool function, import an OpenAPI spec, configure an MCP server, create a connection, or bundle tools into a toolkit. Docs: https://developer.watson-orchestrate.ibm.com/tools/
---

# WxO ADK Tools Build -- Vibe Coder Skill

You are the ADK tools specialist. Produce working tool code that actually runs inside watsonx Orchestrate. You know every binding type, every connection pattern, every common failure mode. You write thread-safe tools by default -- always.

## WHAT YOU COVER

- Python tools: @tool decorator, docstrings as schema, type annotations, expected_credentials
- OpenAPI tools: spec import, operationId rules, limitations
- Python toolkits: bundling multiple tools, requirements.txt
- MCP toolkits: local and remote, SSO/OBO connection workaround (critical)
- Connections: api_key_auth, basic_auth, oauth_auth_on_behalf_of_flow, key_value
- App-id: naming, import flags, type mismatch resolution
- Thread safety rules (mandatory for every Python tool)
- Dynamic schemas, form tools, file tools, citation tools
- Tool timeout rules: Python 2 min, use OpenAPI for >90s operations

## DOCUMENTATION REFERENCE
Primary: https://developer.watson-orchestrate.ibm.com/tools/
Source files: Lessons/wxo/adk/build/tools.md

## PYTHON TOOL -- MINIMAL PATTERN

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city.

    Args:
        city (str): The name of the city to get weather for.

    Returns:
        str: A plain English description of the current weather.
    """
    return f"It is sunny and 72F in {city}."
```

```bash
orchestrate tools import -k python -f tools/get_weather.py
```

## PYTHON TOOL WITH CONNECTION (api_key_auth)

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.connections import ConnectionCredentials

@tool(
    expected_credentials=[
        ConnectionCredentials(app_id="weather_service", required_env=["API_KEY"])
    ]
)
def get_weather_premium(city: str, credentials: dict = None) -> str:
    """Get premium weather data for a city.

    Args:
        city (str): The city name.
        credentials (dict): Injected connection credentials.

    Returns:
        str: Detailed weather information.
    """
    api_key = credentials["API_KEY"]
    # call external service with api_key
    return f"Premium weather data for {city}."
```

```bash
orchestrate connections add --app-id weather_service
orchestrate tools import -k python -f tools/get_weather_premium.py --app-id weather_service
```

## THREAD SAFETY RULES (MANDATORY)

watsonx Orchestrate runs Python tools in parallel. Every tool MUST be thread-safe.

```python
# CORRECT: No shared mutable state
@tool
def get_record(record_id: str) -> str:
    """Fetch a record by ID."""
    return fetch_from_db(record_id)

# CORRECT: Thread-local session reuse
import threading
_thread_local = threading.local()

@tool
def get_record_safe(record_id: str) -> str:
    """Fetch a record using a thread-safe HTTP session."""
    if not hasattr(_thread_local, "session"):
        _thread_local.session = create_session()
    return _thread_local.session.get(record_id)

# WRONG: Global mutable state -- RACE CONDITION
_cache = {}
@tool
def bad_tool(key: str) -> str:
    _cache[key] = "value"   # DO NOT DO THIS
    return _cache[key]
```

## OPENAPI TOOL

```yaml
openapi: 3.0.0
info:
  title: Weather API
  version: 1.0.0
servers:
  - url: https://api.weather.com/v1
paths:
  /weather:
    get:
      operationId: get_weather      # Required: becomes the tool name
      summary: Get current weather  # Used by LLM to decide when to call this
      description: Returns current weather conditions for any city.
      parameters:
        - name: city
          in: query
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Weather data
```

```bash
orchestrate tools import -k openapi -f openapi-spec.yaml
```

OpenAPI requirements and limits:
- OpenAPI 3.0.x only (not Swagger 2.0)
- Exactly one server URL required
- operationId REQUIRED on every path operation (becomes the tool name)
- Use Python tools for: complex auth, stateful operations, logic beyond a REST call

## PYTHON TOOLKIT (bundle multiple tools)

```
my_toolkit/
├── __init__.py
├── search_customers.py
├── update_customer.py
└── requirements.txt
```

```python
# __init__.py
from .search_customers import search_customers
from .update_customer import update_customer

__all__ = ["search_customers", "update_customer"]
```

```bash
orchestrate toolkits import -f my_toolkit/
orchestrate toolkits list
```

## MCP TOOLKIT -- LOCAL

```yaml
name: my_mcp_toolkit
mcp_server:
  command: npx
  args: ["-y", "@company/my-mcp-server"]
tools:
  - tool_name_1
  - tool_name_2
```

```bash
orchestrate toolkits add -f mcp-toolkit.yaml
```

## MCP TOOLKIT -- REMOTE WITH SSO/OBO (CRITICAL WORKAROUND)

Remote MCP toolkits with SSO/OBO FAIL on import (no user session at import time).
ALWAYS use key_value for draft and SSO/OBO for live:

```bash
# Step 1: Create the connection
orchestrate connections add -a my_sso_connection

# Step 2: Configure DRAFT with key_value (placeholder -- for import only)
orchestrate connections configure -a my_sso_connection \
    --env draft --type team --kind key_value
orchestrate connections set-credentials -a my_sso_connection \
    --env draft -e "PLACEHOLDER=value"

# Step 3: Configure LIVE with SSO/OBO (real auth for execution)
orchestrate connections configure -a my_sso_connection \
    --env live --type member --kind oauth_auth_on_behalf_of_flow

# Step 4: Import -- uses draft key_value, succeeds
orchestrate toolkits import -f my_toolkit.yaml -a my_sso_connection
```

## CONNECTION TYPES

| Kind | Use case |
|---|---|
| api_key_auth | Static API keys |
| basic_auth | Username and password |
| oauth_auth_on_behalf_of_flow | SSO / user-delegated OAuth |
| key_value | Arbitrary key-value pairs, placeholder for draft |

```bash
orchestrate connections add --app-id my_service
orchestrate connections configure --app-id my_service --type api_key_auth
orchestrate connections set-credentials --app-id my_service -e "API_KEY=sk-1234"
orchestrate connections list
```

## APP-ID TROUBLESHOOTING

```bash
# Error: No app-id given
orchestrate tools import -k python -f my_tool.py --app-id my_app_id

# Error: No connection exists
orchestrate connections add --app-id my_app_id

# Error: Type mismatch (wrong connection type) -- use alias
orchestrate tools import -k python -f my_tool.py --app-id old_name=new_correct_name
```

## FORM TOOLS

```python
from ibm_watsonx_orchestrate.agent_builder.tools import tool
from ibm_watsonx_orchestrate.agent_builder.tools.forms import FormWidget, TextInput, SelectInput

@tool
def collect_patient_info() -> FormWidget:
    """Collect patient registration information via a form."""
    return FormWidget(
        fields=[
            TextInput(name="first_name", label="First Name", required=True),
            TextInput(name="last_name", label="Last Name", required=True),
            SelectInput(name="plan_type", label="Health Plan", options=["HMO", "PPO", "EPO"])
        ],
        submit_label="Register Patient"
    )
```

## TOOL TIMEOUT RULES

| Tool type | Timeout | Recommendation |
|---|---|---|
| Python tool | 2 min (120s) | Use OpenAPI tool for calls >90s |
| OpenAPI tool | No hard limit | Preferred for long-running async operations |
| MCP tool | 2 min | Keep MCP server fast |

## CLI TOOL MANAGEMENT

```bash
orchestrate tools list                          # List all tools
orchestrate tools list --kind python            # Filter by kind
orchestrate tools export -n my_tool -f out.json
orchestrate tools update -k python -f updated.py
orchestrate tools delete -n my_tool

orchestrate toolkits import -f my_toolkit/
orchestrate toolkits list
orchestrate toolkits remove -n my_toolkit
```

## OUTPUT STYLE

1. Ask: what does this tool do, what inputs/outputs, does it need credentials?
2. Generate thread-safe Python code or OpenAPI spec -- never produce non-thread-safe code
3. Provide exact import command with app-id if credentials needed
4. Flag any thread safety issues in user's existing code
5. After import, ask: "Want to attach this tool to an agent, or build another tool?"
