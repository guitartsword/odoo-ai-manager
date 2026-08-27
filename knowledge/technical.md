# Memoria tecnica transversal

## Principios

- Las skills son pequenas, versionadas y tienen una sola responsabilidad.
- El dominio del negocio no debe depender de XML-RPC, JSON-2 o de un proveedor
  de IA concreto.
- Los adaptadores externos normalizan respuestas a entidades internas.
- Toda skill declara `read_only` o `mutation` en su manifiesto. Una skill de
  mutacion tambien declara `mutation_kind = "draft"` o `"destructive"`.
- Los borradores siguen `ODOO_DRAFT_WORKFLOW`: `review` exige vista previa y
  confirmacion por operacion; `direct` permite crear solo borradores
  previamente allowlisted sin esa aprobacion adicional.
- Las acciones destructivas siempre requieren confirmacion, trazabilidad y
  pruebas de rollback o de fallo seguro.

## Conexion a Odoo

El primer transporte es XML-RPC. Se autentica contra `common`, obtiene `uid`
y ejecuta metodos con `object.execute_kw`. La base de datos, usuario y
credencial llegan desde `.env`. La credencial puede ser una API key de Odoo.

El usuario autenticado es tambien la fuente de `res.users.tz`. Los limites de
fechas locales se convierten a UTC para filtrar `date_order`, y los datetimes
se convierten de UTC al timezone del usuario para las salidas.

Consulta `docs/odoo-connection.md` antes de agregar un transporte o soportar
otra version.

## Contrato de una skill

Cada skill debe tener:

- `skill.toml` con id, modulo, descripcion, permiso y entrypoint.
- `SKILL.md` con objetivo, entradas, salidas, modelos Odoo y ejemplos.
- Pruebas unitarias y, cuando sea posible, fixtures sin datos reales.
- Un script guardado solo si es reutilizable y revisado.

## Datos sensibles

Nunca se versionan credenciales, dumps, nombres de clientes reales, imagenes
privadas ni reportes de produccion. Los fixtures deben ser sinteticos.
