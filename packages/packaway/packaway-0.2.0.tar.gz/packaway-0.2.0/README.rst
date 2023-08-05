Packaway: Packaging Static Checker
==================================

Packaway is a tool for enforcing encapsulation and access control in Python
by performing static code analysis.

Currently the distribution supplies a flake8 plugin.

Installing
----------

To install::

    $ pip install packaway


Flake8 plugin
-------------

To verify the packaway flake8 plugin is installed::

    $ flake8 --version
    3.8.3 (mccabe: 0.6.1, packaway-import: 0.1.2, pycodestyle: 2.6.0, pyflakes: 2.2.0) CPython 3.8.1 on Linux

To lint your file::

    $ flake8 example.py
    example.py:1:1: DEP401 Importing private name 'package._name'.

This plugin currently provides two import rules:

#. DEP401: Disallowing import of private modules
#. DEP501: Disallowing imports using regular expression patterns

DEP401: Packaging rules using underscores
-----------------------------------------

Whether a module is internal or not is indicated by whether its name has a
single preceding underscore. If it does, then it is only "visible" within the
package the module resides. Similarly, a function whose name has a preceding
underscore is only "visible" to members with in the same module where the
function is defined.

Suppose a project has the following structure::

    ./package
        ./person
            __init__.py
            api.py
            _greeting.py
            _reading.py
        ./office
            __init__.py
            api.py
            _hours.py
            ./_legal
                __init__.py
                api.py
                _compliance.py
            ./_accounting
                __init__.py
                api.py
                _booking.py

One may use the plugin to capture the following import violations::

    ./office/api.py:7:1: DEP401 Importing private name 'person._reading'.
    ./office/api.py:13:1: DEP401 Importing private name 'office._legal._compliance'.
    ./office/_hours.py:2:1: DEP401 Importing private name 'office._accounting._booking'.
    ./office/_hours.py:8:1: DEP401 Importing private name 'package.office._legal.api'.
    ./office/_legal/_compliance.py:8:1: DEP401 Importing private name 'office._accounting._booking'.
    ./person/_greeting.py:5:1: DEP401 Importing private name 'person._reading._private_name'.
    ./person/api.py:5:1: DEP401 Importing private name 'person._reading._private_name'.


See the ``examples/package`` folder for this example.

DEP501: Import rules using regular expressions
----------------------------------------------

There maybe situations where the use of preceding underscores may not be
possible (e.g. backward compatibility constraints). One can specify import
rules at a lower level using file name patterns and import module name
patterns.

Suppose a project has the following structure::

    ./regex_rule_example
        ./business
            ./subpackage
                __init__.py
                bad.py
        ./data
            __init__.py
            api.py
        ./web
            __init__.py
            api.py

The ``business`` package contains business logic and should not import from
the ``web`` nor the ``data`` package. In this case, one can add the following
rules to the configuration file for flake8::

    [flake8]
    disallowed =
        business/*: web.*
        business/subpackage/*: data.*

On the right hand side is the regular expression for matching disallowed import
module names (after being normalized to an absolute import). On the left hand
side are UNIX-style patterns for matching source files on which the import rule
applies.

See the ``examples/regex_rule_example`` folder for this example.

Limitations
-----------
This tool does not capture accessing privately named attribute on a module
(an object in general) that can otherwise be imported following the above
rules.

Motivation
----------
Python does not enforce encapsulations. While this is enpowering for use cases
where encapsulation matters little and has made Python hugely accessible to
beginners, this means more disciplines are required for developers working on
large systems (with great power comes great responsibility).

Consequently, Python developers often rely on implicit naming conventions such
as a preceding underscore to signal something being hidden. However this can
only be enforced by vigorous code review. For a team of developers with
different skill levels, this is difficult to achieve for a large project.
Even the most seasoned developer with the best intention could still make
mistakes, especially if the intended visibility of a software component isn't
obvious.

Many programming languages (e.g. Java, C#, C++) offer programmers ways to
control over what is hidden and what is accessible via "access modifiers"
or keywords such as "public", "private" and "internal". These protections are
enforced by the compilers, but can be overruled with some efforts.

Packaway is created in order to provide a relatively easy way to enforce
encapsulation in Python at the module level in a way that is not intrusive.
