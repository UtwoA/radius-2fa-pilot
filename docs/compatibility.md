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
| MikroTik L2TP VPN | подтверждён transport | заблокировано MS-CHAPv2 | не проверялось | требует MS-CHAPv2 support |

## Методика Проверки

1. Добавить gateway IP в `config/radius_clients.yml`.
2. Настроить shared secret через env.
3. Настроить VPN-шлюз на RADIUS server.
4. Проверить `password+OTP`.
5. Отдельно проверить `Access-Challenge`, если продукт заявляет поддержку интерактивного challenge.

Если `Access-Challenge` не поддерживается или клиент не показывает второй prompt, использовать `password+OTP`.

Для проверки серверного challenge-flow без VPN-клиента можно использовать:

```powershell
radius-totp test-radius --server RADIUS_IP --secret SHARED_SECRET --username USER --password PASSWORD --otp 123456 --challenge
```

## Результаты Проверок

### MikroTik CHR L2TP VPN

Дата проверки: 2026-05-13.

Стенд:

- MikroTik CHR в VirtualBox;
- L2TP/IPsec VPN gateway;
- Windows built-in VPN client;
- RADIUS server: `185.216.71.170:1812`;
- source IP MikroTik до VPS: `46.138.31.92`;
- RADIUS client name: `mikrotik-chr`.

Что подтверждено:

- MikroTik отправляет RADIUS `Access-Request` на сервис;
- UDP `1812` и shared secret работают на transport-уровне;
- сервис отвечает MikroTik RADIUS `Access-Reject`;
- RADIUS-пакеты видны через `tcpdump` на VPS.

Наблюдаемый блокер:

```text
Rejecting RADIUS packet: Missing password
```

Причина: Windows L2TP/IPsec + MikroTik L2TP использует MS-CHAP/MS-CHAPv2, а текущая V1-реализация ожидает PAP-style атрибут `User-Password`.

Попытка принудительно включить только PAP на MikroTik приводит к разрыву VPN-сессии до завершения подключения со стороны Windows-клиента.

Итог:

```text
MikroTik L2TP VPN transport через RADIUS подтверждён.
Полная password+OTP-аутентификация требует поддержки MS-CHAPv2
или другого режима MikroTik/VPN-клиента, который передаёт User-Password.
```

Следующая инженерная задача:

- добавить поддержку MS-CHAPv2;
- либо проверить другой MikroTik VPN/PPP режим с PAP;
- либо выбрать следующий gateway для полного success-path теста, например pfSense OpenVPN или OpenVPN Access Server.
