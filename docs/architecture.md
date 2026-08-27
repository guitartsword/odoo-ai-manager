# Arquitectura

## Flujo previsto

```text
Pregunta del usuario
        |
Agente de IA + contexto de negocio
        |
Seleccion de modulo y skill
        |
Control de permiso read_only / mutation + tipo de mutacion
        |
Adaptador Odoo versionado
        |
Respuesta, Excel u otra salida
```

## Capas

- `knowledge` y `modules`: memoria explicita del negocio y de la tecnica.
- `skills`: contrato que explica cuando y como usar una capacidad.
- `scripts/saved`: implementaciones reutilizables organizadas por modulo y
  permiso.
- `src/odoo_ai_manager/domain`: modelos y protocolos independientes del
  transporte.
- `src/odoo_ai_manager/infrastructure`: Odoo, XLSX y otros sistemas externos.
- `src/odoo_ai_manager/application`: catalogo y orquestacion de casos de uso.

El agente externo (OpenCode, Codex, Claude Code u otro) aporta la interfaz de
lenguaje y puede crear nuevas herramientas para modelos o extensiones que no
esten en el catalogo. El repositorio aporta el contexto, los contratos, el
cliente Odoo y las pruebas; no intenta contener una implementacion cerrada de
todos los modulos.

## Decisiones de seguridad

La conexion se crea en `read_only` por defecto. El cliente tiene una operacion
separada para mutaciones y exige modo `mutation` mas una allowlist exacta.
Las mutaciones `draft` pueden requerir confirmacion por operacion o crear el
borrador directamente segun `ODOO_DRAFT_WORKFLOW`; las `destructive` siempre
exigen confirmacion explicita. Esto no sustituye los permisos de Odoo: ambos
controles deben existir.

La IA no debe ejecutar SQL directo ni construir metodos de mutacion a partir
de texto libre. Para operaciones relacionadas, preferir un metodo de servidor
de Odoo que haga la transaccion completa.

## Evolucion

1. CLI y skills de consulta, con salidas XLSX.
2. Interfaz de preguntas para usuarios no tecnicos.
3. Registro de auditoria y aprobaciones.
4. Skills de mutacion con previews y permisos separados.
5. Adaptador JSON-2 para versiones que lo requieran.
