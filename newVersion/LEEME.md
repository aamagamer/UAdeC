# Rediseño del sitio · Dirección de Planeación / Portal SIE — UAdeC

Versión: noviembre 2026 · Tecnologías: HTML, CSS y JavaScript puros.

---

## 1. ¿Qué hay en esta carpeta?

```
newVersion/
├── sitio/                    ← ESTO es lo que se sube al servidor
│   ├── index.html            Inicio (Dirección de Planeación)
│   ├── sie.html              ¿Qué es el SIE?
│   ├── numeralia.html        Numeralia por ciclo (5 ciclos, con pestañas)
│   ├── indicadores.html      Aspirantes y planta docente
│   ├── documentos.html       Cuadernillos e informes del Rector
│   ├── auditorias.html       Auditorías de matrícula 911
│   ├── cubos.html            Modelos OLAP
│   ├── somos-uadec.html      Coahuila y la UAdeC
│   ├── contacto.html         Formulario + datos de contacto
│   ├── aviso-de-privacidad.html  Aviso de privacidad + política de cookies
│   ├── 404.html              Página de error personalizada
│   ├── .htaccess             Seguridad, caché, GZIP, redirecciones (Apache)
│   ├── web.config            Lo mismo para servidores Windows/IIS
│   ├── robots.txt · sitemap.xml · site.webmanifest · favicon.ico
│   ├── assets/css · assets/js · assets/fonts · assets/img
│   └── docs/                 PDFs (auditorías, cuadernillos, informes)
├── fuente/                   Código legible para editar (NO se sube)
│   ├── build.py              Generador de todas las páginas
│   ├── sizes.json            Medidas de las imágenes
│   ├── css/main.css          CSS sin minificar
│   └── js/main.js · boot.js  JS sin minificar
├── nginx.conf.ejemplo        Configuración equivalente para Nginx
├── INFORME-SEGURIDAD.md      Problemas encontrados en el sitio anterior y cómo se resolvieron
└── LEEME.md                  Este archivo
```

## 2. Cómo publicarlo

1. Haz un respaldo del sitio actual del servidor.
2. **Elimina del servidor la carpeta `contacto/`** del sitio anterior (contiene PHPMailer 5.2.16, con una vulnerabilidad crítica; ver `INFORME-SEGURIDAD.md`). También conviene borrar `bootstrap/`, `js/`, `menu/`, `fonts/`, `css/`, `images/` y los `.html` viejos.
3. Sube **el contenido** de `sitio/` (no la carpeta en sí) a la raíz pública del dominio, incluidos los archivos ocultos `.htaccess` (en FileZilla: *Servidor → Forzar mostrar archivos ocultos*).
4. Abre el sitio y verifica:
   - Que cargue el inicio y el menú.
   - Que `https://TU-DOMINIO/una-pagina-que-no-existe` muestre la página 404 personalizada.
   - Que las URLs viejas redirijan (por ejemplo `somosuadec.html` → `somos-uadec.html`, `pdf/aud_20151_gral.pdf` → `docs/aud_20151_gral.pdf`).
   - Los encabezados de seguridad en <https://securityheaders.com> (debe salir **A** o **A+** con HTTPS).

### Si el sitio vive en una subcarpeta (ej. `uadec.mx/planeacion/`)
La página 404 usa rutas absolutas (`/assets/...`) porque se muestra en cualquier URL. En ese caso:
- En `.htaccess` cambia `ErrorDocument 404 /404.html` por `ErrorDocument 404 /planeacion/404.html`.
- En `404.html` reemplaza `"/assets/` por `"/planeacion/assets/` y `"/index.html` por `"/planeacion/index.html` (y lo mismo para los otros enlaces).
- Las redirecciones del `.htaccess` también llevan `/` al inicio: agrega `/planeacion`.

## 3. Pendientes antes de publicar (importante)

| # | Qué revisar | Dónde |
|---|---|---|
| 1 | **Dominio real.** Puse `https://planeacion.uadec.mx` como dominio provisional en la URL canónica, las etiquetas para redes sociales, el `sitemap.xml` y el `robots.txt`. Reemplázalo por el dominio real con *Buscar y reemplazar* en todos los archivos de `sitio/`, o cambia `SITE_URL` en `fuente/build.py` y vuelve a generar. | todos los `.html`, `sitemap.xml`, `robots.txt` |
| 2 | **Aviso de privacidad.** Es una propuesta basada en la LGPDPPSO (DOF 20-03-2025) y la ley de datos personales de Coahuila. **Debe validarlo la Unidad de Transparencia o el área jurídica de la UAdeC** antes de publicarse. | `aviso-de-privacidad.html` |
| 3 | **Correo que recibe el formulario:** `planeacion@uadec.edu.mx`. Si debe ser otro (el sitio anterior enviaba a una cuenta personal del SIE), cámbialo en `CONFIG.contactEmail` de `assets/js/main.js` y en `CONTACT` de `fuente/build.py`. | `main.js` |
| 4 | **Cifras del inicio** (41,534 estudiantes del ciclo 2025-2, 60+ escuelas, 3 unidades, 65+ años): las tomé del borrador `plane_2026-ultimo.html`. Confírmalas. | `index.html` |
| 5 | **Acceso a los modelos (Cognos):** el enlace `http://dwhouse.uadec.mx/cognos` no es seguro (HTTP). Pidan al área de TI habilitar HTTPS en ese servidor. | `cubos.html` |
| 6 | **Activar HTTPS** cuando el servidor tenga certificado: descomenta las 2 líneas de "Forzar HTTPS" en `.htaccess` (HSTS se activa solo). | `.htaccess` |

