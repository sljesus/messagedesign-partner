
# SOP — Configuración de Correo Titan con Cloudflare
**Empresa:** SST México  
**Tipo de documento:** Procedimiento Operativo Estándar (SOP)  
**Versión:** 1.0  
**Objetivo:** Garantizar la correcta configuración del correo Titan cuando el dominio utiliza Cloudflare como proveedor DNS.

---

# 1. Propósito
Establecer un procedimiento claro para configurar correctamente los registros de autenticación de correo (MX, SPF, DKIM y DMARC) al utilizar **Titan Email con DNS administrado en Cloudflare**, evitando problemas de envío, recepción o reputación del dominio.

---

# 2. Alcance
Este procedimiento aplica cuando:

- El dominio usa **Cloudflare como DNS**
- El servicio de correo es **Titan Email**
- El dominio fue migrado desde **HostGator u otro hosting**
- Se requiere asegurar autenticación de correo para:
  - correo empresarial
  - automatizaciones
  - aplicaciones externas

---

# 3. Requisitos previos

Antes de iniciar verificar:

- Acceso a **Cloudflare**
- Acceso al **portal de cliente HostGator**
- Acceso a **administración de Titan**
- Dominio activo

---

# 4. Arquitectura recomendada de correo

| Servicio | Uso |
|--------|--------|
Titan | correo empresarial |
Mailgun | envíos automáticos |
GoHighLevel | automatización CRM |

Separar correos **humanos** y **automatizados** protege la reputación del dominio.

---

# 5. Registros DNS necesarios

## MX (Recepción de correos)

| Tipo | Host | Valor | Prioridad |
|----|----|----|----|
MX | @ | mx1.titan.email | 10 |
MX | @ | mx2.titan.email | 20 |

---

## SPF (Autorización de envío)

Ejemplo recomendado:

v=spf1 include:spf.titan.email include:mailgun.org include:spf.leadconnectorhq.com ~all

Esto autoriza:

- Titan
- Mailgun
- GoHighLevel

---

## DKIM (Firma criptográfica)

El DKIM debe generarse desde Titan.

Ruta:

HostGator Portal → Correos → Administrar correos → Reputación del correo

Luego:

Añadir registro DKIM

Titan generará algo como:

Host:
titan4._domainkey

Valor:
v=DKIM1; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...

---

# 6. Crear DKIM en Cloudflare

Ruta:

Cloudflare → DNS → Add Record

Configuración:

Tipo: TXT  
Nombre: titan4._domainkey  
Contenido: valor DKIM proporcionado por Titan  
TTL: Auto  
Proxy: DNS Only (nube gris)

IMPORTANTE:
Los registros de correo **no deben estar proxied por Cloudflare**.

---

# 7. Verificación

Volver al panel de Titan y seleccionar:

Volver a comprobar

Estado esperado:

DKIM verificado

---

# 8. Flujo de envío de correo

Cliente de correo  
↓  
Servidor SMTP Titan  
↓  
Firma DKIM  
↓  
Servidor receptor  
↓  
Inbox del destinatario

---

# 9. Problemas comunes

## Problema: No se pueden enviar correos

Causas posibles:

- DKIM faltante
- SPF incorrecto
- DNS migrado sin recrear registros

Solución:

Verificar DKIM en Titan y recrearlo en Cloudflare.

---

## Problema: correos llegan a spam

Verificar:

- SPF válido
- DKIM verificado
- DMARC configurado
- reputación del dominio

---

# 10. Buenas prácticas

Nunca usar proxy de Cloudflare para:

- SMTP
- IMAP
- POP
- registros MX

Mantener siempre:

DNS Only (nube gris)

---

# 11. Checklist de implementación

Antes de finalizar verificar:

[ ] MX configurado  
[ ] SPF válido  
[ ] DKIM verificado  
[ ] DMARC configurado  
[ ] Registros de correo sin proxy  
[ ] Prueba de envío exitosa  

---

# 12. Conclusión

Cuando un dominio cambia su proveedor DNS a Cloudflare, es obligatorio recrear los registros de autenticación del correo.

Si DKIM no existe, Titan no podrá firmar correos y el envío fallará.

Agregar correctamente el registro DKIM restaura la capacidad de envío y mejora la reputación del dominio.
