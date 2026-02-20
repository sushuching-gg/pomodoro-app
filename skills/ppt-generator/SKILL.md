---
name: ppt-generator
description: Generate PowerPoint presentations from Markdown files. Use this skill when the user wants to create slides, presentations, or PPTX files from text or markdown content.
---

# PPT Generator

This skill converts Markdown files into PowerPoint (.pptx) presentations.

## Interaction Protocol

Before using this skill to generate a presentation, **ALWAYS** clarify the following with the user:
1.  **Style/Vibe**: Ask what design style they prefer (e.g., Minimalist, Corporate, Cyberpunk). Check if they have a specific design_spec.yaml or want you to create one.
2.  **Length**: Ask for the target number of slides (e.g., "Approximately 15 slides").

## Usage

1.  **Prepare Content**: Create a markdown file (e.g., `slides.md`).
    *   Use `# Title` for slide titles.
    *   Use `- Bullet` for content.
    *   Use `![alt](image.png)` for images.

2.  **Generate**: Run the script.

```bash
python skills/ppt-generator/scripts/md2pptx.py <input.md> <output.pptx> [--template <template.pptx>]
```

## Examples

See `skills/ppt-generator/examples/example.md` for a sample input.

