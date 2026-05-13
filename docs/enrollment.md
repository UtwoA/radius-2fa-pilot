# Enrollment Пользователей

## Регистрация

```bash
radius-totp enroll username --qr-path username.png
```

Команда:

- генерирует TOTP secret;
- формирует OTP URI;
- создаёт QR-код;
- просит тестовый OTP;
- включает 2FA только после успешного подтверждения.

## Повторный QR

```bash
radius-totp show-qr username --qr-path username.png
```

Используется, если нужно повторно показать QR для уже сохранённого secret.

## Сброс

```bash
radius-totp reset username
```

Сбрасывает secret, выключает 2FA и очищает `last_used_timestep`.

## Включение И Отключение

```bash
radius-totp enable username
radius-totp disable username
```

Отключённый пользователь проходит только по успешной проверке пароля. Это позволяет включать 2FA поэтапно.
