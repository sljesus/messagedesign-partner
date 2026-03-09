# Configuración DNS - sstmexico.com

## Resumen Ejecutivo

**Fecha:** Marzo 2026
**Dominio:** sstmexico.com
**Proveedor DNS:** Cloudflare
**Proveedor Hosting:** HostGator (IP: 162.241.60.214)
**Correo:** Titan (dominio principal) + Mailgun (subdominio md)

---

## Comparativa ANTES ↔ DESPUÉS

| Tipo | Nombre | Contenido (ANTES) | Contenido (DESPUÉS) | Estado / Acción |
|------|--------|-------------------|---------------------|-----------------|
| A | localhost | 127.0.0.1 | ❌ Eliminado | Obsoleto (loopback) |
| A | autoconfig | 162.241.60.214 (Proxied) | 162.241.60.214 (DNS only) | Cambiado a DNS only |
| A | autodiscover | 162.241.60.214 (Proxied) | 162.241.60.214 (DNS only) | Cambiado a DNS only |
| A | cpcalendars | 162.241.60.214 (Proxied) | 162.241.60.214 (DNS only) | Cambiado a DNS only |
| A | cpcontacts | 162.241.60.214 (Proxied) | 162.241.60.214 (DNS only) | Cambiado a DNS only |
| A | mail | 162.241.60.214 (Proxied) | 162.241.60.214 (DNS only) | Cambiado a DNS only |
| A | sstmexico.com | 162.241.60.214 (Proxied) | 162.241.60.214 (Proxied) | Se mantiene (web principal) |
| A | webdisk | 162.241.60.214 (Proxied) | 162.241.60.214 (DNS only) | Cambiado a DNS only |
| A | whm | 162.241.60.214 (Proxied) | 162.241.60.214 (DNS only) | Cambiado a DNS only |
| CNAME | cpanel | sstmexico.com (Proxied) | sstmexico.com (DNS only) | Cambiado a DNS only |
| CNAME | email.md | mailgun.org (DNS only) | mailgun.org (DNS only) | Se mantiene |
| CNAME | ftp | sstmexico.com (Proxied) | sstmexico.com (DNS only) | Cambiado a DNS only |
| CNAME | md | sites.ludicrous.cloud (DNS only) | sites.ludicrous.cloud (DNS only) | Se mantiene |
| CNAME | webmail | sstmexico.com (Proxied) | sstmexico.com (DNS only) | Cambiado a DNS only |
| CNAME | www | sstmexico.com (Proxied) | sstmexico.com (Proxied) | Se mantiene (web) |
| MX | md | mxb.mailgun.org (10) | mxb.mailgun.org (10) | Se mantiene |
| MX | md | mxa.mailgun.org (10) | mxa.mailgun.org (10) | Se mantiene |
| MX | sstmexico.com | mx1.titan.email (10) | mx1.titan.email (10) | Se mantiene |
| MX | sstmexico.com | mx2.titan.email (20) | mx2.titan.email (20) | Se mantiene |
| SRV | _autodiscover._tcp | 0 0 443 cpanelemaildiscovery.cpanel.net | ❌ Eliminado | No se usa Outlook |
| SRV | _caldavs._tcp | 0 0 2080 mx84.hostgator.mx | ❌ Eliminado | Calendarios obsoletos |
| SRV | _caldav._tcp | 0 0 2079 mx84.hostgator.mx | ❌ Eliminado | Calendarios obsoletos |
| SRV | _carddavs._tcp | 0 0 2080 mx84.hostgator.mx | ❌ Eliminado | Contactos obsoletos |
| SRV | _carddav._tcp | 0 0 2079 mx84.hostgator.mx | ❌ Eliminado | Contactos obsoletos |
| TXT | _acme-challenge | "aD8yiSxK0DeivEhEj7gAhTGOPqPOvwlwYLTi4lJ-QaQ" | ❌ Eliminado | Temporal de Let's Encrypt |
| TXT | _caldavs._tcp | "path=/" | ❌ Eliminado | Asociado a SRV eliminado |
| TXT | _caldav._tcp | "path=/" | ❌ Eliminado | Asociado a SRV eliminado |
| TXT | _carddavs._tcp | "path=/" | ❌ Eliminado | Asociado a SRV eliminado |
| TXT | _carddav._tcp | "path=/" | ❌ Eliminado | Asociado a SRV eliminado |
| TXT | _cpanel-dcv-test-record | "_cpanel-dcv-test-record=obYMS7tpk7sk2j3FbeG0ZwihgOnluFInVGQkMuT5kw01LEl6TgknIIkadUtTWvi0" | ❌ Eliminado | Validación temporal de cPanel |
| TXT | default._domainkey | DKIM largo del hosting | ❌ Eliminado | DKIM antiguo (no usado) |
| TXT | _dmarc.md | "v=DMARC1;p=none;" | "v=DMARC1;p=none;" | Se mantiene |
| TXT | _dmarc | "v=DMARC1; p=quarantine; rua=mailto:contacto@sstmexico.com; ruf=mailto:contacto@sstmexico.com; sp=quarantine; pct=100" | "v=DMARC1; p=quarantine; rua=mailto:contacto@sstmexico.com; ruf=mailto:contacto@sstmexico.com; sp=quarantine; pct=100" | Se mantiene |
| TXT | md | "v=spf1 include:mailgun.org include:spf.leadconnectorhq.com ~all" | "v=spf1 include:mailgun.org include:spf.leadconnectorhq.com ~all" | Se mantiene |
| TXT | mx._domainkey.md | DKIM de Mailgun | DKIM de Mailgun | Se mantiene |
| TXT | smtp._domainkey | DKIM del hosting | ❌ Eliminado | DKIM antiguo (no usado) |
| TXT | sstmexico.com | "v=spf1 include:spf.titan.email ~all" | "v=spf1 include:spf.titan.email ~all" | Se mantiene |
| TXT | titan4._domainkey | DKIM de Titan | DKIM de Titan | Se mantiene |

