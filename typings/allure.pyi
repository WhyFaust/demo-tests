from typing import Any, Callable, TypeVar

_T = TypeVar("_T")

def feature(name: str) -> Callable[[_T], _T]: ...
def step(name: str) -> Callable[[_T], _T]: ...
def attach(
    body: Any,
    name: str | None = None,
    attachment_type: Any | None = None,
    extension: str | None = None,
) -> None: ...

class AttachmentType:
    PNG: Any
    TEXT: Any
    HTML: Any
