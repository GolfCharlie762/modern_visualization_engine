"""
Layout Manager Module: Handles arrangement and positioning of visualization elements
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np


class LayoutManager:
    """
    Manages the layout and positioning of visualization elements.
    
    Handles grid layouts, flexible layouts, and custom arrangements for dashboards
    and multi-view visualizations.
    """
    
    def __init__(self):
        self.layouts = {}
        self.current_layout = None
        
    def create_grid_layout(self, rows: int, cols: int, 
                          element_ids: List[str],
                          padding: float = 10.0) -> Dict[str, Any]:
        """
        Create a grid layout for arranging visualization elements.
        
        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid
            element_ids: List of element IDs to arrange
            padding: Padding between elements
            
        Returns:
            Dictionary containing layout information
        """
        layout_id = f"grid_{rows}x{cols}_{len(self.layouts)}"
        
        # Calculate dimensions for each cell
        cell_width = 1.0 / cols
        cell_height = 1.0 / rows
        
        layout_info = {
            "type": "grid",
            "rows": rows,
            "cols": cols,
            "padding": padding,
            "elements": {}
        }
        
        # Assign positions to each element
        for idx, element_id in enumerate(element_ids):
            row = idx // cols
            col = idx % cols
            
            if row >= rows:
                break  # Not enough space in grid
                
            # Calculate position and size
            x = col * cell_width
            y = row * cell_height
            width = cell_width
            height = cell_height
            
            # Apply padding
            pad_x = padding / 100.0  # Normalize padding
            pad_y = padding / 100.0
            
            layout_info["elements"][element_id] = {
                "position": (x + pad_x/2, y + pad_y/2),
                "size": (width - pad_x, height - pad_y),
                "row": row,
                "col": col
            }
            
        self.layouts[layout_id] = layout_info
        self.current_layout = layout_id
        
        return layout_info
        
    def create_flex_layout(self, direction: str, element_ids: List[str],
                          ratios: Optional[List[float]] = None,
                          spacing: float = 10.0) -> Dict[str, Any]:
        """
        Create a flexible layout for arranging elements.
        
        Args:
            direction: Direction of layout ('horizontal', 'vertical')
            element_ids: List of element IDs to arrange
            ratios: Ratios for sizing elements (defaults to equal sizes)
            spacing: Spacing between elements
            
        Returns:
            Dictionary containing layout information
        """
        layout_id = f"flex_{direction}_{len(self.layouts)}"
        
        if ratios is None:
            ratios = [1.0] * len(element_ids)
            
        if len(ratios) != len(element_ids):
            raise ValueError("Ratios list must match length of element IDs")
            
        # Normalize ratios
        total_ratio = sum(ratios)
        normalized_ratios = [r/total_ratio for r in ratios]
        
        layout_info = {
            "type": "flex",
            "direction": direction,
            "spacing": spacing,
            "elements": {}
        }
        
        # Calculate positions based on direction
        if direction == "horizontal":
            current_pos = 0.0
            for i, (element_id, ratio) in enumerate(zip(element_ids, normalized_ratios)):
                width = ratio
                height = 1.0
                x = current_pos
                y = 0.0
                
                layout_info["elements"][element_id] = {
                    "position": (x, y),
                    "size": (width, height)
                }
                
                current_pos += width + (spacing / 100.0)  # Normalize spacing
                
        elif direction == "vertical":
            current_pos = 0.0
            for i, (element_id, ratio) in enumerate(zip(element_ids, normalized_ratios)):
                width = 1.0
                height = ratio
                x = 0.0
                y = current_pos
                
                layout_info["elements"][element_id] = {
                    "position": (x, y),
                    "size": (width, height)
                }
                
                current_pos += height + (spacing / 100.0)  # Normalize spacing
        else:
            raise ValueError("Direction must be 'horizontal' or 'vertical'")
            
        self.layouts[layout_id] = layout_info
        self.current_layout = layout_id
        
        return layout_info
        
    def create_custom_layout(self, element_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a custom layout with specific positioning for each element.
        
        Args:
            element_configs: List of dictionaries with element configuration
                           Each dict should have 'id', 'position', and 'size' keys
            
        Returns:
            Dictionary containing layout information
        """
        layout_id = f"custom_{len(self.layouts)}"
        
        layout_info = {
            "type": "custom",
            "elements": {}
        }
        
        for config in element_configs:
            element_id = config['id']
            position = config.get('position', (0.0, 0.0))
            size = config.get('size', (0.25, 0.25))  # Default to 25% of space
            
            layout_info["elements"][element_id] = {
                "position": position,
                "size": size
            }
            
        self.layouts[layout_id] = layout_info
        self.current_layout = layout_id
        
        return layout_info
        
    def apply_layout(self, layout_id: str) -> Dict[str, Any]:
        """
        Apply a previously created layout to arrange elements.
        
        Args:
            layout_id: ID of the layout to apply
            
        Returns:
            Layout information dictionary
        """
        if layout_id not in self.layouts:
            raise ValueError(f"Layout {layout_id} does not exist")
            
        self.current_layout = layout_id
        return self.layouts[layout_id]
        
    def get_element_position(self, element_id: str) -> Optional[Tuple[float, float]]:
        """
        Get the position of a specific element in the current layout.
        
        Args:
            element_id: ID of the element
            
        Returns:
            Position tuple (x, y) or None if element not found
        """
        if self.current_layout is None:
            return None
            
        layout = self.layouts[self.current_layout]
        element_info = layout["elements"].get(element_id)
        
        if element_info:
            return element_info["position"]
        else:
            return None
            
    def get_element_size(self, element_id: str) -> Optional[Tuple[float, float]]:
        """
        Get the size of a specific element in the current layout.
        
        Args:
            element_id: ID of the element
            
        Returns:
            Size tuple (width, height) or None if element not found
        """
        if self.current_layout is None:
            return None
            
        layout = self.layouts[self.current_layout]
        element_info = layout["elements"].get(element_id)
        
        if element_info:
            return element_info["size"]
        else:
            return None