# Inventario

## Proposito

Responder preguntas sobre existencias, movimientos, almacenes, ubicaciones,
lotes, series y reabastecimiento.

## Definiciones

- Disponible, a mano, reservado y pronosticado no son sinonimos.
- Un movimiento creado no necesariamente esta validado.
- La ubicacion y la fecha de corte son obligatorias para interpretar una
  cantidad.
- Una transferencia preparada puede ser un borrador; validar la transferencia
  o ajustar existencias es una mutacion de alto riesgo.
- Si existen varios almacenes, la IA debe preguntar cual corresponde antes de
  preparar una transferencia.
- Crear un producto requiere confirmar tipo (servicio, consumible o producto),
  seguimiento de inventario, uso en PoS, categoria y si se vende o compra.
  Debe mostrar un producto similar y un preview antes de crearlo.

## Preguntas frecuentes

- Existencia actual por almacen.
- Productos bajo minimo.
- Transferencias pendientes y lotes por vencer.
