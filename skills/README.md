# Skills

Una skill es una capacidad pequena y reusable que la IA puede seleccionar a
partir de una pregunta de negocio.

Cada carpeta `skills/<modulo>/<nombre>/` debe incluir:

- `skill.toml`: contrato mecanico con `id`, `module`, `access` y `entrypoint`;
  las skills de mutacion agregan `mutation_kind`.
- `SKILL.md`: instrucciones para la IA, entradas, salidas, modelos y riesgos.

Los valores de `access` son:

- `read_only`: solo lee datos y genera analisis o archivos.
- `mutation` + `mutation_kind = "draft"`: deja un documento editable y sigue
  `ODOO_DRAFT_WORKFLOW`.
- `mutation` + `mutation_kind = "destructive"`: cambia estados o datos con
  consecuencias permanentes; siempre requiere preview y confirmacion.

El catalogo de la CLI solo descubre manifests versionados. Los scripts de
`scripts/temporary` no se consideran skills automaticamente.
