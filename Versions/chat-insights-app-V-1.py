import os
import sys
import json
import re
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
from collections import Counter
import shutil

# Global variables
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "ChatInsights")
CONFIG_FILE = os.path.join(OUTPUT_DIR, "config.json")

class ChatInsightsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatInsights - AI Chat Analysis Tool")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Default configuration
        self.config = {
            "assistant_name": "Atlas",
            "user_name": "Eden",
            "system_name": "Custom Eden info",
            "output_dir": OUTPUT_DIR,
            "last_import_file": "",
            "themes": {
                "dark": {"bg": "#2e2e2e", "fg": "#ffffff", "button": "#3d3d3d", "highlight": "#4a86e8"},
                "light": {"bg": "#f0f0f0", "fg": "#333333", "button": "#e0e0e0", "highlight": "#4a86e8"}
            },
            "current_theme": "light"
        }
        self.load_config()
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create tabs
        self.import_tab = ttk.Frame(self.notebook)
        self.concepts_tab = ttk.Frame(self.notebook)
        self.settings_tab = ttk.Frame(self.notebook)
        self.training_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.import_tab, text="Import & Process")
        self.notebook.add(self.concepts_tab, text="Concept Tracker")
        self.notebook.add(self.training_tab, text="Training Data")
        self.notebook.add(self.settings_tab, text="Settings")
        
        # Create import tab
        self.create_import_tab()
        
        # Create concepts tab
        self.create_concepts_tab()
        
        # Create settings tab
        self.create_settings_tab()
        
        # Create training tab
        self.create_training_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_config(self):
        """Load configuration from file or create default"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    # Update config with saved values, keeping defaults for any missing keys
                    for key, value in saved_config.items():
                        self.config[key] = value
            
            # Ensure output directory exists
            os.makedirs(self.config["output_dir"], exist_ok=True)
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            return False
    
    def create_import_tab(self):
        """Create import and process tab"""
        frame = ttk.Frame(self.import_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # File selection
        file_frame = ttk.LabelFrame(frame, text="ChatGPT JSON Export File")
        file_frame.pack(fill=tk.X, pady=10)
        
        self.file_path_var = tk.StringVar()
        if self.config["last_import_file"] and os.path.exists(self.config["last_import_file"]):
            self.file_path_var.set(self.config["last_import_file"])
        
        file_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, width=70)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
        
        browse_btn = ttk.Button(file_frame, text="Browse", command=self.browse_file)
        browse_btn.pack(side=tk.RIGHT, padx=5, pady=5)
        
        # Processing options
        options_frame = ttk.LabelFrame(frame, text="Processing Options")
        options_frame.pack(fill=tk.X, pady=10)
        
        # Export path
        path_frame = ttk.Frame(options_frame)
        path_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(path_frame, text="Output Directory:").pack(side=tk.LEFT, padx=5)
        
        self.output_dir_var = tk.StringVar(value=self.config["output_dir"])
        output_dir_entry = ttk.Entry(path_frame, textvariable=self.output_dir_var, width=50)
        output_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        browse_dir_btn = ttk.Button(path_frame, text="Browse", command=self.browse_output_dir)
        browse_dir_btn.pack(side=tk.RIGHT, padx=5)
        
        # Custom naming options
        names_frame = ttk.Frame(options_frame)
        names_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # User name
        ttk.Label(names_frame, text="Your Name:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.user_name_var = tk.StringVar(value=self.config["user_name"])
        ttk.Entry(names_frame, textvariable=self.user_name_var, width=20).grid(row=0, column=1, padx=5, pady=2)
        
        # Assistant name
        ttk.Label(names_frame, text="Assistant Name:").grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)
        self.assistant_name_var = tk.StringVar(value=self.config["assistant_name"])
        ttk.Entry(names_frame, textvariable=self.assistant_name_var, width=20).grid(row=0, column=3, padx=5, pady=2)
        
        # System name
        ttk.Label(names_frame, text="System Name:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.system_name_var = tk.StringVar(value=self.config["system_name"])
        ttk.Entry(names_frame, textvariable=self.system_name_var, width=20).grid(row=1, column=1, padx=5, pady=2)
        
        # Action buttons
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        self.process_btn = ttk.Button(buttons_frame, text="Process ChatGPT Export", command=self.process_export)
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        self.analyze_btn = ttk.Button(buttons_frame, text="Process & Analyze Concepts", command=self.process_and_analyze)
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        # Log output
        log_frame = ttk.LabelFrame(frame, text="Process Log")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Results section
        results_frame = ttk.LabelFrame(frame, text="Results")
        results_frame.pack(fill=tk.X, pady=10)
        
        self.result_text = ttk.Label(results_frame, text="No processing has been done yet", wraplength=600)
        self.result_text.pack(padx=10, pady=10)
        
        self.open_output_btn = ttk.Button(results_frame, text="Open Output Folder", command=self.open_output)
        self.open_output_btn.pack(pady=5)
        self.open_output_btn.config(state=tk.DISABLED)
    
    def create_concepts_tab(self):
        """Create concept tracking tab"""
        frame = ttk.Frame(self.concepts_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Info section
        info_frame = ttk.LabelFrame(frame, text="Concept Tracker")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = """
The Concept Tracker analyzes your conversations to identify key topics and how they evolve over time.
It generates an Obsidian-compatible vault with concept notes, maps of content, and dashboards.

Once you've processed your ChatGPT export, you can run the concept tracker to:
1. Identify recurring themes and topics in your conversations
2. Track how concepts evolve over time
3. Discover relationships between different concepts
4. Generate a knowledge graph of your AI interactions
        """
        
        info_label = ttk.Label(info_frame, text=info_text, wraplength=600, justify=tk.LEFT)
        info_label.pack(padx=10, pady=10)
        
        # Core concepts
        concepts_frame = ttk.LabelFrame(frame, text="Core Concepts to Track")
        concepts_frame.pack(fill=tk.X, pady=10)
        
        self.concepts_text = scrolledtext.ScrolledText(concepts_frame, height=10)
        self.concepts_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add default concepts
        default_concepts = """
