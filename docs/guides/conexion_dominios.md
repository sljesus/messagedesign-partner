# Guía de Conexión de Dominios en GoHighLevel

## Información

- **Agencia:** Message Design
- **Prestador de servicios:** SST México

---

## Introducción

Conectar tu dominio propio a GoHighLevel permite que tus funnels y sitios web aparezcan con tu dominio (ej: `tuempresa.com` en lugar de `tuempresa.highlevel.com`).

---

## Registradores Compatibles

- **Namecheap** (Recomendado)
- **GoDaddy**
- **Google Domains**
- **Cloudflare**
- **Name.com**
- **Domain.com**

---

## Pasos para Conectar Dominio

### Paso 1: Obtener los DNS de GoHighLevel

1. Ve a **Settings → Domains & URL Redirects** en GoHighLevel
2. Haz clic en **Add Domain**
3. Ingresa tu dominio (sin `www.` ej: `tuempresa.com`)
4. El sistema te mostrará los registros DNS necesarios

**Registros típicos:**
| Tipo | Host/Name | Value/Points to |
|------|-----------|-----------------|
| A | @ | 142.251.134.17 |
| CNAME | www | connect.highlevel.com |
| CNAME | funnel | funnel.highlevel.com |
| CNAME | store | store.highlevel.com |

### Paso 2: Configurar en tu Registrador

#### En Namecheap:
1. Inicia sesión en tu cuenta
2. Ve a **Domain List** → selecciona tu dominio
3. Haz clic en **Advanced DNS**
4. Agrega los registros:

```
Host: @          Type: A Record       Value: 142.251.134.17
Host: www        Type: CNAME          Value: connect.highlevel.com
Host: funnel     Type: CNAME          Value: funnel.highlevel.com
Host: store      Type: CNAME          Value: store.highlevel.com
```

#### En GoDaddy:
1. Inicia sesión
2. Ve a **Mis productos → Dominios**
3. Selecciona tu dominio → **DNS**
4. Agrega los registros en **Registros**

#### En Cloudflare:
1. Ve a tu dashboard
2. Selecciona el dominio
3. Clic en **DNS**
4. Agrega los registros:

```
Type: A      Name: @         Content: 142.251.134.17
Type: CNAME Name: www        Content: connect.highlevel.com
Type: CNAME Name: funnel     Content: funnel.highlevel.com
Type: CNAME Name: store      Content: store.highlevel.com
```

### Paso 3: Verificar en GoHighLevel

1. Regresa a **Settings → Domains**
2. Clic en **Verify** o espera a que se detecte automáticamente
3. El SSL (https) se genera automáticamente
4. Puede tomar 15 minutos a 24 horas

---

## Estructura de Subdominios

### Para Funnels:
- `tuempresa.com` → Sitio principal
- `www.tuempresa.com` → Redirige al sitio principal

### Para Funnels específicos:
- `funnel1.tuempresa.com` → Asignar en configuración del funnel
- En GoHighLevel: Funnel → Settings → Domain → Add Domain

### Para Stores (Tienda):
- `tienda.tuempresa.com` → Tienda e-commerce
- En GoHighLevel: Stores → Settings → Domain

---

## Troubleshooting

### Dominio no verifica:
1. Verifica que los registros DNS sean correctos
2. Espera hasta 24 horas por propagación
3. Confirma que no haya conflictos con otros registros
4. Verifica que el dominio no esté en pausa

### SSL no funciona:
1. Verifica que el dominio esté verificado
2. Intenta forzar SSL desde GoHighLevel
3. Confirma que no haya redirect loops

### Subdominio no carga:
1. Verifica que el CNAME apunte correctamente
2. Confirma que el funnel/website esté publicado
3. Revisa la configuración en GoHighLevel

---

## Mejores Prácticas

1. **Usa el mismo dominio principal** para todo
2. **Configura www como CNAME** que apunte a connect.highlevel.com
3. **Mantén registros mínimos** para evitar conflictos
4. **Espera la propagación** antes de reportar problemas
5. **Respaldar configuración DNS** antes de hacer cambios

---

## Checklist de Verificación

- [ ] Agregar registro A (apunta a IP de GHL)
- [ ] Agregar CNAME www
- [ ] Agregar CNAME funnel (si aplica)
- [ ] Agregar CNAME store (si aplica)
- [ ] Verificar en GoHighLevel
- [ ] Confirmar SSL activo
- [ ] Probar en navegador (pestaña incógnito)
- [ ] Probar con y sin www
