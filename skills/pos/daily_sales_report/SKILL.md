# Reporte diario de ventas PoS

## Cuando usarla

Usa esta skill cuando la persona pida ventas de PoS, ventas por producto,
ventas por tienda o sesion, cobros por metodo de pago o un Excel de ese
periodo.

## Acceso

- Modo: `read_only`.
- No crea ni modifica ordenes, pagos, productos, sesiones o inventario.
- Puede leer `pos.order.line`, `pos.order`, `pos.payment`, `product.product` y
  `res.users`.

## Entradas

- `start_date`: obligatorio, fecha local del usuario de Odoo.
- `end_date`: opcional e inclusivo. Si falta, no se agrega limite superior.
- `output_path`: ruta del XLSX.

## Salida

El XLSX contiene:

- `Ventas PoS`: una fila por linea de producto.
- `Pagos PoS`: una fila por pago individual, con metodo e importe exacto.
- `Resumen pagos`: totales agrupados por metodo.

Los pagos no se repiten cuando una orden tiene varias lineas. `Precio` es el
precio unitario de la linea; no es el importe pagado.

## Timezone

La herramienta obtiene `res.users.tz` del usuario autenticado. Interpreta el
periodo en esa zona, convierte sus limites a UTC para Odoo y convierte las
horas de `date_order` de regreso antes de escribir Excel.

## Ejemplos

```powershell
uv run odoo-pos-daily-sales --start-date 2026-08-22 --end-date 2026-08-22
```

Si una orden tiene pagos Visa por 1000 y Efectivo por 695, `Pagos PoS` muestra
dos filas y `Resumen pagos` muestra ambos totales separados.
