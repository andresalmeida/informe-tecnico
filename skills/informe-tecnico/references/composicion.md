# Composición institucional

El perfil `institucional` conserva las medidas originales descritas aquí. En `institucional-apa` prevalecen las reglas de párrafo, referencias, títulos y notas de [apa.md](apa.md); la cabecera y el control documental siguen siendo institucionales.

La referencia local aporta una cabecera tabulada de dos filas, título a la izquierda, identidad a la derecha, fecha/versión/página en la segunda fila, línea de pie y tablas densas. Conservar esa gramática sin reproducir el logo ni la autoridad de la entidad original.

- Papel A4 o Carta; márgenes laterales de 21 mm. Encabezado separado del cuerpo; pie con unidad responsable alineada al margen izquierdo y código/estado al derecho, sobre la misma línea base. Contar físicamente desde la portada para evitar ambigüedad entre el visor y «Página X de Y».
- La cabecera usa una única retícula: columnas inferiores de 42 %, 29 % y 29 %; el título superior abarca las dos primeras. El borde izquierdo de entidad/logo coincide exactamente con el de paginación y se dibuja como un separador continuo. Ninguna celda mantiene porcentajes independientes para ese mismo borde. El comprobador inspecciona esta geometría en cada página.
- Fondo blanco, tinta oscura y un acento. Azul sobrio neutral como ejemplo, no obligatorio. La identidad parametriza color, borde, logo, entidad y unidad. `border` controla la intensidad de líneas; `frame` habilita un marco exterior opcional. La cabecera ya aporta estructura sin requerir un marco completo.
- Usar una familia sans legible. En el motor, Helvetica integrada para español occidental; para otros alfabetos integrar TTF compatibles y verificar glifos antes de producir. Cuerpo 10,5 pt/14,5 pt; tablas 9 pt/12 pt; notas 8,5 pt. No comprimir una tabla hasta hacerla ilegible.
- Títulos de 16/12 pt; numeración jerárquica automática hasta tres niveles. No mayúsculas en párrafos enteros. Reservar la tipografía monoespaciada para código, no para fingir tecnicidad.
- Tablas con encabezado contrastado y filas legibles, pocos trazos, ancho ajustado al tipo de dato. Códigos como cadenas; cifras alineadas si ayuda a compararlas. Repetir título y encabezados al continuar. No partir una fila entre páginas en este motor.
- Figura vectorial con título, explicación y fuente. Título de tabla arriba; pie explicativo de figura debajo. Mantener cada figura y su explicación en la misma página.
- No degradados, sombras, iconos decorativos, sellos ficticios, tarjetas tipo dashboard ni portadas de publicidad. Usar espacio para separar funciones, no añadir un adorno a cada sección.
- Estado y significado deben sobrevivir a impresión en gris: escribir «Inactivo», «Eliminado» o «Pendiente» y añadir leyenda cuando sea necesaria. El color es apoyo, no el único portador de información.

Una marca clara puede requerir tinta oscura en el encabezado; el motor calcula contraste del texto de tabla con el acento. Comprobar también el logo a tamaño real y evitar escalarlo de forma no proporcional.

Los procedimientos opcionales mantienen el cuerpo e interlineado del perfil: acciones numeradas con sangría colgante y resultado esperado debajo, sin marcas de aprobación. Su título se conserva con el contenido siguiente; los pasos pasan completos a la página siguiente cuando caben. Los avisos llevan borde fino oscuro, rótulo explícito y fondo blanco; su significado no depende del color. Un aviso dentro de un paso precede a la acción. Estos bloques no alteran la cabecera, los estilos de tablas/figuras ni el formato de los documentos que no los usan.
