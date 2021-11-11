====================
diablo3_assistant_py
====================

What's This?
============

Some python scripts to assist playing Diablo III (Diablo 3, Diablo3, Diablo_3), mainly are keyboard and mouse macros.

Usage
======

Install Needed Libs
-------------------

.. code-blocks::

    pip install keyboard
    pip install mouse
    pip install ruamel.yaml
    pip install psutil

Note that:

    ``psutil`` will be easily installed if you are using python version <= 3.9.x.
    If you are using python 3.10.x, it will be complex to install this package for it might
    through out errors about lack of installation of C++ Builders.

Edit/Confirm Configurations
--------------------------

File: ``conf.py``

The Configurations are stored in YAML format, which is comfortable for human reading and writing.

The data scheme is described with in the the configuration file.

Select a Plan Name
-----------------

In ``diablo3_assist_stable.py`` 's end part, there's a ``if __name__ == '__main__'`` block,

edit the value of ``plan`` to a plan name written in ``conf.py``

Run the Script and Enjoy it!
---------------------------

.. code-block:: shell

    python ./diablo3_assist_stable.py

-   Press hotkey(s) bound to 'on' to start looping.
-   Press hotkey(s) bound to 'off' to stop(pause) looping.
-   Press the hotkey(only 1) to  'exit' to terminate the whole script.

Known Issues
------------

Versions <= 20211111:

    Held keys will be released if they are touched
    while they are loopped by the script, but the others are still looping.
    This will makes the loop incomplete, which I am not sure
    whether it's an issue. You could simply press <stop> and <start> hot key
    to restart the loop.

Release Notes
=============

See the commit messages.


Thanks To
=========

According to good ideas of August Mao,
this script was changed to a data-driven coding paradigm,
which provides a higher level of abstraction.
