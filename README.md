# Odoo AI Manager

Repositorio publico para compartir conocimiento de negocio, skills y scripts
reutilizables para trabajar con Odoo mediante IA.

La idea no es dar acceso directo al codigo a una persona no tecnica. La IA
lee el conocimiento del negocio, selecciona una skill aprobada y ejecuta una
herramienta con permisos explicitos. Las consultas son `read_only` por
defecto. Las acciones que cambian Odoo deben vivir en `mutation` y requieren
una vista previa y confirmacion expresa.

## Inicio rapido

Requisitos del host: Python 3.12+, `uv` y `git`. En este host ya estan
disponibles. Para revisar o instalar dependencias:

```powershell
.\scripts\bootstrap.ps1 -InstallMissing
uv run odoo-ai-manager doctor
```

Configura las credenciales en `.env` usando `.env.example` como referencia.
Nunca subas `.env`, API keys, reportes reales ni datos de clientes.

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

Ejemplos de preguntas que la primera version puede preparar:

- "Cuanto vendimos ayer por metodo de pago?"
- "Que productos tienen menos existencia?"
- "Que compras estan pendientes de recibir?"
- "Genera un Excel de ventas del mes por tienda."

Para una accion de mutacion, la IA debe mostrar el cambio propuesto, pedir
confirmacion y registrar el resultado. Nunca debe crear productos, ajustar
inventario, subir imagenes o publicar asientos solo por interpretar una
pregunta ambigua.

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
