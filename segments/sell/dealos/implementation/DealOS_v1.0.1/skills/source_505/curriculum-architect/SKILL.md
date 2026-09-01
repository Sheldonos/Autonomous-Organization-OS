---
name: curriculum-architect
description: A complete framework for designing, structuring, and generating comprehensive educational curriculum. Use when a user asks to build out course content by individual lesson, by grade level, or across an entire multi-year (e.g., K-12) spectrum. This skill automates the research, scoping, and generation of end-to-end mastery learning paths, incorporating interactive elements like questions, challenges, and simulations.
---

# Curriculum Architect

This skill provides a structured workflow for generating comprehensive educational curriculum. It is designed to take a user from a novice state to mastery by building out course content at any scale: a single lesson, a full grade-level course, or an entire multi-year (e.g., K-12) progression.

## Core Principles

1. **End-to-End Mastery**: Curriculum must guide the learner from "I don't know anything" to a mastery level of comprehension.

1. **Interactive Design**: Lessons should not just be passive text. They must include a combination of:
  - Questions
  - Challenges
  - Inputs
  - Output simulations

1. **Proactive & Adaptive Planning**: The system should proactively plan courses based on deep research of educational standards, and adaptively build out lessons based on logical progression.

## Intake & Scope Definition

When triggered, first determine the scope of the user's request. Ask clarifying questions if the scope is ambiguous.

**Identify the Scope Level:**

1. **Micro (Lesson Level):** A single, focused topic (e.g., "Photosynthesis," "Introduction to Fractions").

1. **Meso (Grade/Course Level):** A complete course for a specific grade or subject (e.g., "4th Grade Math," "High School Biology").

1. **Macro (Lifespan/K-12 Level):** A multi-year progression (e.g., "K-12 STEM Curriculum," "Pre-K to College Computer Science").

## Workflow by Scope

Follow the appropriate workflow based on the identified scope.

### Macro Scope (Lifespan / K-12)

When building a multi-year curriculum, the goal is to map the progression of concepts across grades.

1. **Research Standards**: Use the `search` tool to research national or international educational standards (e.g., Common Core, NGSS) for the requested subject across all grades.

1. **Define Grade-Level Milestones**: Map out the core competencies and mastery goals for each grade level.

1. **Generate the Master Blueprint**: Create a high-level document outlining the progression. Use the template in `/home/ubuntu/skills/curriculum-architect/templates/macro_blueprint_template.md`.

1. **Drill Down (Optional)**: Ask the user if they would like to drill down into a specific grade level to build out its course content (proceed to Meso Scope).

### Meso Scope (Grade / Course Level)

When building a course for a specific grade or subject, the goal is to break the subject down into units and lessons.

1. **Research Course Standards**: Research the specific standards and learning objectives for the target grade/subject.

1. **Structure Units**: Divide the course into logical units or modules (e.g., Unit 1: Mechanics, Unit 2: Thermodynamics).

1. **Sequence Lessons**: Within each unit, list the sequential lessons required to achieve the unit's objectives. Ensure a logical progression of prerequisite knowledge.

1. **Generate the Course Syllabus**: Create a detailed syllabus document. Use the template in `/home/ubuntu/skills/curriculum-architect/templates/meso_syllabus_template.md`.

1. **Drill Down (Optional)**: Ask the user if they would like to generate the detailed content for a specific lesson (proceed to Micro Scope).

### Micro Scope (Lesson Level)

When building an individual lesson, the goal is to create interactive, mastery-focused content.

1. **Define Learning Objectives**: Clearly state what the student will be able to do by the end of the lesson.

1. **Structure the Content**: Break the lesson into:
  - **Introduction/Hook**: Engaging entry point.
  - **Direct Instruction**: Core concepts.
  - **Guided Practice (Interactive)**: Questions, inputs, and output simulations.
  - **Independent Challenge**: A task to prove mastery.

1. **Generate the Lesson Plan**: Write the full lesson content. Use the template in `/home/ubuntu/skills/curriculum-architect/templates/micro_lesson_template.md`.

## Deliverables

Always deliver the final curriculum documents as Markdown files attached via the `message` tool. Ensure the formatting is clean, professional, and utilizes tables and clear headings.

---

## customers-win-suppliers-win-strategist