AI: \\bAI\\b|Artificial Intelligence|GPT|Claude|LLM
ATLAS: \\bATLAS\\b|A_T_L_A_S
MACO: \\bMACO\\b|MACAO|Multiple Ant Colony
Server: Server|RCON|Admin|Discord Bot
Framework: Framework|Structure|System
Python: Python|Script|Code|Programming
Emergent: Emergent|Resonance|Cognition
Optimization: Optimization|Optimizer|Performance
Mental Health: Mental Health|Depression|Anxiety|Support
Neurodiversity: Neuro|ADHD|Autism
"""
        self.concepts_text.insert(tk.END, default_concepts.strip())
        
        # Run tracker button
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        self.run_tracker_btn = ttk.Button(buttons_frame, text="Run Concept Tracker", command=self.run_concept_tracker)
        self.run_tracker_btn.pack(side=tk.LEFT, padx=5)
        
        # Stats frame
        self.stats_frame = ttk.LabelFrame(frame, text="Concept Statistics")
        self.stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.stats_text = scrolledtext.ScrolledText(self.stats_frame, height=10)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Open Obsidian folder button
        self.open_obsidian_btn = ttk.Button(frame, text="Open Obsidian Vault", command=self.open_obsidian)
        self.open_obsidian_btn.pack(pady=5)
        self.open_obsidian_btn.config(state=tk.DISABLED)
    
    def create_training_tab(self):
        """Create training data tab"""
        frame = ttk.Frame(self.training_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Info section
        info_frame = ttk.LabelFrame(frame, text="Training Data Generation")
        info_frame.pack(fill=tk.X, pady=10)
        
        info_text = """
This tool can generate instruction-response pairs from your conversations for fine-tuning your own LLM models.
The training data is exported in JSONL format, with each line containing an instruction and its corresponding response.

You can use this data to:
1. Fine-tune existing LLM models to respond more like your assistant
2. Create a personalized AI assistant that reflects your interaction style
3. Train specialized models for specific domains based on your conversations
        """
        
        info_label = ttk.Label(info_frame, text=info_text, wraplength=600, justify=tk.LEFT)
        info_label.pack(padx=10, pady=10)
        
        # Options
        options_frame = ttk.LabelFrame(frame, text="Training Data Options")
        options_frame.pack(fill=tk.X, pady=10)
        
        # Minimum conversation length
        min_len_frame = ttk.Frame(options_frame)
        min_len_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(min_len_frame, text="Minimum instruction length (characters):").pack(side=tk.LEFT, padx=5)
        
        self.min_length_var = tk.IntVar(value=10)
        ttk.Spinbox(min_len_frame, from_=1, to=100, textvariable=self.min_length_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Format selection
        format_frame = ttk.Frame(options_frame)
        format_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(format_frame, text="Export format:").pack(side=tk.LEFT, padx=5)
        
        self.format_var = tk.StringVar(value="jsonl")
        ttk.Radiobutton(format_frame, text="JSONL (for fine-tuning)", variable=self.format_var, value="jsonl").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(format_frame, text="CSV", variable=self.format_var, value="csv").pack(side=tk.LEFT, padx=5)
        
        # Action buttons
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill=tk.X, pady=10)
        
        self.generate_btn = ttk.Button(buttons_frame, text="Generate Training Data", command=self.generate_training_data)
        self.generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Preview frame
        preview_frame = ttk.LabelFrame(frame, text="Training Data Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.preview_text = scrolledtext.ScrolledText(preview_frame)
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def create_settings_tab(self):
        """Create settings tab"""
        frame = ttk.Frame(self.settings_tab)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Theme settings
        theme_frame = ttk.LabelFrame(frame, text="Theme")
        theme_frame.pack(fill=tk.X, pady=10)
        
        self.theme_var = tk.StringVar(value=self.config["current_theme"])
        ttk.Radiobutton(theme_frame, text="Light", variable=self.theme_var, value="light", command=self.apply_theme).pack(side=tk.LEFT, padx=20, pady=10)
        ttk.Radiobutton(theme_frame, text="Dark", variable=self.theme_var, value="dark", command=self.apply_theme).pack(side=tk.LEFT, padx=20, pady=10)
        
        # Default path settings
        path_frame = ttk.LabelFrame(frame, text="Default Paths")
        path_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(path_frame, text="Default Output Folder:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        
        default_output_var = tk.StringVar(value=self.config["output_dir"])
        ttk.Entry(path_frame, textvariable=default_output_var, width=50).grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Button(path_frame, text="Browse", command=lambda: self.browse_dir(default_output_var)).grid(row=0, column=2, padx=5, pady=5)
        
        # Action buttons
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(buttons_frame, text="Save Settings", command=self.save_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Reset to Defaults", command=self.reset_settings).pack(side=tk.LEFT, padx=5)
        
        # About section
        about_frame = ttk.LabelFrame(frame, text="About ChatInsights")
        about_frame.pack(fill=tk.X, pady=10)
        
        about_text = """
ChatInsights v1.0
A tool for analyzing and extracting insights from your AI chat conversations.

This application combines the functionality of:
- The ChatGPT export processor (converting JSON to readable text files)
- The Concept Tracker (analyzing topics and their evolution)
- Training data generator (creating instruction-response pairs for LLM fine-tuning)

