---
id: platillos
titulo: Cómo creo, edito y elimino platillos
audiencia: dueno
categoria: menu
resumen: Agregar un platillo con nombre, precio, descripción y foto; cambiar su estado; eliminarlo con confirmación.
palabras_clave: [platillo, producto, agregar platillo, precio, foto del platillo, imagen, activo, inactivo, archivado, eliminar platillo]
ruta_app: /:slug/menu/config
actualizado: 2026-10-27
relacionados: [categorias, ordenar-arrastrando, ver-y-compartir-el-menu]
---
# Cómo creo, edito y elimino platillos

## Para quién es
Para el **dueño**.

## Antes de empezar
- Tener al menos una [categoría](categorias.md).
- Si quieres foto: una imagen **JPG, PNG o WebP de hasta 8 MB**.

## Pasos: crear un platillo
1. En **Menú** pulsa **Nuevo platillo**. Se abre una ventana.
2. Llena los campos:
   - **Nombre** (obligatorio).
   - **Descripción** (opcional): ingredientes, tamaño, etc.
   - **Categoría**: escribe para buscarla en **Buscar categoría…** y elígela.
   - **Precio**. La **Moneda** se muestra bloqueada: es la de tu restaurante.
   - **Estado**: **Activo** (se muestra a tus clientes), **Inactivo** (se oculta pero lo conservas) o **Archivado**.
   - **Posición**: opcional. Es más fácil [ordenar arrastrando](ordenar-arrastrando.md).
   - **Imagen**: pulsa **Subir imagen**, elige la foto. Para cambiarla usa **Cambiar imagen**; para quitarla, la **×** pequeña sobre la foto (**Quitar imagen**).
3. Pulsa **Crear Platillo**. El botón se bloquea y dice **Guardando…** hasta terminar.
4. La ventana se cierra y el platillo aparece en su categoría.

## Pasos: editar
1. En el platillo pulsa **Editar**, cambia lo que necesites y pulsa **Actualizar Platillo**.
2. Para **ocultarlo temporalmente** (por ejemplo, se acabó), cámbialo a **Inactivo**; vuelve a **Activo** cuando lo tengas.

## Pasos: eliminar
1. Pulsa **Eliminar** en el platillo.
2. Aparece «**Eliminar platillo** — ¿Seguro que quieres eliminar «Nombre»? Esta acción no se puede deshacer.»
3. Pulsa **Eliminar** para confirmar, o **Cancelar**.

## Qué verás
Avisos verdes: «✓ ¡Platillo agregado al menú!», «✓ Platillo actualizado.» o «✓ Platillo eliminado del menú.». La lista se actualiza sin recargar y conserva tu posición en la pantalla.

## Problemas comunes
| Si ves… | Pasa porque… | Qué hacer |
|---|---|---|
| «debe ser una imagen (JPG, PNG o WebP)» | El archivo es de otro tipo (por ejemplo PDF) | Sube una imagen JPG, PNG o WebP |
| «no puede pesar más de 8 MB» | La foto es muy pesada | Reduce su tamaño o sube otra |
| El botón se queda en **Guardando…** | La foto es grande o la conexión es lenta | Espera unos segundos; si falla verás un aviso rojo y podrás reintentar |
| Mi cliente no ve el platillo | Está **Inactivo** o **Archivado**, o su categoría no existe | Ponlo en **Activo** |
| Un platillo no se puede mover a una categoría de otro restaurante | Cada restaurante tiene sus propias categorías | Usa solo las categorías de ese restaurante |

## Relacionado
- [Ordenar con arrastrar y soltar](ordenar-arrastrando.md)
- [Cómo hace un pedido tu cliente](../08-para-tus-clientes/hacer-un-pedido.md)
