# Instrucciones para agentes de IA

## Contexto obligatorio

Antes de trabajar, lee:

1. `knowledge/business.md`
2. `knowledge/technical.md`
3. `modules/<modulo>/business.md`
4. `modules/<modulo>/technical.md`
5. La `SKILL.md` de la herramienta que vas a usar

Si falta informacion, dilo y formula una pregunta concreta. No inventes
reglas contables, definiciones de margen, disponibilidad o impuestos.

## Seguridad

- El modo predeterminado es `read_only`.
- No ejecutes una skill de `mutation` sin confirmacion expresa despues de
  mostrar una vista previa del cambio.
- No leas ni imprimas `.env`, contrasenas, API keys o datos innecesarios.
- Usa el usuario de Odoo con los privilegios minimos necesarios.
- No guardes datos reales en `scripts/temporary` ni en el repositorio.
- Si la peticion es ambigua, primero aclara compania, fechas, moneda y alcance.

## Respuestas de negocio

Explica los resultados en lenguaje de negocio. Incluye el periodo, filtros,
moneda y fuente. Separa claramente datos obtenidos de Odoo, calculos e
interpretaciones. Si generas un archivo, informa su ruta y formato.

## Cambios al repositorio

Mantener la documentacion de negocio y tecnica junto con cada modulo. Agrega
pruebas para cada skill nueva. No conviertas un script temporal en skill
guardada sin revisar su permiso, entradas, salidas y manejo de errores.
