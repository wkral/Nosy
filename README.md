Nosy
====

Nosy will watch your project's source folder and execute a command of your
choosing whenever a watched source file changes.


Config file precedence:
-----------------------

    `pwd`/.nosy
    ~/.nosy

JSON Config example:
--------------------

    { "exec": "nosetests",
      "watch": ["*.py", "*.html", "*.js"] }
