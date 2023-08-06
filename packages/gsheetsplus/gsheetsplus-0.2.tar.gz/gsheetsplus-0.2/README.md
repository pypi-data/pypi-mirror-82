gsheetsplus
=======

|PyPI version| |License| |Supported Python| |Format|

|Travis| |Codecov| |Readthedocs-stable| |Readthedocs-latest|

``gsheetsplus`` is an extension over the ``gsheets`` library to provide added functionalities like plotting graphs between two axis.

``gsheets`` is a small wrapper around the `Google Sheets API`_ (v4) to provide
more convenient access to `Google Sheets`_ from Python scripts.

`Turn on the API`_, download an OAuth client ID as JSON file, and create a
``Sheets`` object from it. Use its index access (``__getitem__``) to retrieve
SpreadSheet objects by their id, or use ``.get()`` with a sheet URL.
Iterate over the ``Sheets`` object for all spreadsheets, or fetch spreadsheets
by title with the ``.find()`` and ``.findall()`` methods.

SpreadSheet objects are collections of WorkSheets, which provide access to the
cell values via spreadsheet coordinates/slices (e.g. ``ws['A1']``) and
zero-based cell position (e.g. ``ws.at(0, 1)``).

Links
-----

- GitHub: https://github.com/tanmaypandey7/gsheetsplus
- PyPI: https://pypi.org/project/gsheetsplus/