### Inconsistencias encontradas en los datos originales (ya corregidas o señaladas)
- **Ago–Dic 2015, bachillerato:** la imagen de la tabla decía 10,584, pero la suma por unidad y el texto del ciclo dan **11,230**. Se usó 11,230.
- **Ago–Dic 2016, posgrado:** el texto decía 1,494, pero la tabla por unidad suma **1,841** y el total de 36,084 cuadra con 1,841. Se usó 1,841 y se dejó una nota.
- **Ene–Jun 2015, profesores de tiempo completo:** el texto decía 1,099, pero la gráfica y la suma (3,077 − 2,068) dan **1,009**. Se usó 1,009.
- **Ene–Jun 2017:** el texto decía "829 PTC del nivel *medio superior*", pero la gráfica indica que son de nivel **superior**. Se corrigió.
- **Ene–Jun 2015, becas:** el total publicado es 2,243, pero los 5 tipos suman 2,217. Se dejaron ambos como estaban; conviene confirmarlo.
- Se corrigieron erratas: "Fonteriza", "Sierra Moajada", "Franciso I.", "Eduación", "MOVILIDIAD".

## 4. Cómo editar el contenido

**Opción A — cambios pequeños:** edita directamente el `.html` en `sitio/`. Respeta una regla de seguridad: **no uses `style="..."` ni `<script>` dentro del HTML**, porque la política de seguridad (CSP) los bloquea a propósito. Los estilos van en `assets/css/main.css` y el código en `assets/js/main.js`.

**Opción B — recomendada (por ejemplo, para agregar un ciclo nuevo a la numeralia):**
1. Edita `fuente/build.py`. Los ciclos están en la lista `CYCLES`: copia un bloque, cambia las cifras y ponlo al inicio para que sea la pestaña por defecto.
2. Genera de nuevo:
   ```bash
   cd fuente
   OUT=../sitio python3 build.py
   ```
3. Si cambiaste el CSS o el JS en `fuente/`, minifícalos (necesitas Node.js):
   ```bash
   npx csso-cli css/main.css -o ../sitio/assets/css/main.css
   npx terser js/main.js -c -m --comments false -o ../sitio/assets/js/main.js
   ```
   Si no tienes Node, puedes copiar el archivo sin minificar; funciona igual, solo pesa un poco más.
4. Cambia `VER` en `build.py` (por ejemplo a la fecha de hoy) para que los navegadores descarguen el CSS/JS nuevo.

**Imágenes nuevas:** súbelas en formato **WebP**, con un ancho máximo de 1600 px. Puedes convertirlas gratis en <https://squoosh.app> (calidad 75–80).

## 5. Qué incluye el rediseño

- **Diseño** basado en el borrador de la Dirección de Planeación (azul institucional #062a7a + oro #f4b400, tipografía Poppins) y aplicado a todo el Portal SIE.
- **Animaciones:** entrada del hero, aparición al hacer scroll, contadores animados, barras de datos animadas, efectos al pasar el cursor sobre tarjetas y botones, menú y visor de imágenes. Respetan la opción del sistema *reducir movimiento*.
- **Velocidad:**
  - El inicio pasó de unos **1.7 MB y 46 peticiones** a unos **400 KB y 14 peticiones**.
  - CSS de 7 KB y JS de 3.5 KB comprimidos con GZIP.
  - Imágenes en WebP con tamaños responsivos y carga diferida. En total pasaron de ~30 MB a ~2 MB.
  - Fuentes alojadas en el propio sitio y caché de un año.
  - Lighthouse (móvil, servidor sin compresión): **Rendimiento 96–98 · Accesibilidad 100 · Buenas prácticas 100 · SEO 100**.
- **Datos reales en HTML:** las tablas de matrícula y aspirantes antes eran imágenes JPG. Ahora son tablas que se pueden leer, copiar e indexar en buscadores, con barras de datos hechas en CSS. Las gráficas originales se conservaron en una galería con visor ampliable.
- **SEO:** título y descripción únicos en cada página, URL canónica, Open Graph/Twitter, datos estructurados (Schema.org), `sitemap.xml`, `robots.txt`, redirecciones 301 desde las URLs anteriores y manifiesto web.
- **Accesibilidad:** HTML semántico, enlace "Saltar al contenido", navegación completa con teclado (menú, pestañas con flechas, Esc), textos alternativos, contraste suficiente, estilos para impresión.
- **Privacidad:** banner de cookies honesto (el sitio no usa cookies de rastreo), panel de preferencias, aviso de privacidad, y ninguna conexión a Google, Facebook ni otros terceros al cargar la página.
- **Página 404** personalizada con enlaces útiles.

## 6. Si en el futuro quieren estadísticas de visitas

El banner ya está preparado. En `assets/js/main.js` hay un evento `consent:updated`. Carga el script de analítica **solo** cuando `detail.analytics === true` y agrega su dominio a la directiva CSP (`script-src` y `connect-src`) en `.htaccess` y en la etiqueta `<meta http-equiv="Content-Security-Policy">` de las páginas. Actualiza la tabla de cookies del aviso de privacidad. Recomendación: una herramienta sin cookies, como Plausible o GoatCounter.

## 7. Créditos y licencias

- Íconos: [Lucide](https://lucide.dev) (licencia ISC), en `assets/img/LICENSE-lucide.txt`.
- Tipografía: Poppins (SIL Open Font License), en `assets/fonts/LICENSE-OFL.txt`.
- Contenido, logotipos e imágenes: Universidad Autónoma de Coahuila.
