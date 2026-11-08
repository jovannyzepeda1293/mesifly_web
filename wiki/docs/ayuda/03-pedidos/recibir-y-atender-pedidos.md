---
id: recibir-y-atender-pedidos
titulo: Cómo recibo y atiendo los pedidos
audiencia: todos
categoria: pedidos
resumen: Ver los pedidos nuevos en vivo, abrir el detalle y marcarlos como atendidos.
palabras_clave: [cancelar pedido, cancelados, filtrar por día, pedidos, nuevo pedido, atender pedido, marcar como atendido, pendientes, atendidos, detalle del pedido, alerta]
ruta_app: /:slug/orders
actualizado: 2026-11-08
relacionados: [conectar-telegram, hacer-un-pedido, dashboard]
---
# Cómo recibo y atiendo los pedidos

## Para quién es
Para el **dueño** y los **empleados**.

## Antes de empezar
- Tu menú debe estar visible (suscripción activa o en prueba) y dentro de [horario de atención](horario-de-atencion.md).
- Para recibir avisos en el teléfono, [conecta Telegram](conectar-telegram.md).

## Pasos
1. Entra a **Pedidos** (barra de arriba). Si estás en el **Dashboard**, también hay un botón **Pedidos**.
2. Verás tres pestañas: **Pendientes** (por atender), **Atendidos** y **Cancelados** (historial). En **Atendidos** y **Cancelados** hay un filtro **Día** que empieza en **hoy**: elige otra fecha y pulsa **Filtrar** (o **Hoy** para volver).
3. Cuando entra un pedido nuevo mientras tienes la página abierta, aparece un aviso **¡Nuevo pedido!** con el nombre del cliente y el total. Pulsa **Ver pedido** para ir a él.
4. Pulsa **Ver detalle** en un pedido para abrir **Detalle del pedido**: **Cliente**, **Teléfono**, **Dirección**, **Notas**, **Comentarios de productos**, **Productos**, **Subtotal**, **Envío**, **Propina** y **Total**, además de cuándo fue **Recibido**.
5. Cuando lo hayas entregado o resuelto, pulsa **Marcar como atendido**.
6. Si el pedido no se va a entregar, abre **Ver detalle**, despliega **Cancelar pedido**, escribe el **Motivo** (de 3 a 200 caracteres) y pulsa **Confirmar cancelación**. Un pedido ya atendido también se puede cancelar.
7. Pulsa **Cerrar** para salir del detalle.

## Qué verás
- «Pedido marcado como atendido.» y el pedido pasa de **Pendientes** a **Atendidos**, donde queda con la hora en que se atendió.
- «Pedido cancelado.» y el pedido pasa a **Cancelados**, con el motivo, quién lo canceló y cuándo. Un pedido cancelado **ya no cuenta** en tus ventas, pedidos ni productos más pedidos. La cancelación no se puede deshacer.
- Los pedidos que se cobran en la app de escritorio ([Mesifly Local](../04-mi-restaurante/mesifly-local.md)) aparecen en **Atendidos** con la etiqueta **Escritorio**, la mesa y el método de pago.
- La lista carga más pedidos al llegar al final («Cargando más pedidos…»).
- Si no hay nada: «No hay pedidos.»

## Problemas comunes
| Si ves… | Pasa porque… | Qué hacer |
|---|---|---|
| No me llegan pedidos | El menú no está visible, estás fuera de horario o el cliente no confirmó el pedido | Revisa [Menú no disponible](../08-para-tus-clientes/menu-no-disponible.md) |
| No me llega el aviso en el teléfono | Telegram no está conectado | [Conéctalo](conectar-telegram.md) |
| No veo el aviso «¡Nuevo pedido!» | La página estaba cerrada | Abre **Pedidos**: ahí aparecen todos los pendientes |
| «Escribe el motivo de la cancelación» | El motivo está vacío o tiene menos de 3 caracteres | Escríbelo y confirma de nuevo |
| El pago | La plataforma no cobra al cliente | El pago lo acuerdas directamente con tu cliente (efectivo o transferencia) |

## Relacionado
- [Conectar Telegram para recibir avisos](conectar-telegram.md)
- [El dashboard](../06-consultar-informacion/dashboard.md)
