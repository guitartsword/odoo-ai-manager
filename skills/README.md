# Skills

Una skill es una capacidad pequena y reusable que la IA puede seleccionar a
partir de una pregunta de negocio.

Cada carpeta `skills/<modulo>/<nombre>/` debe incluir:

- `skill.toml`: contrato mecanico con `id`, `module`, `access` y `entrypoint`.
- `SKILL.md`: instrucciones para la IA, entradas, salidas, modelos y riesgos.

Los valores de `access` son:

- `read_only`: solo lee datos y genera analisis o archivos.
- `mutation`: cambia datos, requiere preview y confirmacion explicita.

El catalogo de la CLI solo descubre manifests versionados. Los scripts de
`scripts/temporary` no se consideran skills automaticamente.
