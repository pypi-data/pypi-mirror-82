Python Elasticsearch-to-CSV Export Tool
=======================================

Simple Python CLI tool to easily extract a massive amount of Elasticsearch documents into a csv file, exploiting multiprocessing features and leveraging the underneath elasticsearch-py package.

|

Requirements
------------

In order to install and use the `elasticsearch-tocsv <https://pypi.org/project/elasticsearch-tocsv/>`_ tool, you need to install the following packages first:

  * `elasticsearch-py <https://pypi.org/project/elasticsearch>`_
  * `requests <https://pypi.org/project/requests/>`_
  * `pandas <https://pypi.org/project/pandas/>`_
  * `pytz <https://pypi.org/project/pytz/>`_
  * `tqdm <https://pypi.org/project/tqdm/>`_ (unless you want to disable the loading progress bars)
  * `python >= 3.8 <https://www.python.org/downloads/release/python-380/>`_ (needed to avoid multiprocessing<-->logger problems)

|


Installation
------------

Install the ``elasticsearch-tocsv`` package with:

    $ ``pip3 install elasticsearch-tocsv``

Requiring of a version of python >=3.8 is not really mandatory (even 3.7 should work but needs to be tested first) but it's highly recommended since previous versions might have problems when logging in multiprocessing mode.

|

Arguments description
---------------------

Running ``elasticsearch_tocsv --help`` on the terminal you will be presented with all the possible arguments you can launch the command with. Some of them are mandatory, some others might depend on different ones. Here's the complete list of what the arguments are, if they are mandatory or optional and what they are thought for. Later on some use cases will be reported.

  **MANDATORY**

  * **-f, --fields**

    | Elasticsearch fields, passed as a string with commas between fields and no whitespaces (e.g. "field1,field2").

  * **-i, --index**

    | Elasticsearch index pattern to query on. To use wildcard (*), it'd be better to put the index between quotes (e.g. "my-indices*").

|
|


  **OPTIONAL**

  * **-af, --aggregation_fields** *[default: None]*

    | Set this option if you want to generate an additional file (raw exports file will still be generated) containing the info aggregated according to specific fields. 
    | Specify the fields to aggregate on as a string with commas between fields and no whitespaces (e.g. "field1,field2").

  * **-asi, --allow_short_interval** *[default: False]*

    | Set this option to True to allow the --load_balance_interval to go below 1 day. 
    | With this option enabled the --load_balance_interval can be set down to 1 minute (1m).

  * **-at, --aggregation_type** *[default: count]*

    | Aggregation function to use when generating the aggregated csv file. 
    | It can be one of the following: ['count', 'min', 'max', 'mean', 'sum']. 
    | *This option requires the --aggregation_fields to be set*.

  * **-b, --batch_size** *[default: 5000]*

    | Batch size for the scroll API. Max 10000. 
    | Increasing it might impact the ES instance heap memory. If you want to set a value greater than 10000, you must set the *max_result_window* elasticsearch property accordingly first. 
    | Please check out the `elasticsearch documentation <https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules.html>`_ before increasing that value. 

  * **-c, --cert_verification** *[default: False]*

    | Require ssl certificate verification. Set to True to enable it
    | *This option is ignored if --ssl is not set to True*.

  * **-cp, --certificate_path** *[default: '']*

    | Path to the certificate to verify the instance certificate against.
    | *This option is ignored if --ssl and --cert_verification are not set to True*.

  * **-dp, --disable_progressbar** *[default: False]*

    | Turn off the progressbar visualization.
    | Set to True to simply be noticed when processes have done fetching data, without the loading progressbars.
    | Might be useful in case you redirect the output to a file.

  * **-e, --export_path** *[default: es_export.csv]*

    | Path where to store the csv file. Make sure the user who's launching the script is allowed to write to that path. 
    | *WARNING*: At the end of the process, unless --keep_partial is set to True, all the files with filenames "[--export_path]_process*.csv" will be removed. Make sure you're setting a --export_path which won't accidentally delete any other file apart from the ones created by this script.

  * **-ed, --ending_date** *[default: now+1000y]*

    | Query ending date. Must be set in iso 8601 format, without the timezone (e.g. "YYYY-MM-ddTHH:mm:ss").
    | Timezone can be specified with the --timezone option.
    | *This option requires the --time_field to be set*.

  * **-em, --enable_multiprocessing** *[default: False]*

    | Enable the multiprocess options. Set to True to exploit multiprocessing. 
    | *This option requires the --time_field to be set*.

  * **-h, --help**

  * **-ho, --host** *[default: localhost]*

    | Elasticsearch host

  * **-k, --keep_partials** *[default: False]*

    | During the processing, various partial csv files will be created before joining them into a single csv. Set this flag to True if you want to keep also these partial files.
    | Notice the partial files will be kept anyway if something goes wrong during the creation of the final file.

  * **-lbi, --load_balance_interval** *[default: None]*

    | Set this option to build process intervals by events count rather than equally spaced over time. The shorter the interval, the better the events-to-process division, the heavier the initial computation to build the intervals. 
    | It cannot go below 1d if *--allow_short_interval* is not set. 
    | Allowed values are a number followed by one of *[m, h, d, M, y]*, like *1d* for 1 day or *4M* for 4 months. 
    | *Multiprocessing must be enabled to set this option*.

  * **-mf, --metadata_fields** *[default: '']*

    | Elasticsearch metadata fields (*_index*, *_type*, *_id*, *_score*), passed as a string with commas between fields and no whitespaces (e.g. "_id,_index").

  * **-o, --scroll_timeout** *[default: 4m]*

    | Scroll window timeout. Default to 4 minutes.

  * **-p, --port** *[default: 9200]*

    | Elasticsearch port.

  * **-pcs, --partial_csv_size** *[default: 10000000]*

    | Max number of rows each partial csv can contain. The higher the number of fields to extract, the lower this number should be not to keep too many data in memory. 
    | *If set, must be greater than --batch_size (default 5000)*

  * **-pn, --process_number** *[default to max number of cpu of the machine]*

    | Number of processes to run the script on.

  * **-pw, --password** *[default: None]*

    | Elasticsearch password in clear. 
    | If set, the *--secret_password* will be ignored. 
    | If both this and *--secret_password* are not set, a prompt password will be asked (leave it blank if not needed). 

  * **-q, --query_string** *[default: *]*

    | Elasticsearch query string. Put it between quotes and escape internal quotes characters (e.g. "one_field: foo AND another_field.keyword: \"bar\"").

  * **-rd, --remove_duplicates** *[default: False]*

    | Set to True to remove all duplicated events.
    | *WARNING*: two events with the same values of the fields specified in *--fields* will be considered duplicated and then unified even if on ES they might not be equal because of other fields not included in *--fields* (e.g. *_id*). 
    | Check out the *--metadata_fields* option to include further info like the ES _id.

  * **-s, --ssl** *[default: False]*

    | Require ssl connection. Set to True to enable it.

  * **-sd, --starting_date** *[default: now-1000y]*

    | Query starting date. Must be set in iso 8601 format, without the timezone (e.g. "YYYY-MM-ddTHH:mm:ss")
    | Timezone can be specified with the --timezone option.
    | *This option requires the --time_field to be set*.

  * **-spw, --secret_password** *[default: None]*

    | Env var pointing the Elasticsearch password. If both this a *--password* are not set, a prompt password will be asked (leave it blank if not needed).

  * **-t, --time_field** *[default: None]*

    | Time field to query on. If not set and *--starting_date* or *--ending_date* are set an exception will be raised.

  * **-tz, --timezone** *[default to timezone of the machine]*

    | Timezone to set according to the time zones naming convention (e.g. "America/New_York" or "Europe/Paris" or "UTC").

  * **-u, --user** *[default: '']*

    | Elasticsearch user, if any.

