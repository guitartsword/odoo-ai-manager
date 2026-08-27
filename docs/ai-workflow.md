# Flujo para usuarios no tecnicos

## Pregunta

La persona escribe una pregunta de negocio sin conocer modelos o campos de
Odoo. El agente debe identificar modulo, periodo, compania, moneda y nivel de
detalle. Si falta algo que cambie el resultado, pregunta antes de consultar.

## Consulta

El agente carga el `business.md` y `technical.md` del modulo, encuentra una
skill `read_only` y ejecuta solo sus entradas documentadas. La respuesta debe
explicar el resultado con terminos del negocio, no con una lista de llamadas
XML-RPC.

## Archivo o analisis

Los reportes se guardan en una ruta indicada por el usuario. Deben incluir
filtros, timezone, moneda y fecha de generacion cuando sea relevante. Los
datos de pagos, ventas e inventario deben poder reconciliarse con Odoo.

## Mutacion

Crear productos, subir fotos, ajustar inventario, confirmar compras o tocar
contabilidad son acciones de alto riesgo. El agente debe:

1. Explicar la accion y mostrar los registros afectados.
2. Mostrar los valores nuevos y los que no cambiara.
3. Pedir confirmacion clara.
4. Ejecutar una skill `mutation` con usuario y permisos adecuados.
5. Devolver resultado, errores y referencia de auditoria.
