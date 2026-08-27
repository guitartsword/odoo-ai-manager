# Tecnica de inventario

## Modelos habituales

- `product.product`: producto y referencia.
- `stock.quant`: cantidad por ubicacion.
- `stock.move`: movimiento planificado o realizado.
- `stock.picking`: transferencia, recepcion o entrega.
- `stock.location`: ubicacion.

No uses `stock.quant` sin documentar compania, ubicacion y fecha de lectura.
Crear una transferencia preparada puede declararse `mutation_kind = "draft"` y
seguir `ODOO_DRAFT_WORKFLOW`. Validar pickings, cambiar cantidades o crear
ajustes sobre `stock.quant` es `mutation_kind = "destructive"` y requiere
confirmacion siempre. Crear `product.product` tambien es destructivo: exige
preview, producto similar y confirmacion de sus campos funcionales.
