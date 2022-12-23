"""Sphinx configuration."""
project = "Tic Tac Toe Game"
author = "Alexis Torelli"
copyright = "2022, Alexis Torelli"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
