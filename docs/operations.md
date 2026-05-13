# Эксплуатация

## Запуск

```bash
docker compose -f docker-compose.vps.yml up -d
docker compose -f docker-compose.vps.yml logs -f radius-totp
```

## Проверка БД

```bash
docker compose -f docker-compose.vps.yml exec postgres psql -U radius_totp -d radius_totp -c "\dt"
```

## Audit Log

```bash
docker compose -f docker-compose.vps.yml exec postgres psql -U radius_totp -d radius_totp -c "SELECT created_at, username, result, reason, radius_client FROM auth_logs ORDER BY created_at DESC LIMIT 20;"
```

Типовые причины:

- `ok`;
- `enroll_ok`;
- `ad_auth_failed`;
- `invalid_totp`;
- `invalid_format`;
- `reused_totp`;
- `otp_required`;
- `invalid_challenge_state`.

## Troubleshooting

`Access-Reject` без записи в `auth_logs` обычно означает проблему до бизнес-логики: shared secret, RADIUS dictionary, неверный client IP или формат пакета.

`ad_auth_failed` означает, что пароль не подтверждён AD/LDAPS или AD недоступен. Сервис в таких случаях работает fail closed.

`invalid_totp` означает неверный код или неправильную привязку authenticator.

`invalid_format` означает, что OTP не соответствует ожидаемому формату из 6 цифр.

`reused_totp` означает повтор уже принятого timestep.

В режиме `password+OTP` код короче 6 цифр может попасть в проверку пароля как часть полной строки. В этом случае audit reason может быть `ad_auth_failed`.
