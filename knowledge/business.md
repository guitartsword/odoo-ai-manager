# Conocimiento transversal del negocio

Este documento es la memoria compartida de la organizacion. Debe ser
completado y revisado por las personas que conocen la operacion; la IA no debe
tratar los valores de ejemplo como hechos universales.

## Organizacion

- Nombre comercial:
- Companias incluidas:
- Moneda principal:
- Paises y zonas horarias:
- Tiendas, almacenes y puntos de venta:

## Definiciones que deben confirmarse

- "Venta": indicar si incluye ventas de PoS, pedidos confirmados o ambos.
- "Ingreso": indicar si se mide por total con impuestos, sin impuestos o por
  pagos registrados.
- "Existencia": distinguir disponible, pronosticada, reservada y cantidad a
  mano.
- "Compra": distinguir solicitud de cotizacion, orden confirmada y factura de
  proveedor.
- "Margen": documentar costo, descuentos, impuestos y moneda usados.

## Reglas de respuesta

- Las fechas se interpretan en el timezone del usuario de Odoo.
- Las preguntas sin rango de fechas deben pedir aclaracion, salvo que una
  skill defina un periodo por defecto.
- Los totales deben identificar moneda y compania.
- Los pagos no son automaticamente iguales a ventas: una orden puede tener
  varios metodos de pago, reembolsos o diferencias de redondeo.
- Las cifras de inventario deben indicar la ubicacion y el momento de corte.

## Preguntas abiertas

Registra aqui decisiones pendientes del negocio, por ejemplo que estados de
orden se consideran venta valida o como se reportan devoluciones.