Created by Eden with assistance from Atlas
        """
        
        about_label = ttk.Label(about_frame, text=about_text, wraplength=600, justify=tk.LEFT)
        about_label.pack(padx=10, pady=10)

    def browse_file(self):
        """Open file dialog to select conversations.json"""
        filename = filedialog.askopenfilename(
            title="Select ChatGPT Export File",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        if filename:
            self.file_path_var.set(filename)
            self.config["last_import_file"] = filename
            self.save_config()
    
    def browse_output_dir(self):
        """Open directory dialog to select output location"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)
            self.config["output_dir"] = directory
            self.save_config()
    
    def browse_dir(self, var):
        """Generic directory browser that updates a StringVar"""
        directory = filedialog.askdirectory()
        if directory:
            var.set(directory)
    
    def log(self, message):
        """Add message to log and scroll to end"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_status(self, message):
        """Update status bar"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def process_export(self):
        """Process the ChatGPT export file"""
        file_path = self.file_path_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid ChatGPT export file")
            return
        
        # Update config
        self.config["output_dir"] = self.output_dir_var.get()
        self.config["user_name"] = self.user_name_var.get()
        self.config["assistant_name"] = self.assistant_name_var.get()
        self.config["system_name"] = self.system_name_var.get()
        self.save_config()
        
        # Run in a separate thread to keep UI responsive
        self.process_btn.config(state=tk.DISABLED)
        self.analyze_btn.config(state=tk.DISABLED)
        
        processing_thread = threading.Thread(target=self._process_export_thread, args=(file_path,))
        processing_thread.daemon = True
        processing_thread.start()
    
    def process_and_analyze(self):
        """Process export and then run concept tracker"""
        file_path = self.file_path_var.get()
        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Please select a valid ChatGPT export file")
            return
        
        # Update config
        self.config["output_dir"] = self.output_dir_var.get()
        self.config["user_name"] = self.user_name_var.get()
        self.config["assistant_name"] = self.assistant_name_var.get()
        self.config["system_name"] = self.system_name_var.get()
        self.save_config()
        
        # Run in a separate thread to keep UI responsive
        self.process_btn.config(state=tk.DISABLED)
        self.analyze_btn.config(state=tk.DISABLED)
        
        processing_thread = threading.Thread(target=self._process_and_analyze_thread, args=(file_path,))
        processing_thread.daemon = True
        processing_thread.start()
    
    def _process_export_thread(self, file_path):
        """Background thread for processing exports"""
        try:
            self.update_status("Processing ChatGPT export...")
            self.log("Starting to process ChatGPT export file...")
            
            output_dir = self.config["output_dir"]
            data_dir = os.path.join(output_dir, "data")
            os.makedirs(data_dir, exist_ok=True)
            
            # Load the ChatGPT export
            with open(file_path, 'r', encoding='utf-8') as f:
                conversations_data = json.load(f)
            
            # Process conversations
            self.log(f"Processing {len(conversations_data)} conversations...")
            created_dirs, pruned_data = self.write_conversations_and_json(conversations_data, data_dir)
            
            # Create training pairs
            self.log("Generating training data pairs...")
            training_pairs = self.create_training_pairs(pruned_data, os.path.join(data_dir, "training_data.jsonl"))
            
            # Generate conversation titles file for concept tracker
            self.log("Generating conversation titles file for concept tracker...")
            titles_file = self.generate_conversation_titles(data_dir)
            
            self.log("Processing complete!")
            self.log(f"Processed {len(conversations_data)} conversations")
            self.log(f"Created files in {len(set([info['directory'] for info in created_dirs]))} directories")
            self.log(f"Generated {len(training_pairs)} training data pairs")
            
            # Update result
            self.result_text.config(text=f"Successfully processed {len(conversations_data)} conversations. " +
                                      f"Generated {len(training_pairs)} training pairs and prepared data for concept tracking.")
            
            # Enable buttons
            self.open_output_btn.config(state=tk.NORMAL)
            self.process_btn.config(state=tk.NORMAL)
            self.analyze_btn.config(state=tk.NORMAL)
            self.run_tracker_btn.config(state=tk.NORMAL)
            self.generate_btn.config(state=tk.NORMAL)
            
            self.update_status("Processing complete")
            
        except Exception as e:
            self.log(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while processing: {str(e)}")
            self.process_btn.config(state=tk.NORMAL)
            self.analyze_btn.config(state=tk.NORMAL)
            self.update_status("Processing failed")
    
    def _process_and_analyze_thread(self, file_path):
        """Background thread for processing exports and running concept tracker"""
        try:
            # First process the export
            self._process_export_thread(file_path)
            
            # Then run the concept tracker
            self.notebook.select(1)  # Switch to concept tracker tab
            self.run_concept_tracker()
            
        except Exception as e:
            self.log(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.process_btn.config(state=tk.NORMAL)
            self.analyze_btn.config(state=tk.NORMAL)
            self.update_status("Processing failed")
    
    def parse_concept_regex(self, content):
        """Parse the Concept-regex.md format into concept patterns"""
        concepts = {}
        lines = content.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            if ':' in line:
                concept_name, patterns = line.split(':', 1)
                concept_name = concept_name.strip()
                pattern_text = patterns.strip()
                
                # Clean up the pattern - add word boundaries and handle pipes
                pattern_parts = []
                for part in pattern_text.split('|'):
                    part = part.strip()
                    if part and not part.startswith('\\b') and not part.endswith('\\b'):
                        # Add word boundaries for standalone terms
                        if ' ' not in part:  # Single word
                            part = f'\\b{part}\\b'
                        else:  # Multi-word phrase
                            part = part.replace(' ', '\\s+')
                    pattern_parts.append(part)
                
                if pattern_parts:
                    try:
                        final_pattern = '|'.join(pattern_parts)
                        concepts[concept_name] = re.compile(final_pattern, re.I)
                    except re.error as e:
                        self.log(f"Invalid regex for {concept_name}: {e}")
        
        return concepts
    
    def run_concept_tracker(self):
        """Run the concept tracker on processed data"""
        data_dir = os.path.join(self.config["output_dir"], "data")
        titles_file = os.path.join(data_dir, "conversation_titles.txt")
        
        if not os.path.exists(titles_file):
            messagebox.showerror("Error", "Conversation titles file not found. Please process the ChatGPT export first.")
            return
        
        # Get custom concepts from UI using the new parser
        concepts_text = self.concepts_text.get("1.0", tk.END).strip()
        custom_concepts = self.parse_concept_regex(concepts_text)
        
        if not custom_concepts:
            messagebox.showwarning("Warning", "No valid concepts found. Using default concepts.")
            custom_concepts = None
        
        # Run in a separate thread
        self.run_tracker_btn.config(state=tk.DISABLED)
        
        tracking_thread = threading.Thread(target=self._concept_tracker_thread, args=(titles_file, custom_concepts))
        tracking_thread.daemon = True
        tracking_thread.start()
    
    def _concept_tracker_thread(self, titles_file, custom_concepts):
        """Background thread for concept tracking"""
        try:
            self.update_status("Running concept tracker...")
            self.log("Starting concept tracking analysis...")
            
            obsidian_dir = os.path.join(self.config["output_dir"], "Obsidian", "Concepts")
            os.makedirs(obsidian_dir, exist_ok=True)
            
            # Create and run tracker
            tracker = self.ConceptTracker(custom_concepts)
            results = tracker.process(titles_file, obsidian_dir)
            
            # Display results
            self.stats_text.delete("1.0", tk.END)
            self.stats_text.insert(tk.END, f"Processed {results['conversations']} conversations\n")
            self.stats_text.insert(tk.END, f"Orphaned conversations: {results['orphaned']}\n\n")
            self.stats_text.insert(tk.END, "Concept mentions:\n")
            
            for concept, count in sorted(results['concepts'].items(), key=lambda x: x[1], reverse=True):
                if count > 0:
                    self.stats_text.insert(tk.END, f"- {concept}: {count} mentions\n")
            
            self.stats_text.insert(tk.END, "\nAdditional terms found:\n")
            for term, count in sorted(results['additional_terms'].items(), key=lambda x: x[1], reverse=True)[:15]:
                self.stats_text.insert(tk.END, f"- {term}: {count} occurrences\n")
            
            self.log("Concept tracking complete!")
            self.open_obsidian_btn.config(state=tk.NORMAL)
            self.run_tracker_btn.config(state=tk.NORMAL)

        except Exception as e:
            self.log(f"Error in concept tracking: {str(e)}")
            self.update_status("Concept tracking failed")
            self.run_tracker_btn.config(state=tk.NORMAL)
            return

        # --- Add call to copy conversations ---
        try:
            data_dir_for_copy = os.path.join(self.config["output_dir"], "data")
            self.copy_conversations_to_obsidian(data_dir_for_copy, obsidian_dir)
            self.update_status("Concept tracking and conversation copy complete")
        except Exception as copy_e:
            self.log(f"Error copying conversations to Obsidian: {copy_e}")
            self.update_status("Concept tracking complete, but conversation copy failed")
            # --- End of added call ---
            
        except Exception as e:
            self.log(f"Error in concept tracker: {str(e)}")
            messagebox.showerror("Error", f"An error occurred in concept tracker: {str(e)}")
            self.run_tracker_btn.config(state=tk.NORMAL)
            self.update_status("Concept tracking failed")

    def copy_conversations_to_obsidian(self, data_dir, obsidian_dir):
        """Copy .txt conversation files to Obsidian vault as .md files"""
        self.log("Copying conversation logs to Obsidian vault...")
        source_data_dir = data_dir
        # Place conversations in a dedicated subfolder within the Obsidian vault
        target_obsidian_convos_dir = os.path.join(obsidian_dir, "Conversations") 
        os.makedirs(target_obsidian_convos_dir, exist_ok=True)
        
        copied_count = 0
        skipped_count = 0
        for root, _, files in os.walk(source_data_dir):
            for file in files:
                # Only process .txt files, excluding specific metadata/output files
                if file.endswith(".txt") and file not in ["conversation_titles.txt", "training_data.txt"]:
                    src_path = os.path.join(root, file)
                    
                    # Determine relative path to preserve structure
                    relative_path = os.path.relpath(root, source_data_dir)
                    target_subdir = os.path.join(target_obsidian_convos_dir, relative_path)
                    os.makedirs(target_subdir, exist_ok=True)
                    
                    # Define destination path and rename to .md
                    dest_filename = file[:-4] + ".md"
                    dest_path = os.path.join(target_subdir, dest_filename)
                    
                    try:
                        # Use copy2 to preserve metadata like modification time
                        shutil.copy2(src_path, dest_path) 
                        copied_count += 1
                    except Exception as e:
                        self.log(f"Error copying {file}: {e}")
                        skipped_count += 1
                        
        self.log(f"Copied {copied_count} conversation files to {target_obsidian_convos_dir}.")
        if skipped_count > 0:
             self.log(f"Skipped {skipped_count} files due to errors.")

    def generate_training_data(self):
        """Generate training data from processed conversations"""
        data_dir = os.path.join(self.config["output_dir"], "data")
        pruned_file = os.path.join(data_dir, "pruned.json")
        
        if not os.path.exists(pruned_file):
            messagebox.showerror("Error", "Processed conversation data not found. Please process the ChatGPT export first.")
            return
        
        # Run in a separate thread
        self.generate_btn.config(state=tk.DISABLED)
        
        training_thread = threading.Thread(target=self._training_data_thread, args=(pruned_file,))
        training_thread.daemon = True
        training_thread.start()
    
    def _training_data_thread(self, pruned_file):
        """Background thread for generating training data"""
        try:
            self.update_status("Generating training data...")
            self.log("Starting training data generation...")
            
            # Load pruned data
            with open(pruned_file, 'r', encoding='utf-8') as f:
                pruned_data = json.load(f)
            
            # Generate training data with options from UI
            min_length = self.min_length_var.get()
            format_type = self.format_var.get()
            
            output_file = os.path.join(self.config["output_dir"], f"training_data.{format_type}")
            training_pairs = self.create_training_pairs(pruned_data, output_file, min_length)
            
            # Show preview
            self.preview_text.delete("1.0", tk.END)
            
            if training_pairs:
                self.preview_text.insert(tk.END, f"Generated {len(training_pairs)} training pairs\n\n")
                self.preview_text.insert(tk.END, "Sample training pairs:\n\n")
                
                for i, pair in enumerate(training_pairs[:5]):
                    self.preview_text.insert(tk.END, f"--- Pair {i+1} ---\n")
                    self.preview_text.insert(tk.END, f"Instruction: {pair['instruction'][:100]}...\n")
                    self.preview_text.insert(tk.END, f"Response: {pair['response'][:100]}...\n\n")
            else:
                self.preview_text.insert(tk.END, "No training pairs were generated. Check your conversations data.")
            
            self.log(f"Training data generation complete! Created {len(training_pairs)} pairs.")
            self.generate_btn.config(state=tk.NORMAL)
            self.update_status("Training data generation complete")
            
        except Exception as e:
            self.log(f"Error generating training data: {str(e)}")
            messagebox.showerror("Error", f"An error occurred while generating training data: {str(e)}")
            self.generate_btn.config(state=tk.NORMAL)
            self.update_status("Training data generation failed")
    
    def open_output(self):
        """Open the output directory"""
        output_dir = self.config["output_dir"]
        if os.path.exists(output_dir):
            self.open_folder(output_dir)
        else:
            messagebox.showerror("Error", "Output directory does not exist")
    
    def open_obsidian(self):
        """Open the Obsidian vault directory"""
        obsidian_dir = os.path.join(self.config["output_dir"], "Obsidian", "Concepts")
        if os.path.exists(obsidian_dir):
            self.open_folder(obsidian_dir)
        else:
            messagebox.showerror("Error", "Obsidian directory does not exist")
    
    def open_folder(self, path):
        """Open a folder in the default file explorer"""
        if sys.platform == 'win32':
            os.startfile(path)
        elif sys.platform == 'darwin':  # macOS
            os.system(f'open "{path}"')
        else:  # Linux
            os.system(f'xdg-open "{path}"')
    
    def apply_theme(self):
        """Apply the selected theme"""
        # This is a placeholder - would need more advanced styling code
        # to fully implement theming with ttk
        self.config["current_theme"] = self.theme_var.get()
        self.save_config()
        messagebox.showinfo("Theme Changed", "Theme will be fully applied when you restart the application")
    
    def save_settings(self):
        """Save current settings to config file"""
        # Update config with current UI values
        self.config["output_dir"] = self.output_dir_var.get()
        self.config["user_name"] = self.user_name_var.get()
        self.config["assistant_name"] = self.assistant_name_var.get()
        self.config["system_name"] = self.system_name_var.get()
        self.config["current_theme"] = self.theme_var.get()
        
        if self.save_config():
            messagebox.showinfo("Settings Saved", "Your settings have been saved successfully")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
            # Reset to defaults
            self.config = {
                "assistant_name": "Atlas",
                "user_name": "Eden",
                "system_name": "Custom Eden info",
                "output_dir": os.path.join(os.path.expanduser("~"), "ChatInsights"),
                "last_import_file": "",
                "themes": {
                    "dark": {"bg": "#2e2e2e", "fg": "#ffffff", "button": "#3d3d3d", "highlight": "#4a86e8"},
                    "light": {"bg": "#f0f0f0", "fg": "#333333", "button": "#e0e0e0", "highlight": "#4a86e8"}
                },
                "current_theme": "light"
            }
            
            # Update UI
            self.output_dir_var.set(self.config["output_dir"])
            self.user_name_var.set(self.config["user_name"])
            self.assistant_name_var.set(self.config["assistant_name"])
            self.system_name_var.set(self.config["system_name"])
            self.theme_var.set(self.config["current_theme"])
            
            self.save_config()
            messagebox.showinfo("Settings Reset", "Settings have been reset to defaults")
    
    # Conversation processing functions (from chatjson_splitter.py)
    def get_conversation_messages(self, conversation):
        """Get messages from a conversation"""
        messages = []
        current_node = conversation.get("current_node")
        mapping = conversation.get("mapping", {})
        
        while current_node:
            node = mapping.get(current_node, {})
            message = node.get("message") if node else None
            content = message.get("content") if message else None
            author = message.get("author", {}).get("role", "") if message else ""
            
            if content and content.get("content_type") == "text":
                parts = content.get("parts", [])
                if parts and isinstance(parts[0], str) and parts[0].strip():
                    if author != "system" or (message.get("metadata", {}) if message else {}).get("is_user_system_message"):
                        if author == "assistant":
                            author = self.config["assistant_name"]
                        elif author == "system":
                            author = self.config["system_name"]
                        elif author == "user":
                            author = self.config["user_name"]
                        messages.append({"author": author, "text": parts[0]})
            
            current_node = mapping.get(current_node, {}).get("parent")
        
        return messages[::-1]
    
    def write_conversations_and_json(self, conversations_data, data_dir):
        """Write conversations to text files and create pruned.json"""
        created_directories_info = []
        pruned_data = {}
        
        for conversation in conversations_data:
            updated = conversation.get('update_time')
            if not updated:
                continue
            
            updated_date = datetime.fromtimestamp(updated)
            directory_name = updated_date.strftime('%B_%Y')
            directory_path = os.path.join(data_dir, directory_name)
            
            # Ensure the month-year directory exists
            os.makedirs(directory_path, exist_ok=True)
            
            title = conversation.get('title', 'Untitled')
            sanitized_title = re.sub(r"[^a-zA-Z0-9_]", "_", title)[:120]
            file_name = os.path.join(directory_path, f"{sanitized_title}_{updated_date.strftime('%d_%m_%Y_%H_%M_%S')}.txt")
            
            messages = self.get_conversation_messages(conversation)
            
            # Write conversation to a text file
            with open(file_name, 'w', encoding="utf-8") as file:
                for message in messages:
                    file.write(f"{message['author']}\n")
                    file.write(f"{message['text']}\n")
            
            # Store conversation metadata in pruned.json
            if directory_name not in pruned_data:
                pruned_data[directory_name] = []
            
            pruned_data[directory_name].append({
                "title": title,
                "create_time": datetime.fromtimestamp(conversation.get('create_time')).strftime('%Y-%m-%d %H:%M:%S'),
                "update_time": updated_date.strftime('%Y-%m-%d %H:%M:%S'),
                "messages": messages
            })
            
            created_directories_info.append({
                "directory": directory_path,
                "file": file_name
            })
        
        # Save pruned conversations to pruned.json inside data directory
        pruned_json_path = os.path.join(data_dir, "pruned.json")
        with open(pruned_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(pruned_data, json_file, ensure_ascii=False, indent=4)
        
        return created_directories_info, pruned_data
    
    def create_training_pairs(self, pruned_data, output_file=None, min_length=10):
        """Convert conversation data to instruction-response pairs for fine-tuning."""
        if output_file is None:
            output_file = os.path.join(self.config["output_dir"], "data", "training_data.jsonl")
        
        training_pairs = []
        
        for month, conversations in pruned_data.items():
            for conversation in conversations:
                messages = conversation["messages"]
                
                # Process message pairs (User -> Assistant)
                for i in range(len(messages) - 1):
                    # Find User->Assistant pairs
                    if messages[i]["author"] == self.config["user_name"] and messages[i+1]["author"] == self.config["assistant_name"]:
                        # Skip very short instructions
                        if len(messages[i]["text"]) < min_length:
                            continue
                            
                        # Create a training pair
                        pair = {
                            "instruction": messages[i]["text"],
                            "response": messages[i+1]["text"]
                        }
                        training_pairs.append(pair)
        
        # Write to the appropriate format
        if output_file.endswith('.jsonl'):
            # Write to JSONL format (one JSON object per line)
            with open(output_file, 'w', encoding='utf-8') as f:
                for pair in training_pairs:
                    f.write(json.dumps(pair, ensure_ascii=False) + '\n')
        
        elif output_file.endswith('.csv'):
            # Write to CSV format
            import csv
            with open(output_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["instruction", "response"])
                for pair in training_pairs:
                    writer.writerow([pair["instruction"], pair["response"]])
        
        self.log(f"Created {len(training_pairs)} training pairs in {output_file}")
        return training_pairs
    
    def generate_conversation_titles(self, data_dir):
        """Generate the conversation_titles.txt file for concept tracker"""
        titles_file = os.path.join(data_dir, "conversation_titles.txt")
        
        # Add header for Obsidian
        with open(titles_file, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write("tags:\n")
            f.write("  - help\n")
            f.write("  - management\n")
            f.write("  - memory\n")
            f.write("  - support\n")
            f.write("---\n\n\n")
        
        # Get list of all text files in data directory and subdirectories
        all_files = []
        for root, _, files in os.walk(data_dir):
            for file in files:
                if file.endswith('.txt') and file != 'conversation_titles.txt' and file != 'training_data.txt':
                    all_files.append(os.path.join(root, file))
        
        # Sort files by date (extracted from filename)
        all_files.sort(key=lambda x: os.path.basename(x).split('_')[-5:] if len(os.path.basename(x).split('_')) >= 5 else "")
        
        # Write file list to conversation_titles.txt
        with open(titles_file, 'a', encoding='utf-8') as f:
            for i, file_path in enumerate(all_files, 1):
                # Just write the filename without the full path for readability
                filename = os.path.basename(file_path)
                f.write(f"{i}. {filename}\n")
        
        return titles_file
    
    # Concept tracker implementation (from concept-tracker.py)
    class ConceptTracker:
        """
        Analyzes conversation titles to track concepts and terminology over time
        and generate Obsidian markdown files for concept tracking.
        """
        
        def __init__(self, core_concepts=None):
            # Set default core concepts if none provided
            if core_concepts is None:
                self.core_concepts = {
                    'AI': re.compile(r'\bAI\b|Artificial Intelligence|GPT|Claude|LLM', re.I),
                    'ATLAS': re.compile(r'\bATLAS\b|A_T_L_A_S', re.I),
                    'MACO': re.compile(r'\bMACO\b|MACAO|Multiple Ant Colony', re.I),
                    'Server': re.compile(r'Server|RCON|Admin|Discord Bot', re.I),
                    'Framework': re.compile(r'Framework|Structure|System', re.I),
                    'Python': re.compile(r'Python|Script|Code|Programming', re.I),
                    'Squad': re.compile(r'\bSquad\b|Server|Gaming', re.I),
                    'Emergent': re.compile(r'Emergent|Resonance|Cognition', re.I),
                    'Optimization': re.compile(r'Optimization|Optimizer|Performance', re.I),
                    'Quantum': re.compile(r'Quantum|Q-', re.I),
                    'GPU': re.compile(r'GPU|RTX|Graphics', re.I),
                    'Mental Health': re.compile(r'Mental Health|Depression|Anxiety|Support', re.I),
                    'Neurodiversity': re.compile(r'Neuro|ADHD|Autism', re.I),
                }
            else:
                self.core_concepts = core_concepts

        def process_conversation_file(self, filename):
            """Process a file containing conversation titles and extract data."""
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            conversations = []
            # Pattern to match your numbered filename format
            pattern = r'^(\d+)\.\s+(.+)_(\d{2})_(\d{2})_(\d{4})_(\d{2})_(\d{2})_(\d{2})\.txt$'
            
            for line in lines:
                match = re.match(pattern, line.strip())
                if match:
                    # Extract components from the filename
                    conv = {
                        'id': int(match.group(1)),
                        'title': match.group(2).replace('_', ' '),
                        'day': match.group(3),
                        'month': match.group(4),
                        'year': match.group(5),
                        'hour': match.group(6),
                        'minute': match.group(7),
                        'second': match.group(8),
                        'date': f"{match.group(3)}/{match.group(4)}/{match.group(5)}",
                        'time': f"{match.group(6)}:{match.group(7)}:{match.group(8)}",
                        'filename': line.strip()[line.find(' ')+1:],
                        'clean_filename': line.strip()[line.find(' ')+1:].replace('.txt', '')
                    }
                    conversations.append(conv)
            
            return conversations

        def extract_concepts(self, conversations):
            """Extract key concepts from conversation titles."""
            concept_mentions = {concept: [] for concept in self.core_concepts}
            
            # Extract concepts based on regex patterns
            for conv in conversations:
                for concept, pattern in self.core_concepts.items():
                    if pattern.search(conv['title']):
                        concept_mentions[concept].append(conv)
            
            return concept_mentions
        
        def extract_additional_terms(self, conversations, min_occurrences=3):
            """Extract additional recurring terms that might be concepts."""
            # Extract all words from titles
            all_words = []
            for conv in conversations:
                words = re.findall(r'\b[A-Za-z][A-Za-z0-9]{2,}\b', conv['title'])
                all_words.extend([w for w in words if len(w) > 3])  # Only include words longer than 3 chars
            
            # Count word frequencies
            word_counts = Counter(all_words)
            
            # Filter for words that appear multiple times
            recurring_terms = {word: count for word, count in word_counts.items() 
                            if count >= min_occurrences}
            
            # Remove common words and words already in core concepts
            common_words = {'with', 'that', 'this', 'from', 'have', 'what', 'your', 'request', 'help'}
            for word in list(recurring_terms.keys()):
                if word.lower() in common_words:
                    del recurring_terms[word]
                for concept in self.core_concepts:
                    if word.lower() in concept.lower():
                        del recurring_terms[word]
                        break
            
            return recurring_terms
        
        def identify_orphaned_conversations(self, conversations, concept_mentions):
            """Identify conversations not matched by any concept"""
            orphaned = []
            matched_ids = set()
            
            # Collect all matched conversation IDs
            for concept, mentions in concept_mentions.items():
                for conv in mentions:
                    matched_ids.add(conv['id'])
            
            # Find orphans
            for conv in conversations:
                if conv['id'] not in matched_ids:
                    orphaned.append(conv)
            
            return orphaned

        def analyze_concept_evolution(self, concept_mentions, conversations):
            """Analyze how concepts evolved over time."""
            evolution = {}
            
            for concept, mentions in concept_mentions.items():
                if not mentions:
                    continue
                    
                # Sort mentions by date
                mentions.sort(key=lambda x: f"{x['year']}-{x['month']}-{x['day']}")
                
                # Group by year-month
                monthly_counts = {}
                for conv in mentions:
                    month_key = f"{conv['year']}-{conv['month']}"
                    if month_key not in monthly_counts:
                        monthly_counts[month_key] = 0
                    monthly_counts[month_key] += 1
                
                # Calculate first and last mention
                first_mention = mentions[0]
                last_mention = mentions[-1]
                
                evolution[concept] = {
                    'first_mention': first_mention,
                    'last_mention': last_mention,
                    'monthly_trend': monthly_counts,
                    'total_mentions': len(mentions)
                }
            return evolution
        
        def find_related_concepts(self, concept_mentions, threshold=0.3):
            """Find concepts that frequently appear together."""
            related = {}
            
            # For each concept pair, calculate co-occurrence
            concepts = list(concept_mentions.keys())
            for i, concept1 in enumerate(concepts):
                if not concept_mentions[concept1]:  # Skip empty concepts
                    continue
                    
                related[concept1] = []
                
                for j, concept2 in enumerate(concepts):
                    if i == j or not concept_mentions[concept2]:
                        continue
                    
                    # Get sets of conversation IDs for each concept
                    conv_ids1 = {conv['id'] for conv in concept_mentions[concept1]}
                    conv_ids2 = {conv['id'] for conv in concept_mentions[concept2]}
                    
                    # Calculate overlap ratio 
                    intersection = len(conv_ids1.intersection(conv_ids2))
                    if intersection > 0:
                        # Use Jaccard similarity coefficient
                        similarity = intersection / len(conv_ids1.union(conv_ids2))
                        
                        if similarity >= threshold:
                            related[concept1].append({
                                'concept': concept2,
                                'similarity': similarity,
                                'shared_conversations': intersection
                            })
            
            # Sort related concepts by similarity
            for concept in related:
                related[concept].sort(key=lambda x: x['similarity'], reverse=True)
            
            return related

        def generate_orphan_analysis(self, orphaned_conversations, output_dir):
            """Generate analysis of orphaned conversations"""
            if not orphaned_conversations:
                return
            
            orphan_path = os.path.join(output_dir, "Orphaned-Conversations.md")
            
            with open(orphan_path, 'w', encoding='utf-8') as f:
                f.write("---\ntags:\n  - orphans\n  - analysis\n---\n\n")
                f.write("# Orphaned Conversations Analysis\n\n")
                f.write(f"Found {len(orphaned_conversations)} conversations not matched by any concept.\n\n")
                
                # Extract common terms from orphans to suggest new concepts
                all_words = []
                for conv in orphaned_conversations:
                    words = re.findall(r'\b[A-Za-z][A-Za-z0-9]{2,}\b', conv['title'])
                    all_words.extend([w for w in words if len(w) > 3])
                
                word_counts = Counter(all_words)
                common_terms = {word: count for word, count in word_counts.items() 
                               if count >= 2}  # Terms appearing at least twice
                
                if common_terms:
                    f.write("## Suggested Additional Concepts\n\n")
                    f.write("Based on orphaned conversation titles, consider adding these concepts:\n\n")
                    
                    for term, count in sorted(common_terms.items(), key=lambda x: x[1], reverse=True)[:20]:
                        f.write(f"- `{term}` ({count} occurrences)\n")
                
                f.write("\n## Orphaned Conversations List\n\n")
                for conv in orphaned_conversations:
                    clean_filename = conv['clean_filename']
                    f.write(f"- [[{clean_filename}]] - {conv['date']} - *{conv['title']}*\n")

        def generate_concept_notes(self, concept_mentions, evolution, related_concepts, output_dir):
            """Generate Obsidian notes for each concept."""
            os.makedirs(output_dir, exist_ok=True)
            
            for concept, mentions in concept_mentions.items():
                if not mentions:
                    continue
                    
                # Sort mentions by date
                mentions.sort(key=lambda x: f"{x['year']}-{x['month']}-{x['day']}")
                
                filename = os.path.join(output_dir, f"{concept.replace(' ', '_')}.md")
                
                with open(filename, 'w', encoding='utf-8') as f:
                    # YAML frontmatter
                    f.write(f"---\n")
                    f.write(f"concept: \"{concept}\"\n")
                    f.write(f"first_mention: \"{evolution[concept]['first_mention']['date']}\"\n")
                    f.write(f"last_mention: \"{evolution[concept]['last_mention']['date']}\"\n")
                    f.write(f"mentions: {len(mentions)}\n")
                    
                    # Add related concepts to frontmatter
                    if related_concepts.get(concept):
                        f.write("related:\n")
                        for related in related_concepts[concept][:5]:  # Top 5 related
                            f.write(f"  - \"{related['concept']}\"\n")
                    
                    f.write("tags:\n")
                    f.write(f"  - concept/{concept.lower()}\n")
                    f.write(f"  - tracking\n")
                    f.write(f"---\n\n")
                    
                    # Content
                    f.write(f"# {concept}\n\n")
                    
                    f.write(f"## Overview\n")
                    f.write(f"Concept tracked across {len(mentions)} conversations from {evolution[concept]['first_mention']['date']} to {evolution[concept]['last_mention']['date']}.\n\n")
                    
                    # Evolution section
                    f.write("## Evolution\n")
                    f.write("Monthly mentions:\n\n")
                    
                    for month, count in evolution[concept]['monthly_trend'].items():
                        f.write(f"- {month}: {count} conversations\n")
                    
                    # Related concepts section
                    if related_concepts.get(concept):
                        f.write("\n## Related Concepts\n")
                        for related in related_concepts[concept][:5]:
                            f.write(f"- [[{related['concept']}]] - {related['shared_conversations']} shared conversations ({related['similarity']:.2f} similarity)\n")
                    
                    # Chronological mentions
                    f.write("\n## Chronological Mentions\n\n")
                    for conv in mentions:
                        clean_filename = conv['clean_filename']
                        f.write(f"- [[{clean_filename}]] - {conv['date']}\n")
        
        def generate_moc(self, concept_mentions, evolution, output_dir):
            """Generate a Map of Content for all concepts."""
            moc_path = os.path.join(output_dir, "Concepts-MOC.md")
            
            with open(moc_path, 'w', encoding='utf-8') as f:
                f.write("---\ntags:\n  - MOC\n  - concepts\n---\n\n")
                f.write("# Concepts Map of Content\n\n")
                
                # Calculate date range from all conversations
                all_convs = []
                for mentions in concept_mentions.values():
                    all_convs.extend(mentions)
                
                if all_convs:
                    all_convs.sort(key=lambda x: f"{x['year']}-{x['month']}-{x['day']}")
                    first_date = all_convs[0]['date']
                    last_date = all_convs[-1]['date']
                    f.write(f"## Overview\nTracking key concepts across conversations from {first_date} to {last_date}.\n\n")
                else:
                    f.write("## Overview\nTracking key concepts across conversations.\n\n")
                
                f.write("## Key Concepts\n\n")
                
                # Sort concepts by number of mentions
                sorted_concepts = sorted(
                    [(concept, mentions) for concept, mentions in concept_mentions.items() if mentions],
                    key=lambda x: len(x[1]), 
                    reverse=True
                )
                
                for concept, mentions in sorted_concepts:
                    # Only include concepts with mentions
                    f.write(f"- [[{concept}]] - {len(mentions)} mentions")
                    if concept in evolution and 'first_mention' in evolution[concept]:
                        f.write(f" (first: {evolution[concept]['first_mention']['date']})")
                    f.write("\n")
                
                f.write("\n## Concept Categories\n\n")
                f.write("- [[AI Systems]]\n")
                f.write("- [[Programming Projects]]\n")
                f.write("- [[Data Analysis]]\n")
                f.write("- [[Development Topics]]\n")
                f.write("- [[Security & Privacy]]\n")
                
                f.write("\n## Dataview Queries\n\n")
                f.write("```dataview\nTABLE concept, mentions, first_mention\nFROM #concept\nSORT mentions DESC\n```\n")
        
        def generate_dashboard(self, concept_mentions, evolution, output_dir):
            """Generate an Obsidian dashboard for concept tracking with embedded queries."""
            dashboard_path = os.path.join(output_dir, "Concept-Dashboard.md")
            
            with open(dashboard_path, 'w', encoding='utf-8') as f:
                f.write("---\ntags:\n  - dashboard\n  - concepts\n---\n\n")
                f.write("# Concept Tracking Dashboard\n\n")
                
                f.write("## Concept Timeline\n\n")
                f.write("```dataview\nCALENDAR file.cday\nFROM #concept\n```\n\n")
                
                f.write("## Top Concepts\n\n")
                f.write("```dataview\nTABLE concept, mentions AS \"Count\"\nFROM #concept\nSORT mentions DESC\nLIMIT 10\n```\n\n")
                
                f.write("## Recent Updates\n\n")
                f.write("```dataview\nTABLE concept, mentions, last_mention AS \"Last Updated\"\nFROM #concept\nSORT file.mtime DESC\nLIMIT 5\n```\n\n")
                
                f.write("## Concept Network\n\n")
                f.write("For a visual network of concept relationships, consider using the Obsidian Graph View filtered to show only concept notes.\n\n")
                
                f.write("## Concept Categories\n\n")
                # Create a table of concept categories and their counts
                categories = {
                    'AI Systems': ['AI', 'GPT', 'Claude', 'LLM', 'Language Model'],
                    'Programming': ['Python', 'JavaScript', 'Code', 'Programming', 'API'],
                    'Data & Analysis': ['Data', 'Database', 'CSV', 'JSON', 'Analysis'],
                    'Development': ['Development', 'Software', 'Application', 'Framework'],
                    'Cloud & Infrastructure': ['Cloud', 'AWS', 'Azure', 'Deploy'],
                    'Security': ['Security', 'Privacy', 'Encryption', 'Authentication']
                }
                
                for category, related_terms in categories.items():
                    count = 0
                    for concept, mentions in concept_mentions.items():
                        if any(term.lower() in concept.lower() for term in related_terms):
                            count += len(mentions)
                    
                    f.write(f"- **{category}**: {count} mentions\n")

        def generate_term_analysis(self, terms, output_dir):
            """Generate a note about additional recurring terms found in titles."""
            terms_path = os.path.join(output_dir, "Recurring-Terms.md")
            
            with open(terms_path, 'w', encoding='utf-8') as f:
                f.write("---\ntags:\n  - terminology\n  - analysis\n---\n\n")
                f.write("# Recurring Terms in Conversations\n\n")
                f.write("These terms appear frequently in your conversation titles and may represent additional concepts to track.\n\n")
                
                f.write("## Term Frequency\n\n")
                
                # Sort terms by frequency
                sorted_terms = sorted(terms.items(), key=lambda x: x[1], reverse=True)
                
                for term, count in sorted_terms:
                    f.write(f"- **{term}**: {count} occurrences\n")
                
                f.write("\n## Suggested New Concepts\n\n")
                f.write("Consider adding these high-frequency terms to your concept tracking system:\n\n")
                
                # Suggest the top terms as potential concepts
                for term, count in sorted_terms[:10]:
                    if count >= 5:  # Only suggest terms with 5+ occurrences
                        f.write(f"- [[{term}]] ({count} occurrences)\n")

        def process(self, input_file, output_dir):
            """Process conversations and generate Obsidian notes."""
            conversations = self.process_conversation_file(input_file)
            concept_mentions = self.extract_concepts(conversations)
            evolution = self.analyze_concept_evolution(concept_mentions, conversations)
            related_concepts = self.find_related_concepts(concept_mentions)
            
            # Generate Obsidian files
            os.makedirs(output_dir, exist_ok=True)
            self.generate_concept_notes(concept_mentions, evolution, related_concepts, output_dir)
            self.generate_moc(concept_mentions, evolution, output_dir)
            self.generate_dashboard(concept_mentions, evolution, output_dir)
            
            # Additional analysis
            additional_terms = self.extract_additional_terms(conversations)
            self.generate_term_analysis(additional_terms, output_dir)
            
            # Identify and analyze orphaned conversations
            orphaned_conversations = self.identify_orphaned_conversations(conversations, concept_mentions)
            self.generate_orphan_analysis(orphaned_conversations, output_dir)
            
            return {
                'conversations': len(conversations),
                'concepts': {concept: len(mentions) for concept, mentions in concept_mentions.items()},
                'additional_terms': additional_terms,
                'orphaned': len(orphaned_conversations)
            }

def main():
    root = tk.Tk()
    app = ChatInsightsApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()