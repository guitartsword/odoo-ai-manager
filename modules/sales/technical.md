# Tecnica de ventas

## Modelos habituales

- `sale.order`: cotizaciones y pedidos.
- `sale.order.line`: productos, cantidades y precios.
- `res.partner`: clientes.
- `product.product`: variantes y referencias.

## Estados

Validar en la instancia antes de usar `state`: Odoo y modulos instalados pueden
agregar estados o reglas. Consultar `fields_get` y documentar filtros en cada
skill.

## Skills

Las consultas deben ser `read_only`. Crear una cotizacion o pedido no
confirmado es `mutation_kind = "draft"` y sigue `ODOO_DRAFT_WORKFLOW`.
Confirmar pedidos o ejecutar acciones que cambien su estado es destructivo y
requiere preview y confirmacion.
