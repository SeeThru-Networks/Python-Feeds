**************
SeeThru Feeds
**************

The SeeThru Networks python feed framework is a framework for creating feeds of services that either you or others have created.

Fundamentally feeds resolve to red, amber or green and a message, these feeds act as external feeds to the SeeThru platform.

Requirements
============

* Python: 3.5+

Installation
============

To install the latest development version, run:

::

  git clone https://github.com/SeeThru-Networks/Python-Feeds.git
  cd Python-Feeds
  pip3 install .
  pip3 install -r ./requirements.txt

This will install the SeeThru Feeds module as well as it's dependencies.

Usage
=====

You use a `ScriptResult` to store the result that you wish to publish to SeeThru Networks.

**Type Definition:**
::

    Creates a new script result

    Args:
        status: The status of the result
        message: The message of the result, "green", "amber" or "red"


**Example:**
::

    from SeeThru_Feeds.Model.Scripts.ScriptResult import ScriptResult
    
    result = ScriptResult("green", "message")


Once a `ScriptResult` has been created, you can then publish this to SeeThru Networks, you do this via a `Feed`.

::

    from SeeThru_Feeds.Model.Feeds.Feed import Feed

    f = Feed()
    f.set_api_key("Access_Token", "Secret_Key")
    f.set_guid("Guid")
    f.set_script_result(result)
    f.push()

Framework
=========

It is easy to get started with a feed scheme using the SeeThru Feeds module:

::

    seethrufeeds createfeedscheme <Scheme_Name> --path <Directory>

This command creates a new feed scheme with the scheme name in the given path

    If the path is left blank, the feed scheme is created in a subdirectory with the name ``Scheme_Name``

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
	├── config.json
	└── manage.py

The vendor directories are locations for you to store components and/or scripts that weren't created by you
and haven't been installed from PyPI, it provides separation between the scripts that you and others have created.

``manage.py`` is a python file which acts as an interface between the module and the feed scheme directory. 
Interaction with the feed scheme can be performed via manage.py.

``config.json`` is a configuration file that you can use to tell the module how to interact with the feedscheme,
the main purpose being to run the scheme.

By default the ``config.json`` is laid out as such:

:: 

    {
        "Header": {
            "Scheme_Name": "Scheme_Name",
            "Scheme_Description": "Enter a description for your feed scheme",
            "Scheme_Author": "Enter the author of your feed scheme",
            "Scheme_Owner": "Enter the owner for your feed scheme",
            "Creation_Date": "YYYY-mm-dd HH:MM:SS"
        }
    }

``Scheme_Name`` will have the scheme name that you defined when you created the feed scheme.
The other values you can fill out to give metadata to the feedscheme.

The ``config.json`` file will get filled out as you execute more functions from ``manage.py``, this is the default layout.

The feed scheme in its current state is fairly useless as it doesn't contain any scripts to execute.

    A script is a test that gets ran which evaluates to a colour code with a message.
    Each script is independent of each other.

    Think of a script as the test definition.

Scripts can be provided by others or created yourself

    **Only** use scripts provided by others if you trust the source, a malicious script can be dangerous

Once you have a script, you can add it to your config file

    Each script entry in the config file is an *instance* of that script, the same script can be used multiple times,
    each with a different name and properties

Say, for example, you were provided a script. You should add that script to ``Scripts/Vendor/``.
However, at this moment, the script would never run as it hasn't been added to the feedscheme config.

To add a script to the config file, you can run:

::

    python3 manage.py addscript <Script_Name> --script <Script_Object_Path>

* Script_Name:
    This is the name that you would like to give the instance of the script.
* Script_Object_Path:
    The script to import, relative to the base directory of the feedscheme.

    e.g. A script in the vendor folder would be represented as ``Scripts.Vendor@MyScript``.

    This is essentially a python import formatted as ``from@import``
    i.e. ``from SeeThru_Feeds.Library.Scripts.TCPPortOpen import PortOpen`` => ``SeeThru_Feeds.Library.Scripts.TCPPortOpen@PortOpen``

The script entered into the config looks like this:

::

    "<Script_Name>": {
        "Meta": {
            "Script_Name": ">Script_Name>",
            "Script_Output_Path": "<Script_Output_Path>",
            "Script_Object_Path": "<Script_Object_Path>"
        }
    }

