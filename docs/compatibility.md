# Совместимость VPN

Решение поддерживает VPN-шлюзы и системы удалённого доступа через RADIUS. Совместимость с конкретным продуктом подтверждается интеграционным тестом.

Серверная часть `password+OTP` и `Access-Challenge` проверена встроенным RADIUS test-client на VPS-стенде. Следующий этап — проверка первого реального VPN-шлюза.

| Система | RADIUS auth | password+OTP | Access-Challenge | Статус |
|---|---:|---:|---:|---|
| Cisco VPN | целевой | целевой | требует теста | TBD |
| Check Point VPN | целевой | целевой | требует теста | TBD |
| Fortigate VPN | целевой | целевой | требует теста | TBD |
| Huawei VPN | целевой | целевой | требует теста | TBD |
| OpenVPN Access Server | целевой | целевой | требует теста | TBD |
| pfSense OpenVPN | целевой | целевой | требует теста | TBD |
| UserGate VPN | целевой | целевой | требует теста | TBD |
| С-Терра VPN | целевой | целевой | требует теста | TBD |
| MikroTik L2TP VPN | целевой | целевой | требует теста | TBD |

## Методика Проверки

1. Добавить gateway IP в `config/radius_clients.yml`.
2. Настроить shared secret через env.
3. Настроить VPN-шлюз на RADIUS server.
4. Проверить `password+OTP`.
5. Отдельно проверить `Access-Challenge`, если продукт заявляет поддержку интерактивного challenge.
6. Зафиксировать результат в матрице совместимости и в отдельной инструкции для продукта.

Если `Access-Challenge` не поддерживается или клиент не показывает второй prompt, использовать `password+OTP`.

Для проверки серверного challenge-flow без VPN-клиента можно использовать:

```powershell
radius-totp test-radius --server RADIUS_IP --secret SHARED_SECRET --username USER --password PASSWORD --otp 123456 --challenge
```

Дополнительные гипотезы и порядок исследования описаны в [Vendor Integration Research](vendor-research.md).
