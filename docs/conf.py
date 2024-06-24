"""Sphinx configuration."""
project = "D4Utils"
author = "Per Unneberg"
copyright = "2024, Per Unneberg"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
