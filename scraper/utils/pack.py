import re
from io import BytesIO
from zipfile import ZipFile


def pack_files_into_archive(files: list) -> bytes:
    """
    Pack files into archive file. Returns byte content of archive.

    :param files: list of (filename, file_data)
    :return: archive file's bytes
    """

    byte_stream = BytesIO()

    with ZipFile(byte_stream, 'w') as z:
        for filename, file_data in files:
            z.writestr(fix_filename(filename), file_data)

    return byte_stream.getvalue()


def fix_filename(filename: str) -> str:
    """
    Remove special characters from filename.

    :param filename: filename
    :return: fixed filename
    """

    filename = re.sub(r'[/]', '_', filename)

    return re.sub(r'[^\d\w.-]', '', filename)
