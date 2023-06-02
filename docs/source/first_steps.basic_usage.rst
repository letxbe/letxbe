Basic usage
===========

Here is an example of a flow using ``LXB``:

   1. Initialization of the class: authenticate to LetXBe.
   2. Post a target.
   3. Get the prediction.


After initialisation, a more complex flow would be:
   1. Post an artefact.
   2. Post a target connected to the artefact.
   3. Get the target's prediction

For the difference between a ``Target`` and an ``Artefact``, we refer to the
:ref:`Type <type>` module.

Initialization and authentication
---------------------------------

You need a ``client_id`` and a ``client_secret`` to initialize the ``LXB`` class.

.. code:: python

   from letxbe import LXB

   CLIENT_ID = "ClientID"
   CLIENT_SECRET = "ClientSecret"

   lxb = LXB(CLIENT_ID, CLIENT_SECRET)

You can access the bearer token used in the authorization header via
the property ``LXB.authorization_header``.

Common actions
--------------

Post a target
^^^^^^^^^^^^^

.. code:: python

   from letxbe.type import ClientEnv, Metadata

   atms_slug = "automatisme-slug"
   client_env = ClientEnv.PROD

   metadata = Metadata(
      client_env=client_env,
      name="Name to give the document for users to identify it easily.",
   )

   filename = "your_target_file.pdf"
   file = (filename, open(filename, "rb").read())

   target_slug = lxb.post_target(atms_slug, metadata, file)
   # >  target_slug = "your_target_file051394-16733444059802482"

Post an artefact
^^^^^^^^^^^^^^^^
*DOCUMENTATION IN PROGRESS*

.. code:: python

   from letxbe.type import ClientEnv, Metadata

   atms_slug = "automatisme-slug"
   client_env = ClientEnv.PROD

   role = "artefact_role"

   # An existent artefact can be connected to the new one
   other_role = "other_artefact_role"
   other_artefact_slug = "other-artefact-slug"

   metadata = Metadata(
      client_env=client_env,
      name="Name to give the document for users to identify it easily.",
      form={},
      artefact={
         other_role: {"slug": other_artefact_slug}
      }
   )

   filename = "your_artefact_file.csv"
   file = (filename, open(filename, "rb").read())

   new_artefact_slug = lxb.post_artefact(
      atms_slug, role, metadata, file
   )
   # >  new_artefact_slug = "your_artefact_file051394-16733444059802482"

Post a target connected to an artefact
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
*DOCUMENTATION IN PROGRESS*

.. code:: python

   from letxbe.type import ClientEnv, Metadata

   atms_slug = "automatisme-slug"
   client_env = ClientEnv.PROD

   # An existent artefact can be connected to the target
   artefact_role = "artefact_role"
   artefact_slug = "artefact-slug"

   metadata = Metadata(
      client_env=client_env,
      name="Name to give the document for users to identify it easily.",
      form={},
      artefact={
         artefact_role: {"slug": artefact_slug}
      }
   )

   filename = "your_target_file.csv"
   file = (filename, open(filename, "rb").read())

   new_target_slug = lxb.post_target(atms_slug, metadata, file)
   # >  new_target_slug = "your_target_file051394-16733444059802482"

Post a feedback
^^^^^^^^^^^^^^^
*DOCUMENTATION IN PROGRESS*

.. code:: python

   from letxbe.type import Feedback
   from letxbe.type.enum import FeedbackVote

   atms_slug = "automatisme-slug"
   doc_slug = "document-slug"
   feedback = Feedback.parse_obj(
      {
         "identifier": "optional-identifier",
         "comment": "feedback to add",
         "result": {
            "label-key": {
               "value": "predicted-value-for-label-key",
               "vote": FeedbackVote.INVALID
            }
         }
      }
   )

   feedback_response = lxb.post_feedback(atms_slug, doc_slug, feedback)

Get a document
^^^^^^^^^^^^^^

Depending on the ``doc_slug``, the output of ``get_document`` will be either a
``Target`` or an ``Artefact``.

.. code:: python

   atms_slug = "automatisme-slug"
   doc_slug = "document-slug"

   document = lxb.get_document(atms_slug, doc_slug)

Recommendations
---------------

Execution time
^^^^^^^^^^^^^^

Documents sent via ``post_target`` and ``post_artefact`` are executed one by one.
The average time of execution per document can vary from a few seconds to one minute,
depending on the number of pages and the resources allocated to the project.

Filenames with extension
^^^^^^^^^^^^^^^^^^^^^^^^

Whenever you post a document, remember to include the extension in the
``filename``, e.g.,

   * not valid filename: ``my_awesome_pdf``; 
   * valid filename: ``my_awesome_pdf.pdf``.

A filename without extension would not be parsed unless explicitly
declared in the automatisme configuration.

Large batch of files
^^^^^^^^^^^^^^^^^^^^

LetXbe does not support processing a batch of files, i.e., it is not
possible to send a list of files.

As of today, the best practice to parse a large amount of files, is to
send them one by one. We recommend sending a file *after the previous
one has been received*.
