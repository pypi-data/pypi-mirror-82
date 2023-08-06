File Validation
----------------

Python file validation module for structured text files.

This module runs through the rules defined within a config file and validates the data based on the given rules. Complex rules can be defined using regex expressions without boundaries.

System Requirements
--------------------

**Operating System**: Windows/Linux/Mac

**Python version**: 3.7 and above

Usage
-----

The module is available as a part of PyPI and can be easily installed
using ``pip``

::

    pip install filevalidation

Create a config file with ``.ini`` extension and specify the rules based off the below template

.. code-block:: yaml

    # This template can be used as the base to generate configuration files as required.
    # Do not use this configuration template directly for validation.
    # Use "#" or ";" for commenting lines within the configuration file. Do not comment section headers (enclosed within [])
    # By default : key:value pairs are case sensitive, unless explicitly specified.

    [global.settings]

    # Column delimiter in file
    Delimiter = \t

    # Expected file encoding
    Encoding =  utf-8

    [file.rules]

    # Expected filename. For complex filename, use regex pattern
    Filename = <filename>_\d{8}.txt

    # The below message is displayed if the file failed the filename validation test
    FilenameErrorMessage = The given file did not meet the expected filename or format.

    [header.rules]

    # Whether the header needs to be validated across the specified rules; yes/no
    ValidateHeader = yes

    # Treat header as case sensitive; yes/no
    CaseSensitive = yes

    # The below message is displayed if the file failed the header validation test where it could not find a match for the given header(s)
    # {headername} placeholder is dynamically replaced with the appropriate expected header during runtime and is optional. This placeholder cannot be used elsewhere.
    HeaderErrorMessage = Could not find a match for the header "{headername}"

    # Match header count to that of the given header; yes/no
    MatchHeaderCount = yes

    # The below message is displayed if the file failed the header validation test where the given header count and the expected header count do not match.
    # {requiredcount} placeholder is dynamically replaced with the expected header count during runtime
    # {availablecount} placeholder is dynamically replaced with the available header count from the file during runtime and is optional. This placeholder cannot be used elsewhere.
    HeaderCountErrorMessage = Header count does not match (required : {requiredcount} | available : {availablecount})

    [header]

    # Expected headers here. Each header in a new line
    header_1
    header_2
    header_n


    [column.rules]

    # Whether the column needs to be validated across the specified rules; yes/no
    ValidateColumn = yes


    [EmptyCheck]

    # [EmptyCheck] can be used to valiate whether the given value is Empty or not
    # The specified field/column records will be flagged if their value is empty or blank
    # This check trims out any leading/trailing white spaces before validation
    # Specify each FieldName to be validated in new line
    # Ex: FieldName1
    #     FieldName2

    # Note: If a field/column is not part of empty check, an empty/blank value is considered a valid value and other checks are skipped.

    header_n


    [EmptyCheck.description]

    # Description to describe in short about the check performed. This is included in the final report
    # {fieldname} placeholder is dynamically replaced with the appropriate expected header during runtime and is optional.
    Description = Empty check description here.

    [NumericCheck]

    # [NumericCheck] can be used to valiate whether the given value is a Number
    # The specified field/column records will be flagged if their value is not a number
    # This validates to True if the value is integer/decimal irrespective of signed/unsigned
    # Specify each FieldName to be validated in new line
    # Ex: FieldName1
    #     FieldName2

    [NumericCheck.description]

    # Description to describe in short about the check performed. This is included in the final report
    # {fieldname} placeholder is dynamically replaced with the appropriate expected header during runtime and is optional.
    Description = Numeric check description here.

    [IntegerCheck]

    # [IntegerCheck] can be used to valiate whether the given number is Integer or not
    # The specified field/column records will be flagged if their value is not an integer
    # This validates to True if the value is a positive/negative integer value
    # Specify each FieldName to be validated in new line
    # Ex: FieldName1
    #     FieldName2

    [IntegerCheck.description]

    # Description to describe in short about the check performed. This is included in the final report
    # {fieldname} placeholder is dynamically replaced with the appropriate expected header during runtime and is optional.
    Description = Integer check description here.

    [DecimalCheck]

    # [DecimalCheck] can be used to valiate whether the given number is Decimal or not
    # The specified field/column records will be flagged if their value is not a decimal
    # This validates to True if the value is a positive/negative decimal value
    # Specify each FieldName to be validated in new line
    # Ex: FieldName1
    #     FieldName2

    [DecimalCheck.description]

    # Description to describe in short about the check performed. This is included in the final report
    # {fieldname} placeholder is dynamically replaced with the appropriate expected header during runtime and is optional.
    Description = Decimal check description here.

    [FormatCheck]

    # [FormatCheck] validates the value on the given regex format.
    # The specified field/column records will be flagged if their value is not of expected format
    # Optionally, count can be specified to match the expected count of occurence of the given pattern
    # Optionally, ignorecase can be set to True or False to manage case-sensitivity on the regex pattern
    # Ex: FieldName = {"pattern": "[A-Za-z]", "count": 1}
    # Ex: FieldName = {"pattern": "[A-Za-z]"}
    # Ex: FieldName = {"pattern": "[A-Za-z]", "ignorecase": True}

    header_n = {"pattern": "^(C|B|X)$"}

    [FormatCheck.description]

    # Description to describe in short about the check performed. This is included in the final report
    # {fieldname} placeholder is dynamically replaced with the appropriate expected header during runtime and is optional.
    Description = Format check description here.

    [LengthCheck]

    # [LengthCheck] validates if the value falls between the min and max values. Here min value is optional
    # The specified field/column records will be flagged if their value is not of expected length
    # This check trims out any leading/trailing white spaces before validation
    # Ex: FieldName = {"min": 2, "max": 10}
    # Ex: FieldName = {"max": 255}
    # key:value is case-sensitive

    header_n = {"min": 1, "max": 1}


    [LengthCheck.description]

    # Description to describe in short about the check performed. This is included in the final report
    # {fieldname} placeholder is dynamically replaced with the appropriate expected header during runtime and is optional.
    Description = Length check description here.

