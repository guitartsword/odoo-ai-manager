# Conexion versionada a Odoo

## Odoo 16 y 17

La documentacion oficial de Odoo 16 y 17 describe XML-RPC como API externa:

- `https://www.odoo.com/documentation/16.0/developer/reference/external_api.html`
- `https://www.odoo.com/documentation/17.0/developer/reference/external_api.html`

El flujo usado por el primer adaptador es:

1. Crear `https://servidor/xmlrpc/2/common` y
   `https://servidor/xmlrpc/2/object`.
2. Ejecutar `common.authenticate(db, login, password_or_api_key, {})`.
3. Usar el `uid` con `object.execute_kw(db, uid, credential, model, method,
   args, kwargs)`.
4. Preferir `search_read`, campos explicitos y paginacion.
5. Usar `fields_get` cuando una skill necesite descubrir campos disponibles.

En Odoo 16 el usuario de integracion necesita permisos de acceso al modelo y
la edicion de Odoo debe permitir API externa. Una API key sustituye a la
contrasena, pero conserva los privilegios del usuario.

## Timezone del usuario

Los campos `Datetime` de Odoo se almacenan en UTC. La interfaz web los muestra
en `res.users.tz`, pero una integracion no debe asumir esa conversion. El
adaptador lee `res.users.tz` del usuario autenticado, interpreta las fechas de
la pregunta en esa zona y convierte los limites a UTC antes de consultar.
Tambien convierte los resultados a esa zona antes de generar un archivo.

El adaptador toma la compania principal del usuario (`res.users.company_id`)
como alcance por defecto, agrega `allowed_company_ids` al contexto y filtra
las ordenes por esa compania. Si una operacion necesita otra compania, debe
declararla explicitamente y mantenerla dentro de los permisos del usuario.

## Configuracion local

El configurador se inicia con `uv run odoo-ai-manager configure` y escucha en
`127.0.0.1` por defecto. Pide version, dominio HTTPS, token, correo y base de
datos, y escribe esos valores en `.env` sin volver a mostrar el token.

La pregunta opcional sobre borradores guarda `ODOO_DRAFT_WORKFLOW`:

- `review`: vista previa y confirmacion antes de cada borrador.
- `direct`: permite crear borradores allowlisted directamente; es una opcion
  pensada para usuarios avanzados de Odoo.

El valor por defecto es `review`. Esta preferencia no elimina la confirmacion
obligatoria para acciones destructivas.

## Versiones posteriores

Odoo 19 documenta la API externa JSON-2:

- `https://www.odoo.com/documentation/19.0/developer/reference/external_api.html`

JSON-2 usa `POST /json/2/<model>/<method>`, autenticacion `Bearer` con API key,
argumentos nombrados y `X-Odoo-Database` cuando corresponde. La misma
documentacion marca XML-RPC/JSON-RPC como legacy con una retirada prevista
para Odoo 22.

Por eso el proyecto no debe seleccionar una implementacion solo por el numero
de version. Debe separar:

- transporte y autenticacion;
- operaciones de lectura y mutacion;
- modelos internos de las respuestas de Odoo;
- descubrimiento de campos y capacidades;
- normalizacion de errores.

La skill de ventas PoS usa actualmente XML-RPC y esta probada con el esquema
de Odoo 16. Para otra version se debe verificar primero los modelos instalados,
campos personalizados, permisos y transporte disponible.
