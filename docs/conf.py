from datetime import date
import django
import os
import sys
from pathlib import Path

#sys.path.insert(0, str(Path('../../apis_core').resolve()))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'ANERO'
copyright = f"2016 - {date.today().year}, Austrian Centre for Digital Humanities at the Austrian Academy of Sciences"
# The default is "Author name not set"
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-author
author = ''
#release = '0.72.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["myst_parser", "autodoc2", "sphinx.ext.autodoc", "sphinx.ext.viewcode", "sphinx.ext.autodoc"]

autodoc2_packages = [{"path": "../apis_core", "exclude_dirs": ["__pycache__", "migrations"]}]

# the substitution extension allows us to use jinja variables
# in the markdown files. for the substitution list see the
# `myst_substitutions` definition
myst_enable_extensions = ["substitution"]


templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"

# the default is '{project} {release} documentation
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_title
html_title = "Anero"

myst_substitutions = {
        "project_name": project
}