---

## Resumen Numérico de Cambios

| Concepto | ANTES | DESPUÉS |
|----------|-------|---------|
| Total registros | 38 | 24 |
| Registros eliminados | - | 14 |
| Registros cambiados a DNS only | - | 11 |
| Registros mantenidos sin cambios | - | 13 |

---

## Acciones Clave Realizadas

### 1. Eliminación de Registros Obsoletos

- **localhost (A)** - Loopback innecesario
- **_acme-challenge (TXT)** - Temporal de Let's Encrypt
- **_cpanel-dcv-test-record (TXT)** - Validación temporal de cPanel
- **Todos los SRV y TXT de CalDAV/CardDAV** (8 registros) - Calendarios/contactos obsoletos
- **_autodiscover._tcp (SRV)** - No se usa Outlook
- **default._domainkey y smtp._domainkey (DKIM)** - DKIM antiguo del hosting (HostGator)

### 2. Corrección de Proxy en Servicios No Web

Se cambiaron de **Proxied** a **DNS only:**

| Tipo | Nombre |
|------|--------|
| A | autoconfig |
| A | autodiscover |
| A | cpcalendars |
| A | cpcontacts |
| A | mail |
| A | webdisk |
| A | whm |
| CNAME | cpanel |
| CNAME | ftp |
| CNAME | webmail |

### 3. Mantenimiento de Proxy en Servicios Web

- **sstmexico.com** (raíz) - Proxied
- **www** - Proxied

### 4. Conservación de Registros de Correo

- MX de Titan (sstmexico.com)
- MX de Mailgun (md)
- SPF, DKIM y DMARC

---

## Estado Final - Registros Actuales

### A Records
| Nombre | IP | Proxy |
|--------|-----|-------|
| autoconfig | 162.241.60.214 | DNS only |
| autodiscover | 162.241.60.214 | DNS only |
| cpcalendars | 162.241.60.214 | DNS only |
| cpcontacts | 162.241.60.214 | DNS only |
| mail | 162.241.60.214 | DNS only |
| sstmexico.com | 162.241.60.214 | Proxied |
| webdisk | 162.241.60.214 | DNS only |
| whm | 162.241.60.214 | DNS only |

### CNAME Records
| Nombre | Valor | Proxy |
|--------|-------|-------|
| cpanel | sstmexico.com | DNS only |
| email.md | mailgun.org | DNS only |
| ftp | sstmexico.com | DNS only |
| md | sites.ludicrous.cloud | DNS only |
| webmail | sstmexico.com | DNS only |
| www | sstmexico.com | Proxied |

### MX Records
| Nombre | Servidor | Prioridad |
|--------|----------|-----------|
| md | mxb.mailgun.org | 10 |
| md | mxa.mailgun.org | 10 |
| sstmexico.com | mx1.titan.email | 10 |
| sstmexico.com | mx2.titan.email | 20 |

### TXT Records
| Nombre | Valor |
|--------|-------|
| _dmarc.md | "v=DMARC1;p=none;" |
| _dmarc | "v=DMARC1; p=quarantine; rua=mailto:contacto@sstmexico.com; ruf=mailto:contacto@sstmexico.com; sp=quarantine; pct=100" |
| md | "v=spf1 include:mailgun.org include:spf.leadconnectorhq.com ~all" |
| mx._domainkey.md | DKIM de Mailgun |
| sstmexico.com | "v=spf1 include:spf.titan.email ~all" |
| titan4._domainkey | DKIM de Titan |

---

## Servicios Configurados

### Correo Electrónico
- **Titan** - Correo principal (@sstmexico.com)
- **Mailgun** - Correo para subdominio md (@md.sstmexico.com)

### Hosting/Servicios
- cPanel: https://cpanel.sstmexico.com:2083
- Webmail: https://webmail.sstmexico.com:2083
- WHM: https://whm.sstmexico.com:2087
- FTP: ftp.sstmexico.com

### Sitio Web
- Principal: https://sstmexico.com (protegido por Cloudflare)
- Subdominio md: https://md.sstmexico.com

---

## Pruebas Recomendadas

### 1. Correo Electrónico
- [ ] Enviar correo desde @sstmexico.com a Gmail/Outlook
- [ ] Verificar que llega a bandeja de entrada (no spam)
- [ ] Revisar cabeceras para firma DKIM
- [ ] Verificar DMARC con MXToolbox

### 2. Acceso a Servicios
- [ ] cPanel: https://cpanel.sstmexico.com:2083
- [ ] Webmail: https://webmail.sstmexico.com:2083
- [ ] WHM: https://whm.sstmexico.com:2087

### 3. Sitio Web
- [ ] https://sstmexico.com carga correctamente
- [ ] https://www.sstmexico.com carga correctamente
- [ ] SSL activo (candado verde)

---

## Notas

- La alerta de Cloudflare sobre "exposición de IP" en registros DNS only es normal y debe ignorarse
- Los servicios internos (cPanel, FTP, correo) necesitan IP real para funcionar
- En el futuro, si se integra Outlook, seguir instrucciones de Titan (generalmente CNAME, no SRV)

---

## Fecha de Actualización

Marzo 2026

---

**Documento preparado por:** SST México
**Para:** Message Design
