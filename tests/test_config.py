from __future__ import annotations

from radius_totp.config import load_radius_clients_file, parse_local_users, parse_radius_clients


def test_parse_radius_clients() -> None:
    clients = parse_radius_clients("10.0.0.1:secret1:cisco,10.0.0.2:secret2")

    assert clients[0].host == "10.0.0.1"
    assert clients[0].secret == "secret1"
    assert clients[0].name == "cisco"
    assert clients[0].preferred_flow == "password_plus_otp"
    assert clients[1].name == "10.0.0.2"


def test_parse_local_users() -> None:
    users = parse_local_users("demo.user:DemoPassword123, admin:AnotherPassword")

    assert users == (("demo.user", "DemoPassword123"), ("admin", "AnotherPassword"))


def test_load_radius_clients_file_reads_secret_from_env(tmp_path, monkeypatch) -> None:
    config_path = tmp_path / "radius_clients.yml"
    config_path.write_text(
        """
clients:
  - name: fortigate-main
    host: 10.10.10.5
    secret_env: RADIUS_SECRET_FORTIGATE
    preferred_flow: both
    description: Fortigate VPN
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("RADIUS_SECRET_FORTIGATE", "secret-value")

    clients = load_radius_clients_file(config_path)

    assert len(clients) == 1
    assert clients[0].name == "fortigate-main"
    assert clients[0].host == "10.10.10.5"
    assert clients[0].secret == "secret-value"
    assert clients[0].preferred_flow == "both"
    assert clients[0].description == "Fortigate VPN"
