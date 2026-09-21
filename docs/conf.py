import pathlib
import sys
import tomllib

sys.path.insert(0, str(pathlib.Path('..').resolve()))


def _get_project_meta():
    with pathlib.Path('../pyproject.toml').open(mode='rb') as pyproject:
        return tomllib.load(pyproject)['tool']['poetry']


pkg_meta = _get_project_meta()
project = str(pkg_meta['name'])
copyright = '2019, dry-python team'
author = 'dry-python team'
version = str(pkg_meta['version'])
release = version
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'myst_parser',
    'sphinx_autodoc_typehints',
    'sphinxcontrib.mermaid',
]
autoclass_content = 'class'
autodoc_member_order = 'bysource'
autodoc_member_order = 'bysource'
autodoc_default_options = {
    'members': True,
    'undoc-members': '_laws',
    'exclude-members': '__dict__,__weakref__',
    'show-inheritance': True,
}
suppress_warnings = ['myst.header', 'myst.xref_missing']
always_document_param_types = True
templates_path = ['_templates']
source_suffix = ['.rst', '.md']
master_doc = 'index'
language = 'en'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
add_module_names = False
html_theme = 'furo'
html_static_path = ['_static']
napoleon_numpy_docstring = False
todo_include_todos = True
