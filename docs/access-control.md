# Acceso y comparticion

## Lo que si resuelve este repositorio

- Cada modulo tiene conocimiento de negocio y tecnica separado.
- Cada skill declara `read_only` o `mutation`.
- Los scripts persistentes se separan por modulo y permiso.
- El agente puede cargar solo el contexto de un modulo.
- GitHub Actions y revisiones pueden proteger cambios.

## Lo que no resuelve una carpeta

GitHub no aplica permisos de lectura por carpeta dentro de un repositorio. Al
ser publico, cualquier persona puede leer todos los modulos. `CODEOWNERS`,
branches protegidas y revisiones controlan cambios, no lectura.

Si un empleado debe ver solo inventario, usa repositorios separados, por
ejemplo `odoo-ai-manager-core` y `odoo-ai-manager-inventory`, o repositorios
privados por modulo. Asigna equipos de GitHub con permisos apropiados y
configura tambien un usuario de Odoo con los grupos minimos.

Nunca uses la estructura del repositorio como sustituto de permisos de Odoo.
