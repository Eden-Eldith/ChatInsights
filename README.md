# ChatInsights
## The Personal Knowledge Graph You Didn't Know You Already Wrote
![My Personal Vault](https://i.imgur.com/6J00Gu1.png)
ChatInsights is a Python application designed to process your **ChatGPT, Claude, and Deepseek** JSON exports, analyze conversation concepts, and generate a structured Obsidian vault for knowledge management. It also extracts training data pairs for potential LLM fine-tuning.
> ⚡️ Inspired by this Reddit post: [Mining Your AI Conversation History — r/ChatGPTPro](https://www.reddit.com/r/ChatGPTPro/comments/1jzzgie/mining_your_ai_conversation_history_the_complete/)
>
> While I originally built this tool to manage my own GPT conversations, this post aligned so perfectly with the vision that I decided to finalize and share it.

---

## 🆕 What's New

### Version 3 (Current) - December 2025

| Version | Platforms Supported | Key Features |
|---------|---------------------|--------------|
| v1 | ChatGPT only | Basic conversation export, concept tracking, training data |
| v2 | ChatGPT + Claude | Multi-platform support, auto-detection, empty file cleanup |
| **v3** | **ChatGPT + Claude + Deepseek** | **Model headers, thinking blocks, summaries, reasoning chains** |

#### 🚀 Deepseek Platform Support
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
- Works with Claude's extended thinking feature
- Also captures `tool_use` blocks with `(Tool Use)` suffix

#### 📝 Claude Conversation Summaries
- Extracts AI-generated conversation summaries from Claude exports
- Summaries appear in a dedicated section at the top of each conversation file:
```markdown
## Conversation Summary
[Summary text here]

============================================================
```

#### 🔗 Deepseek Reasoning Chain Support
- Extracts `THINK` fragments as reasoning/thinking blocks with `(Thinking)` suffix
- `REQUEST` fragments mapped to user messages
- `RESPONSE` fragments mapped to assistant messages
- Proper handling of Deepseek's `mapping` structure with `fragments` arrays

### Version 2 Highlights

- **Claude Support**: Process Anthropic Claude conversation exports
- **Auto-Detection**: Automatic platform detection based on JSON structure
- **Platform Selection**: Manual override for platform selection (auto/chatgpt/claude)
- **Empty File Cleanup**: Automatically moves 0KB "untitled" files to cleanup folder
- **Improved File Sorting**: Fixed sorting function for date extraction from filenames

---

## Features

*   **Multi-Platform Export Processing:** Reads `conversations.json` from **ChatGPT, Claude, and Deepseek** and extracts conversation data with auto-detection.
*   **Model Identification:** Outputs include model headers showing which AI model was used (e.g., `gpt-4o`, `deepseek-chat`, `Claude`).
*   **Thinking Block Extraction:** Captures Claude's extended thinking and Deepseek's reasoning chains with `(Thinking)` suffix.
*   **Text Log Generation:** Creates individual `.txt` files for each conversation, organized by month and year in a `data` subdirectory.
*   **Obsidian Vault Creation:** Automatically generates an Obsidian-ready vault structure:
    *   **Concept Notes:** Creates `.md` files for key concepts identified in conversation titles (using customizable regex). Includes metadata, evolution trends, related concepts, and links to relevant conversations.
    *   **Conversation Logs:** Copies the raw conversation logs into an `Obsidian/Conversations` subdirectory (preserving the monthly structure) and converts them to `.md` files, allowing direct linking from concept notes.
    *   **Maps of Content (MOC):** Generates `Concepts-MOC.md` linking to all identified concept notes.
    *   **Dashboard:** Creates `Concept-Dashboard.md` with Dataview queries for visualizing concept data within Obsidian.
    *   **Term Analysis:** Generates `Recurring-Terms.md` highlighting frequently used terms in titles that might be potential new concepts.
*   **Training Data Extraction:** Generates instruction-response pairs from user-assistant interactions in JSONL or CSV format, suitable for fine-tuning LLMs.
*   **Streamlined Workflow:** The process of getting conversation logs into the Obsidian vault is now fully automated within the app.
*   **GUI:** Provides a user-friendly interface built with Tkinter.

## Requirements

*   Python 3.x
*   Tkinter (usually included with standard Python installations)

## How to Use

# Video Version 
<a href="http://www.youtube.com/watch?feature=player_embedded&v=P8TMdz2KOGI" target="_blank">
  <img src="http://img.youtube.com/vi/P8TMdz2KOGI/0.jpg" alt="tutorial" width="240" height="180" border="10" />
</a>


# Text Version:
(I usually just double click it)

1.  **Run the script:**
    ```bash
    python chat-insights-app.py
    ```
2.  **Select Export File:** In the "Import & Process" tab, click "Browse" to select your `conversations.json` file downloaded from ChatGPT, Claude, or Deepseek.
3.  **Select Platform (Optional):** The app auto-detects the platform, but you can manually select ChatGPT, Claude, or Deepseek if needed.
4.  **Configure (Optional):**
    *   Adjust the "Output Directory" if you don't want to use the default (`~/ChatInsights`).
    *   Change the "Your Name", "Assistant Name", and "System Name" to match your usage. These names are used when generating text logs and training data.
    *   Go to the "Concept Tracker" tab and customize the "Core Concepts to Track" list. Each line should be `ConceptName: regex_pattern`.
4.  **Process and Analyze:** Click the **"Process & Analyze Concepts"** button. This performs the following steps:
    *   Processes the JSON export.
    *   Creates `.txt` logs in the `data` subdirectory.
    *   Generates `pruned.json` and `training_data.jsonl` in the `data` subdirectory.
    *   Analyzes conversation titles based on the defined concepts.
    *   Generates the Obsidian vault structure (`.md` files for concepts, MOC, dashboard, terms) in the `Obsidian/Concepts` subdirectory.
    *   **Automatically copies** the `.txt` conversation logs from `data` into `Obsidian/Conversations`, renaming them to `.md`.
5.  **Open in Obsidian:**
    *   Once processing is complete, click the "Open Output Folder" button to see all generated files.
    *   Click the "Open Obsidian Vault" button. This opens the `Obsidian/Concepts` folder.
    *   In Obsidian, choose "Open folder as vault" and select the `Obsidian/Concepts` directory generated by the tool (e.g., `~/ChatInsights/Obsidian/Concepts`).
    *   You can now browse the concept notes, MOC, dashboard, and click the links within concept notes (like `[[conversation_filename]]`) to directly open the corresponding conversation log.

---

### 📚 Universal Concept Tracker Template

This tool lets you track recurring themes or topics across your ChatGPT conversation history. You can define the concepts you care about, and the app will automatically tag and organize them in your Obsidian vault.

#### 🛠 How It Works
Each concept is matched using simple keywords. You don’t need to know regular expressions — just list related terms separated by `|` (the vertical bar), and the tool will match any of them.

#### 📌 Starter Template (Edit This!)

Paste this into the **Concept Tracker** tab to get started:

```
AI: AI | Artificial Intelligence | GPT | Claude | LLM | Deepseek 
Machine Learning: Machine Learning | ML | Training | Fine-Tuning  
Coding: Python | Script | Code | Programming  
Frameworks: Framework | Architecture | Structure | System  
Optimization: Optimization | Optimizer | Performance | Speed  
Server Tools: Server | RCON | Admin | Discord Bot  
Mental Health: Mental Health | Depression | Anxiety | Support  
Neurodiversity: Neurodivergent | ADHD | Autism  
YourProjectName: [ Add your own custom keywords here ]  
```

#### 🧠 Tips
- You can add more concepts by following the same pattern:  
  `ConceptName: keyword1 | keyword2 | keyword3`
- Keywords are **case-insensitive**, so don’t worry about capitalization.
- For personal terms (like codenames or aliases), just add a line like:  
  `ATLAS: ATLAS | A_T_L_A_S`  
- Be as broad or specific as you want — it’s your knowledge map.

---

## Output Structure

Assuming the default output directory (`~/ChatInsights`):

```
~/ChatInsights/
├── config.json             # Stores application settings
├── data/                   # Raw processing output
│   ├── April_2025/         # Example month/year folder
│   │   ├── convo_title_1_dd_mm_yyyy_hh_mm_ss.txt
│   │   └── ...
│   ├── May_2025/
│   │   └── ...
│   ├── _empty_untitled_cleanup/  # Empty untitled files moved here
│   │   └── cleanup_log_*.txt
│   ├── conversation_titles.txt # List used by concept tracker
│   ├── pruned.json             # Structured conversation data (includes model info)
│   └── training_data.jsonl     # Default training data output
├── Obsidian/
│   └── Concepts/             # Your Obsidian Vault Root
│       ├── Conversations/      # Copied & renamed conversation logs
│       │   ├── April_2025/
│       │   │   ├── convo_title_1_dd_mm_yyyy_hh_mm_ss.md
│       │   │   └── ...
│       │   └── May_2025/
│       │       └── ...
│       ├── AI.md               # Example concept note
│       ├── ATLAS.md            # Example concept note
│       ├── ...                 # Other concept notes
│       ├── Concepts-MOC.md     # Map of Content for concepts
│       ├── Concept-Dashboard.md # Dashboard with Dataview queries
│       └── Recurring-Terms.md  # Analysis of frequent terms
└── training_data.csv       # Optional CSV training data output
```

---

- If you have alot of Notes, Then you may want to follow this [fix for the obsidian graph](https://www.reddit.com/r/ObsidianMD/comments/16hvjiy/fix_for_a_slow_obsidian_graph_view/)
- To take this futher, Use the obsidian plugin [Ai Tagger Universe](https://github.com/niehu2018/obsidian-ai-tagger-universe) and I reccomend [Gemma3 on Ollama 1b version](https://ollama.com/library/gemma3) as the model for super fast tagging 

---

## Supported Platforms

| Platform | Export Format | Detected By | Model Extraction |
|----------|--------------|-------------|------------------|
| ChatGPT | `conversations.json` | `mapping` with `message.author.role` (no `fragments`) | ✅ `model_slug` from metadata |
| Claude | `conversations.json` | `chat_messages` with `sender` field | ⚠️ Defaults to "Claude" |
| Deepseek | `conversations.json` | `mapping` with `message.fragments` array | ✅ `model` field from messages |

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

## Credits

- **Original Application (v1)**: Eden_Eldith (P.C O'Brien) & The Claude 3 Models
- **v2 & v3 Enhancements**: GitHub Copilot (Claude Opus 4.5)
- **December 2025** 
