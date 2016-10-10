"""Markdown filters

This file contains a collection of utility filters for dealing with 
markdown within Jinja templates.
"""
# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

import os
import subprocess
import warnings
from io import TextIOWrapper, BytesIO

try:
    from .markdown_mistune import markdown2html_mistune
except ImportError as e:
    # store in variable for Python 3
    _mistune_import_error = e
    def markdown2html_mistune(source):
        """mistune is unavailable, raise ImportError"""
        raise ImportError("markdown2html requires mistune: %s" % _mistune_import_error)

from nbconvert.utils.exceptions import ConversionException
from nbconvert.utils.version import check_version
from ipython_genutils.py3compat import cast_bytes
from .pandoc import convert_pandoc


__all__ = [
    'markdown2html',
    'markdown2html_pandoc',
    'markdown2html_mistune',
    'markdown2latex',
    'markdown2rst',
]


def markdown2latex(source, markup='markdown', extra_args=None):
    """
    Deprecated since version 5.0.

    Convert a markdown string to LaTeX via pandoc.

    This function will raise an error if pandoc is not installed.
    Any error messages generated by pandoc are printed to stderr.

    Parameters
    ----------
    source : string
      Input string, assumed to be valid markdown.
    markup : string
      Markup used by pandoc's reader
      default : pandoc extended markdown
      (see http://pandoc.org/README.html#pandocs-markdown)

    Returns
    -------
    out : string
      Output as returned by pandoc.
    """
    warnings.warn("""`markdown2latex` is deprecated in favor of 
                  `nbconvert.filters.pandoc.generic_pandoc` with 
                  appropriate arguments since nbconvert 5.0""")
    return generic_pandoc(source, markup, 'latex', extra_args=extra_args)


def markdown2html_pandoc(source, extra_args=None):
    """
    Deprecated since version 5.0.
    
    Convert a markdown string to HTML via pandoc.
    """
    extra_args = extra_args or ['--mathjax']
    warnings.warn("""`markdown2html_pandoc` is deprecated in favor of 
                  `nbconvert.filters.pandoc.generic_pandoc` with
                  appropriate arguments since nbconvert 5.0""")
    return generic_pandoc(source, 'markdown', 'html', extra_args=extra_args)


# The mistune renderer is the default, because it's simple to depend on it
markdown2html = markdown2html_mistune

def markdown2rst(source, extra_args=None):
    """
    Deprecated since version 5.0.

    Convert a markdown string to ReST via pandoc.

    This function will raise an error if pandoc is not installed.
    Any error messages generated by pandoc are printed to stderr.

    Parameters
    ----------
    source : string
      Input string, assumed to be valid markdown.

    Returns
    -------
    out : string
      Output as returned by pandoc.
    """
    warnings.warn("""`markdown2rst` is deprecated in favor of 
                  `nbconvert.filters.pandoc.generic_pandoc` with
                  appropriate arguments since nbconvert 5.0""")
    return generic_pandoc(source, 'markdown', 'rst', extra_args=extra_args)
