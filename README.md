# RADIUS 2FA Pilot

Production-pilot версия сервиса двухфакторной аутентификации для VPN и удалённого доступа через RADIUS.

Основной сценарий:

```text
VPN Gateway / Firewall
    ↓ RADIUS
RADIUS TOTP Service
    ↓
Microsoft AD / LDAPS
    ↓
TOTP Verification
    ↓
Access-Accept / Access-Reject
```

## Возможности V1

- Проверка пароля через Microsoft AD/LDAPS.
- Проверка TOTP-кодов по RFC 6238.
- Совместимость с Google Authenticator и Яндекс Ключом.
- Режим `password+OTP` для максимальной совместимости.
- Режим `Access-Challenge` для шлюзов, которые поддерживают интерактивный второй шаг.
- YAML-конфигурация RADIUS-клиентов с per-client flow.
- Зашифрованное хранение TOTP-секретов.
- Защита от повторного использования TOTP timestep.
- PostgreSQL audit log.

## Целевые VPN И Системы Доступа

Решение работает на уровне стандартного RADIUS-протокола. Поддержка конкретного VPN-клиента подтверждается интеграционным тестом на соответствующем VPN-шлюзе.

Целевые системы:

- Cisco VPN;
- Check Point VPN;
- Fortigate VPN;
- Huawei VPN;
- OpenVPN Access Server;
- pfSense OpenVPN;
- UserGate VPN;
- С-Терра VPN;
- MikroTik L2TP VPN.

## Документация

- [Архитектура](docs/architecture.md)
- [Конфигурация](docs/configuration.md)
- [Развёртывание](docs/deployment.md)
- [Enrollment пользователей](docs/enrollment.md)
- [Эксплуатация](docs/operations.md)
- [Совместимость VPN](docs/compatibility.md)
- [Демонстрационный протокол](docs/demo-protocol.md)

## Статус

Фактически проверено на VPS `185.216.71.170`:

- `password+OTP`: успешный вход, повтор OTP, неверный OTP;
- `Access-Challenge`: challenge, успешный второй шаг, повтор OTP, неверный формат OTP;
- PostgreSQL audit log;
- YAML-конфигурация RADIUS-клиентов;
- Docker Compose deployment.

AD/LDAPS-интеграция реализована как production-backend, но требует проверки в инфраструктуре заказчика с реальным доменом и сертификатами LDAPS.

Telegram push не входит в V1 и рассматривается как следующий метод 2FA.
