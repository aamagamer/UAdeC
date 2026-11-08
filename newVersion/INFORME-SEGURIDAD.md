# Informe de seguridad · Sitio anterior del Portal SIE vs. rediseño

Fecha de revisión: 7 de noviembre de 2026. Revisé los archivos de la carpeta `SIE/` que entregaron (no hice pruebas contra el servidor en producción).

## Resumen

| Severidad | Hallazgo en el sitio anterior | Estado en el rediseño |
|---|---|---|
| 🔴 Crítica | `contacto/class.phpmailer.php` es **PHPMailer 5.2.16**, versión con vulnerabilidades públicas de ejecución remota de código (CVE-2016-10033 y CVE-2016-10045, corregidas en 5.2.18 y 5.2.20). | Eliminado. El sitio nuevo no usa PHP y el `.htaccess` **bloquea la ejecución de cualquier `.php`**. |
| 🔴 Alta | `contacto/contact.php` usa el correo que escribe el visitante como remitente (`$mail->From = $email`), sin validar ni limpiar nada, sin límite de envíos ni protección anti-bots. Esto permite falsificar remitentes y abusar del servidor de correo institucional (`mailgate2.uadec.mx`) para enviar spam. También muestra errores internos (`ErrorInfo`). | Reemplazado por un formulario que valida en el navegador y abre la aplicación de correo de quien escribe. **No hay nada en el servidor que se pueda abusar.** |
| 🟠 Alta | Librerías JavaScript obsoletas con vulnerabilidades XSS conocidas: jQuery 1.8.3, jQuery 1.10.1, `jquery-latest.js`, jQuery UI 1.10.3, Bootstrap 3 y otros plugins. | Eliminadas. Todo el código es JavaScript propio de unos 9 KB, sin dependencias. |
| 🟠 Media | Se cargaban scripts y estilos de terceros **por HTTP sin cifrar** (`http://code.jquery.com/jquery-latest.js`, `http://meyerweb.com/...reset.css`). Alguien en la misma red podría inyectar código. | No se carga nada externo. CSP: `script-src 'self'`. |
| 🟠 Media | Sin encabezados de seguridad (CSP, X-Frame-Options, nosniff, HSTS, etc.). El sitio podía mostrarse dentro de un `iframe` ajeno (*clickjacking*). | Se agregaron todos en `.htaccess` y `web.config`, y un CSP de respaldo en cada página. |
| 🟡 Media | El acceso a los modelos Cognos (`http://dwhouse.uadec.mx/cognos`) es **HTTP**: las credenciales viajan sin cifrar. | Fuera del alcance de este sitio. **Recomendación: que TI habilite HTTPS en ese servidor.** |
| 🟡 Baja | Archivos `.DS_Store` (revelan la estructura de carpetas) y archivos de demostración de plantillas (`menu/demo.html`, `images/thumbs/`). | No se incluyen. El `.htaccess` bloquea archivos ocultos y de respaldo (`.bak`, `.sql`, `.env`, `.log`, etc.). |
| 🟡 Baja | Se publicaba un correo personal (no institucional) del personal del SIE, lo que atrae spam. | Se usa el correo institucional del área. |
| 🟡 Baja | Posible listado de directorios (sin `index.html` en `pdf/`, `images/`, etc.). | `Options -Indexes`. |

## Medidas incluidas en el rediseño

**Encabezados HTTP** (`.htaccess` / `web.config`):
- `Content-Security-Policy` estricta: solo recursos del propio dominio, sin scripts ni estilos en línea, sin `eval`, `frame-ancestors 'none'`, `object-src 'none'`, `base-uri 'self'` y `form-action 'self' mailto:`.
- `Strict-Transport-Security` (solo con HTTPS), `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy`, `Permissions-Policy` (cámara, micrófono, geolocalización y otros apagados), `Cross-Origin-Opener-Policy`, `Cross-Origin-Resource-Policy`.
- Se ocultan `X-Powered-By` y la firma del servidor.

**Superficie de ataque mínima:**
- Sitio 100 % estático: sin PHP, sin base de datos y sin panel de administración que vulnerar.
- Solo se permiten los métodos `GET` y `HEAD`.
- Se bloquean extensiones ejecutables (`.php`, `.phtml`, `.cgi`, `.asp`, `.jsp`, `.pl`, `.phar`), archivos ocultos y respaldos.
- Límite de 100 KB por petición.
- Sin listado de directorios.

**Código seguro:**
- El JavaScript nunca usa `innerHTML`, `eval` ni manejadores en línea. Los datos del formulario se limpian de caracteres de control y se codifican con `encodeURIComponent`.
- Validación de formato y longitud en todos los campos, más un campo trampa anti-bots.
- Los enlaces externos llevan `rel="noopener noreferrer"`.

**Privacidad:** no hay cookies de terceros, ni rastreadores, ni fuentes de Google, ni mapas incrustados. El mapa estático de Google del borrador anterior se quitó: además de no funcionar sin una clave de API, enviaba datos de cada visitante a Google.

## Recomendaciones para el servidor

1. **Instalar un certificado SSL** (Let's Encrypt es gratuito) y activar la redirección a HTTPS del `.htaccess`.
2. **Borrar del servidor la carpeta `contacto/`** y todos los archivos del sitio anterior. No basta con no enlazarlos: si siguen en el servidor, se pueden atacar.
3. En la configuración principal de Apache (no se puede desde `.htaccess`), poner `ServerTokens Prod` y `ServerSignature Off` para no revelar la versión del servidor.
4. Mantener actualizados Apache/IIS y el sistema operativo, y usar SFTP en lugar de FTP para subir archivos.
5. Hacer respaldos periódicos del sitio.
6. Verificar el resultado en <https://securityheaders.com> y en <https://observatory.mozilla.org>.
