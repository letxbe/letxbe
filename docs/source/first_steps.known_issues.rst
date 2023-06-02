Known Issues
============

List of known issues
--------------------

Queue not respecting order
^^^^^^^^^^^^^^^^^^^^^^^^^^

The documents are not parsed following the order of upload.

Output typing
^^^^^^^^^^^^^

The response of ``get_document`` is either a ``Target`` or an
``Artefact`` instance. In both cases, the enum-values are reproduced as
python enums and not as strings, e.g.,
``'status_code': <DocumentStatus.SUCCESS: '200'>`` instead of
``'status_code': '200'``.

Overwriting the filename via metadata
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is possible to overwrite the filename of a file by specifying the
variable ``name`` in the metadata sent together with the file. Whenever
this is the case, the original file name is lost and cannot be
recovered.

No explicit and no documented errors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We are working to make every error explicit and documented. For the
moment, there are chances that you encounter not-documented and/or
not-explicit errors.

Too large files
^^^^^^^^^^^^^^^

Files exceeding 100MB cannot be posted for the moment due to Tornado
limitations. We are working to support larger files.

Report an issue
---------------

Use github default issue tracker or contact us via email at
team@letxbe.ai.