The ``Meta`` section defines the meta about the script instance, this includes:
    * Script_Name:
        The name of the script instance

    * Script_Object_Path:
        This is the import path of the script object, i.e. the python line ``from Scripts.Script_File import Script_Object_Name`` translates to ``Scripts.Script_File@Script_Object_Name``.

        The Script_Object_Name is the script that will actually get executed and must inherit from ``SeeThru_Feeds.Model.Scripts.Script_Base``.

    * Script_Output_Path:
        This is the location that the output of the script will be stored, in general this should be under ``Outputs/`` and should have a file extension of ``.json``.

There are other sections of a script instance in the config file:
    * Fillables
    * States

Fillables:
    A fillable is a value that a script takes, the fillable is both named and typed.

    All fillables for a script in the config file exist under the ``Fillables`` section, and take the format:
    ``"<Fillable_Name>": "<Fillable_Value>"``

    e.g.
    ::

        "Fillables": {
            "host": "seethrunetworks.com"
        }

    This assigns the value ``seethrunetworks.com`` to the ``host`` fillable of the script

States:
    Some scripts may use the script state engine, this means that the script evaluates to a state
    which then gets translated into a status and message .

    A script will have default statuses and messages for the states that it uses however these can be overwritten.

    To overwrite a state for a script instance in the config file, you can run:

    ::

        python3 manage.py addscriptstate <Script_Name> --name <State_Name> --status <Status> --message "<Message>"

    Script_Name:
        This is the name of the script to overwrite the state of.

    State_Name:
        The name of the state to overwrite.

    Status
        The status to give the state, one of ``red``, ``amber`` or ``green``.

    Message
        The message to give the state.

    States have their own section for a script instance in the config file, e.g.

    ::

        "States": {
            "<State_Name>": {
                "Name": "<State_Name>",
                "Status": "<Status>",
                "Message": "<Message>"
            }
        }

Overall, the scripts section of the config file may look like this:

::

    "Scripts": {
        "<Script_Name>": {
            "Meta": {
                "Script_Name": "<Script_Name>",
                "Script_Output_Path": "<Script_Output_Path>",
                "Script_Object_Path": "<Script_Object_Path>"
            },
            "Fillables": {
                "<Fillable_Name>": "<Fillable_Value>"
            },
            "States": {
                "<State_Name>": {
                    "Name": "<State_Name>",
                    "Status": "<Status>",
                    "Message": "<Message>"
                }
            }
        }
    }

A new script can also be created via the cli:

::
    python3 manage.py createscript <Script_Name>

This will create a new script file in the ``Scripts/`` directory of the feed scheme using the template script,
naming it the same as ``Script_Name``. The script in the file will also have a name of ``Script_Name``.

This will also create an entry for the script in the config file, effectively running ``addscript`` for the new script.

The template script file looks as follows:

:: 

    from SeeThru_Feeds.Model.Scripts.ScriptBase import ScriptBase
    from SeeThru_Feeds.Model.Scripts.ScriptResult import ScriptResult
    from SeeThru_Feeds.Model.Properties.Properties import FillableProperty, ResultProperty


    class <Script_Name>(ScriptBase):
        EXAMPLE_PROPERTY = FillableProperty(name="example_property", required=False)

        Attr_Title="<Script_Name>"

        # ------ Script Overrides ------
        def script_run(self): pass
        def script_evaluate(self, result):
            result.set_status("green")
            result.set_message("")

The ``Script_Name`` occurrences will be replaced with the name that you gave.

``script_run`` is where your actual script should run it's tests, e.g. performing a ping and getting the latency.

Any properties that are needed by the Script should be declared in the class using the ``FillableProperty``
and ``ResultProperty`` objects, the properties perform validation on the values given to them

An example of a FillableProperty would be the ``host`` used in a test, this would have the parameters
``required=True`` and ``oftype=str`` to say that the property is required and must be of type string.
This is validated when the properties are used throughout the test

Any properties that are the result of your tests should be stored in ResultProperties,
this is so that users of your script know what your script produces and to provide a common interface for
accessing properties of a script.

An example of a ResultProperty would be a ``latency`` property, which stores the latency of a ping test.

``script_evaluate`` is where your script's test results should get evaluated into red, amber or green and a message produced.
The method takes a result parameter which will be of type ScriptResult. This object stores the colour and message of the script.
These can be set by using ``result.set_message()`` and ``Result.set_status()``.

To run your feed scheme, in the base directory you need to run:

::

	python3 manage.py runfeedscheme

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