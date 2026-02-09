"""
Config Module: Configuration management for the Vision Engine
"""

import json
import os
from typing import Any, Dict, Optional


class Config:
    """
    Configuration manager for the Vision Engine.
    
    Handles loading, storing, and managing configuration settings.
    """
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self.settings = self._default_settings()
        
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
    
    def _default_settings(self) -> Dict[str, Any]:
        """Return default configuration settings."""
        return {
            "rendering": {
                "backend": "auto",
                "antialiasing": True,
                "vsync": True,
                "multisampling": 4,
                "max_fps": 60
            },
            "performance": {
                "use_gpu_acceleration": True,
                "lod_enabled": True,
                "streaming_buffer_size": 1024,
                "max_concurrent_operations": 8
            },
            "visualization": {
                "default_color_scheme": "viridis",
                "show_axes": True,
                "show_grid": True,
                "theme": "dark"
            },
            "data_processing": {
                "chunk_size": 10000,
                "use_zero_copy": True,
                "compression_enabled": True
            },
            "logging": {
                "level": "INFO",
                "performance_logging": True
            }
        }
    
    def load_from_file(self, filepath: str):
        """Load configuration from a JSON file."""
        try:
            with open(filepath, 'r') as f:
                file_config = json.load(f)
                self._merge_configs(self.settings, file_config)
        except FileNotFoundError:
            print(f"Config file {filepath} not found, using defaults")
        except json.JSONDecodeError:
            print(f"Invalid JSON in config file {filepath}, using defaults")
    
    def save_to_file(self, filepath: str):
        """Save current configuration to a JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.settings, f, indent=4)
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        Get a configuration value using dot notation.
        
        Args:
            key_path: Path to the setting using dot notation (e.g. 'rendering.backend')
            default: Default value to return if key doesn't exist
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.settings
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any):
        """
        Set a configuration value using dot notation.
        
        Args:
            key_path: Path to the setting using dot notation (e.g. 'rendering.backend')
            value: Value to set
        """
        keys = key_path.split('.')
        config_ref = self.settings
        
        for key in keys[:-1]:
            if key not in config_ref:
                config_ref[key] = {}
            config_ref = config_ref[key]
        
        config_ref[keys[-1]] = value
    
    def update(self, new_settings: Dict[str, Any]):
        """Update configuration with new settings."""
        self._merge_configs(self.settings, new_settings)
    
    def _merge_configs(self, base: Dict[str, Any], override: Dict[str, Any]):
        """Recursively merge override config into base config."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_configs(base[key], value)
            else:
                base[key] = value
    
    def reset_to_defaults(self):
        """Reset all settings to default values."""
        self.settings = self._default_settings()


# Global configuration instance
vision_engine_config = Config()