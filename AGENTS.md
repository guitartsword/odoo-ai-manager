# Instrucciones para agentes de IA

## Contexto obligatorio

Antes de trabajar, lee:

1. `knowledge/business.md`
2. `knowledge/technical.md`
3. `modules/<modulo>/business.md`
4. `modules/<modulo>/technical.md`
5. La `SKILL.md` de la herramienta que vas a usar, si existe

Este repositorio es un starter kit, no un catalogo completo de Odoo. Los
modulos y skills existentes son ejemplos de patron. Si el modulo, la
extension o la skill no existe, usa el cliente generico, inspecciona los
modelos/campos disponibles y crea el contexto y las pruebas que falten.

Si falta informacion de negocio, dilo y formula una pregunta concreta. No
inventes reglas contables, definiciones de margen, disponibilidad o impuestos.
La ausencia de documentacion tecnica se resuelve inspeccionando Odoo (por
ejemplo con `fields_get`) y documentando lo observado, no adivinando.

## Seguridad

- El modo predeterminado es `read_only`.
- Toda skill de `mutation` debe declarar si crea un `draft` o ejecuta una accion
  `destructive`.
- Un `draft` requiere vista previa y confirmacion por defecto. Si la persona
  eligio `direct` en el configurador y la operacion esta en la allowlist, puede
  crearse sin aprobacion adicional por operacion; el resultado debe quedar
  registrado.
- Una accion `destructive` siempre requiere vista previa y confirmacion
  expresa, aunque el flujo de borradores sea `direct`.
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