|

Usage examples
--------------

  * Connection to localhost to export fields *["@timestamp", "field_1", "field_2"]* of all the data of the ``my_sample_index`` index::

    $ elasticsearch_tocsv -i my_sample_index -f "@timestamp,field_1,field_2"

  * Connection to host 10.20.30.40 to export fields *["@timestamp", "field_1", "field_2"]* of the January 2020 data of the ``my_sample_index``. Export to the file *my_export_file.csv*::

    $ elasticsearch_tocsv -ho 10.20.30.40 -i my_sample_index -f "@timestamp,field_1,field_2" -sd "2020-01-01T00:00:00" -ed "2020-02-01T00:00:00" -t "@timestamp" -e my_export_file.csv

  * Connection to localhost over SSL to export fields *["@timestamp", "field_1", "field_2"]* of all the data of the ``my_sample_index`` index. Authentication is required::

    $ elasticsearch_tocsv -i my_sample_index -f "@timestamp,field_1,field_2" -s True -u my_user

  * Connection to localhost over SSL with certificate verification to export fields *["@timestamp", "field_1", "field_2"]* of all the data of the ``my_sample_index`` index::

    $ elasticsearch_tocsv -i my_sample_index -f "@timestamp,field_1,field_2" -s True -c True -ca "path/to/certificate.pem"

  * Connection to localhost to export fields *["@timestamp", "field_1", "field_2"]* of all the data of the ``my_sample_index`` index, exploiting multiprocessing::

    $ elasticsearch_tocsv -i my_sample_index -f "@timestamp,field_1,field_2" -em True -t "@timestamp"

  * Connection to localhost to export fields *["@timestamp", "field_1", "field_2"]* of the January 2020 data of the ``my_sample_index`` index, exploiting multiprocessing but dividing processing intervals by load time with a 1 day precision::

    $ elasticsearch_tocsv -i my_sample_index -f "@timestamp,field_1,field_2" -sd "2020-01-01T00:00:00" -ed "2020-02-01T00:00:00" -t "@timestamp" -em true -lbi 1d

|

Known bugs and required fixes
-----------------------------

  1. **Standard output multiprocessing printing when progress bars are not disabled**
    
    This is a known issue. When multiprocessing is enabled, progress bars printing might get a bit messy from time to time. No real problems in the usage but I know it might be a bit annoying. It's gonna be fixed as soon as possible hopefully.``