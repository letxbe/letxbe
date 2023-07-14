import os
import uuid

from letxbe.type import ClientEnv, Metadata, Target

ATMS_SLUG = "demo-courrier"

# Files
CURRENT_DIR_PATH = os.path.dirname(os.path.realpath(__file__))
TEST_FILES_PATH = os.path.join(CURRENT_DIR_PATH, "file")
FILE_NAME = "CGS20221101.pdf"

# Atms configuration
CLIENT_ENV = ClientEnv.TEST

# Example data
with open(os.path.join(TEST_FILES_PATH, FILE_NAME), "rb") as file:
    tgt_file = (FILE_NAME, file.read())


def test_main(lxb):
    if not lxb:
        return

    slug = str(uuid.uuid4())

    tgt_metadata = Metadata(
        client_env=CLIENT_ENV,
        form={},
    )
    new_tgt_slug = lxb.post_target(ATMS_SLUG, tgt_metadata, tgt_file, slug)

    assert isinstance(new_tgt_slug, str)
    assert new_tgt_slug == slug

    document = lxb.get_document(ATMS_SLUG, new_tgt_slug)

    assert isinstance(document, Target)
