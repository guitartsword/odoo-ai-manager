# Tecnica de contabilidad

## Modelos habituales

- `account.move`: facturas, notas y asientos.
- `account.move.line`: lineas contables.
- `account.payment`: pagos.
- `account.account`: cuentas.
- `account.journal`: diarios.

Las skills deben filtrar compania y estados explicitamente. Crear un
`account.move` en borrador puede ser `mutation_kind = "draft"` y seguir
`ODOO_DRAFT_WORKFLOW`; publicar, conciliar, registrar pagos o crear asientos
requiere `mutation_kind = "destructive"` y confirmacion explicita.
