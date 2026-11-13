# Circular Product Redesign

A Claude skill that guides the circular redesign of a physical product, step by step.

It is built on three connected layers:

- **A 7-step roadmap (Steps 0 to 6)** that orders the work, from diagnosing the existing product to evaluating the redesign.
- **Six design strategy axes** that guide what to design: *Narrow, Slow (long life), Slow (life extension), Close, Regenerate, Inform*.
- **A value-retention hierarchy** applied to each component: *Maintain → Repair → Reuse → Refurbish → Remanufacture → Recycle*.

The skill produces a baseline diagnosis, several distinct concepts, a quantitative comparison, illustrations and, on request, a CAD brief and a checked conceptual STEP file.

## Installation

### With Claude Code

Clone the repository into your personal skills folder:

```bash
git clone https://github.com/ielhassani/circular-product-redesign.git ~/.claude/skills/circular-product-redesign
```

On Windows (PowerShell):

```powershell
git clone https://github.com/ielhassani/circular-product-redesign.git "$HOME\.claude\skills\circular-product-redesign"
```

To use it in a single project only, clone it into `.claude/skills/circular-product-redesign` at the root of that project instead.

Then restart Claude Code.

### With Claude (web or desktop app)

1. Click **Code → Download ZIP** at the top of this page.
2. In Claude, open the settings, go to the **Skills** section, and upload the ZIP file.
3. Turn the skill on.

The folder inside the ZIP must contain the `SKILL.md` file directly.

## Usage

Describe the product you want to redesign. For example:

> Use the circular-product-redesign skill to redesign this electric kettle. Here is a photo and what I know about its materials.

In Claude Code, you can also type `/circular-product-redesign`.

Tips:

- Give as much information as you can: photos, materials, dimensions, use, current end of life. The skill always separates what is observed, calculated, assumed or unknown.
- Say how far to go. By default, the skill runs a full redesign (concepts, comparison, illustrations, CAD). You can ask for the diagnosis only, or the concepts only.
- For a new product, state the reference service it should be compared with.

## Repository contents

| File or folder | Purpose |
|---|---|
| `SKILL.md` | Main skill instructions |
| `references/` | Detailed method: roadmap, assessment, comparison data, CAD, deliverables, sources |
| `scripts/calculate_scores.py` | Supplementary design score to compare two options |
| `scripts/compare_concepts.py` | The same score for several concepts |
| `scripts/verify_step.py` | Round-trip check of a STEP file |
| `agents/openai.yaml` | Configuration for use with OpenAI Codex |

## Requirements

- **Python 3** for the scoring scripts. They use only the standard library.
- **CadQuery** (`pip install cadquery`), only to check STEP files with `verify_step.py`.

## Limitations to keep in mind

- The scores from the scripts are supplementary design indicators. They are not a circularity percentage, an MCI value or an ISO result.
- Illustrations and CAD models are **conceptual**. They do not prove safety, compliance or manufacturability.
- Always check current standards, regulations and recycling routes against primary sources.
