from __future__ import annotations

from cryptography.fernet import Fernet

from radius_totp.auth import AuthResult
from radius_totp.config import RadiusClient, Settings
from radius_totp.radius_server import RadiusTotpServer


class FakeAuthService:
    def authenticate_initial_with_policy(self, *args, **kwargs):
        return AuthResult(ok=False, reason="otp_required")

    def reject(self, username: str, reason: str, radius_client: str | None = None) -> AuthResult:
        return AuthResult(ok=False, reason=reason)


class FakePacket:
    source = ("10.10.10.5", 10000)


def make_settings(flow: str) -> Settings:
    return Settings(
        database_dsn="postgresql://example",
        fernet_key=Fernet.generate_key().decode("utf-8"),
        auth_backend="local",
        local_users=(("demo.user", "DemoPassword123"),),
        ad_server="",
        ad_port=636,
        ad_use_ssl=True,
        ad_start_tls=False,
        ad_tls_validate=True,
        ad_connect_timeout=5,
        ad_receive_timeout=10,
        ad_login_format="upn",
        ad_domain="",
        ad_base_dn="",
        ad_user_upn_suffix="",
        ad_bind_dn=None,
        ad_bind_password=None,
        radius_listen_host="127.0.0.1",
        radius_auth_port=18120,
        radius_dictionary="radius/dictionary",
        radius_clients_file=None,
        radius_clients=(RadiusClient("10.10.10.5", "secret", "vpn1", flow, "test"),),
        otp_issuer="Demo VPN",
        otp_valid_window=1,
        enable_password_otp=True,
        enable_access_challenge=True,
    )


def test_radius_server_uses_password_otp_flow() -> None:
    server = RadiusTotpServer(make_settings("password_plus_otp"), FakeAuthService())

    assert server._client_allows_password_otp(FakePacket()) is True
    assert server._client_allows_access_challenge(FakePacket()) is False


def test_radius_server_uses_access_challenge_flow() -> None:
    server = RadiusTotpServer(make_settings("access_challenge"), FakeAuthService())

    assert server._client_allows_password_otp(FakePacket()) is False
    assert server._client_allows_access_challenge(FakePacket()) is True


def test_radius_server_rejects_invalid_challenge_state() -> None:
    server = RadiusTotpServer(make_settings("access_challenge"), FakeAuthService())

    result = server._handle_challenge_response("demo.user", "123456", "missing-state", "vpn1")

    assert result.ok is False
    assert result.reason == "invalid_challenge_state"
