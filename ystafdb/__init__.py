__all__ = (
    "generate_foaf_uris",
    "generate_ystafdb_metadata_uris"
)
VERSION = (0, 4)
__version__ = ".".join(str(v) for v in VERSION)

data_dir = "data"

from .ystafdb_metadata import generate_ystafdb_metadata_uris
from .foaf import generate_foaf_uris


def generate_ystafdb(base_dir):
    generate_foaf_uris(base_dir)
    generate_ystafdb_metadata_uris(base_dir)
