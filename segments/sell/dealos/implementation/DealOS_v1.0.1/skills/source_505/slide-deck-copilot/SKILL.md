---
name: slide-deck-copilot
description: A complete workflow for analyzing an existing presentation, clarifying technical ambiguities, and generating new or revised slides that perfectly match the original deck's visual style. Use when a user uploads a presentation and asks to revise a slide, add a new slide, or clarify technical content within the deck.
---

# Slide Deck Copilot

This skill provides a structured workflow for acting as a presentation copilot. It ensures that when a user asks to modify an existing deck, the resulting slides are technically accurate, contextually aware, and visually indistinguishable from the original presentation.

## Core Principles

1. **Context First**: Never generate a slide without first reading the specific slide mentioned AND the surrounding slides in the provided deck to understand the narrative flow and technical context.

1. **Visual Cloning**: The generated slides MUST perfectly match the visual style of the original deck (colors, typography, layout patterns, logos, and card styles).

1. **Technical Clarity**: When revising a slide to address a technical ambiguity, ensure the clarification is explicit, accurate, and tailored to the specific audience (e.g., explaining that a lightweight container is not a full app server).

1. **Standalone Delivery**: The output should be a new, standalone presentation project containing only the requested new/revised slides, ready for the user to export and insert into their master deck.

## Workflow

When a user uploads a presentation and requests modifications or additions, follow these steps:

1. **Analyze the Source Material**:
  - Use the `file` tool (`view` action) to read the specific slide mentioned by the user AND the surrounding slides (at least 2 slides before and after).
  - Extract the exact visual style: background colors, accent colors, typography weight/size, layout structures (e.g., two-column cards), and logo placements.
  - Understand the technical context and identify the ambiguity the user is asking about.

1. **Draft the Content**:
  - Write the markdown content for the new/revised slides.
  - Ensure the content directly addresses the user's concern (e.g., adding a clarification callout box).
  - Structure the content to fit the extracted visual layout (e.g., headers, subheaders, card bodies).

1. **Initialize the Slide Project**:
  - Use the `slide_initialize` tool to create a new project.
  - Set `generate_mode` to `html`.
  - In the `style_instruction`, explicitly define the `aesthetic_direction`, `color_palette`, and `typography` extracted from the source deck.

1. **Build the Slides**:
  - Use the `slide_edit` tool to write the HTML/CSS for each slide.
  - **CRITICAL**: Implement the exact visual cloning. Use CSS to recreate the specific card styles, accent bars, and logo placements observed in the source deck.
  - Ensure the layout is responsive and fits within the 1280x720 container without overflowing.

1. **Deliver the Result**:
  - Use the `slide_present` tool to finalize the project.
  - Deliver the `manus-slides://` URL to the user, explaining exactly what was changed and how it matches their original deck.

## References

- `references/visual-cloning-guide.md`: Techniques for extracting and replicating visual styles from a source PDF/image into HTML/CSS slides.

- `references/technical-clarification-patterns.md`: Patterns for structuring technical clarifications (e.g., comparison tables, callout boxes) within a slide layout.

---

## solitude-of-roman-writer

