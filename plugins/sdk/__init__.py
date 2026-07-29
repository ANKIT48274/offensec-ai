"""Plugin development kit for building OffenSec AI plugins."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BasePlugin(ABC):
    """Base class that all OffenSec AI plugins must extend."""

    name: str = ""
    version: str = "1.0.0"
    description: str = ""
    author: str = ""
    capabilities: list[str] = []

    @abstractmethod
    async def initialize(self) -> None: ...

    @abstractmethod
    async def execute(self, context: dict[str, Any]) -> dict[str, Any]: ...

    async def cleanup(self) -> None: ...


class ToolPlugin(BasePlugin):
    """Base class for tool integration plugins."""

    tool_name: str = ""

    async def initialize(self) -> None:
        pass

    async def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class MethodologyPlugin(BasePlugin):
    """Base class for methodology extension plugins."""

    async def initialize(self) -> None:
        pass

    async def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class ReporterPlugin(BasePlugin):
    """Base class for custom report format plugins."""

    format_name: str = ""

    async def initialize(self) -> None:
        pass

    async def execute(self, context: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
