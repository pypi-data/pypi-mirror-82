"""Defines any IO utilities used by isort"""
import re
import tokenize
from contextlib import contextmanager
from io import BytesIO, StringIO, TextIOWrapper
from pathlib import Path
from typing import Callable, Iterator, NamedTuple, TextIO, Union

from isort.exceptions import UnsupportedEncoding

_ENCODING_PATTERN = re.compile(br"^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)")


class File(NamedTuple):
    stream: TextIO
    path: Path
    encoding: str

    @staticmethod
    def detect_encoding(filename: str, readline: Callable[[], bytes]):
        try:
            return tokenize.detect_encoding(readline)[0]
        except Exception:
            raise UnsupportedEncoding(filename)

    @staticmethod
    def from_contents(contents: str, filename: str) -> "File":
        encoding = File.detect_encoding(filename, BytesIO(contents.encode("utf-8")).readline)
        return File(StringIO(contents), path=Path(filename).resolve(), encoding=encoding)

    @property
    def extension(self):
        return self.path.suffix.lstrip(".")

    @staticmethod
    def _open(filename):
        """Open a file in read only mode using the encoding detected by
        detect_encoding().
        """
        buffer = open(filename, "rb")
        try:
            encoding = File.detect_encoding(filename, buffer.readline)
            buffer.seek(0)
            text = TextIOWrapper(buffer, encoding, line_buffering=True, newline="")
            text.mode = "r"  # type: ignore
            return text
        except Exception:
            buffer.close()
            raise

    @staticmethod
    @contextmanager
    def read(filename: Union[str, Path]) -> Iterator["File"]:
        file_path = Path(filename).resolve()
        stream = None
        try:
            stream = File._open(file_path)
            yield File(stream=stream, path=file_path, encoding=stream.encoding)
        finally:
            if stream is not None:
                stream.close()


class _EmptyIO(StringIO):
    def write(self, *args, **kwargs):
        pass


Empty = _EmptyIO()
