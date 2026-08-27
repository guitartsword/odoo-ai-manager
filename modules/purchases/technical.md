# Tecnica de compras

## Modelos habituales

- `purchase.order`: solicitudes y ordenes de compra.
- `purchase.order.line`: productos, cantidades y precios.
- `stock.picking`: recepciones y transferencias.
- `res.partner`: proveedores.

Validar estados, companias, almacenes y campos personalizados antes de
publicar una skill. Crear una RFQ u orden no confirmada es `mutation` con
`mutation_kind = "draft"` y sigue `ODOO_DRAFT_WORKFLOW`. Confirmar una orden,
modificar cantidades o validar una recepcion es `destructive`.
