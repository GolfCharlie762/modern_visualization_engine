"""
Renderer Module: Main rendering interface and manager
"""

import numpy as np
from typing import Any, Dict, List, Optional, Callable
from .shader_manager import ShaderManager
from .vulkan_backend import VulkanBackend
from .webgpu_backend import WebGPUBackend


class Renderer:
    """
    Main renderer class that manages the rendering pipeline.
    
    Provides unified interface for different rendering backends
    and handles rendering operations like drawing, animation, and streaming.
    """
    
    def __init__(self, backend: str = "auto", interactive: bool = True):
        """
        Initialize the renderer.
        
        Args:
            backend: Rendering backend ('vulkan', 'metal', 'dx12', 'webgpu', 'auto')
            interactive: Enable interactive features
        """
        self.backend_name = backend
        self.interactive = interactive
        self.shader_manager = ShaderManager()
        
        # Initialize appropriate backend based on selection
        if backend == "vulkan" or (backend == "auto" and self._supports_vulkan()):
            self.backend = VulkanBackend()
        elif backend == "webgpu" or (backend == "auto" and self._supports_webgpu()):
            self.backend = WebGPUBackend()
        else:
            # Default to Vulkan if auto and no specific support detected
            self.backend = VulkanBackend()
            
        self.is_initialized = False
        self.viewport_size = (800, 600)
        
    def _supports_vulkan(self) -> bool:
        """Check if Vulkan is supported on this system."""
        try:
            # In a real implementation, this would check for Vulkan availability
            # For now, we'll assume it's supported
            return True
        except:
            return False
            
    def _supports_webgpu(self) -> bool:
        """Check if WebGPU is supported (typically in browser environment)."""
        try:
            # In a real implementation, this would check for WebGPU availability
            # For now, we'll assume it's supported in appropriate contexts
            return True
        except:
            return False
    
    def initialize(self):
        """Initialize the rendering backend."""
        if not self.is_initialized:
            self.backend.initialize()
            self.is_initialized = True
            
    def render(self, scene: Dict[str, Any]):
        """
        Render a scene.
        
        Args:
            scene: Scene dictionary containing nodes and their properties
        """
        if not self.is_initialized:
            self.initialize()
            
        # Prepare scene for rendering
        prepared_scene = self._prepare_scene(scene)
        
        # Render using backend
        self.backend.render(prepared_scene)
        
    def render_dashboard(self, dashboard_scene: Dict[str, Any]):
        """
        Render a dashboard scene.
        
        Args:
            dashboard_scene: Dashboard scene dictionary
        """
        if not self.is_initialized:
            self.initialize()
            
        # Prepare dashboard scene for rendering
        prepared_scene = self._prepare_dashboard_scene(dashboard_scene)
        
        # Render using backend
        self.backend.render(prepared_scene)
        
    def display(self):
        """Display the rendered output."""
        self.backend.display()
        
    def save(self, filename: str, **kwargs):
        """
        Save the rendered output to a file.
        
        Args:
            filename: Output filename
            **kwargs: Additional saving options
        """
        self.backend.save(filename, **kwargs)
        
    def animate(self, update_func: Callable, interval: int = 50, **kwargs):
        """
        Create an animated visualization.
        
        Args:
            update_func: Function to update the data at each frame
            interval: Animation interval in milliseconds
            **kwargs: Additional animation options
        """
        if not self.is_initialized:
            self.initialize()
            
        self.backend.animate(update_func, interval, **kwargs)
        
    def stream(self, data_generator, **kwargs):
        """
        Visualize streaming data in real-time.
        
        Args:
            data_generator: Generator yielding data chunks
            **kwargs: Additional streaming options
        """
        if not self.is_initialized:
            self.initialize()
            
        self.backend.stream(data_generator, **kwargs)
        
    def add_interaction(self, interaction_type: str, callback: Callable, **kwargs):
        """
        Add interactive elements to the visualization.
        
        Args:
            interaction_type: Type of interaction ('click', 'hover', 'zoom', 'pan')
            callback: Function to call when interaction occurs
            **kwargs: Additional interaction options
        """
        if self.interactive:
            self.backend.add_interaction(interaction_type, callback, **kwargs)
            
    def export_interactive(self, filename: str, **kwargs):
        """
        Export the visualization as an interactive HTML file.
        
        Args:
            filename: Output filename
            **kwargs: Additional export options
        """
        self.backend.export_interactive(filename, **kwargs)
        
    def _prepare_scene(self, scene: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare a scene for rendering by processing nodes and materials.
        
        Args:
            scene: Raw scene dictionary
            
        Returns:
            Prepared scene dictionary ready for rendering
        """
        # Process each node in the scene
        processed_nodes = {}
        
        for node_id, node_data in scene["nodes"].items():
            # Get appropriate shader for the geometry type
            geometry_type = node_data["geometry_type"]
            material_props = node_data["material_properties"]
            
            # Compile or retrieve appropriate shader
            shader_program = self.shader_manager.get_shader_for_geometry(
                geometry_type, material_props
            )
            
            # Process the node's data for rendering
            processed_node = {
                "id": node_id,
                "type": node_data["type"],
                "geometry_type": geometry_type,
                "data": self._process_node_data(node_data["data"]),
                "material_properties": material_props,
                "transform": np.array(node_data["transform"]),
                "visible": node_data["visible"],
                "shader": shader_program
            }
            
            processed_nodes[node_id] = processed_node
            
        return {
            "nodes": processed_nodes,
            "camera": scene["camera"],
            "lighting": scene["lighting"],
            "viewport_size": self.viewport_size
        }
        
    def _prepare_dashboard_scene(self, dashboard_scene: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare a dashboard scene for rendering.
        
        Args:
            dashboard_scene: Raw dashboard scene dictionary
            
        Returns:
            Prepared dashboard scene dictionary ready for rendering
        """
        # Similar to _prepare_scene but with additional dashboard-specific processing
        processed_nodes = {}
        
        for node_id, node_data in dashboard_scene["nodes"].items():
            # Get appropriate shader for the widget type
            node_type = node_data["type"]
            geometry_type = node_data["geometry_type"]
            material_props = node_data["material_properties"]
            
            # Compile or retrieve appropriate shader
            shader_program = self.shader_manager.get_shader_for_widget(
                node_type, geometry_type, material_props
            )
            
            # Process the node's data for rendering
            processed_node = {
                "id": node_id,
                "type": node_type,
                "geometry_type": geometry_type,
                "data": self._process_node_data(node_data["data"]),
                "material_properties": material_props,
                "transform": np.array(node_data["transform"]),
                "visible": node_data["visible"],
                "shader": shader_program
            }
            
            processed_nodes[node_id] = processed_node
            
        return {
            "nodes": processed_nodes,
            "camera": dashboard_scene["camera"],
            "lighting": dashboard_scene["lighting"],
            "viewport_size": self.viewport_size
        }
        
    def _process_node_data(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process node data for rendering.
        
        Args:
            node_data: Raw node data dictionary
            
        Returns:
            Processed node data ready for rendering
        """
        # Process GPU buffers
        processed_data = {}
        
        for key, value in node_data.items():
            if hasattr(value, 'transfer_to_gpu'):
                # This is a GPU buffer, make sure it's transferred
                value.transfer_to_gpu()
                processed_data[key] = value
            else:
                # Regular data, pass through
                processed_data[key] = value
                
        return processed_data