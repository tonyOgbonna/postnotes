import streamlit as st
import json
import keyring
import re
import sys
from googleapiclient.discovery import build
from pathlib import Path
from youtube_transcript_api import YouTubeTranscriptApi
from datetime import datetime
from llm_adapters import OpenAIAdapter, AnthropicAdapter, OllamaAdapter
from config_manager import ConfigManager

# Add project root to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

# YouTube Service
def extract_system_instruction_name(instruction_path: str) -> str:
    """Extracts the system instruction name from the first level 1 header in the file."""
    try:
        with open(instruction_path, 'r') as f:
            first_line = f.readline().strip()
            match = re.match(r'^#\s+(.*)$', first_line)
            if match:
                return match.group(1)
            else:
                return "Untitled"
    except Exception:
        return "Untitled"

class YouTubeService:
    @staticmethod
    def get_video_id(url: str) -> str:
        return url.split('v=')[1].split('&')[0]

    @staticmethod
    def get_transcript(video_id: str):
        return YouTubeTranscriptApi.get_transcript(video_id)

    @staticmethod
    def get_video_info(video_id: str):
        youtube = build(
            "youtube",
            "v3",
            developerKey=keyring.get_password("postnotes", "youtube_api_key")
        )
        
        request = youtube.videos().list(
            part="snippet",
            id=video_id
        )
        response = request.execute()
        
        snippet = response["items"][0]["snippet"]
        return {
            "channel": snippet["channelTitle"],
            "title": YouTubeService.sanitize_file_name(snippet["title"]),
            "video_id": video_id
        }

    @staticmethod
    def sanitize_folder_name(name: str) -> str:
        return name

    @staticmethod
    def sanitize_file_name(name: str) -> str:
        return "".join([c if c.isalnum() or c in " -" else "" for c in name]).strip()

# LLM Adapters
class LLMOrchestrator:
    def __init__(self, provider):
        self.provider = provider
        self.adapters = {
            'openai': OpenAIAdapter(),
            'anthropic': AnthropicAdapter(),
            'ollama': OllamaAdapter()
        }

    def process_transcript(self, transcript, system_instruction):
        adapter = self.adapters[self.provider]
        return adapter.process(transcript, system_instruction)

# Obsidian Integration
class ObsidianGateway:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)

    def save_note(self, content, channel_name, filename, system_instruction_name, video_info, llm_provider):
        channel_dir = self.vault_path / video_info["channel"]
        channel_dir.mkdir(exist_ok=True)

        # Extract title from LLM output
        title_match = re.search(r'### Title:\s*(.*)', content)
        if title_match:
            llm_title = title_match.group(1).strip()
        else:
            llm_title = video_info['title']  # Fallback to video title

        # Create filename from LLM title and system instruction name
        new_filename = f"{llm_title} - {system_instruction_name}.md"

        # Create frontmatter
        frontmatter = f"""---
title: "{video_info['title']}"
link: "https://youtube.com/watch?v={video_info['video_id']}"
channel: "{video_info["channel"]}"
processed_at: {datetime.now().isoformat()}
llm_model: "{llm_provider}"
system_instruction: "{system_instruction_name}.md"
tags: ["{system_instruction_name.replace(' ', '-')}"]
---
"""

        (channel_dir / new_filename).write_text(frontmatter + content)

# Main App
def main_page():
    st.title("PostNotes Processor")
    config = ConfigManager.load_config()

    # Initialize session state for processed videos
    if "processed_videos" not in st.session_state:
        st.session_state.processed_videos = {}

    # Ensure system instructions directory exists
    Path(config["system_instructions_path"]).mkdir(exist_ok=True)

    with st.form("processing_form"):
        url = st.text_input("YouTube Video URL", placeholder="https://youtube.com/watch?v=...")
        system_instruction = st.selectbox(
            "Processing Style",
            [f.name for f in Path(config["system_instructions_path"]).glob("*.md") if f.is_file()]
        )

        if st.form_submit_button("Process Video"):
            # Check if the video has already been processed with the same style
            if url in st.session_state.processed_videos and system_instruction in st.session_state.processed_videos[url]:
                st.warning(f"This video has already been processed with the '{system_instruction}' style.")
                return

            with st.status("Processing..."):
                try:
                    # Get and process transcript
                    video_id = YouTubeService.get_video_id(url)
                    st.write(f"Getting transcript for video: {video_id}")
                    transcript = YouTubeService.get_transcript(video_id)

                    # Process with LLM
                    st.write("Generating notes...")
                    llm = LLMOrchestrator(config["llm_provider"])
                    processed_content = llm.process_transcript(transcript, system_instruction)

                    # Get video info and save
                    video_info = YouTubeService.get_video_info(video_id)
                    obsidian = ObsidianGateway(config["obsidian_vault_path"])

                    # Extract system instruction name
                    instruction_path = Path(config["system_instructions_path"]) / system_instruction
                    system_instruction_name = extract_system_instruction_name(instruction_path)

                    obsidian.save_note(
                        processed_content,
                        video_info["channel"],
                        f"{video_info['title']}_{video_id}.md",
                        system_instruction_name,
                        video_info,
                        config["llm_provider"]
                    )

                    st.success("Note created successfully!")
                    st.markdown(processed_content, unsafe_allow_html=True)

                    # Update session state with processed video
                    if url not in st.session_state.processed_videos:
                        st.session_state.processed_videos[url] = []
                    st.session_state.processed_videos[url].append(system_instruction)

                except Exception as e:
                    st.error(f"Processing failed: {str(e)}")

    # Display processed videos
    if st.session_state.processed_videos:
        st.subheader("Processed Videos")
        
        # Create a list of dictionaries for the data editor
        processed_videos_list = []
        for url, styles in st.session_state.processed_videos.items():
            for style in styles:
                processed_videos_list.append({"url": url, "style": style})
        
        # Add a remove button for each row
        for i, row in enumerate(processed_videos_list):
            col1, col2, col3 = st.columns([0.6, 0.3, 0.1])
            with col1:
                st.write(row["url"])
            with col2:
                st.write(row["style"])
            with col3:
                if st.button("Remove", key=f"remove_{i}"):
                    url_to_remove = row["url"]
                    style_to_remove = row["style"]
                    st.session_state.processed_videos[url_to_remove].remove(style_to_remove)
                    if not st.session_state.processed_videos[url_to_remove]:
                        del st.session_state.processed_videos[url_to_remove]
                    st.rerun()

def settings_page():
    st.title("Configuration Settings")
    config = ConfigManager.load_config()
    
    with st.form("config_form"):
        vault_path = st.text_input(
            "Obsidian Vault Path", 
            value=config["obsidian_vault_path"],
            placeholder="/path/to/obsidian/vault"
        )
        llm_provider = st.selectbox(
            "LLM Provider",
            ["anthropic", "openai", "ollama"],
            index=["anthropic", "openai", "ollama"].index(config["llm_provider"])
        )
        
        if st.form_submit_button("Save Configuration"):
            new_config = {
                "obsidian_vault_path": vault_path,
                "system_instructions_path": config["system_instructions_path"],
                "llm_provider": llm_provider,
                "output_template": config["output_template"]
            }
            ConfigManager.save_config(new_config)
            st.success("Configuration saved!")

def main():
    st.set_page_config(layout="wide")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Main", "Settings"])

    if page == "Main":
        main_page()
    elif page == "Settings":
        settings_page()

if __name__ == "__main__":
    main()