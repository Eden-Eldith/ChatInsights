# ChatInsights Changelog & Version Summary

## Version Overview

| Version | Platforms Supported | Key Features |
|---------|---------------------|--------------|
| v1 | ChatGPT only | Basic conversation export, concept tracking, training data |
| v2 | ChatGPT + Claude | Multi-platform support, auto-detection, empty file cleanup |
| v3 | ChatGPT + Claude + Deepseek | Model headers, thinking blocks, summaries, reasoning chains |

---

## License Change - 2nd December 2025

### 📜 License Updated: MIT → GNU GPLv3

As of 2nd December 2025, ChatInsights is now licensed under the **GNU General Public License v3.0**.

#### What This Means
- **Prior Downloads (v1, v2 before this date)**: If you downloaded ChatInsights before 2nd December 2025, those copies remain covered under the MIT License that was included at the time.
- **New Downloads (from 2nd December 2025)**: All versions in this repository are now licensed under GPLv3. Any derivative works must also be open source under GPLv3.

#### Changes Made
- ✅ Added GPL license header to all Python files (`chat-insights-app.py` and all files in `Versions/` folder)
- ✅ Updated `LICENSE` file with full GPLv3 text
- ✅ Updated `README.md` with License section explaining the change
- ✅ Updated this `CHANGELOG.md` to document the license transition

#### License Header Added to All .py Files
```python
"""
ChatInsights - AI Chat Export Analysis Tool
Copyright (C) 2025 Eden_Eldith (P.C. O'Brien) c:

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""
```

---

## v3 (Current) - December 2025

### New Features

#### 🆕 Deepseek Platform Support
- Full support for Deepseek conversation exports
- Handles Deepseek's unique `fragments` message structure (REQUEST, RESPONSE, THINK)
- Auto-detection distinguishes Deepseek from ChatGPT format
- Deepseek radio button added to platform selection

#### 🏷️ Model Identification Headers
All exported `.md` and `.txt` files now include a header showing:
```
# Model: gpt-4o / deepseek-chat / Claude
# Title: Conversation Title
# Date: YYYY-MM-DD HH:MM:SS

============================================================
```

**Platform Support:**
- ✅ **ChatGPT**: Extracts `model_slug` from message metadata (e.g., `gpt-4o`, `gpt-5-instant`)
- ✅ **Deepseek**: Extracts `model` field from messages (e.g., `deepseek-chat`, `deepseek-coder`)
- ⚠️ **Claude**: Defaults to "Claude" (Anthropic does not include model version in exports)

#### 🧠 Claude Thinking Block Extraction
- Extracts Claude's internal reasoning/thinking blocks from conversations
- Thinking blocks are marked with `(Thinking)` author suffix in output
- Captures the `thinking` text from `content[*].type='thinking'` blocks
- Works with Claude's extended thinking feature content
- Also captures `tool_use` blocks with `(Tool Use)` suffix

#### 📝 Claude Conversation Summaries
- Extracts AI-generated conversation summaries from Claude exports
- Summaries appear in a dedicated section at the top of each conversation file
- Format:
```markdown
## Conversation Summary
[Summary text here]

============================================================
```

#### 🔗 Deepseek Reasoning Chain Support
- Full support for Deepseek's conversation format
- Extracts `THINK` fragments as reasoning/thinking blocks with `(Thinking)` suffix
- `REQUEST` fragments mapped to user messages
- `RESPONSE` fragments mapped to assistant messages
- Proper handling of Deepseek's `mapping` structure with `fragments` arrays

#### 👨‍💻 Developer Attribution
- Code includes docstring header with version info and feature list
- About section in Settings tab credits the development

### Technical Changes (v2 → v3)

#### New Functions
- `get_chatgpt_model_slug()`: Extracts model from ChatGPT message metadata
- `get_deepseek_model()`: Extracts model from Deepseek messages
- `get_deepseek_messages()`: Parses Deepseek fragment-based message structure
- `process_deepseek_conversations()`: Full Deepseek export processing pipeline

#### Enhanced Functions
- `detect_platform()`: Now detects Deepseek by checking for `fragments` in mapping nodes
- `get_claude_messages()`: 
  - Now iterates through `content` array checking `type` field
  - Handles `thinking`, `text`, `tool_use`, and `tool_result` block types
  - Properly extracts thinking text from `content_block.thinking` field
- `process_claude_conversations()`: 
  - Writes model headers at file top
  - Extracts and writes conversation summaries
  - Stores model and summary in pruned.json
- `process_chatgpt_conversations()`: 
  - Writes model headers at file top
  - Stores model in pruned.json

#### UI Changes
- Window title updated: "ChatInsights v3 - AI Chat Analysis Tool (ChatGPT, Claude & Deepseek)"
- Added Deepseek radio button to platform selection
- About section updated with v3 feature list

---

## v2 - Multi-Platform Support

### Changes from v1 → v2

#### New Features
- **Claude Support**: Added processing for Anthropic Claude conversation exports
- **Auto-Detection**: Automatic platform detection based on JSON structure
- **Platform Selection**: Manual override for platform selection (auto/chatgpt/claude)
- **Empty File Cleanup**: Automatically moves 0KB "untitled" files to cleanup folder
- **Improved File Sorting**: Fixed sorting function to properly handle date extraction from filenames

#### UI Changes
- Window title changed: "ChatInsights v2 - AI Chat Analysis Tool (ChatGPT & Claude)"
- File selection label: "AI Chat Export File (ChatGPT or Claude)"
- Platform radio buttons added (Auto-detect, ChatGPT, Claude)
- Platform info label shows detected platform
- Process button renamed: "Process AI Export"
- Default concept list updated with Claude-specific terms
- About section updated to reflect multi-platform support

