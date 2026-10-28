# Centro de ayuda de Mesifly (wiki base)

Wiki en Markdown que responde las dudas de quien usa el sistema: **cómo darse de alta, crear el menú, copiar enlaces, recibir pedidos, consultar información**, etc. Está escrita para **personas que no son técnicas** (dueños, empleados y clientes del restaurante).

Sirve de dos formas:

1. **Contenido para la página de ayuda de Mesifly** (se puede publicar tal cual).
2. **Base para otro proyecto**: la estructura, la plantilla y las reglas son genéricas; solo cambian los textos (ver [Reutilizar en otro proyecto](#reutilizar-en-otro-proyecto)).

## Índice

### 1. Primeros pasos
- [Crear tu cuenta](01-primeros-pasos/crear-cuenta.md)
- [Iniciar sesión y recuperar tu contraseña](01-primeros-pasos/iniciar-sesion.md)
- [El asistente de alta paso a paso](01-primeros-pasos/asistente-de-alta.md)
- [Prueba gratis y suscripción](01-primeros-pasos/prueba-gratis-y-suscripcion.md)

### 2. Tu menú
- [Subir fotos de tu menú (la IA lo arma por ti)](02-menu/subir-fotos-del-menu.md)
- [Crear y editar categorías](02-menu/categorias.md)
- [Crear y editar platillos](02-menu/platillos.md)
- [Ordenar con arrastrar y soltar](02-menu/ordenar-arrastrando.md)
- [Buscar, ver la vista previa y copiar el enlace](02-menu/ver-y-compartir-el-menu.md)

### 3. Pedidos
- [Recibir y atender pedidos](03-pedidos/recibir-y-atender-pedidos.md)
- [Conectar Telegram para recibir avisos](03-pedidos/conectar-telegram.md)
- [Horario de atención](03-pedidos/horario-de-atencion.md)

### 4. Tu restaurante
- [Datos, logo y color de tu restaurante](04-mi-restaurante/configurar-restaurante.md)
- [Varios restaurantes (sucursales)](04-mi-restaurante/varios-restaurantes.md)

### 5. Tu equipo
- [Crear empleados](05-equipo/crear-empleados.md)
- [Cómo entra un empleado y qué puede hacer](05-equipo/acceso-de-empleados.md)

### 6. Consultar información
- [El dashboard: ventas y productos más pedidos](06-consultar-informacion/dashboard.md)
- [Resumen de ventas de todos tus restaurantes](06-consultar-informacion/resumen-de-ventas.md)

### 7. Cuenta y plan
- [Tu perfil y tu contraseña](07-cuenta-y-plan/perfil-y-contrasena.md)
- [Tu plan: cuántos menús tienes](07-cuenta-y-plan/plan-y-menus.md)
- [Eliminar tu cuenta](07-cuenta-y-plan/eliminar-cuenta.md)

### 8. Para tus clientes
- [Cómo hace un pedido tu cliente](08-para-tus-clientes/hacer-un-pedido.md)
- [Por qué un cliente ve «Menú no disponible» o «Fuera de horario»](08-para-tus-clientes/menu-no-disponible.md)

### Consulta rápida
- [Preguntas frecuentes](preguntas-frecuentes.md)
- [Glosario](glosario.md)
- [Historial de cambios de esta ayuda](CHANGELOG.md)

---

## Convenciones (léelas antes de editar)

- **Idioma y tono:** español neutro, tuteo («tu menú», «recibe tus pedidos»), frases cortas. Nada de jerga técnica.
- **Una pregunta = un artículo.** Cada archivo responde una tarea concreta («cómo copio el enlace de mi menú»).
- **Nombres exactos de la pantalla:** los botones y campos se escriben **en negritas y tal como aparecen** (por ejemplo, **Nuevo platillo**). Si cambias un texto en la aplicación, cámbialo aquí.
- **Estructura fija de cada artículo:** *Para quién es → Antes de empezar → Pasos → Qué verás → Problemas comunes → Relacionado*. Usa la [plantilla](_plantillas/articulo.md).
- **Metadatos (front matter)** al inicio de cada archivo: `id`, `titulo`, `audiencia`, `categoria`, `resumen`, `palabras_clave`, `ruta_app`, `actualizado`, `relacionados`. Sirven para buscadores, índices y para generar la página.
- **Solo lo que existe.** Si una función no está en la aplicación, no se documenta. Lo dudoso se marca con `[POR CONFIRMAR]`, nunca se inventa.
- **Precios y límites** se escriben en un solo lugar ([`_variables.md`](_variables.md)) y se repiten tal cual en los artículos.

## Cómo se mantiene al día

Cada cambio en la aplicación que afecte lo que el usuario ve o hace **debe actualizar esta wiki en el mismo trabajo**. La regla está en [`.claude/rules/docs-sync.md`](../../.claude/rules/docs-sync.md) y el procedimiento en la habilidad [`mesifly-user-docs`](../../.claude/skills/mesifly-user-docs/SKILL.md). La prueba `spec/docs/ayuda_spec.rb` revisa que los metadatos estén completos y que ningún enlace interno esté roto.

## Reutilizar en otro proyecto

1. Copia la carpeta `docs/ayuda/` completa (incluye `_plantillas/` y `_variables.md`) y la regla y habilidad de `.claude/`.
2. Abre [`_variables.md`](_variables.md) y reemplaza los valores (nombre del producto, dominio, precio, prueba gratis, etc.). Busca y reemplaza esos mismos valores en los artículos.
3. Revisa **artículo por artículo** contra el sistema nuevo: borra lo que no exista, reescribe los pasos y los nombres de botones, y añade lo nuevo con la plantilla.
4. Adapta la tabla «qué código toca qué artículo» de la regla `docs-sync.md` a las carpetas del proyecto nuevo.
5. Publica: el front matter de cada archivo alcanza para generar una página de ayuda (lista por `categoria`, buscador por `palabras_clave` y `resumen`, y migas de pan por carpeta). Cualquier generador de sitios estáticos o una ruta que lea los `.md` sirve; los enlaces entre artículos son relativos.
