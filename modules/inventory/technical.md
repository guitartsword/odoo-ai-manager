# Tecnica de inventario

## Modelos habituales

- `product.product`: producto y referencia.
- `stock.quant`: cantidad por ubicacion.
- `stock.move`: movimiento planificado o realizado.
- `stock.picking`: transferencia, recepcion o entrega.
- `stock.location`: ubicacion.

No uses `stock.quant` sin documentar compania, ubicacion y fecha de lectura.
Crear ajustes, validar pickings o cambiar cantidades requiere `mutation` y
confirmacion.