With the config rules in place, create an instance of ``ValidateFile`` class and pass the path to the config file and source file as args. Then call the ``getresult()`` method which will return the validation summary as a python dictionary.

.. code-block:: python

    from validatefile.main import ValidateFile

    val = ValidateFile(configfile='/path/to/config/file', sourcefile='/path/to/source/file')

    res = val.getresult(outputdir=None)

    print(res)

When ``outputdir`` (path to a directory) is specified in ``getresult()``, validation results are written to an output file (tab delimited text file) in the given directory. This output file along with the source columns will contain 2 additional columns - ``_is_error`` and ``_error_desc``
where

* ``_is_error`` - (bool) This flag will be set to ``1`` if the line item / record failed any of the validation with respect to the given rules

* ``_error_desc`` - (str) Contains description of the error that caused the ``_is_error`` flag to appear as ``1``

.. code-block:: python

    from validatefile.main import ValidateFile

    val = ValidateFile(configfile='/path/to/config/file', sourcefile='/path/to/source/file')

    res = val.getresult(outputdir='/path/to/output/dir')

    print(res)

Sample outputs:

* No errors

.. code-block:: python

    {'Results': {'TotalRecordsAnalysed': 1000000, 'RecordsPassed': 1000000, 'RecordsFailed': 0, 'ErrorDetails': [], 'OutputFile': '/path/to/output/file.txt'}}

* Contains errors

.. code-block:: python

    {'Results': {'TotalRecordsAnalysed': 100, 'RecordsPassed': 0, 'RecordsFailed': 100, 'ErrorDetails': [{'FormatCheck': 100}], 'OutputFile': '/path/to/output/file.txt'}}


.. code-block:: python

    {'Results': {'TotalRecordsAnalysed': 10, 'RecordsPassed': 0, 'RecordsFailed': 10, 'ErrorDetails': [{'Level': 'Filename', 'Error': 'The given file did not meet the expected filename or format.'}, {'FormatCheck': 10}], 'OutputFile': '/path/to/output/file.txt'}}
