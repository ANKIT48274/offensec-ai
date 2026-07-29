"""Sandbox policy engine — defines and enforces plugin runtime restrictions."""

from __future__ import annotations

from enum import Enum


class NetworkAccess(Enum):
    NONE = "none"
    INTERNAL_ONLY = "internal_only"
    FULL = "full"


class FilesystemAccess(Enum):
    READ_ONLY = "read_only"
    ISOLATED = "isolated"
    NONE = "none"


class SandboxPolicy:
    def __init__(
        self,
        network: NetworkAccess = NetworkAccess.NONE,
        filesystem: FilesystemAccess = FilesystemAccess.ISOLATED,
        max_memory_mb: int = 256,
        max_timeout_s: int = 60,
        allow_subprocess: bool = False,
    ) -> None:
        self.network = network
        self.filesystem = filesystem
        self.max_memory_mb = max_memory_mb
        self.max_timeout_s = max_timeout_s
        self.allow_subprocess = allow_subprocess
