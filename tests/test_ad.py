from __future__ import annotations

from radius_totp.ad import ActiveDirectoryAuthenticator, ActiveDirectoryConfig


def test_ad_formats_upn_login() -> None:
    auth = ActiveDirectoryAuthenticator(
        ActiveDirectoryConfig(server="ad.local", user_upn_suffix="example.local", login_format="upn")
    )

    assert auth._format_login("ivan.petrov") == "ivan.petrov@example.local"


def test_ad_formats_domain_login() -> None:
    auth = ActiveDirectoryAuthenticator(
        ActiveDirectoryConfig(server="ad.local", domain="EXAMPLE", login_format="domain")
    )

    assert auth._format_login("ivan.petrov") == "EXAMPLE\\ivan.petrov"


def test_ad_keeps_explicit_login() -> None:
    auth = ActiveDirectoryAuthenticator(
        ActiveDirectoryConfig(server="ad.local", user_upn_suffix="example.local", login_format="upn")
    )

    assert auth._format_login("EXAMPLE\\ivan.petrov") == "EXAMPLE\\ivan.petrov"
    assert auth._format_login("ivan.petrov@example.local") == "ivan.petrov@example.local"
