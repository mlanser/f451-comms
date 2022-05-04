"""Sphinx configuration."""
import os
import sys
from datetime import datetime

# Extend 'sys.path' so Sphinx can find our 'src' dir
sys.path.insert(0, os.path.abspath(".."))

project = "f451 Communications"
author = "Martin Lanser"
copyright = f"{datetime.now().year}, {author}"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx_argparse_cli",
    "sphinx_click",
    "sphinx_rtd_theme",
]

# Misc settings
autodoc_typehints = "description"
html_theme = "sphinx_rtd_theme"
todo_include_todos = True

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True
