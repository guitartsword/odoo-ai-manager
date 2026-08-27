# Modulos

Cada modulo representa un area de negocio y contiene dos documentos:

- `business.md`: vocabulario, indicadores y reglas que debe entender la IA.
- `technical.md`: modelos Odoo, campos, estados, permisos y detalles de las
  skills.

Los documentos se mantienen separados para poder cargar solo el contexto
necesario. La separacion no crea permisos de GitHub por si misma; consulta
`docs/access-control.md`.
