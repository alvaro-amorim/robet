import pytest

from app.core.config import Settings
from app.core.security_flags import ForbiddenCapability, SecurityFlagError, assert_capability_allowed


def test_forbidden_flags_block_real_money():
    with pytest.raises(SecurityFlagError):
        assert_capability_allowed(ForbiddenCapability.REAL_MONEY, Settings(enable_real_money_mode=False))


def test_forbidden_flags_block_auto_betting():
    with pytest.raises(SecurityFlagError):
        assert_capability_allowed(ForbiddenCapability.AUTO_BETTING, Settings(enable_auto_betting=False))
