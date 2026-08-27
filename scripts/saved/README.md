# Scripts guardados

Esta carpeta contiene scripts reutilizables y revisados. Se organizan por
modulo y permiso:

```text
scripts/saved/<modulo>/read_only/
```

El modo debe coincidir con el `access` del manifest de la skill. Un script de
mutacion nunca debe aceptar cambios silenciosamente.
