# MF7011 · Formulación y Evaluación de Proyectos Sostenibles — reglas del repo

Repositorio **público** (GitHub Pages publica `_site/` desde `main`). Leer esto antes de escribir cualquier archivo.

## 1. Material del profesor: se produce SIEMPRE en `instructor/pdf/SN/`

- Todo lo que el profesor lleva al salón (slides impresos, notas por slide, plan de sesión, guías) sale de **un solo comando**:

  ```bash
  python3 recursos/exportar-profesor.py 3          # sesión 3 → instructor/pdf/S3/
  python3 recursos/exportar-profesor.py 3 --abrir  # y abre la carpeta
  ```

- **Destino fijo: `instructor/pdf/SN/` dentro del repo.** Nunca `~/Downloads`, nunca un directorio temporal como destino final: Downloads se vacía; el repo se queda.
- `instructor/` está en `.gitignore` (contiene reveals, respuestas preparadas y errores plantados). Existe solo en este Mac y en el respaldo privado. **Nunca `git add` nada de `instructor/`.**
- Si el profesor pide "las slides", "las notas", "el paquete", "lo de mañana": correr el script y señalar la carpeta. No inventar otro pipeline.

### Fuentes de las notas del profesor (dos capas)

| Capa | Dónde | Para qué | Público |
|---|---|---|---|
| `::: {.notes}` en `slides/s0N/*.qmd` | el deck | mecánica breve (MIN x–y, qué observar) | el `.qmd` está en GitHub; el sitio las elimina |
| `instructor/notas-slides/sN-<deck>.md` | guion extendido | qué decir, números, trampas, referencias a la guía | privado |
| `instructor/notas-slides/sN-glosario.md` | tabla de 4 columnas | primeras páginas de los PDF de notas | privado |

Reveals y respuestas preparadas van al `.md` del instructor, **no** al `.qmd`.
Formato del `.md`: una sección `## <título exacto de la slide>` por slide (slides sin título: su primera línea de texto; la de título de Quarto: `Portada`), `### Etiqueta` para agrupar, `{min="18:00 – 18:15"}` opcional. El script avisa de secciones huérfanas (título renombrado) y de slides que no caben en pantalla.

## 2. Flujo estándar antes de una sesión

1. Editar `slides/s0N/*.qmd` y `instructor/notas-slides/sN-*.md` (+ `instructor/planes-sesion/sN.md`, guías `instructor/*-sN.md`).
2. `python3 recursos/exportar-profesor.py N` → leer los avisos → abrir `instructor/pdf/SN/`.
3. Imprimir `SN_<Deck>_Notas_por_slide.pdf` (A4 horizontal).
4. Commit + push **solo de lo público**. GitHub Actions renderiza con `--profile publico` (sin notas) y falla si alguna se filtra.

## 3. Renders

- `quarto render` (sin perfil) = con notas, para clase. `quarto render --profile publico` = lo que ve el estudiante.
- El script renderiza siempre sin perfil y se detiene si el HTML no trae notas.

## 4. Otras reglas

- `semestres/` tiene datos reales de estudiantes (Ley 1581/2012): nunca versionar ni copiar fuera del repo.
- Lecturas con copyright de terceros: solo a Interactiva (D2L) vía `LECTURAS` en `interactiva/datos.py`; nunca dentro del zip de importación.
- Las cifras de las slides salen de `datos/analisis_*.py`; si cambia un supuesto se re-corre el script y se sincronizan las slides.
- El profesor no es experto en finanzas corporativas: cada término técnico (WACC, CapEx, escudo fiscal…) va con definición breve y fórmula.
