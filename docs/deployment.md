# Развёртывание

## Docker Compose

V1 рассчитан на запуск как отдельный сервис рядом с PostgreSQL:

```bash
docker compose -f docker-compose.vps.yml up -d --build
docker compose -f docker-compose.vps.yml ps
```

PostgreSQL применяет начальную SQL-схему из `sql/001_schema.sql` при первом создании volume.

Перед production-запуском заполните `.env` и `config/radius_clients.yml`. Shared secrets указываются через env-переменные, а не напрямую в YAML.

Папка `config/` монтируется в контейнер как read-only, поэтому изменение списка RADIUS-клиентов требует перезапуска сервиса, но не требует пересборки образа:

```bash
docker compose -f docker-compose.vps.yml restart radius-totp
```

## Firewall

RADIUS использует UDP `1812`. В production порт должен быть открыт только для доверенных VPN-шлюзов/firewall.

Принцип:

```text
allow UDP 1812 from VPN_GATEWAY_IP
deny UDP 1812 from all others
```

Не открывайте UDP `1812` в интернет без ограничения источников.

## Secrets

Минимальные secrets:

- `FERNET_KEY`;
- PostgreSQL password;
- RADIUS shared secrets;
- AD bind credentials, если используется service account.

Секреты не должны попадать в git. В репозитории хранятся только `.env.example` и `config/radius_clients.yml.example`.
