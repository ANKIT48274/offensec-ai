"""Domain value objects for OffenSec AI."""

from __future__ import annotations

import ipaddress
import re
from dataclasses import dataclass
from enum import Enum
from typing import Any


class Severity(Enum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

    @property
    def score(self) -> int:
        mapping = {
            Severity.NONE: 0,
            Severity.LOW: 1,
            Severity.MEDIUM: 2,
            Severity.HIGH: 3,
            Severity.CRITICAL: 4,
        }
        return mapping[self]

    @classmethod
    def from_cvss(cls, score: float) -> Severity:
        if score <= 0.0:
            return cls.NONE
        if score < 4.0:
            return cls.LOW
        if score < 7.0:
            return cls.MEDIUM
        if score < 9.0:
            return cls.HIGH
        return cls.CRITICAL


class Confidence(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CONFIRMED = "confirmed"

    @property
    def score(self) -> float:
        mapping = {
            Confidence.LOW: 0.25,
            Confidence.MEDIUM: 0.50,
            Confidence.HIGH: 0.75,
            Confidence.CONFIRMED: 1.0,
        }
        return mapping[self]


class FindingStatus(Enum):
    OPEN = "open"
    IN_REVIEW = "in_review"
    CONFIRMED = "confirmed"
    FALSE_POSITIVE = "false_positive"
    ACCEPTED_RISK = "accepted_risk"
    REMEDIATED = "remediated"


class AssessmentStatus(Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ARCHIVED = "archived"


class TargetType(Enum):
    IPV4 = "ipv4"
    IPV6 = "ipv6"
    HOSTNAME = "hostname"
    CIDR = "cidr"
    URL = "url"
    DOMAIN = "domain"
    RANGE = "range"


class TestTechnique(Enum):
    BLACK_BOX = "black_box"
    GREY_BOX = "grey_box"
    WHITE_BOX = "white_box"


@dataclass(frozen=True)
class IPAddress:
    value: str

    def __post_init__(self) -> None:
        try:
            ipaddress.ip_address(self.value)
        except ValueError as e:
            from backend.domain.exceptions import ValidationError

            raise ValidationError("IPAddress", str(e)) from e

    @property
    def version(self) -> int:
        return ipaddress.ip_address(self.value).version

    @property
    def is_private(self) -> bool:
        return ipaddress.ip_address(self.value).is_private


@dataclass(frozen=True)
class CIDR:
    value: str

    def __post_init__(self) -> None:
        try:
            ipaddress.ip_network(self.value, strict=False)
        except ValueError as e:
            from backend.domain.exceptions import ValidationError

            raise ValidationError("CIDR", str(e)) from e

    def contains(self, address: IPAddress) -> bool:
        return ipaddress.ip_address(address.value) in ipaddress.ip_network(self.value, strict=False)


@dataclass(frozen=True)
class Port:
    number: int
    protocol: str = "tcp"

    def __post_init__(self) -> None:
        from backend.domain.exceptions import ValidationError

        if not 1 <= self.number <= 65535:
            raise ValidationError(
                "Port", f"Port number must be between 1 and 65535, got {self.number}"
            )
        if self.protocol not in ("tcp", "udp"):
            raise ValidationError("Port", f"Protocol must be 'tcp' or 'udp', got '{self.protocol}'")


@dataclass(frozen=True)
class Hostname:
    value: str
    HOSTNAME_RE = re.compile(
        r"^(?:(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)\.)*(?:[a-zA-Z]{2,63})$"
    )

    def __post_init__(self) -> None:
        from backend.domain.exceptions import ValidationError

        if not self.HOSTNAME_RE.match(self.value):
            raise ValidationError("Hostname", f"'{self.value}' is not a valid hostname")


@dataclass(frozen=True)
class URL:
    value: str
    URL_RE = re.compile(r"^https?://[^\s/$.?#].[^\s]*$", re.IGNORECASE)

    def __post_init__(self) -> None:
        from backend.domain.exceptions import ValidationError

        if not self.URL_RE.match(self.value):
            raise ValidationError("URL", f"'{self.value}' is not a valid URL")

    @property
    def hostname(self) -> str:
        from urllib.parse import urlparse

        return urlparse(self.value).hostname or ""

    @property
    def path(self) -> str:
        from urllib.parse import urlparse

        return urlparse(self.value).path


@dataclass(frozen=True)
class Service:
    name: str
    port: Port
    version: str | None = None
    banner: str | None = None
    state: str = "open"

    def __post_init__(self) -> None:
        from backend.domain.exceptions import ValidationError

        if not self.name:
            raise ValidationError("Service", "Service name cannot be empty")
        if self.state not in ("open", "filtered", "closed"):
            raise ValidationError("Service", f"Invalid service state: '{self.state}'")


@dataclass(frozen=True)
class Credential:
    username: str | None = None
    password: str | None = None
    hash: str | None = None
    domain: str | None = None
    service: str | None = None

    def __post_init__(self) -> None:
        if not any([self.username, self.password, self.hash]):
            from backend.domain.exceptions import ValidationError

            raise ValidationError(
                "Credential", "At least one of username, password, or hash must be provided"
            )


@dataclass(frozen=True)
class FindingReference:
    source: str = ""
    id: str = ""
    url: str | None = None
    description: str | None = None


@dataclass(frozen=True)
class AttackPath:
    source_target: str = ""
    destination_target: str = ""
    technique: str = ""
    technique_id: str | None = None
    description: str | None = None
    prerequisites: list[str] | None = None
    tools: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_target": self.source_target,
            "destination_target": self.destination_target,
            "technique": self.technique,
            "technique_id": self.technique_id,
            "description": self.description,
            "prerequisites": self.prerequisites or [],
            "tools": self.tools or [],
        }


@dataclass
class ScopeDefinition:
    targets: list[str] | None = None
    excluded_targets: list[str] | None = None
    techniques: list[str] | None = None
    allowed_tools: list[str] | None = None
    rate_limit: int | None = None
    max_depth: int | None = None
    intrusive_testing: bool = False

    def includes(self, target: str) -> bool:
        if self.excluded_targets and target in self.excluded_targets:
            return False
        return bool(self.targets and target in self.targets)
