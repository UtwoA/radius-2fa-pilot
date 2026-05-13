# Демонстрационный Протокол V1

Стенд:

- VPS: `185.216.71.170`;
- путь: `/opt/radius-2fa-pilot`;
- тестовый RADIUS client: Windows host `2.26.102.134`;
- тестовый пользователь: `demo.user`;
- локальный password backend: `DemoPassword123`;
- shared secret: `testing123`.

## Старт RADIUS-Сервиса

```console
root@VPS-utwoa:/opt/radius-2fa-pilot# docker compose -f docker-compose.vps.yml ps
NAME                   IMAGE                          COMMAND                  SERVICE       STATUS                        PORTS
radius-totp-postgres   postgres:16-alpine             "docker-entrypoint.s…"   postgres      Up (healthy)                  5432/tcp
radius-totp-service    radius-2fa-pilot-radius-totp   "radius-totp serve"      radius-totp   Up                            0.0.0.0:1812->1812/udp

root@VPS-utwoa:/opt/radius-2fa-pilot# docker compose -f docker-compose.vps.yml logs --tail=30 radius-totp
radius-totp-service  | 2026-05-13 19:24:40,878 INFO radius_totp.radius_server Starting RADIUS server on 0.0.0.0:1812
```

## Enrollment

```console
root@VPS-utwoa:/opt/radius-2fa-pilot# docker compose -f docker-compose.vps.yml exec radius-totp radius-totp enroll demo.user --qr-path /tmp/demo.user.png
OTP URI: otpauth://totp/Demo%20VPN:demo.user?secret=WSGK6KSKG2COTGF7MLWIHEQEQE547JYO&issuer=Demo%20VPN
QR code written to: /tmp/demo.user.png
Enter test OTP code:
2FA enabled for demo.user
```

## password+OTP

```console
PS C:\radius-2fa-pilot> radius-totp test-radius --server 185.216.71.170 --secret testing123 --username demo.user --password DemoPassword123 --otp 257102
Access-Accept
Reply-Message: Access granted

PS C:\radius-2fa-pilot> radius-totp test-radius --server 185.216.71.170 --secret testing123 --username demo.user --password DemoPassword123 --otp 257102
Access-Reject
Reply-Message: Access denied

PS C:\radius-2fa-pilot> radius-totp test-radius --server 185.216.71.170 --secret testing123 --username demo.user --password DemoPassword123 --otp 25713
Access-Reject
Reply-Message: Access denied
```

Проверено:

- корректный OTP даёт `Access-Accept`;
- повтор уже принятого OTP даёт `Access-Reject`;
- неверный формат OTP даёт `Access-Reject`.

## Access-Challenge

Для проверки `Access-Challenge` у клиента в `config/radius_clients.yml` был включён flow:

```yaml
preferred_flow: access_challenge
```

Проверка:

```console
PS C:\radius-2fa-pilot> radius-totp test-radius --server 185.216.71.170 --secret testing123 --username demo.user --password DemoPassword123 --otp 220970 --challenge
Access-Accept
Reply-Message: Access granted

PS C:\radius-2fa-pilot> radius-totp test-radius --server 185.216.71.170 --secret testing123 --username demo.user --password DemoPassword123 --otp 220970 --challenge
Access-Reject
Reply-Message: Access denied

PS C:\radius-2fa-pilot> radius-totp test-radius --server 185.216.71.170 --secret testing123 --username demo.user --password DemoPassword123 --otp 22090 --challenge
Access-Reject
Reply-Message: Access denied
```

Проверено:

- первый RADIUS-запрос с паролем создаёт `Access-Challenge`;
- второй RADIUS-запрос с OTP завершает вход через `Access-Accept`;
- повтор OTP и неверный формат OTP отклоняются.

## Audit Log

```console
root@VPS-utwoa:/opt/radius-2fa-pilot# docker compose -f docker-compose.vps.yml exec postgres psql -U radius_totp -d radius_totp -c "SELECT created_at, username, result, reason, radius_client FROM auth_logs ORDER BY created_at DESC LIMIT 20;"
          created_at           | username  |  result   |     reason     |    radius_client
-------------------------------+-----------+-----------+----------------+---------------------
 2026-05-13 19:29:20.326386+00 | demo.user | reject    | invalid_format | windows-test-client
 2026-05-13 19:29:20.091126+00 | demo.user | challenge | otp_required   | windows-test-client
 2026-05-13 19:29:16.923996+00 | demo.user | reject    | reused_totp    | windows-test-client
 2026-05-13 19:29:16.68756+00  | demo.user | challenge | otp_required   | windows-test-client
 2026-05-13 19:29:11.927421+00 | demo.user | accept    | ok             | windows-test-client
 2026-05-13 19:29:11.580238+00 | demo.user | challenge | otp_required   | windows-test-client
 2026-05-13 19:28:13.753763+00 | demo.user | reject    | ad_auth_failed | windows-test-client
 2026-05-13 19:28:11.235287+00 | demo.user | reject    | reused_totp    | windows-test-client
 2026-05-13 19:28:06.832006+00 | demo.user | accept    | ok             | windows-test-client
 2026-05-13 19:25:03.829346+00 | demo.user | accept    | enroll_ok      |
```

Примечание: в режиме `password+OTP` OTP короче 6 цифр может фиксироваться как `ad_auth_failed`, потому что вся строка воспринимается как пароль и не проходит password check.
