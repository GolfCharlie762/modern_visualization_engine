"""
Scene Manager Module: Manages the scene graph and visualization components
"""

from typing import Any, Dict, List, Optional
import numpy as np


class SceneNode:
    """Base class for all scene nodes."""
    
    def __init__(self, node_id: str, node_type: str):
        self.node_id = node_id
        self.node_type = node_type
        self.children = []
        self.parent = None
        self.visible = True
        self.transform = np.eye(4)  # 4x4 identity matrix
        
    def add_child(self, child: 'SceneNode'):
        """Add a child node to this node."""
        child.parent = self
        self.children.append(child)
        
    def remove_child(self, child: 'SceneNode'):
        """Remove a child node from this node."""
        if child in self.children:
            child.parent = None
            self.children.remove(child)


class GeometryNode(SceneNode):
    """Scene node representing geometric data."""
    
    def __init__(self, node_id: str, geometry_type: str, data: Dict[str, Any]):
        super().__init__(node_id, "geometry")
        self.geometry_type = geometry_type
        self.data = data  # Contains vertices, indices, colors, etc.
        self.material_properties = {}


class SceneManager:
    """
    Manages the scene graph for the visualization.
    
    Handles adding, removing, and updating visualization elements in the scene.
    Implements adaptive LOD system and incremental updates.
    """
    
    def __init__(self):
        self.root_node = SceneNode("root", "root")
        self.nodes = {"root": self.root_node}
        self.camera_settings = {}
        self.lighting_settings = {}
        
    def add_line(self, data: Dict[str, Any], **kwargs) -> str:
        """
        Add a line visualization to the scene.
        
        Args:
            data: Line data containing x, y coordinates and other properties
            **kwargs: Additional styling options
            
        Returns:
            ID of the created node
        """
        node_id = f"line_{len(self.nodes)}"
        line_node = GeometryNode(node_id, "line", data)
        line_node.material_properties.update(kwargs)
        
        self.root_node.add_child(line_node)
        self.nodes[node_id] = line_node
        
        return node_id
    
    def add_scatter(self, data: Dict[str, Any], **kwargs) -> str:
        """
        Add a scatter plot to the scene.
        
        Args:
            data: Scatter data containing x, y coordinates, colors, sizes, etc.
            **kwargs: Additional styling options
            
        Returns:
            ID of the created node
        """
        node_id = f"scatter_{len(self.nodes)}"
        scatter_node = GeometryNode(node_id, "scatter", data)
        scatter_node.material_properties.update(kwargs)
        
        self.root_node.add_child(scatter_node)
        self.nodes[node_id] = scatter_node
        
        return node_id
        
    def add_bar(self, data: Dict[str, Any], **kwargs) -> str:
        """
        Add a bar chart to the scene.
        
        Args:
            data: Bar chart data containing x positions and heights
            **kwargs: Additional styling options
            
        Returns:
            ID of the created node
        """
        node_id = f"bar_{len(self.nodes)}"
        bar_node = GeometryNode(node_id, "bar", data)
        bar_node.material_properties.update(kwargs)
        
        self.root_node.add_child(bar_node)
        self.nodes[node_id] = bar_node
        
        return node_id
        
    def add_histogram(self, data: Dict[str, Any], **kwargs) -> str:
        """
        Add a histogram to the scene.
        
        Args:
            data: Histogram data containing bin edges and counts
            **kwargs: Additional styling options
            
        Returns:
            ID of the created node
        """
        node_id = f"histogram_{len(self.nodes)}"
        histogram_node = GeometryNode(node_id, "histogram", data)
        histogram_node.material_properties.update(kwargs)
        
        self.root_node.add_child(histogram_node)
        self.nodes[node_id] = histogram_node
        
        return node_id
        
    def update_node(self, node_id: str, data: Dict[str, Any]) -> bool:
        """
        Update an existing node with new data.
        
        Args:
            node_id: ID of the node to update
            data: New data for the node
            
        Returns:
            True if update was successful, False otherwise
        """
        if node_id in self.nodes:
            node = self.nodes[node_id]
            node.data.update(data)
            return True
        return False
        
    def remove_node(self, node_id: str) -> bool:
        """
        Remove a node from the scene.
        
        Args:
            node_id: ID of the node to remove
            
        Returns:
            True if removal was successful, False otherwise
        """
        if node_id in self.nodes and node_id != "root":
            node = self.nodes[node_id]
            if node.parent:
                node.parent.remove_child(node)
            del self.nodes[node_id]
            return True
        return False
        
    def get_scene(self) -> Dict[str, Any]:
        """
        Get the current scene representation.
        
        Returns:
            Dictionary containing the scene structure and data
        """
        scene_dict = {
            "nodes": {nid: {
                "type": node.node_type,
                "geometry_type": getattr(node, 'geometry_type', None),
                "data": getattr(node, 'data', {}),
                "material_properties": getattr(node, 'material_properties', {}),
                "transform": node.transform.tolist(),
                "visible": node.visible
            } for nid, node in self.nodes.items() if nid != "root"},
            "camera": self.camera_settings,
            "lighting": self.lighting_settings
        }
        return scene_dict
        
    def create_dashboard(self, widgets: List[Dict], layout: str = "grid") -> str:
        """
        Create a dashboard with multiple visualization widgets.
        
        Args:
            widgets: List of widget configurations
            layout: Dashboard layout type
            
        Returns:
            ID of the dashboard container node
        """
        dashboard_id = f"dashboard_{len(self.nodes)}"
        dashboard_node = SceneNode(dashboard_id, "dashboard")
        
        # Add widgets as child nodes
        for i, widget_config in enumerate(widgets):
            widget_id = f"widget_{dashboard_id}_{i}"
            widget_node = SceneNode(widget_id, "widget")
            widget_node.properties = widget_config
            dashboard_node.add_child(widget_node)
            
        self.root_node.add_child(dashboard_node)
        self.nodes[dashboard_id] = dashboard_node
        
        return dashboard_id
        
    def get_dashboard(self) -> Dict[str, Any]:
        """
        Get the dashboard scene representation.
        
        Returns:
            Dictionary containing the dashboard structure and widgets
        """
        return self.get_scene()