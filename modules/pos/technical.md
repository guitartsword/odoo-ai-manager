# Tecnica de punto de venta

## Modelos de Odoo 16 usados por la primera skill

- `pos.order.line`: producto, cantidad, precio y orden.
- `pos.order`: referencia, fecha, PoS, sesion y pagos.
- `pos.payment`: metodo y monto individual.
- `product.product`: referencia interna (`default_code`).
- `res.users`: timezone del usuario autenticado (`tz`).
- `res.users.company_id`: compania activa usada como alcance por defecto.

## Primera skill

`skills/pos/daily_sales_report` consulta ordenes en estados `paid`, `done` e
`invoiced`. Produce `Ventas PoS`, `Pagos PoS` y `Resumen pagos` en XLSX. Es
`read_only` y no cambia Odoo.

Verifica campos y permisos en cada instancia, especialmente si existen
modulos personalizados o una version distinta de Odoo.

Las skills de PoS deben ser `read_only` salvo una necesidad concreta. Crear o
modificar `pos.order`, `pos.payment` o `pos.session` es una accion destructiva
para este proyecto y requiere preview, intencion explicita y confirmacion; no
se habilita por `ODOO_DRAFT_WORKFLOW = direct`.
