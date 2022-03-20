import sys
from types import TracebackType
from typing import AnyStr, Optional, IO, Type


class OutputRedirect(IO):
    origin_host = None
    origin_attr = None
    origin_obj = None
    f = None

    def __init__(self, origin_host, origin_attr, fileName: str, encoding='utf-8') -> None:
        super().__init__()
        self.origin_host = origin_host
        self.origin_attr = origin_attr
        self.f = open(fileName, 'w+', encoding=encoding)
        self.origin_obj = getattr(origin_host, origin_attr)
        setattr(self.origin_host, self.origin_attr, self)

    def write(self, s: AnyStr) -> int:
        self.origin_obj.write(s)
        self.f.write(s)
        self.f.flush()
        return 0

    def __getattribute__(self, name):
        if name in OutputRedirect.__dict__.keys():
            return super().__getattribute__(name)
        return self.origin_obj.__getattribute__(name)

    def __enter__(self) -> IO[AnyStr]:
        return self

    def __exit__(self, t: Optional[Type[BaseException]], value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> Optional[bool]:
        setattr(self.origin_host, self.origin_attr, self.origin_obj)
        return self.f.close()


class StdoutRedirect(OutputRedirect):
    def __init__(self, fileName: str, encoding='utf-8') -> None:
        super().__init__(sys, 'stdout', fileName, encoding)


class StderrRedirect(OutputRedirect):
    def __init__(self, fileName: str, encoding='utf-8') -> None:
        super().__init__(sys, 'stderr', fileName, encoding)
