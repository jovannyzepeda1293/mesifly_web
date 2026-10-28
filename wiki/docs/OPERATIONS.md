# Manual de operaciones

## Accesos y roles

| Rol | Acceso |
|---|---|
| super_admin | `/super_admin` — métricas globales y listado de clientes |
| owner | dashboard, pedidos, menú, tienda, perfil, empleados, plan |
| staff | dashboard resumido, pedidos, edición de menú (no crea usuarios ni contrata plan) |

## Seed

```bash
bin/rails db:seed
```

- Super admin: `admin@mesifly.com` / `change_me_123!` (forzar cambio en primer login)
- Demo: `demo@mesifly.com` / `Change_me_123!`

## Onboarding del dueño

1. Registro (email+password u OAuth Google).
2. Wizard: datos de negocio → subir fotos del menú (opcional, IA DeepSeek) → suscripción Stripe.
3. Redirige a `/:slug/dashboard`.

## Flujo del comensal

1. Abre `/:slug` (menú público).
2. Agrega al carrito → checkout (nombre, teléfono, dirección).
3. Confirma → `Order` con `public_token` → Telegram al restaurante + ActionCable.

## Notificaciones Telegram

- Nuevo pedido (a `telegram_chat_id` de la sucursal).
- Pago exitoso / fallido / cancelación (vía `Telegram::Notifier`).

El `telegram_chat_id` se configura en `/:slug/cuenta/tienda`, o vinculando `t.me/MesiflyBot?start=<token>`.

## Stripe

- 1 Customer por Restaurant, 1 Subscription con N SubscriptionItem (uno por sucursal).
- Trial 14 días solo en la primera alta.
- Precio $5 USD/mes por sucursal; proration `create_prorations`.
- Cancelación `cancel_at_period_end: true`.

## Gate de suscripción

Si `subscription.status` no es `trialing` ni `active`, la vista del comensal muestra "Menú no disponible". El dashboard sigue accesible para reactivar.

## Respaldos

```bash
bin/rails backup:daily
```

`pg_dump` → S3 (retención 7 días). Programar diariamente.

## Monitoreo

- Sentry (`SENTRY_DSN`) para errores.
- Health check `GET /up`.
- Logs a stdout (`RAILS_LOG_TO_STDOUT`).

## Resolución de problemas

- **429 Too Many Requests**: límites de Rack::Attack (login 5/20s, registro 10/h, checkout 20/h).
- **Menú no disponible**: suscripción no activa; revisar webhooks de Stripe.
- **Extracción IA falla**: `MenuExtraction` queda en `failed`; reintentar o cargar el menú manualmente.
