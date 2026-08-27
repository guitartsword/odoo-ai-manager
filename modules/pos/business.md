# Punto de venta

## Proposito

Analizar ventas de mostrador, sesiones, cajas, productos y cobros por metodo
de pago.

## Reglas conocidas

- Una orden puede tener varias lineas de producto.
- Una orden puede tener varios registros de pago; no se debe repetir el
  importe de un pago por cada linea.
- Venta y pago son conceptos distintos y deben reconciliarse.
- Las sesiones permiten agrupar la operacion de una caja o tienda.
- Devoluciones y pagos negativos deben conservar su signo.
- Las capacidades iniciales deben priorizar reportes y configuracion en
  `read_only`.
- Crear una orden, pago o sesion de PoS afecta la operacion de caja y requiere
  confirmar expresamente la intencion; el modo directo de borradores no lo
  omite.

## Preguntas frecuentes

- Ventas del dia por tienda, sesion, producto o metodo de pago.
- Diferencia entre total vendido y total cobrado.
- Sesiones abiertas o pendientes de cierre.
