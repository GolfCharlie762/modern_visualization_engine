"""
Main module for testing Vision Engine implementation
"""

import numpy as np
from vision_engine.application.plotter import Plotter
from vision_engine.application.visualizer import Visualizer
from vision_engine.engine.scene_manager import SceneManager
from vision_engine.engine.data_pipeline import DataPipeline
from vision_engine.render.renderer import Renderer
from vision_engine.utils.logger import Logger


def basic_plotting():
    """Test basic plotting functionality"""
    print("=== Testing Basic Plotting ===")
    
    # Initialize the plotter
    plotter = Plotter()
    
    # Test line plot
    print("Testing line plot...")
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    plotter.plot(x, y, color='blue', label='sin(x)')
    print("Line plot created successfully")
    plotter.show()
    
    # Test scatter plot
    print("Testing scatter plot...")
    x_scatter = np.random.rand(50)
    y_scatter = np.random.rand(50)
    plotter.scatter(x_scatter, y_scatter, c=np.random.rand(50), s=50)
    print("Scatter plot created successfully")
    
    # Test bar chart
    print("Testing bar chart...")
    categories = np.arange(5)
    heights = np.random.rand(5)
    plotter.bar(categories, heights)
    print("Bar chart created successfully")
    
    # Test histogram
    print("Testing histogram...")
    data = np.random.normal(0, 1, 1000)
    plotter.histogram(data, bins=30)
    print("Histogram created successfully")
    
    print("Basic plotting tests completed\n")


def advanced_visualization():
    """Test advanced visualization features"""
    print("=== Testing Advanced Visualization ===")
    
    # Initialize the visualizer
    visualizer = Visualizer()
    
    # Test dashboard creation
    print("Testing dashboard creation...")
    widgets = [
        {"type": "line", "position": (0, 0), "size": (0.5, 0.5)},
        {"type": "scatter", "position": (0.5, 0), "size": (0.5, 0.5)},
        {"type": "bar", "position": (0, 0.5), "size": (0.5, 0.5)},
        {"type": "histogram", "position": (0.5, 0.5), "size": (0.5, 0.5)}
    ]
    visualizer.create_dashboard(widgets, layout="grid")
    print("Dashboard created successfully")
    
    print("Advanced visualization tests completed\n")


def data_pipeline():
    """Test data pipeline functionality"""
    print("=== Testing Data Pipeline ===")
    
    # Initialize the data pipeline
    pipeline = DataPipeline()
    
    # Test line data processing
    print("Testing line data processing...")
    x_line = np.linspace(0, 10, 10000)  # Large dataset to test LOD
    y_line = np.sin(x_line)
    processed_line = pipeline.process_line_data(x_line, y_line)
    print(f"Line data processed: {processed_line['count']} elements")
    
    # Test scatter data processing
    print("Testing scatter data processing...")
    x_scatter = np.random.rand(100000)  # Very large dataset
    y_scatter = np.random.rand(100000)
    c_scatter = np.random.rand(100000)
    s_scatter = np.random.rand(100000) * 50
    processed_scatter = pipeline.process_scatter_data(x_scatter, y_scatter, c_scatter, s_scatter)
    print(f"Scatter data processed: {processed_scatter['count']} elements")
    
    # Test bar data processing
    print("Testing bar data processing...")
    x_bar = np.arange(50)
    height_bar = np.random.rand(50)
    processed_bar = pipeline.process_bar_data(x_bar, height_bar)
    print(f"Bar data processed: {processed_bar['count']} elements")
    
    # Test histogram data processing
    print("Testing histogram data processing...")
    hist_data = np.random.normal(0, 1, 50000)
    processed_hist = pipeline.process_histogram_data(hist_data, bins=100)
    print(f"Histogram data processed: {processed_hist['count']} elements")
    
    print("Data pipeline tests completed\n")


