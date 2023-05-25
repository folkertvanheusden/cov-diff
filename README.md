cov-diff
--------

This program calculates the difference between two c# coverage test runs.
That way, you can see what has been tested in the first run, what has been tested in the second run but not in the first run and what has not been tested in either run.


how it works
------------

Run:

* cov-diff.py first-run.xml second-run.xml difference.xml

Indeed, you need to convert the .coverage-files to xml first ( dotnet-coverage merge -o _coverage.xml_ -f xml _mytest.coverage_ ).

difference.xml can then be converted to a report using the regular "ReportGenerator"-tool (https://reportgenerator.io/).
What has been tested in the first run (e.g. in your unittests) is not colored. What has been tested in the second run but not in the first is green and not tested in both is red.



Written by Folkert van Heusden <mail@vanheusden.com>

Released under the GPL v3.
