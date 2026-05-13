# Архитектура

## Основной Поток

```text
VPN Gateway / Firewall
    ↓ RADIUS Access-Request
RADIUS TOTP Service
    ↓
Microsoft AD / LDAPS password bind
    ↓
TOTP validation
    ↓
RADIUS Access-Accept / Access-Reject
```

Сервис не интегрируется отдельно с каждым VPN-клиентом. Интеграция выполняется через VPN-шлюз или firewall, который умеет отправлять RADIUS authentication requests.

## Режимы Передачи TOTP

### password+OTP

Пользователь вводит пароль и TOTP одной строкой:

```text
UserPassword123456
```

Последние 6 цифр трактуются как TOTP-код. Этот режим является обязательным fallback для максимальной совместимости.

### Access-Challenge

Сервис сначала проверяет пароль через AD/LDAPS, затем возвращает RADIUS `Access-Challenge`. Если VPN-шлюз и клиент поддерживают интерактивный второй шаг, пользователь видит отдельный запрос OTP.

Совместимость `Access-Challenge` подтверждается отдельно для каждого gateway/client.

Тестовый CLI поддерживает отдельную проверку challenge-flow:

```powershell
radius-totp test-radius --server RADIUS_IP --secret SHARED_SECRET --username USER --password PASSWORD --otp 123456 --challenge
```

## AD/LDAPS

Production-режим использует `AUTH_BACKEND=ad`. LDAPS включён по умолчанию, ошибки AD обрабатываются fail closed: при невозможности проверить пароль сервис возвращает `Access-Reject`.

Поддерживаемые форматы bind-логина:

- `upn`: `username@example.local`;
- `domain`: `DOMAIN\username`;
- `raw`: переданный username без изменения;
- `auto`: UPN при наличии suffix, иначе domain-login.

## TOTP

TOTP проверяется по RFC 6238:

- 6 digits;
- SHA1;
- period 30 seconds;
- configurable valid window;
- replay protection через `last_used_timestep`.

## Future Method: Telegram Push

Telegram push не входит в V1. Для него потребуется отдельный механизм auth sessions, Telegram enrollment, callback handling и timeout policy, потому что RADIUS-клиенты ограничивают время ожидания ответа.
