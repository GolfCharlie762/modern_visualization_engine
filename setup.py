"""
Setup script for Vision Engine
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("LICENSE", "r", encoding="utf-8") as fh:
    license_text = fh.read()

setup(
    name="vision-engine",
    version="0.1.0",
    author="Vision Engine Team",
    author_email="info@visionengine.org",
    description="Modern Python Visualization Framework with GPU acceleration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vision-engine/vision-engine",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "cython>=0.29.0",  # For performance-critical components
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
        ]
    },
    entry_points={
        "console_scripts": [
            "vision-engine=vision_engine.cli:main",
        ],
    }
)