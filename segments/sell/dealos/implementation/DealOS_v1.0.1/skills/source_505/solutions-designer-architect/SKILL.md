---
name: solutions-designer-architect
description: A complete workflow for building IBM DevOps Solution Workbench (Solutions Designer) architecture projects. Use when a user asks to map out, design, or build an architecture in Solutions Designer, or when generating step-by-step build guides for Solutions Designer projects.
---

# IBM DevOps Solution Workbench Architect

This skill provides the complete workflow and data model for building architecture projects in IBM DevOps Solution Workbench (Solutions Designer). It ensures that all generated architectures are comprehensive, enterprise-grade, and ready to be manually entered into the Solutions Designer UI.

## Core Principles

1. **Completeness**: Every model element MUST include all 11 fields required by the Solutions Designer UI (Label, File Name, Type, Summary, Description, Status, Technologies, Icon, Tags, Contained In, Contains).

1. **C4 Model Compliance**: Architectures MUST follow the C4 model hierarchy (System Context -> Container -> Component).

1. **Business Alignment**: Every architecture MUST include Business elements (User Stories, User Tasks) and Risks/Tech Debt items that map to the technical components.

1. **Traceability**: Relationships MUST be explicitly defined between all elements to ensure the generated diagrams are accurate.

## Workflow

When asked to build an architecture for Solutions Designer, follow these steps:

1. **Analyze the Request**: Understand the business domain, core systems, and key integrations.

1. **Design the Architecture**: Map out the C4 model (Persons, Systems, Containers, Components).

1. **Generate the Build Guide**: Use the template in `references/build-guide-template.md` to generate a complete, step-by-step guide for the user.

1. **Deliver the Guide**: Provide the guide to the user, offering to act as a copilot while they enter the data into the Solutions Designer UI.

## References

- `references/build-guide-template.md`: The exact Markdown template to use when generating the step-by-step build guide.

- `references/element-types.md`: A reference guide for the different types of model elements supported by Solutions Designer and their required fields.

- `references/relationship-types.md`: A reference guide for the valid relationship types between different model elements.

## Example Output

When generating a build guide, the output MUST strictly follow the structure defined in `references/build-guide-template.md`. Do not skip any sections or fields.

---

## specialized-prompt-writer

