"""
Vision Engine: Modern Python Visualization Framework
"""

__version__ = "0.1.0"
__author__ = "Vision Engine Team"

from .application import *
from .engine import *
from .render import *

__all__ = [
    # Application layer exports
    "Plotter",
    "Visualizer",
    # Engine layer exports
    "SceneManager",
    "DataPipeline",
    # Render layer exports
    "Renderer",
    "ShaderManager",
]