# Seguridad

No publiques credenciales, API keys, bases de datos, dumps, fotos privadas ni
reportes de produccion. Reporta vulnerabilidades sin incluir secretos en un
issue publico.

El repositorio separa lectura, borradores y acciones destructivas para facilitar
revisiones, pero los permisos efectivos deben estar en Odoo y, para modulos
sensibles, en repositorios privados separados. `ODOO_DRAFT_WORKFLOW=direct`
solo evita la aprobacion adicional de borradores allowlisted; nunca habilita
acciones destructivas. Usa usuarios de integracion dedicados, HTTPS, API keys
rotables y privilegios minimos.
