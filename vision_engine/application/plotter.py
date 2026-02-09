"""
Plotter Module: High-level plotting functionality
"""

import numpy as np
from typing import Any, Dict, List, Optional, Union
from ..engine.scene_manager import SceneManager
from ..engine.data_pipeline import DataPipeline
from ..render.renderer import Renderer


class Plotter:
    """
    Main plotting interface for the Vision Engine.
    
    Provides high-level methods for creating various types of visualizations
    with automatic optimization and hardware acceleration.
    """
    
    def __init__(self, backend: str = "auto"):
        """
        Initialize the Plotter.
        
        Args:
            backend: Rendering backend ('vulkan', 'metal', 'dx12', 'webgpu', 'display', 'auto')
        """
        self.backend = backend
        self.scene_manager = SceneManager()
        self.data_pipeline = DataPipeline()
        self.renderer = Renderer(backend=backend)
        
    def plot(self, x: np.ndarray, y: np.ndarray, **kwargs) -> None:
        """
        Create a line plot.
        
        Args:
            x: X-axis data
            y: Y-axis data
            **kwargs: Additional styling options
        """
        # Process data through pipeline
        processed_data = self.data_pipeline.process_line_data(x, y)
        
        # Add to scene
        self.scene_manager.add_line(processed_data, **kwargs)
        
        # Render
        self.renderer.render(self.scene_manager.get_scene())
        
    def scatter(self, x: np.ndarray, y: np.ndarray, c: Optional[np.ndarray] = None, 
                s: Optional[Union[float, np.ndarray]] = None, **kwargs) -> None:
        """
        Create a scatter plot.
        
        Args:
            x: X-axis data
            y: Y-axis data
            c: Color values
            s: Size values
            **kwargs: Additional styling options
        """
        # Process data through pipeline
        processed_data = self.data_pipeline.process_scatter_data(x, y, c, s)
        
        # Add to scene
        self.scene_manager.add_scatter(processed_data, **kwargs)
        
        # Render
        self.renderer.render(self.scene_manager.get_scene())
        
    def bar(self, x: np.ndarray, height: np.ndarray, **kwargs) -> None:
        """
        Create a bar chart.
        
        Args:
            x: X-axis positions
            height: Bar heights
            **kwargs: Additional styling options
        """
        # Process data through pipeline
        processed_data = self.data_pipeline.process_bar_data(x, height)
        
        # Add to scene
        self.scene_manager.add_bar(processed_data, **kwargs)
        
        # Render
        self.renderer.render(self.scene_manager.get_scene())
        
    def histogram(self, data: np.ndarray, bins: int = 50, **kwargs) -> None:
        """
        Create a histogram.
        
        Args:
            data: Input data
            bins: Number of bins
            **kwargs: Additional styling options
        """
        # Process data through pipeline
        processed_data = self.data_pipeline.process_histogram_data(data, bins)
        
        # Add to scene
        self.scene_manager.add_histogram(processed_data, **kwargs)
        
        # Render
        self.renderer.render(self.scene_manager.get_scene())
        
    def show(self) -> None:
        """Display the current visualization."""
        self.renderer.display()
        
    def save(self, filename: str, **kwargs) -> None:
        """
        Save the visualization to a file.
        
        Args:
            filename: Output filename
            **kwargs: Additional saving options
        """
        self.renderer.save(filename, **kwargs)