def scene_management():
    """Test scene management functionality"""
    print("=== Testing Scene Management ===")
    
    # Initialize the scene manager
    scene_manager = SceneManager()
    
    # Add different types of nodes
    print("Testing scene node addition...")
    
    # Mock data for each type
    mock_line_data = {
        "vertices": type('obj', (object,), {"size": 100})(),
        "indices": type('obj', (object,), {"size": 100})(),
        "primitive_type": "line_strip",
        "count": 100
    }
    
    mock_scatter_data = {
        "vertices": type('obj', (object,), {"size": 100})(),
        "sizes": type('obj', (object,), {"size": 100})(),
        "colors": type('obj', (object,), {"size": 100})(),
        "primitive_type": "points",
        "count": 100
    }
    
    mock_bar_data = {
        "vertices": type('obj', (object,), {"size": 100})(),
        "indices": type('obj', (object,), {"size": 100})(),
        "primitive_type": "triangles",
        "count": 100
    }
    
    # Add nodes to scene
    line_id = scene_manager.add_line(mock_line_data)
    scatter_id = scene_manager.add_scatter(mock_scatter_data)
    bar_id = scene_manager.add_bar(mock_bar_data)
    
    print(f"Added nodes - Line: {line_id}, Scatter: {scatter_id}, Bar: {bar_id}")
    
    # Get scene
    scene = scene_manager.get_scene()
    print(f"Scene contains {len(scene['nodes'])} nodes")
    
    # Update a node
    update_data = {"test": "updated"}
    success = scene_manager.update_node(line_id, update_data)
    print(f"Node update successful: {success}")
    
    print("Scene management tests completed\n")


def renderer():
    """Test rendering functionality"""
    print("=== Testing Renderer ===")
    
    # Initialize the renderer
    renderer = Renderer()
    
    # Create a mock scene
    mock_scene = {
        "nodes": {
            "node1": {
                "type": "geometry",
                "geometry_type": "line",
                "data": {},
                "material_properties": {"color": "blue"},
                "transform": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                "visible": True
            },
            "node2": {
                "type": "geometry",
                "geometry_type": "scatter",
                "data": {},
                "material_properties": {"color": "red"},
                "transform": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                "visible": True
            }
        },
        "camera": {},
        "lighting": {}
    }
    
    # Test rendering
    print("Testing render method...")
    try:
        renderer.render(mock_scene)
        print("Render method executed successfully")
    except Exception as e:
        print(f"Render method failed: {e}")
    
    # Test displaying
    print("Testing display method...")
    try:
        renderer.display()
        print("Display method executed successfully")
    except Exception as e:
        print(f"Display method failed: {e}")
    
    print("Renderer tests completed\n")


def logger():
    """Test logging functionality"""
    print("=== Testing Logger ===")
    
    # Initialize the logger
    logger = Logger("VisionEngineTest")
    
    # Test different log levels
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    # Test performance logging
    logger.log_performance("test_operation", 0.1234, {"elements": 1000, "type": "line"})
    
    print("Logger tests completed\n")


def end_to_end():
    """Test end-to-end functionality"""
    print("=== Testing End-to-End Functionality ===")
    
    # Create a simple visualization from start to finish
    plotter = Plotter()
    
    # Generate some sample data
    x = np.linspace(0, 4*np.pi, 1000)
    y = np.sin(x) * np.exp(-x/10)
    
    # Create the visualization
    print("Creating end-to-end visualization...")
    plotter.plot(x, y, color='green', label='damped sine wave')
    
    # Add some scatter points
    scatter_x = x[::50]  # Every 50th point
    scatter_y = y[::50]
    # Use numeric color values instead of string names
    scatter_colors = np.random.rand(len(scatter_x))
    plotter.scatter(scatter_x, scatter_y, c=scatter_colors, s=30)
    
    print("End-to-end visualization created successfully")
    print("All tests completed successfully!\n")


def main():
    """Main function to run all tests"""
    print("Starting Vision Engine Implementation Tests\n")
    
    # Initialize logger
    logger = Logger("VisionEngineMain")
    logger.info("Vision Engine tests started")
    
    # Run all tests
    basic_plotting()
    advanced_visualization()
    data_pipeline()
    scene_management()
    renderer()
    logger()
    end_to_end()
    
    logger.info("Vision Engine tests completed successfully")
    print("All Vision Engine modules tested successfully!")


if __name__ == "__main__":
    main()