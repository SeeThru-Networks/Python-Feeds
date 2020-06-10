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
  cd Python-Feeds
  python setup.py install (or python3 setup.py install)

This will install the SeeThru Feeds module. You can also install the module in a ``virtualenv`` if you would like to do so.

Alternative Installation (WIP)
==============================

If you have docker on your system, use the included docker config (Dockerfile and docker-compose.yml) like this:

`docker-compose up -d`

That will download the necessary images and bring the container up. Once it is up, the following command
gives you a bash shell which uses that python. At a later time, we might add tests to run through this
container in CI/CD created environments.

`docker-compose exec python_feeds /bin/bash`

Why use docker-compose? It gives us a friendly service name (python_feeds) and at a later time, when we set up a
network of services to do automated testing, it will be useful.

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

The ``config.toml`` file will get filled out as you execute more functions from ``manage.py`` but this is the default config file contents.

The feed scheme in its current state is fairly useless as it doesn't contain any scripts to execute.

If you were to add a script that you found online and trust, you should add it to ``scripts/vendor/``.
However this script wouldn't be executed automatically when the feedscheme is ran as the script doesn't exist in ``config.toml``.
To make the script execute when the feedscheme is ran, you will want to add this block to the end on your config file:

::

	[[Scripts]]
		[Scripts.Script_Name]
			[Scripts.Script_Name.Meta]
				Script_Object_Path="Scripts.Script_File@Script_Object_Name"
				Script_Output_Path="Outputs/Script_Name.json"
			[Scripts.Script_Name.Fillables]
				fillable_0 = "Value_0"
				fillable_1 = {type="env", name="ENV_Variable_Name"}

The ``Script_Name`` can be anything you want, however this will be used internally to reference the script. 
This means that you could have multiple of the same script in the config file with different names but pass different fillables, to make the single script perform a slightly different test.
For example, you could create a generic script which tests if a socket is open and it requires a host as a ``fillable``, then in the config file, this script can be referenced multiple times to create multiple test feeds.

The ``Meta`` section defines the meta information about the feed, this includes:

* Script_Object_Path: 
	This is the import path of the script object, i.e. the python line ``from Scripts.Script_File import Script_Object_Name`` translates to ``Scripts.Script_File@Script_Object_Name``. 

	The Script_Object_Name is the script that will actually get executed and must inherit from ``SeeThru_Feeds.Model.Scripts.Script_Base``.
* Script_Output_Path: This is the location that the output of the script will be stored, in general this should be under ``outputs/`` and should have a file extension of ``.json``.

The ``Fillables`` section defines the values for the properties that the script will take, the value must follow the restrictions of the fillable property in the script.
e.g. If I had a fillable called ``host`` then in the ``Fillables`` section I would define: ``host= "seethrunetworks.co.uk"``. 
By default the variable that I assign the value to will be the name of the fillable property in the script however this can be changed by the script's author.

A lot of people will want to create a script themselves, this can be done via ``manage.py`` using ``createscript Script_Name``.
This will create a template script in the ``Scripts/`` directory and will create an entry in the ``config.toml`` file with accurate parameters meaning that the entry alread points to the new script.

The template script file looks as follows:

:: 

	from SeeThru_Feeds.Model.Scripts.ScriptBase import ScriptBase
	from SeeThru_Feeds.Model.Scripts.ScriptResult import ScriptResult
	from SeeThru_Feeds.Model.Properties.Properties import FillableProperty, ResultProperty

	class Script_Name(ScriptBase):
			EXAMPLE_PROPERTY = FillableProperty(name="example_property", required=False)

			Script_Title="Script_Name"

			# ------ Script Overrides ------
			def Script_Run(self): pass
			def Script_Evaluate(self, result):
				result.SetStatus("green")
				result.SetMessage("")

The Script_Name occurences will be replaced with the name that you gave.

``Script_Run`` is where your actual script should run it's tests, e.g. performing a ping and getting the latency.

Any properties that are needed by the Script should be declared in the class using the ``FillableProperty`` and ``ResultProperty`` objects, these will be defined later but as a wuick summary, they can ensure that conditions enfored on the values needed before execution.
An example of a FillableProperty would be the ``host`` used in a test, this would have the paremeters ``required=True`` and ``oftype=str`` to say that the property is required and must be of type string.

Any properties that are the result of your tests should be stored in ResultProperties, this is so that users of your script know what your script produces and to provice a common interface for accessing properties of a script.
An example of a ResultProperty would be a ``latency`` property, which stores the latency of a ping test.

``Script_Evaluate`` is where your script's test results should get evaluated into red, amber or green and a message produced. The method takes a result paramater which will be of type ScriptResult. This object stores the colour and message of the script.
These can be set by using ``result.SetMessage()`` and ``Result.SetStatus()``.

To run your feed scheme, in the base directory you need to run:

::

	python manage.py runfeedscheme (or python3 manage.py runfeedscheme)

Definitions
===========
* Component: A smaller piece of a collection of tests
* Script: A test which produces a colour and a message as an output
* Fillables: Values that can be set to a script before the script is ran
* Feed: An instance of a script which serves a specific purpose, it is the same as a SeeThru Feed
* FeedScheme: A collection of feeds that can be executed together

Notes
=====
* All paths including 'includes' are relative to the base directory of the feed scheme