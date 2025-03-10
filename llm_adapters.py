from abc import ABC, abstractmethod
import keyring

class LLMAdapter(ABC):
    @abstractmethod
    def process(self, transcript, system_instruction):
        pass

class OpenAIAdapter(LLMAdapter):
    def process(self, transcript, system_instruction):
        # Implementation for OpenAI
        pass

class AnthropicAdapter(LLMAdapter):
    def process(self, transcript, system_instruction):
        import anthropic
        from pathlib import Path
        from app import ConfigManager  # Add missing import
        
        client = anthropic.Anthropic(
            api_key=keyring.get_password("postnotes", "anthropic")
        )
        
        # Get full path from config
        config = ConfigManager.load_config()
        instruction_path = Path(config["system_instructions_path"]) / system_instruction
        
        with open(instruction_path) as f:
            system_prompt = f.read()
        
        transcript_text = "\n".join(
            f"{entry['start']:.2f}: {entry['text']}"
            for entry in transcript
        )
        
        message = client.messages.create(
            model="claude-3-opus-20240229",
            system=system_prompt,
            max_tokens=4000,
            messages=[
                {
                    "role": "user",
                    "content": f"YouTube transcript:\n{transcript_text}"
                }
            ]
        )
        
        return message.content[0].text

class OllamaAdapter(LLMAdapter):
    def process(self, transcript, system_instruction):
        # Implementation for Ollama
        pass