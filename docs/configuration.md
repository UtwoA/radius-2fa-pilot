# Конфигурация

## `.env`

Основные параметры:

```env
DATABASE_DSN=postgresql://radius_totp:change-me@localhost:5432/radius_totp
FERNET_KEY=replace-with-generated-fernet-key

AUTH_BACKEND=ad

AD_SERVER=ad.example.local
AD_PORT=636
AD_USE_SSL=true
AD_START_TLS=false
AD_TLS_VALIDATE=true
AD_CONNECT_TIMEOUT=5
AD_RECEIVE_TIMEOUT=10
AD_LOGIN_FORMAT=upn
AD_DOMAIN=
AD_BASE_DN=DC=example,DC=local
AD_USER_UPN_SUFFIX=example.local

RADIUS_LISTEN_HOST=0.0.0.0
RADIUS_AUTH_PORT=1812
RADIUS_DICTIONARY=radius/dictionary
RADIUS_CLIENTS_FILE=config/radius_clients.yml

OTP_ISSUER=Corporate VPN
OTP_VALID_WINDOW=1
ENABLE_PASSWORD_OTP=true
ENABLE_ACCESS_CHALLENGE=true
```

`FERNET_KEY` должен быть сгенерирован один раз и сохранён как secret. Потеря ключа означает невозможность расшифровать существующие TOTP-секреты.

## YAML RADIUS Clients

Пример `config/radius_clients.yml`:

```yaml
clients:
  - name: fortigate-main
    host: 10.10.10.5
    secret_env: RADIUS_SECRET_FORTIGATE
    preferred_flow: password_plus_otp
    description: Fortigate VPN gateway
```

`secret_env` указывает имя env-переменной, где лежит shared secret. Значение секрета не хранится в YAML.

Допустимые `preferred_flow`:

- `password_plus_otp`;
- `access_challenge`;
- `both`.

Если `RADIUS_CLIENTS_FILE` не задан, используется legacy-переменная:

```env
RADIUS_CLIENTS=127.0.0.1:testing123:local
```

В репозитории есть минимальный `config/radius_clients.yml` для локального теста. Для production замените список клиентов на реальные IP VPN-шлюзов и задайте отдельный `secret_env` для каждого gateway.
