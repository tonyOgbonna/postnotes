## PostNotes Application Specification

### 1. Introduction

PostNotes is a Streamlit application that automates the process of generating structured Obsidian markdown notes from YouTube video transcripts using Large Language Models (LLMs). It allows users to input a YouTube video URL, select a processing style (system instruction), and generate a formatted note that is saved in their Obsidian vault. The application supports multiple LLM providers and is configurable through a user interface.

### 2. Goals

*   Provide a user-friendly interface for processing YouTube videos and generating Obsidian notes.
*   Automate the process of extracting transcripts, processing them with LLMs, and formatting the output as structured markdown.
*   Support multiple LLM providers to allow users to choose the best model for their needs.
*   Allow users to configure the application through a settings page.
*   Ensure the generated notes are properly formatted and stored in the user's Obsidian vault.

### 3. Features

*   **YouTube Video Processing:**
    *   Takes a YouTube video URL as input.
    *   Extracts the video transcript using the YouTube Transcript API.
    *   Retrieves video metadata (channel name, title) using the YouTube Data API.
*   **LLM Integration:**
    *   Supports multiple LLM providers (Anthropic, OpenAI, Ollama) through an adapter pattern.
    *   Allows users to select a processing style (system instruction) from a directory of markdown files.
    *   Processes the transcript using the selected LLM and system instruction.
*   **Obsidian Note Generation:**
    *   Generates a formatted markdown note from the LLM output.
    *   Includes a YAML frontmatter with metadata (video title, link, channel, processing date, LLM model, system instruction, tags).
    *   Saves the note in the user's Obsidian vault, organized by channel name.
*   **Configuration:**
    *   Allows users to configure the Obsidian vault path, system instructions path, and LLM provider through a settings page.
    *   Stores configuration settings in a JSON file (`config.json`).
*   **User Interface:**
    *   Provides a Streamlit-based user interface with a main page for processing videos and a settings page for configuration.
    *   Keeps track of processed videos to prevent duplicate processing.

### 4. Architecture

The application follows a modular architecture with the following key components:

*   **Streamlit UI:** The main user interface for the application.
*   **YouTube Service:** Responsible for interacting with the YouTube APIs to extract video transcripts and metadata.
*   **LLM Orchestrator:** Manages the integration with different LLM providers through an adapter pattern.
*   **LLM Adapters:** Implementations for specific LLM providers (Anthropic, OpenAI, Ollama).
*   **Obsidian Gateway:** Handles the generation and storage of Obsidian notes in the user's vault.
*   **Configuration Manager:** Loads and saves the application's configuration from/to the `config.json` file.

The data flow is as follows:

1.  The user enters a YouTube video URL and selects a processing style in the Streamlit UI.
2.  The YouTube Service extracts the video transcript and metadata using the YouTube APIs.
3.  The LLM Orchestrator selects the appropriate LLM adapter based on the configuration.
4.  The LLM adapter processes the transcript using the selected LLM and system instruction.
5.  The Obsidian Gateway generates a formatted markdown note from the LLM output and saves it in the user's Obsidian vault.

### 5. Components

#### 5.1. Streamlit UI (`app.py`)

*   Provides the main user interface for the application.
*   Handles user input (YouTube video URL, processing style).
*   Displays processing status and results.
*   Implements the settings page for configuration.

#### 5.2. YouTube Service (`app.py`)

*   Extracts video ID from YouTube URL.
*   Fetches video transcript using the YouTube Transcript API.
*   Retrieves video metadata (channel name, title) using the YouTube Data API.
*   Sanitizes folder and file names for Obsidian compatibility.

#### 5.3. LLM Orchestrator (`app.py`)

*   Manages the integration with different LLM providers.
*   Selects the appropriate LLM adapter based on the configuration.
*   Processes the transcript using the selected LLM and system instruction.

#### 5.4. LLM Adapters (`llm_adapters.py`)

*   Implementations for specific LLM providers (Anthropic, OpenAI, Ollama).
*   Provide a consistent interface for processing transcripts with different LLMs.
*   Use the respective LLM provider's SDK to interact with the LLM API.

#### 5.5. Obsidian Gateway (`app.py`)

*   Handles the generation and storage of Obsidian notes in the user's vault.
*   Generates a formatted markdown note from the LLM output.
*   Includes a YAML frontmatter with metadata (video title, link, channel, processing date, LLM model, system instruction, tags).
*   Saves the note in the user's Obsidian vault, organized by channel name.

#### 5.6. Configuration Manager (`config_manager.py`)

*   Loads and saves the application's configuration from/to the `config.json` file.
*   Provides default configuration values.

### 6. Configuration

The application is configured using the `config.json` file. The following options are available:

*   `obsidian_vault_path`: Path to the Obsidian vault.
*   `system_instructions_path`: Path to the system instructions directory.
*   `llm_provider`: LLM provider to use (anthropic, openai, ollama).
*   `output_template`: Output template to use.

The configuration can be modified through the settings page in the Streamlit UI.

### 7. Implementation Details

*   **Programming Language:** Python
*   **Libraries and Frameworks:**
    *   Streamlit
    *   YouTube Transcript API
    *   Google API Client Library
    *   Anthropic/OpenAI SDKs
    *   Python Keyring
*   **LLM Integration:** Adapter pattern
*   **Configuration Management:** JSON file

### 8. Error Handling

The application implements the following error handling strategies:

*   **YouTube API failures:** Exponential backoff retry (3x).
*   **LLM rate limiting:** Circuit breaker pattern.
*   **File system errors:** Pre-flight permission checks.
*   **Invalid user inputs:** Regex validation + UI tooltips.

### 9. Security Requirements

*   API keys stored using system keyring.
*   Input validation for all user-provided paths.

### 10. Future Enhancements

*   Implement OpenAI and Ollama adapters.
*   Enhance error handling and user-facing error messages.
*   Implement a circuit breaker pattern for LLM rate limiting.
*   Add more configuration options (e.g., output template, LLM parameters).
*   Implement a more robust input validation system.