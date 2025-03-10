import json

class ConfigManager:
    CONFIG_PATH = "config.json"
    DEFAULT_CONFIG = {
        "obsidian_vault_path": "",
        "system_instructions_path": "Academy/projects/postnotes/system_instructions",
        "llm_provider": "anthropic",
        "output_template": "default"
    }

    @staticmethod
    def load_config():
        try:
            with open(ConfigManager.CONFIG_PATH, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return ConfigManager.DEFAULT_CONFIG

    @staticmethod
    def save_config(config):
        with open(ConfigManager.CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)