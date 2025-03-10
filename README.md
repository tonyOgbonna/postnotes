# PostNotes

## Description

PostNotes is a Streamlit application that processes YouTube video transcripts using LLMs and saves the output as structured Obsidian markdown notes. It is configurable and supports multiple LLM providers.

## Project Specification

Create a Streamlit based application that would take a YouTube video url, get the transcript, process the transcript using an LLM according to system instructions to the LLM, format the output as a structured Obsidian markdown, and store the output in a given folder within an Obsidian vault. It should be configurable, featuring a main page and a setting page. The configurable elements should include: the LLM model, system instruction, the output folder within Obsidian vault to save the output file.

Within the given Obsidian Vault it should check for a folder name same as the safe name of the YouTube video channel, if it exists save the result in that folder. If it doesn't create the folder then save the result there.

The available system instructions should be in the form of markdown files stored in a particular folder with the application folder. Each system instruction is identified within the app by their file name.

## Files

- `app.py`: Main Streamlit application file.
- `brief.md`: Project specification.
- `config.json`: Configuration file.
- `config_manager.py`: Configuration manager.
- `llm_adapters.py`: LLM adapter implementations.
- `project_summary.md`: Project summary.
- `spec.md`: Architecture specification.
- `system_instructions/`: Directory containing system instruction files.
- `update.md`: Update instructions.
- `venv/`: Virtual environment directory.

## Configuration

The application is configured using `config.json`. The following options are available:

- `obsidian_vault_path`: Path to the Obsidian vault.
- `system_instructions_path`: Path to the system instructions directory.
- `llm_provider`: LLM provider to use (anthropic, openai, ollama).
- `output_template`: Output template to use.

## Usage

1.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the application:
    ```bash
    streamlit run app.py
    ```

## Architecture

```mermaid
graph TD
    A[User Input] --> B(Streamlit UI)
    B --> C[YouTube Service]
    C --> D[Transcript Extraction]
    D --> E[LLM Orchestrator]
    E --> F[Anthropic Adapter]
    E --> G[OpenAI Adapter]
    E --> H[Ollama Adapter]
    F/G/H --> I[Processed Content]
    I --> J[Obsidian Gateway]
    J --> K[Channel-Specific Folders]
    K --> L[Markdown Notes]