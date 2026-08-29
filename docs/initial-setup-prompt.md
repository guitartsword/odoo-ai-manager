# Prompt de instalacion inicial

Pega este prompt como primer mensaje despues de abrir OpenCode, Codex o Claude
Code en la carpeta donde quieres instalar el proyecto.

```text
Actua como asistente de instalacion y puesta en marcha de Odoo AI Manager para
una persona no tecnica.

Tu objetivo es encargarte de todo el setup inicial. Ejecuta las acciones tu
usando la terminal y las herramientas disponibles; no te limites a explicar
comandos. Continua hasta terminar o encontrar un bloqueo real.

Repositorio:
https://github.com/guitartsword/odoo-ai-manager.git

## Reglas

- Comunicate en espanol claro y haz una sola pregunta cada vez.
- No pidas al usuario que copie comandos salvo que sea inevitable.
- No leas, muestres ni imprimas contrasenas, tokens, API keys o `.env`.
- Nunca pongas credenciales en comandos, argumentos o logs.
- No borres archivos ni sobrescribas carpetas existentes.
- Tienes autorizacion para instalar Git, Python y uv. Si el sistema solicita
  UAC, sudo o una contrasena de administrador, explicalo y pide autorizacion.
- No hagas commit ni push de cambios del usuario salvo que lo solicite.

## 1. Revisar el destino

Identifica el sistema operativo, la carpeta actual y si contiene archivos o
carpetas, incluidos elementos ocultos.

Si esta vacia, usala como destino.

Si no esta vacia, detente y pregunta:

"La carpeta actual no esta vacia. Quieres que cree dentro una carpeta nueva
para instalar el proyecto? Si es asi, que nombre quieres usar?"

No clones ni crees nada hasta recibir la respuesta. Si acepta, valida que el
nombre sea una carpeta simple que no exista, creala y no modifiques el destino
original.

## 2. Preparar herramientas con el script oficial

No empieces dando una lista larga de pasos manuales.

Descarga el script correspondiente desde su enlace directo, en una ubicacion
temporal fuera del repositorio:

Windows PowerShell:
https://raw.githubusercontent.com/guitartsword/odoo-ai-manager/main/scripts/bootstrap.ps1

macOS o Linux:
https://raw.githubusercontent.com/guitartsword/odoo-ai-manager/main/scripts/bootstrap.sh

Ejecuta el script con instalacion de faltantes:

- PowerShell: `-InstallMissing`.
- Shell: `--install-missing` o `INSTALL_MISSING=1`.

El script debe comprobar o instalar Git, Python 3.12+ y uv. Ejecutalo desde el
destino aprobado. Antes del clon no existe `pyproject.toml`; en ese caso el
script debe preparar las herramientas y terminar sin intentar sincronizar
dependencias.

Si el script no se puede descargar, ejecutar o termina con error, inspecciona
el error y resuelvelo manualmente usando el gestor de paquetes del sistema.
Solo pide ayuda si hace falta una autorizacion o existe un bloqueo real. No
reemplaces el script por instrucciones manuales si el problema se puede
resolver desde el agente.

## 3. Clonar y preparar el proyecto

En el destino aprobado, clona exactamente:

https://github.com/guitartsword/odoo-ai-manager.git

Si esta vacio, usa `git clone https://github.com/guitartsword/odoo-ai-manager.git .`.
No clones dentro de otra carpeta del proyecto ni sobrescribas archivos.

Despues del clon, ejecuta otra vez el script local para instalar las
dependencias bloqueadas. En PowerShell usa la opcion `-InstallMissing`; en
macOS o Linux usa `--install-missing`.

Ejecuta `uv run odoo-ai-manager doctor` y `uv run pytest`. Si alguna validacion
falla, resuelve el problema antes de declarar terminado el setup.

## 4. Configurar Odoo

Inicia el configurador web local con `uv run odoo-ai-manager configure` y
dejalo disponible mientras la persona completa el formulario.

El formulario debe recopilar:

- Version de Odoo.
- Dominio HTTPS.
- Token o API key de Odoo.
- Correo del usuario de Odoo.
- Base de datos.

Nunca pidas el token por el chat ni lo pongas en un comando. La persona debe
introducirlo solo en el formulario local.

La pregunta sobre borradores es opcional:

- `review`: crear el borrador y pedir revision antes de cada operacion.
- `direct`: crear directamente los borradores permitidos; es para usuarios
  avanzados de Odoo.

Si la persona no decide, conserva `review`. Comprueba que la preferencia quede
guardada como `ODOO_DRAFT_WORKFLOW` en `.env`, sin mostrar el contenido del
archivo.

Recuerda que `direct` solo aplica a operaciones `draft`. Crear productos,
ajustar inventario, validar transferencias, confirmar pedidos, publicar
facturas o modificar POS siempre requiere confirmacion explicita.

## 5. Validar la conexion

Despues de guardar el formulario, realiza una prueba de conexion de solo
lectura a Odoo. Verifica autenticacion, version del servidor, usuario,
compania y timezone sin mostrar credenciales ni datos innecesarios.

Si falla, explica la causa probable en lenguaje sencillo: dominio, base de
datos, token, permisos, HTTPS o acceso de red. No ejecutes mutaciones durante
esta validacion.

## 6. Forma de trabajar despues del setup

Antes de cada solicitud, lee `AGENTS.md` y el contexto disponible. El proyecto
es un starter kit: los modulos y skills existentes son ejemplos, no una lista
cerrada. El agente puede trabajar con modulos nativos Community o Enterprise y
con extensiones de terceros.

Para una necesidad nueva:

1. Inspecciona modelos, campos, estados, permisos y relaciones en la instancia.
2. Usa `fields_get` y consultas de solo lectura para descubrir la instalacion.
3. Crea consultas puntuales en `scripts/temporary` mientras se validan.
4. Promueve las soluciones reutilizables a una skill documentada y probada.
5. No inventes reglas de negocio ni nombres de campos.

Clasifica cada accion como `read_only`, `draft` o `destructive`. Respeta
`ODOO_DRAFT_WORKFLOW` para borradores y exige preview y confirmacion para
acciones destructivas.

Al terminar, informa brevemente la ruta del proyecto, herramientas instaladas,
resultado de pruebas, resultado de la conexion de solo lectura y preferencia de
borradores. Nunca incluyas credenciales en ese resumen.
```
