# Odoo AI Manager

Repositorio publico para compartir conocimiento de negocio, skills y scripts
reutilizables para trabajar con Odoo mediante IA.

La idea no es dar acceso directo al codigo a una persona no tecnica. La IA
lee el conocimiento del negocio, selecciona una skill aprobada y ejecuta una
herramienta con permisos explicitos. Las consultas son `read_only` por
defecto. Las mutaciones se clasifican como `draft` o `destructive`: los
borradores siguen una preferencia configurable y las acciones destructivas
requieren siempre vista previa y confirmacion expresa.

## Inicio rapido

Desde una terminal nueva:

```powershell
git clone https://github.com/guitartsword/odoo-ai-manager.git
Set-Location odoo-ai-manager
```

Requisitos del host: Python 3.12+, `uv` y `git`. En este host ya estan
disponibles. Para revisar o instalar dependencias:

```powershell
.\scripts\bootstrap.ps1 -InstallMissing
uv run odoo-ai-manager doctor
```

Para que un agente de IA haga el setup completo para una persona no tecnica,
usa [`docs/initial-setup-prompt.md`](docs/initial-setup-prompt.md). Los
scripts de bootstrap tambien se pueden descargar directamente:

- [Windows PowerShell](https://raw.githubusercontent.com/guitartsword/odoo-ai-manager/main/scripts/bootstrap.ps1)
- [macOS/Linux](https://raw.githubusercontent.com/guitartsword/odoo-ai-manager/main/scripts/bootstrap.sh)

Configura la conexion con el formulario web local:

```powershell
uv run odoo-ai-manager configure
```

El formulario pide version de Odoo, dominio HTTPS, token/API key, correo y
base de datos. Tambien pregunta opcionalmente como trabajar con borradores:
`review` muestra y confirma cada uno; `direct` los crea sin aprobacion
adicional y esta pensado para usuarios avanzados. Las acciones destructivas no
se benefician de esta opcion. Nunca subas `.env`, API keys, reportes reales ni
datos de clientes.

Tambien puedes usar `.env.example` como referencia.

```powershell
uv sync
uv run odoo-ai-manager skills list
uv run odoo-ai-manager context pos
```

Para generar el primer reporte:

```powershell
uv run odoo-pos-daily-sales --start-date 2026-08-22 --end-date 2026-08-22
```

El reporte usa el timezone del usuario autenticado en Odoo, consulta fechas
locales convirtiendo sus limites a UTC y guarda las horas del XLSX en el
timezone del usuario.

## Estructura

```text
knowledge/                         Contexto transversal del negocio y tecnica
modules/<modulo>/business.md       Como entiende el negocio ese modulo
modules/<modulo>/technical.md      Modelos, campos y reglas tecnicas
skills/<modulo>/<skill>/            Contrato e instrucciones de una skill
scripts/saved/<modulo>/read_only/  Scripts reutilizables sin mutaciones
scripts/saved/<modulo>/mutation/   Scripts que cambian datos, siempre protegidos
scripts/temporary/                 Experimentos locales, no se cargan por defecto
src/odoo_ai_manager/               Codigo compartido y adaptadores
docs/                               Arquitectura, seguridad y API de Odoo
```

## Alcance del starter kit

Este repositorio no intenta implementar todos los modulos ni todas las
personalizaciones de Odoo. Es una base para trabajar con un agente de IA desde
el checkout: `knowledge/`, `modules/` y `skills/` contienen ejemplos de
estructura, reglas y una primera implementacion, no una lista cerrada de lo
que el agente puede hacer.

Un agente puede trabajar tambien con modulos nativos de Community o Enterprise
y con extensiones de terceros. Para una necesidad nueva debe:

1. Leer `AGENTS.md` y el contexto disponible.
2. Inspeccionar modelos, campos, estados, permisos y relaciones de esa
   instancia de Odoo.
3. Crear una consulta o herramienta en `scripts/temporary` mientras se valida.
4. Promoverla a una skill documentada y probada si se vuelve reutilizable.

OpenCode, Codex o Claude Code se ejecutan desde la raiz del repositorio. El
proyecto no obliga a usar un proveedor de IA, no incluye una API key del
proveedor ni pretende ser una aplicacion final. El agente aporta la interfaz
de lenguaje y este repositorio aporta contexto, patrones, cliente Odoo y
guardrails.

## Modulos iniciales

- `sales`: cotizaciones, pedidos y ventas.
- `purchases`: proveedores, solicitudes y ordenes de compra.
- `pos`: punto de venta, sesiones, pagos y ventas de mostrador.
- `inventory`: existencias, movimientos, lotes y ubicaciones.
- `accounting`: facturas, pagos, cuentas y reportes contables.

Cada modulo tiene un documento de negocio y uno tecnico. Son documentos vivos:
se deben actualizar cuando el equipo confirme una definicion, excepcion o regla.

## Usar el repositorio con IA

Antes de responder una pregunta, el agente debe leer `AGENTS.md`, el contexto
transversal y los documentos del modulo correspondiente. Debe indicar que
skill utilizo, que rango de fechas y compania aplico, y distinguir entre dato
consultado, calculo e inferencia.

Ejemplos de preguntas que la primera skill puede resolver:

- "Cuanto vendimos ayer por metodo de pago?"
- "Que productos tienen menos existencia?"
- "Que compras estan pendientes de recibir?"
- "Genera un Excel de ventas del mes por tienda."

Las preguntas sobre otros modelos o extensiones pueden implementarse siguiendo
el mismo patron; primero hay que verificar la version, los modulos instalados,
los campos y los permisos del usuario de Odoo.

Para una accion de mutacion, la IA debe clasificar el cambio. Los borradores
pueden seguir `ODOO_DRAFT_WORKFLOW`; crear productos, ajustar inventario,
subir imagenes, validar documentos o publicar asientos siempre requieren
preview y confirmacion, y nunca deben ejecutarse por interpretar una pregunta
ambigua.

## API de Odoo y versiones

El primer adaptador usa XML-RPC y esta validado con el esquema de Odoo 16. El
transporte tambien cubre la firma legacy documentada para Odoo 17, pero cada
version o instancia debe probarse antes de declararse compatible. El codigo
separa el transporte de los casos de uso para poder incorporar JSON-2 en
versiones futuras sin reescribir las skills.

La compatibilidad real depende tambien de los modulos instalados, campos
personalizados y permisos del usuario. Por eso las skills declaran sus
modelos y campos, y el adaptador soporta descubrimiento con `fields_get`.

## Desarrollo

```powershell
uv sync
uv run pytest
uv run odoo-ai-manager doctor
```

## Acceso y repositorios

Este repositorio es publico: cualquier persona puede leer todos sus modulos.
La separacion por carpetas ayuda a organizar y revisar cambios, pero no es un
mecanismo de permisos. Para compartir solo un modulo sensible se debe usar un
repositorio separado, equipos de GitHub y permisos minimos en Odoo. Consulta
`docs/access-control.md`.
