1.0
===
Features
--------
-  Added version command.

Fixes
-----
-  Doc fixes: README install and usage instructions; help text.

Development
-----------
-  Updated release checklist.
-  Cleaned .gitignore, unit tests, etc.

0.1.0
=====
API Changes
-----------
-  Reset is now a subcommand:
   ::

      python -m ezoutlet reset 192.168.1.4

   This allows the future addition of multiple commands.

0.0.1-dev3
==========
API Changes
-----------
-  EzOutletReset is now EzOutlet.
-  EzOutlet: reset-specific arguments moved from constructor to reset().

Features
--------
-  Now Python 3 compatible, with universal wheel!

Fixes
-----
-  Doc fixes: LICENSE.txt, setup.py
-  Fixed some failing unit tests.

Development
-----------
-  Added badges for build and version.
-  Unit tests refactored for clarity and flexibility.

0.0.1-dev2
==========

-  Added CONTRIBUTING.rst.
-  Added install instructions to README.rst.

Initial Development Release - 0.0.1-dev1
========================================

-  Basic reset command.
-  API and usage subject to change.
