# Vendor Integration Research

Цель документа — зафиксировать гипотезы совместимости с VPN-шлюзами и системами удалённого доступа до проведения реальных интеграционных тестов.

Ориентир по списку целевых интеграций: раздел «Межсетевые экраны» в документации Multifactor: https://multifactor.ru/docs/getttingstarted/

## Принцип Совместимости

Сервис интегрируется не с пользовательским VPN-клиентом напрямую, а с VPN-шлюзом или firewall через RADIUS.

Базовая гипотеза:

```text
Если продукт умеет отправлять authentication requests на внешний RADIUS-сервер,
то режим password+OTP должен быть проверяемым первым.
```

`Access-Challenge` проверяется отдельно, потому что поддержка интерактивного второго шага зависит от реализации VPN-шлюза и клиента.

## Режимы Проверки

### password+OTP

Пользователь вводит пароль и OTP одной строкой:

```text
UserPassword123456
```

Это основной fallback-режим для максимальной совместимости.

### Access-Challenge

Пользователь сначала вводит пароль. После успешной проверки пароля RADIUS-сервис возвращает `Access-Challenge`, а клиент должен запросить OTP отдельным шагом.

Успешный сценарий:

```text
Access-Request(password)
→ Access-Challenge
→ Access-Request(otp + State)
→ Access-Accept
```

## Гипотезы По Продуктам

| Продукт | Интеграция | Основной тест | Access-Challenge | Приоритет |
|---|---|---|---|---|
| MikroTik L2TP VPN | RADIUS для PPP/L2TP | password+OTP | под вопросом | 1 |
| pfSense OpenVPN | RADIUS auth backend | password+OTP | под вопросом | 2 |
| OpenVPN Access Server | External/RADIUS auth | password+OTP | требует проверки | 3 |
| Fortigate VPN | RADIUS server auth | password+OTP | требует проверки | 4 |
| UserGate VPN | RADIUS auth | password+OTP | требует проверки | 4 |
| Cisco VPN | RADIUS/AAA | password+OTP | требует проверки | 5 |
| Check Point VPN | RADIUS auth | password+OTP | требует проверки | 5 |
| Huawei VPN | RADIUS auth | password+OTP | требует проверки | 5 |
| С-Терра VPN | RADIUS auth | password+OTP | требует проверки | 5 |

## Что Фиксировать При Тесте

Для каждого продукта нужно фиксировать:

- продукт и версию;
- тип VPN;
- IP gateway, с которого идут RADIUS-запросы;
- RADIUS shared secret;
- username format;
- работает ли `password+OTP`;
- работает ли `Access-Challenge`;
- timeout/retry настройки;
- какие RADIUS атрибуты нужны;
- audit log на стороне сервиса;
- ограничения и особенности UI клиента.

## Acceptance Для Интеграции

Интеграция считается подтверждённой для конкретного продукта, если проверены:

- успешный вход с корректным паролем и OTP;
- отказ при неверном OTP;
- отказ при повторном использовании OTP;
- запись событий в audit log;
- стабильная работа при повторных подключениях;
- понятная инструкция настройки gateway.

`Access-Challenge` считается подтверждённым отдельно и не является обязательным условием совместимости, если `password+OTP` работает.

## Первый Рекомендуемый Тест

Первым кандидатом рекомендуется MikroTik CHR или pfSense OpenVPN:

- их проще поднять в лаборатории;
- они позволяют быстро проверить реальный RADIUS gateway-flow;
- результат можно перенести в compatibility matrix как первую подтверждённую интеграцию.
