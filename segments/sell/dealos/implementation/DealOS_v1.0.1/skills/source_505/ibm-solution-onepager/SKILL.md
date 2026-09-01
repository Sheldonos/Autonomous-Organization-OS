---
name: ibm-solution-onepager
description: Generate a professional, print-ready IBM Solution One-Pager in HTML/CSS format. Use when a user asks to create a one-pager, solution brief, or marketing collateral for an IBM product or solution.
---

# IBM Solution One-Pager Generator

This skill provides a reusable HTML/CSS template and workflow for generating professional, print-ready IBM Solution One-Pagers. The design is reverse-engineered from official IBM marketing collateral (specifically the Quantum Computing 101 brief) and strictly adheres to IBM Carbon Design System principles, including typography (IBM Plex Sans), color palette, and structural layout.

## When to Use This Skill

Trigger this skill when a user requests:

- An IBM solution brief or one-pager

- A marketing collateral document for an IBM product

- A summary document comparing an IBM solution to a traditional approach

- A visually appealing, print-ready HTML/CSS document following IBM design guidelines

## Included Resources

- `templates/ibm_solution_onepager.html`: The core HTML/CSS template containing the complete layout, styling, and placeholder structure.

## Workflow: Generating a One-Pager

Follow these steps to generate a customized IBM Solution One-Pager for the user:

### 1. Gather Solution Information

Before generating the document, ensure you have the following information about the solution. If any information is missing, use your knowledge to infer appropriate content or ask the user for clarification:

- **Solution Name & Subtitle**

- **Solution Category** (e.g., "Quantum Computing", "Hybrid Cloud", "AI Automation")

- **Short Definition** (1-2 sentences explaining the solution without jargon)

- **Core Differentiator** ("Why it excels" - 2-3 sentences)

- **Comparison** (Traditional Approach vs. IBM Solution Approach)

- **Key Applications / Use Cases** (At least 3 distinct use cases with short descriptions)

- **Contact Information** (Name, Title, Email, Phone, URL)

### 2. Prepare the Template

1. Read the template file located at `/home/ubuntu/skills/ibm-solution-onepager/templates/ibm_solution_onepager.html`.

1. Create a copy of this template in the user's working directory (e.g., `/home/ubuntu/solution_brief.html`).

### 3. Inject Content

Modify the copied HTML file to inject the gathered information:

- Replace all `[PLACEHOLDER]` text with the actual content.

- **Hero Image:** If the user provides an image, replace the `.image-placeholder` div with an `<img>` tag pointing to the image. If no image is provided, leave the placeholder or generate a relevant image using the `generate` tool.

- **Diagram:** If applicable, replace the `.diagram-placeholder` text with a relevant SVG diagram or image.

- **Icons:** Update the SVG paths in the `.app-icon` divs to match the specific use cases. Use standard, clean line-art SVGs.

- **Cleanup:** Remove the entire `<div class="template-guide">` section at the bottom of the file before finalizing.

### 4. Deliver the Result

1. Verify the HTML file is correctly formatted and all placeholders have been replaced.

1. Use the `message` tool to deliver the final HTML file to the user as an attachment.

1. Provide instructions to the user on how to view and print the document (e.g., "Open the HTML file in your browser and use Ctrl+P / Cmd+P to save it as a PDF").

## Design Guidelines (For Reference)

If you need to modify the CSS or add new sections, adhere to these IBM design principles:

- **Typography:** Always use `IBM Plex Sans` for body text and headings. Use `IBM Plex Mono` for code snippets or phonetic spellings.

- **Colors:**
  - Dark/Backgrounds: `#2d2d2d` (Dark), `#161616` (Black), `#f4f4f4` (Gray-10)
  - Accents: `#ee5396` (Pink), `#0f62fe` (Blue)
  - Gradients: Use subtle, professional gradients (e.g., the pink gradient in the comparison card).

- **Structure:** Maintain clear hierarchy, ample whitespace, and strict alignment. Use pill-shaped labels for section tags.

---

## imagegen

