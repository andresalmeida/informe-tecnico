# Contrato del motor de referencia

Cada tipo lee la raíz, las secciones y el bloque que usa. La raíz reúne la marca, el documento, el formato, los cambios, la ejecución del motor y el resumen del ciclo de vida.

Desde aquí se abre solo el apartado que el tipo necesita.

- [Raíz](contrato/raiz.md)
- [Secciones y bloques](contrato/secciones.md)
- [Bloque fields](contrato/fields.md)
- [Bloque risks](contrato/risks.md)
- [Bloque quote](contrato/quote.md)
- [Bloque requirements](contrato/requirements.md)
- [Bloque impact](contrato/impact.md)
- [Bloque wbs](contrato/wbs.md)
- [Bloque testcase](contrato/testcase.md)

## Alcance real

El motor implementa A4/Carta en vertical, portada, control de cambios, contenido, índices condicionales, encabezado/pie, marcadores y tablas simples con filas no divisibles. No implementa DOCX, numeración romana, tablas anidadas, fórmulas escritas por el usuario (los bloques `quote`, `risks`, `requirements`, `impact` y `wbs` calculan sus propios totales y niveles), mezcla de orientaciones, firmas electrónicas, control de acceso ni PDF/UA. Las cabeceras y pies demasiado largos fallan con mensaje en vez de solaparse. Para un documento con otras necesidades elegir un motor apropiado manteniendo los mismos invariantes.

El manifiesto añade `format` con medidas efectivas. El perfil `institucional-apa` no modifica los márgenes, la portada, la cabecera, los índices ni la numeración técnica; no equivale a un documento académico APA integral. El comprobador estructural no valida la exactitud bibliográfica. El perfil `institucional` conserva sus medidas y la posición tradicional de pies de figura; una fuente sin `format` usa `institucional-apa`.
