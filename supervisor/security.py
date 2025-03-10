"""Fetch last versions from webserver."""
import logging
from pathlib import Path
from typing import Awaitable, Optional

from .const import (
    ATTR_CONTENT_TRUST,
    ATTR_FORCE_SECURITY,
    ATTR_PWNED,
    FILE_HASSIO_SECURITY,
)
from .coresys import CoreSys, CoreSysAttributes
from .exceptions import PwnedError
from .utils.common import FileConfiguration
from .utils.pwned import check_pwned_password
from .validate import SCHEMA_SECURITY_CONFIG

_LOGGER: logging.Logger = logging.getLogger(__name__)


class Security(FileConfiguration, CoreSysAttributes):
    """Handle Security properties."""

    def __init__(self, coresys: CoreSys):
        """Initialize updater."""
        super().__init__(FILE_HASSIO_SECURITY, SCHEMA_SECURITY_CONFIG)
        self.coresys = coresys

    @property
    def content_trust(self) -> bool:
        """Return if content trust is enabled/disabled."""
        return self._data[ATTR_CONTENT_TRUST]

    @content_trust.setter
    def content_trust(self, value: bool) -> None:
        """Set content trust is enabled/disabled."""
        self._data[ATTR_CONTENT_TRUST] = value

    @property
    def force(self) -> bool:
        """Return if force security is enabled/disabled."""
        return self._data[ATTR_FORCE_SECURITY]

    @force.setter
    def force(self, value: bool) -> None:
        """Set force security is enabled/disabled."""
        self._data[ATTR_FORCE_SECURITY] = value

    @property
    def pwned(self) -> bool:
        """Return if pwned is enabled/disabled."""
        return self._data[ATTR_PWNED]

    @pwned.setter
    def pwned(self, value: bool) -> None:
        """Set pwned is enabled/disabled."""
        self._data[ATTR_PWNED] = value

    async def verify_own_content(
        self, checksum: Optional[str] = None, path: Optional[Path] = None
    ) -> Awaitable[None]:
        """Verify content from HA org."""
        _LOGGER.warning("Disabled content-trust, skip validation")
        return

        # TODO(abrownglez): Enable CodeNotary checksum validation.
        # try:
        #     await vcn_validate(checksum, path, org="home-assistant.io")
        # except CodeNotaryUntrusted:
        #     self.sys_resolution.unhealthy = UnhealthyReason.UNTRUSTED
        #     raise
        # except CodeNotaryError:
        #     if self.force:
        #         raise
        #     return

    async def verify_secret(self, pwned_hash: str) -> None:
        """Verify pwned state of a secret."""
        if not self.pwned:
            _LOGGER.warning("Disabled pwned, skip validation")
            return

        try:
            await check_pwned_password(self.sys_websession, pwned_hash)
        except PwnedError:
            if self.force:
                raise
            return
