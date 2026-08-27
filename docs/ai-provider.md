# Proveedor de IA

## Recomendacion

Mantener el proveedor de lenguaje separado de las skills y del cliente Odoo.
Una capa de IA debe recibir contexto, catalogo de skills y herramientas
permitidas; no debe tener acceso generico a `execute_kw`.

El primer MVP puede usar el proveedor que ya tenga la organizacion. OpenAI,
Anthropic, modelos locales u otro servicio deben implementar el mismo contrato
interno de conversacion. La API key debe vivir en un gestor de secretos o en
`.env` local, nunca en `knowledge` ni en una skill.

## Flujo recomendado

1. La interfaz recibe una pregunta en lenguaje natural.
2. Un clasificador identifica modulo, skill y parametros faltantes.
3. El agente carga solo `knowledge` y documentos del modulo necesarios.
4. La skill devuelve datos estructurados.
5. El agente explica el resultado y conserva evidencia de filtros y fuente.

Para una mutacion, el agente debe detenerse antes de ejecutar, presentar un
preview y esperar una confirmacion independiente. El proveedor de IA no debe
ser quien otorgue permisos.

## Interfaz para empleados

La experiencia final recomendada es una pequena aplicacion web autenticada,
con selector de compania, periodo y modulo, historial de conversaciones y
descarga de archivos. El CLI incluido sirve para desarrollo y automatizacion,
no como interfaz definitiva para usuarios no tecnicos.

## Privacidad

Envia al modelo solo los registros y campos necesarios. Para preguntas
agregadas, calcula en Odoo o en el adaptador y entrega totales en vez de
clientes, direcciones o notas completas. Define retencion, auditoria y acceso
antes de conectar datos de produccion.