#### Configuration Changes
- Default names changed from personalized ("Atlas", "Eden") to generic ("Assistant", "User", "System")
- Added `last_platform` config option (auto/chatgpt/claude)

#### Technical Changes
- **New Functions:**
  - `detect_platform()`: Analyzes JSON structure to identify ChatGPT vs Claude
  - `process_claude_conversations()`: Handles Claude export format
  - `get_claude_messages()`: Extracts messages from Claude's `chat_messages` structure
  - `get_chatgpt_messages()`: Renamed/refactored from `get_conversation_messages()`
  - `cleanup_empty_untitled_files()`: Moves empty untitled files to cleanup directory

- **Enhanced Functions:**
  - `_process_export_thread()`: Now calls appropriate processor based on detected platform
  - `browse_file()`: Auto-detects platform on file selection
  - `generate_conversation_titles()`: Improved date parsing with error handling
  - `copy_conversations_to_obsidian()`: Skips cleanup directory and empty untitled files

- **Claude-Specific Handling:**
  - ISO timestamp parsing (vs Unix timestamps for ChatGPT)
  - `chat_messages` array with `sender` field (vs `mapping` with `author.role`)
  - `name` field for title (vs `title` field)
  - `uuid` field for conversation ID (vs `conversation_id`)

#### Bug Fixes
- Fixed duplicate `except` block in `_concept_tracker_thread()`
- Fixed file sorting for filenames with varying underscore counts
- Added skip logic for empty untitled files in Obsidian copy

---

## v1 - Original Release

### Core Features
- **ChatGPT Export Processing**: Parse and convert ChatGPT JSON exports to readable formats
- **Conversation Organization**: Organize by month/year folders
- **Concept Tracking**: Identify and track recurring themes/topics
- **Obsidian Integration**: Generate Obsidian-compatible vault structure
- **Training Data Generation**: Create JSONL training data for LLM fine-tuning
- **Customizable Names**: Set custom names for User/Assistant/System roles (default: Atlas/Eden)
- **Theme Support**: Light/dark theme options
- **Progress Tracking**: Real-time progress bar and logging

### Technical Implementation
- Single platform support (ChatGPT only)
- `get_conversation_messages()`: Traverses ChatGPT's `mapping` tree structure
- `write_conversations_and_json()`: Creates text files and pruned.json
- `create_training_pairs()`: Generates instruction-response pairs
- `generate_conversation_titles()`: Creates title list for concept tracker
- `ConceptTracker` class: Full concept analysis and Obsidian generation

### Output Structure
```
ChatInsights/
├── data/
│   ├── Month_Year/
│   │   └── conversation_files.txt
│   ├── conversation_titles.txt
│   ├── pruned.json
│   └── training_data.jsonl
└── Obsidian/
    └── Concepts/
        ├── Concept_Name.md
        ├── Concepts-MOC.md
        ├── Concept-Dashboard.md
        └── Recurring-Terms.md
```

---

## Detailed Version Comparison

### v1 → v2 Summary

| Aspect | v1 | v2 |
|--------|----|----|
| Platforms | ChatGPT only | ChatGPT + Claude |
| Detection | None | Auto-detection |
| Default Names | Atlas/Eden/Custom Eden info | Assistant/User/System |
| Timestamp Format | Unix only | Unix + ISO |
| Message Structure | `mapping.message.author.role` | + `chat_messages.sender` |
| Empty File Handling | None | Cleanup to separate folder |
| Window Title | "ChatInsights - AI Chat Analysis Tool" | "ChatInsights v2 - AI Chat Analysis Tool (ChatGPT & Claude)" |

### v2 → v3 Summary

| Aspect | v2 | v3 |
|--------|----|----|
| Platforms | ChatGPT + Claude | ChatGPT + Claude + Deepseek |
| Model Tracking | None | Model headers in all output files |
| Thinking Blocks | None | Extracted with (Thinking) suffix |
| Conversation Summary | None | Extracted for Claude exports |
| Message Types | text only | text, thinking, tool_use, tool_result |
| Deepseek Fragments | N/A | REQUEST, RESPONSE, THINK |
| Window Title | "...ChatGPT & Claude" | "...ChatGPT, Claude & Deepseek" |

---

## Known Limitations

### Claude Exports
- **No Model Version**: Anthropic does not include which Claude model (Opus, Sonnet, Haiku, etc.) was used in their exports. The app defaults to showing "Claude" as the model name.
- **Thinking Block Availability**: Thinking blocks only appear if the user had extended thinking enabled during the conversation.

### ChatGPT Exports
- Model slug depends on OpenAI including it in the export (generally reliable)

### Deepseek Exports
- Model field depends on Deepseek including it in the export (generally reliable)
- Requires `fragments` array in message structure

### General
- Very large exports (500MB+) may be slow to process
- Memory usage scales with export size

---

## File Format Support

| Platform | Export Format | Detected By |
|----------|--------------|-------------|
| ChatGPT | `conversations.json` | `mapping` with `message.author.role` (no `fragments`) |
| Claude | `conversations.json` | `chat_messages` with `sender` field |
| Deepseek | `conversations.json` | `mapping` with `message.fragments` array |

---

## Credits

- **Original Application (v1)**: Eden_Eldith (P.C O'Brien) & The Claude 3 Models
- **v2 & v3 Enhancements**: GitHub Copilot (Claude Opus 4.5)
- **December 2025**
