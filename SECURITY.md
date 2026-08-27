# Seguridad

No publiques credenciales, API keys, bases de datos, dumps, fotos privadas ni
reportes de produccion. Reporta vulnerabilidades sin incluir secretos en un
issue publico.

El repositorio separa lectura y mutacion para facilitar revisiones, pero los
permisos efectivos deben estar en Odoo y, para modulos sensibles, en
repositorios privados separados. Usa usuarios de integracion dedicados,
HTTPS, API keys rotables y privilegios minimos.
