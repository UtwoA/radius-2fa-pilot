from __future__ import annotations

import ssl
from dataclasses import dataclass

from ldap3 import ALL, Connection, Server, Tls


@dataclass(frozen=True)
class ActiveDirectoryConfig:
    server: str
    port: int = 636
    use_ssl: bool = True
    start_tls: bool = False
    tls_validate: bool = True
    connect_timeout: int = 5
    receive_timeout: int = 10
    login_format: str = "upn"
    domain: str = ""
    base_dn: str = ""
    user_upn_suffix: str = ""
    bind_dn: str | None = None
    bind_password: str | None = None


class ActiveDirectoryAuthenticator:
    def __init__(self, config: ActiveDirectoryConfig) -> None:
        self._config = config

    def authenticate(self, username: str, password: str) -> bool:
        user = self._format_login(username)
        conn: Connection | None = None
        server = Server(
            self._config.server,
            port=self._config.port,
            use_ssl=self._config.use_ssl,
            get_info=ALL,
            tls=Tls(validate=ssl.CERT_REQUIRED if self._config.tls_validate else ssl.CERT_NONE),
            connect_timeout=self._config.connect_timeout,
        )
        try:
            conn = Connection(
                server,
                user=user,
                password=password,
                auto_bind=False,
                receive_timeout=self._config.receive_timeout,
            )
            if self._config.start_tls:
                conn.open()
                if not conn.start_tls():
                    return False
            return bool(conn.bind())
        except Exception:
            return False
        finally:
            try:
                if conn is not None:
                    conn.unbind()
            except Exception:
                pass

    def _format_login(self, username: str) -> str:
        if "\\" in username or "@" in username:
            return username
        if self._config.login_format == "raw":
            return username
        if self._config.login_format == "domain":
            return f"{self._config.domain}\\{username}" if self._config.domain else username
        if self._config.login_format == "auto":
            if self._config.user_upn_suffix:
                return f"{username}@{self._config.user_upn_suffix}"
            return f"{self._config.domain}\\{username}" if self._config.domain else username
        return f"{username}@{self._config.user_upn_suffix}"
