# letxbe
[![pydantic](https://img.shields.io/badge/dependencies-pydantic-brightgreen)](https://pydantic-docs.helpmanual.io/)
[![requests](https://img.shields.io/badge/dependencies-requests-brightgreen)](https://pypi.org/project/requests)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`letxbe` package is a python wrapper to connect to [LetXbe API](http://letxbe.ai/).


## Install

To install the package run `pip install git+https://github.com/letxbe/letxbe.git`.

### Developers

Developers should clone the repository via `git clone` and then install the developer
requirements via `pip install -r requirements-dev.txt`.

# Basic usage

The main object used in this package is the class `LXB` that must be initialized to
establish the connection with our servers.

Every object used by `LXB` is type-validated via
[pydantic](https://pydantic-docs.helpmanual.io/).

### Recommendations

#### Filenames with extension
Whenever you post a document, remember to include the extension in the `filename`, e.g.,
* not valid filename: `my_awesome_pdf`;
* valid filename: `my_awesome_pdf.pdf`.

A filename without extension would not be parsed unless explicitly declared in the
automatisme configuration.

#### Large batch of files
LetXbe does not support processing a batch of files, i.e., it is not possible to send
a list of files.

As of today, the best practice to parse a large amount of files, is to send them one
by one. We recommend sending a file *after the previous one has been received*.

## Connection
You need the `client_id` and `client_secret` provided by Auth0 to initialise `LXB`:
```python
from letxbe import LXB

CLIENT_ID = "ClientID"
CLIENT_SECRET = "ClientSecret"

lxb = LXB(CLIENT_ID, CLIENT_SECRET)
```
You can access the Authorization header generated by the connection via the 
property `LXB.authorization_header`.

## Common actions

### Post an artefact
```python
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
```

### Post a target connected to an artefact
```python
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
```

### Post a feedback
```python
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
```

### Get a document
```python
atms_slug = "automatisme-slug"
doc_slug = "document-slug"

document = lxb.get_document(atms_slug, doc_slug)
```


# Issues

## Known issues

#### Queue not respecting order
The documents are not parsed following the order of upload.

#### Output typing
The response of `get_document` is either a `Target` or an `Artefact` instance.
In both cases, the enum-values are reproduced as python enums and not as strings, e.g.,
`'status_code': <DocumentStatus.SUCCESS: '200'>` instead of `'status_code': '200'`.

#### Overwriting the filename via metadata
It is possible to overwrite the filename of a file by specifying the variable `name` in
the metadata sent together with the file. Whenever this is the case, the original
file name is lost and cannot be recovered.

#### No explicit and no documented errors
We are working to make every error explicit and documented. For the moment, there are
chances that you encounter not-documented and/or not-explicit errors.

#### Too large files
We do not support
* files larger than 150MB
* PDFs with more than 120 pages

* We are working to support larger files.


## Report an issue

Use github default issue tracker or contact us via email at 
[team@letxbe.ai](mailto:team@letxbe.ai).

# TODO
* add sphinx documentation website

# License

MIT License, see `LICENSE` for more information.

# Changelog

## Alpha

### Alpha

* added LXB class to connect to LetXbe API and basic README documentation
* simple api calls: get_document, post_target, post_artefact, post_feedback
* basic typing for input/output
