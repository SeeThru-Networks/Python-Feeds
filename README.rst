**************
SeeThru Feeds
**************

A Python library for creating tests for services that either you have or others have created.

The tests that you create should have an output of either red, amber or green with a message. This is to enable an end user to easily understand the status of a service that they use without needing to understand the complexities of a test result.

Requirements
============

* Python: 3.x

Installation
============

To install the latest development version, run:

::

  git clone https://github.com/SeeThru-Networks/Python-Feeds.git
  cd python-feeds
  python setup.py install (or python3 setup.py install)

This will install the SeeThru Feeds module. You can also install the module in a ``virtualenv`` if you would like to do so.

Getting Started
===============

It is easy to get started with a testing scheme using the SeeThru Feeds module:

* ``cd`` into the directory you would like your testing scheme
* In the terminal run ``SeeThru_Feeds createfeedscheme <Scheme_Name>``

This will create a new subdirectory with the name given which contains a skeleton structure of a new test scheme.

The directory layout is a follows:

::

    .
    ├── Components
    │   ├── [Your_Components.py]
    │   ├── Vendor/
    │   │   ├── [Vendor_Components.py]
    ├── Scripts          
    │   ├── [Your_Scripts.py]
    │   ├── Vendor/
    │   │   ├── [Vendor_Scripts.py]
    ├── Outputs
    │   ├── [Test_Outputs.json]
    ├── config.toml
    └── manage.py

The vendor directories are locations for you to store components and/or scripts that weren't created by you and haven't been installed from PyPI, it provides seperation.

``manage.py`` is a python file which acts as an interface between the module and the feed scheme directory. 
Interaction with the feed scheme can be performed via manage.py.

``config.toml`` is a toml configuration file that you can use to tell the module how to interact with the feedscheme, the main purpose being to run the scheme.

By default the ``config.toml`` is laid out as such:

:: 

    Scheme_Name = "Scheme_Name"
    Scheme_Description = "Enter a description for your feed scheme"
    Scheme_Author = "Enter the author of your feed scheme"
    Scheme_Owner = "Enter the owner for your feed scheme"
    Creation_Date = "The current date"

``Scheme_Name`` will have the scheme name that you defined when you created the feed scheme. The other values you can fill out to give metadata to the scheme's config file.

The ``config.toml`` file will be filled out as you execute more functions from ``manage.py`` but this is the default config file contents

Definitions
===========
* Component: 
* Script: 
* Feed: 
* FeedScheme: 

API Reference
=============

``toml.load(f, _dict=dict)``
  Parse a file or a list of files as TOML and return a dictionary.

  :Args:
    * ``f``: A path to a file, list of filepaths (to be read into single
      object) or a file descriptor
    * ``_dict``: The class of the dictionary object to be returned

  :Returns:
    A dictionary (or object ``_dict``) containing parsed TOML data

  :Raises:
    * ``TypeError``: When ``f`` is an invalid type or is a list containing
      invalid types
    * ``TomlDecodeError``: When an error occurs while decoding the file(s)

``toml.loads(s, _dict=dict)``
  Parse a TOML-formatted string to a dictionary.

  :Args:
    * ``s``: The TOML-formatted string to be parsed
    * ``_dict``: Specifies the class of the returned toml dictionary

  :Returns:
    A dictionary (or object ``_dict``) containing parsed TOML data

  :Raises:
    * ``TypeError``: When a non-string object is passed
    * ``TomlDecodeError``: When an error occurs while decoding the
      TOML-formatted string

``toml.dump(o, f, encoder=None)``
  Write a dictionary to a file containing TOML-formatted data

  :Args:
    * ``o``: An object to be converted into TOML
    * ``f``: A File descriptor where the TOML-formatted output should be stored
    * ``encoder``: An instance of ``TomlEncoder`` (or subclass) for encoding the object. If ``None``, will default to ``TomlEncoder``

  :Returns:
    A string containing the TOML-formatted data corresponding to object ``o``

  :Raises:
    * ``TypeError``: When anything other than file descriptor is passed

``toml.dumps(o, encoder=None)``
  Create a TOML-formatted string from an input object

  :Args:
    * ``o``: An object to be converted into TOML
    * ``encoder``: An instance of ``TomlEncoder`` (or subclass) for encoding the object. If ``None``, will default to ``TomlEncoder``

  :Returns:
    A string containing the TOML-formatted data corresponding to object ``o``



Licensing
=========

This project is released under the terms of the MIT Open Source License. View
*LICENSE.txt* for more information.