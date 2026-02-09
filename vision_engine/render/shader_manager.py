"""
Shader Manager Module: Unified shader system for all backends
"""

from typing import Any, Dict, List, Optional
import os


class ShaderProgram:
    """Represents a compiled shader program."""
    
    def __init__(self, vertex_shader: str, fragment_shader: str, 
                 geometry_shader: Optional[str] = None):
        self.vertex_shader = vertex_shader
        self.fragment_shader = fragment_shader
        self.geometry_shader = geometry_shader
        self.compiled_handles = {}  # Backend-specific compiled handles
        
    def compile_for_backend(self, backend_type: str):
        """Compile this shader program for a specific backend."""
        # In a real implementation, this would compile the shader
        # for the specific backend (Vulkan, Metal, DX12, WebGPU)
        handle = f"{backend_type}_compiled_{id(self)}"
        self.compiled_handles[backend_type] = handle
        return handle


class ShaderManager:
    """
    Manages shaders for the visualization engine.
    
    Implements unified shader system that works across all backends.
    """
    
    def __init__(self):
        self.shader_cache = {}  # Cache of compiled shaders
        self.default_shaders = self._load_default_shaders()
        
    def _load_default_shaders(self) -> Dict[str, Dict[str, str]]:
        """Load default shaders for common visualization types."""
        return {
            "line": {
                "vertex": self._get_default_line_vertex_shader(),
                "fragment": self._get_default_line_fragment_shader()
            },
            "scatter": {
                "vertex": self._get_default_scatter_vertex_shader(),
                "fragment": self._get_default_scatter_fragment_shader()
            },
            "bar": {
                "vertex": self._get_default_bar_vertex_shader(),
                "fragment": self._get_default_bar_fragment_shader()
            },
            "point": {
                "vertex": self._get_default_point_vertex_shader(),
                "fragment": self._get_default_point_fragment_shader()
            },
            "ui_element": {
                "vertex": self._get_default_ui_vertex_shader(),
                "fragment": self._get_default_ui_fragment_shader()
            }
        }
        
    def _get_default_line_vertex_shader(self) -> str:
        """Get default vertex shader for line plots."""
        return """
        #version 450
        layout(location = 0) in vec3 position;
        
        void main() {
            gl_Position = vec4(position, 1.0);
        }
        """
        
    def _get_default_line_fragment_shader(self) -> str:
        """Get default fragment shader for line plots."""
        return """
        #version 450
        layout(location = 0) out vec4 fragColor;
        
        void main() {
            fragColor = vec4(0.2, 0.6, 1.0, 1.0);  // Blue color
        }
        """
        
    def _get_default_scatter_vertex_shader(self) -> str:
        """Get default vertex shader for scatter plots."""
        return """
        #version 450
        layout(location = 0) in vec3 position;
        layout(location = 1) in float pointSize;
        layout(location = 2) in vec4 color;
        
        out vec4 fragColor;
        
        void main() {
            gl_Position = vec4(position, 1.0);
            gl_PointSize = pointSize;
            fragColor = color;
        }
        """
        
    def _get_default_scatter_fragment_shader(self) -> str:
        """Get default fragment shader for scatter plots."""
        return """
        #version 450
        in vec4 fragColor;
        layout(location = 0) out vec4 outColor;
        
        void main() {
            outColor = fragColor;
        }
        """
        
    def _get_default_bar_vertex_shader(self) -> str:
        """Get default vertex shader for bar charts."""
        return """
        #version 450
        layout(location = 0) in vec3 position;
        
        void main() {
            gl_Position = vec4(position, 1.0);
        }
        """
        
    def _get_default_bar_fragment_shader(self) -> str:
        """Get default fragment shader for bar charts."""
        return """
        #version 450
        layout(location = 0) out vec4 fragColor;
        
        void main() {
            fragColor = vec4(0.8, 0.4, 0.2, 1.0);  // Orange color
        }
        """
        
    def _get_default_point_vertex_shader(self) -> str:
        """Get default vertex shader for point clouds."""
        return """
        #version 450
        layout(location = 0) in vec3 position;
        layout(location = 1) in float pointSize;
        layout(location = 2) in vec4 color;
        
        out vec4 fragColor;
        
        void main() {
            gl_Position = vec4(position, 1.0);
            gl_PointSize = pointSize;
            fragColor = color;
        }
        """
        
    def _get_default_point_fragment_shader(self) -> str:
        """Get default fragment shader for point clouds."""
        return """
        #version 450
        in vec4 fragColor;
        layout(location = 0) out vec4 outColor;
        
        void main() {
            outColor = fragColor;
        }
        """
        
    def _get_default_ui_vertex_shader(self) -> str:
        """Get default vertex shader for UI elements."""
        return """
        #version 450
        layout(location = 0) in vec2 position;
        layout(location = 1) in vec2 texCoord;
        
        out vec2 vTexCoord;
        
        void main() {
            gl_Position = vec4(position, 0.0, 1.0);
            vTexCoord = texCoord;
        }
        """
        
    def _get_default_ui_fragment_shader(self) -> str:
        """Get default fragment shader for UI elements."""
        return """
        #version 450
        in vec2 vTexCoord;
        layout(location = 0) out vec4 fragColor;
        
        void main() {
            fragColor = vec4(1.0, 1.0, 1.0, 1.0);  // White color
        }
        """
        
    def get_shader_for_geometry(self, geometry_type: str, 
                               material_properties: Dict[str, Any]) -> ShaderProgram:
        """
        Get an appropriate shader program for the given geometry type.
        
        Args:
            geometry_type: Type of geometry ('line', 'scatter', 'bar', etc.)
            material_properties: Material properties for customization
            
        Returns:
            ShaderProgram object
        """
        # Check if we have a cached shader for this combination
        cache_key = f"{geometry_type}_{hash(str(sorted(material_properties.items())))}"
        if cache_key in self.shader_cache:
            return self.shader_cache[cache_key]
            
        # Get default shaders for this geometry type
        if geometry_type in self.default_shaders:
            shaders = self.default_shaders[geometry_type]
            vertex_shader = shaders["vertex"]
            fragment_shader = shaders["fragment"]
        else:
            # Use a generic shader if type not recognized
            shaders = self.default_shaders["point"]
            vertex_shader = shaders["vertex"]
            fragment_shader = shaders["fragment"]
            
        # Customize shader based on material properties if needed
        vertex_shader, fragment_shader = self._customize_shader_with_material(
            vertex_shader, fragment_shader, material_properties
        )
        
        # Create and cache the shader program
        shader_program = ShaderProgram(vertex_shader, fragment_shader)
        self.shader_cache[cache_key] = shader_program
        
        return shader_program
        
    def get_shader_for_widget(self, widget_type: str, geometry_type: str,
                             material_properties: Dict[str, Any]) -> ShaderProgram:
        """
        Get an appropriate shader program for the given widget type.
        
        Args:
            widget_type: Type of widget ('button', 'slider', 'chart', etc.)
            geometry_type: Underlying geometry type
            material_properties: Material properties for customization
            
        Returns:
            ShaderProgram object
        """
        # For now, widgets use the same shaders as their underlying geometry
        # In a full implementation, widgets might have special shaders
        return self.get_shader_for_geometry(geometry_type, material_properties)
        
    def _customize_shader_with_material(self, vertex_shader: str, 
                                       fragment_shader: str,
                                       material_properties: Dict[str, Any]) -> tuple:
        """
        Customize shaders based on material properties.
        
        Args:
            vertex_shader: Original vertex shader code
            fragment_shader: Original fragment shader code
            material_properties: Material properties for customization
            
        Returns:
            Tuple of (modified vertex shader, modified fragment shader)
        """
        # Add material properties as uniforms to shaders if they're not already present
        # This is a simplified implementation - a full version would be more sophisticated
        
        modified_vs = vertex_shader
        modified_fs = fragment_shader
        
        # Add uniform declarations for common material properties
        if 'color' in material_properties:
            # Make sure fragment shader supports color uniform
            if 'uniform vec4 materialColor;' not in modified_fs:
                modified_fs = "#version 450\nuniform vec4 materialColor;\n" + modified_fs.replace(
                    "void main() {", 
                    "void main() {\n    vec4 baseColor = materialColor;"
                ).replace(
                    "fragColor =", 
                    "fragColor = baseColor * "
                )
        
        if 'opacity' in material_properties:
            # Make sure fragment shader supports opacity
            if 'uniform float opacity;' not in modified_fs:
                modified_fs = "#version 450\nuniform float opacity;\n" + modified_fs.replace(
                    "fragColor =", 
                    f"fragColor = vec4({material_properties.get('color', '1.0, 1.0, 1.0')}, opacity) * "
                )
        
        return modified_vs, modified_fs
        
    def register_custom_shader(self, name: str, vertex_shader: str, 
                              fragment_shader: str, geometry_types: List[str]):
        """
        Register a custom shader for specific geometry types.
        
        Args:
            name: Name to identify this shader
            vertex_shader: Vertex shader code
            fragment_shader: Fragment shader code
            geometry_types: List of geometry types this shader supports
        """
        for geom_type in geometry_types:
            self.default_shaders[geom_type] = {
                "vertex": vertex_shader,
                "fragment": fragment_shader
            }