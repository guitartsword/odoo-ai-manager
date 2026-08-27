# Contribuir

Antes de agregar una skill:

1. Actualiza el `business.md` y `technical.md` del modulo.
2. Define su manifiesto y `SKILL.md`.
3. Decide explicitamente si es `read_only` o `mutation`.
4. Agrega pruebas con datos sinteticos.
5. Ejecuta `uv run pytest` y `uv run odoo-ai-manager doctor`.

Las mutaciones requieren revision adicional y no deben mezclarse con skills de
consulta.
