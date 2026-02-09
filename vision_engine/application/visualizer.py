"""
Visualizer Module: Advanced visualization functionality
"""

import numpy as np
from typing import Any, Dict, List, Optional, Union
from ..engine.scene_manager import SceneManager
from ..engine.data_pipeline import DataPipeline
from ..render.renderer import Renderer


class Visualizer:
    """
    Advanced visualization interface for complex and interactive visualizations.
    
    Provides methods for creating sophisticated visualizations with advanced features
    like interactivity, animation, and real-time updates.
    """
    
    def __init__(self, backend: str = "auto", interactive: bool = True):
        """
        Initialize the Visualizer.
        
        Args:
            backend: Rendering backend ('vulkan', 'metal', 'dx12', 'webgpu', 'auto')
            interactive: Enable interactive features
        """
        self.backend = backend
        self.interactive = interactive
        self.scene_manager = SceneManager()
        self.data_pipeline = DataPipeline()
        self.renderer = Renderer(backend=backend, interactive=interactive)
        
    def animate(self, update_func, interval: int = 50, **kwargs) -> None:
        """
        Create an animated visualization.
        
        Args:
            update_func: Function to update the data at each frame
            interval: Animation interval in milliseconds
            **kwargs: Additional animation options
        """
        self.renderer.animate(update_func, interval, **kwargs)
        
    def stream(self, data_generator, **kwargs) -> None:
        """
        Visualize streaming data in real-time.
        
        Args:
            data_generator: Generator yielding data chunks
            **kwargs: Additional streaming options
        """
        self.renderer.stream(data_generator, **kwargs)
        
    def create_dashboard(self, widgets: List[Dict], layout: str = "grid") -> None:
        """
        Create an interactive dashboard with multiple visualizations.
        
        Args:
            widgets: List of widget configurations
            layout: Dashboard layout ('grid', 'flex', 'custom')
        """
        self.scene_manager.create_dashboard(widgets, layout)
        self.renderer.render_dashboard(self.scene_manager.get_dashboard())
        
    def add_interaction(self, interaction_type: str, callback, **kwargs) -> None:
        """
        Add interactive elements to the visualization.
        
        Args:
            interaction_type: Type of interaction ('click', 'hover', 'zoom', 'pan')
            callback: Function to call when interaction occurs
            **kwargs: Additional interaction options
        """
        self.renderer.add_interaction(interaction_type, callback, **kwargs)
        
    def export_interactive(self, filename: str, **kwargs) -> None:
        """
        Export the visualization as an interactive HTML file.
        
        Args:
            filename: Output filename
            **kwargs: Additional export options
        """
        self.renderer.export_interactive(filename, **kwargs)