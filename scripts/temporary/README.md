# Scripts temporales

Usa esta carpeta para experimentos y consultas que aun no fueron revisadas.
Su contenido se ignora por git excepto este README y no debe cargarse como
contexto de IA por defecto.

Un agente puede dejar aqui una consulta puntual para cualquier modelo o
extension de Odoo. Debe usar el cliente compartido cuando sea posible,
inspeccionar campos con `fields_get`, evitar credenciales y datos reales, y
verificar primero si la operacion es `read_only`, `draft` o `destructive`.

Antes de mover un script a `scripts/saved`, agrega una skill, define su modo
`read_only` o `mutation`, agrega pruebas y revisa que no guarde secretos ni
datos reales.
