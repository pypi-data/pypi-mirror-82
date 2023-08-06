gsheetsplus
=======

``gsheetsplus`` is an extension over the [gsheets](https://github.com/xflr6/gsheets) library to provide added functionalities like plotting graphs between two axis.

[Turn on the API](https://developers.google.com/sheets/quickstart/python#step_1_turn_on_the_api_name), download an OAuth client ID as JSON file, and create a
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
- Download: https://pypi.org/project/gsheetsplus/#files

Installation
----------

This package runs under 3.8+, use pip to install:

```
pip install gsheetsplus
```
This will also install gsheets, matplotlib and their dependencies.

Quickstart
----------

Log into the [Google Developers Console](https://console.developers.google.com/) with the Google account whose
spreadsheets you want to access. Create (or select) a project and enable the
**Drive API** and **Sheets API** (under **Google Apps APIs**).

Go to the **Credentials** for your project and create **New credentials** >
**OAuth client ID** > of type **Other**. In the list of your **OAuth 2.0 client
IDs** click **Download JSON** for the Client ID you just created. Save the
file as ``client_secrets.json`` in your home directory (user directory).
Another file, named ``storage.json`` in this example, will be created after
successful authorization to cache OAuth data.

On you first usage of ``gsheets`` with this file (holding the client secrets),
your webbrowser will be opened, asking you to log in with your Google account
to authorize this client read access to all its Google Drive files and Google
Sheets.

Create a sheets object:

```python
>>> from gsheets import Sheets

>>> sheets = Sheets.from_files('~/client_secrets.json', '~/storage.json')
>>> sheets  #doctest: +ELLIPSIS
<gsheets.api.Sheets object at 0x...>
```

Fetch a spreadsheet by id or url:

```python
# id only
>>> sheet['1dR13B3Wi_KJGUJQ0BZa2frLAVxhZnbz0hpwCcWSvb20']
<SpreadSheet 1dR13...20 u'Spam'>

# id or url
>>> url = 'https://docs.google.com/spreadsheets/d/1dR13B3Wi_KJGUJQ0BZa2frLAVxhZnbz0hpwCcWSvb20'
>>> s = sheets.get(url)  
>>> s
<SpreadSheet 1dR13...20 u'Spam'>
```
Access worksheets and their values:

```python
# first worksheet with title
>>> s.find('Tabellenblatt2')
<WorkSheet 1747240182 u'Tabellenblatt2' (10x2)>

# worksheet by position, cell value by index
>>> s.sheets[0]['A1']
u'spam'

# worksheet by id, cell value by position
>>> s[1747240182].at(row=1, col=1)
1
```

Dump a worksheet to a CSV file:

```python
>>> s.sheets[1].to_csv('Spam.csv', encoding='utf-8', dialect='excel')
```
Dump all worksheet to a CSV file (deriving filenames from spreadsheet and
worksheet title):

```python
>>> csv_name = lambda infos: '%(title)s - %(sheet)s.csv' % infos
>>> s.to_csv(make_filename=csv_name)
```

Load the worksheet data into a pandas DataFrame (requires ``pandas``):

```python
>>> s.find('Tabellenblatt2').to_frame(index_col='spam')
        eggs
spam      
spam  eggs
...
```

``WorkSheet.to_frame()`` passes its kwargs on to ``pandas.read_csv()`` 

Plot graph between two axis(requires ``pandas``):
```python
>>> df = s.find("Sheet1").to_frame()
>>> sheets.plot(df, "offer_price", "average_sales", "graph")
>>> plt.show()
```

Detailed documentation for Gsheets can be found [here](https://gsheets.readthedocs.io/en/stable/api.html).

See also
--------
- [gsheets](https://github.com/xflr6/gsheets) Base library for gsheetsplus
- [gsheets.py](https://gist.github.com/xflr6/57508d28adec1cd3cd047032e8d81266) self-containd script to dump all worksheets of a Google
  Spreadsheet to CSV or convert any subsheet to a pandas DataFrame (Python 2
  prototype for this library)
- [gspread](https://pypi.org/project/gspread/) Google Spreadsheets Python API (more mature and featureful
  Python wrapper, currently using the XML-based [legacy v3 API](https://developers.google.com/google-apps/spreadsheets/))
- [example Jupyter notebook](https://gist.github.com/egradman/3b8140930aef97f9b0e4) using [gspread](https://pypi.org/project/gspread/) to fetch a sheet into a pandas
  DataFrame
- [df2gspread](https://pypi.org/project/df2gspread/) Transfer data between Google Spreadsheets and Pandas (build
  upon [gspread](https://pypi.org/project/gspread/), currently Python 2 only, GPL)
- [pygsheets](https://pypi.org/project/pygsheets/) Google Spreadsheets Python API v4 (v4 port of [gspread](https://pypi.org/project/gspread/)
  providing further extensions)
- [gspread-pandas](https://pypi.org/project/gspread-pandas/) Interact with Google Spreadsheet through Pandas DataFrames
- [pgsheets](https://pypi.org/project/pgsheets/) Manipulate Google Sheets Using Pandas DataFrames (independent
  bidirectional transfer library, using the [legacy v3 API](https://developers.google.com/google-apps/spreadsheets/), Python 3 only)
- [PyDrive](https://pypi.org/project/PyDrive/) Google Drive API made easy ([google-api-python-client](https://pypi.org/project/google-api-python-client/) wrapper
  for the [Google Drive](https://drive.google.com/) API, currently v2) 


License
-------

This package is distributed under the [MIT license](https://opensource.org/licenses/MIT).
