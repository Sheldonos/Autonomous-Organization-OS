---
name: typst-pdf-maker
description: "Generate professional, high-quality PDF documents using Typst. Use for: creating professional reports, academic papers, resumes, or any structured document requiring precise typography, mathematical formulas, code highlighting, or CJK (Chinese/Japanese/Korean) font support. This is the preferred alternative to LaTeX or Markdown-to-PDF when visual quality and structural control are important."
---

# Typst PDF Maker

This skill provides workflows and templates for generating professional PDF documents using Typst, a modern, fast, and powerful typesetting system.

## When to use this skill

- Creating professional reports with title pages, table of contents, and custom headers/footers

- Writing academic papers or technical documents with mathematical formulas and code blocks

- Generating resumes or CVs using community templates

- Whenever the user needs a highly polished PDF document with complex layouts that Markdown alone cannot handle

## Prerequisites

Typst may already be pre-installed in the sandbox. ALWAYS check first before installing:

```bash
typst --version
```

Only if the command above fails (typst not found), install it with:

```bash
sudo apt-get install -y xz-utils && cd /tmp && wget -q https://github.com/typst/typst/releases/latest/download/typst-x86_64-unknown-linux-musl.tar.xz && tar -xf typst-x86_64-unknown-linux-musl.tar.xz && sudo mv typst-x86_64-unknown-linux-musl/typst /usr/local/bin/
```

## Workflows

### 1. Creating a Professional Report

For general professional documents (reports, whitepapers, proposals ), use the provided basic report template.

1. Copy the template to your working directory:

   ```bash
   cp /home/ubuntu/skills/typst-pdf-maker/templates/basic-report.typ /home/ubuntu/my_report.typ
   ```

1. Edit the `.typ` file to replace `{{TITLE}}`, `{{AUTHOR}}`, and add content.

1. Consult `/home/ubuntu/skills/typst-pdf-maker/references/typst-patterns.md` for syntax on tables, figures, formulas, and code blocks.

1. Compile the document:

   ```bash
   python3 /home/ubuntu/skills/typst-pdf-maker/scripts/generate_pdf.py /home/ubuntu/my_report.typ
   ```

1. Verify the output against the **Verification Checklist** below before delivering to the user.

### 2. Creating a Resume / CV

Typst has an excellent package ecosystem (Typst Universe) with ready-to-use resume templates.

1. Initialize a resume project using a community template (e.g., `basic-resume` or `modern-cv`):

   ```bash
   typst init @preview/basic-resume my_resume
   ```

1. Edit the generated `main.typ` file in the new directory.

1. Compile the document:

   ```bash
   cd my_resume && typst compile main.typ resume.pdf
   ```

### 3. Converting Existing Markdown to PDF

For existing Markdown files, use the [cmarker](https://github.com/SabrinaJewson/cmarker.typ) package to render Markdown directly inside Typst without manual conversion. This preserves professional styling (fonts, headings, code blocks) while keeping the original Markdown untouched.

1. Copy the wrapper template next to the Markdown file:

   ```bash
   cp /home/ubuntu/skills/typst-pdf-maker/templates/md-report.typ /path/to/workdir/md-report.typ
   ```

1. Replace `{{MARKDOWN_FILE}}` in the template with the Markdown filename (path relative to the `.typ` file), e.g.:

   ```bash
   sed -i 's/{{MARKDOWN_FILE}}/my_doc.md/' /path/to/workdir/md-report.typ
   ```

1. Compile (cmarker and mitex packages download automatically on first run):

   ```bash
   typst compile /path/to/workdir/md-report.typ output.pdf
   ```

1. Verify the output against the **Verification Checklist** below before delivering to the user.

Notes:

- LaTeX math in Markdown (`$...$`, `$$...$$`) is rendered via the `mitex` package, already wired in the template (`math: mitex`).

- To add a title page or custom headers, merge the wrapper with `templates/basic-report.typ` styles.

- Useful `cmarker.render` options: `h1-level` (heading level mapping), `raw-typst` (inject raw Typst via HTML comments `<!--typst-begin-exclude-->`), `scope` (override element rendering).

### 4. Iterative Document Development

When heavily editing a Typst document, use the watch mode to continuously recompile upon saving:

```bash
python3 /home/ubuntu/skills/typst-pdf-maker/scripts/generate_pdf.py /home/ubuntu/my_report.typ --watch
```

## Best Practices

- **CJK Font Support**: Always specify fallback fonts for Chinese/Japanese/Korean text. The sandbox has `Noto Serif CJK SC` and `Noto Sans CJK SC` available.

   ```
   #set text(font: ("Libertinus Serif", "Noto Serif CJK SC"))
   ```

- **Debugging**: If compilation fails, Typst provides excellent error messages with line numbers. Read the error output carefully.

- **Images**: If generating a document before images are ready, use the `rect` placeholder pattern (see `references/typst-patterns.md`) instead of broken image links. For image positioning, always use `#figure(...)` for block-level images or the `wrap-it` package for text-wrapping layouts. **Never use ****`#place(...)`**** for images in flowing text** — it is an absolute positioning primitive that drifts across pages when content changes. See `references/typst-patterns.md` §6 for the full decision tree.

- **Packages**: You do not need to manually install packages. Simply `#import "@preview/package-name:version": *` in the document, and Typst will download it automatically during compilation.

## Verification Checklist

Before delivering a PDF, visually inspect the compiled output and confirm:

| Check | What to verify |
| --- | --- |
| Compilation | `typst compile` exits with no errors. |
| Page flow | No unintended blank pages; chapters begin where expected. |
| Element placement | Images, tables, and figures appear on the same page as (or immediately after) the text that references them — not on a distant page. |
| Cross-references | `@label` references resolve to correct numbers, not "??" or wrong targets. |
| Tables | Wide tables are readable; header rows repeat on continuation pages. |
| Fonts | CJK characters render correctly (not as boxes or fallback glyphs). |

## Bundled Resources

- `templates/basic-report.typ`: A comprehensive starting point for professional reports.

- `templates/md-report.typ`: A wrapper template that renders an existing Markdown file into a styled PDF via cmarker.

- `scripts/generate_pdf.py`: A wrapper script for compiling Typst files.

- `references/typst-patterns.md`: Code snippets for common layout requirements (tables, headers, formulas, etc.).

---

## ui-ux-pro-max

