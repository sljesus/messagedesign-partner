# Manual de Onboarding y SOP Operativo
## Message Design - SST México

---

## SECCIÓN 1: CHECKLIST DE REQUERIMIENTOS DEL CLIENTE

### WhatsApp Business API

| Requisito | Descripción | Estado |
|-----------|-------------|--------|
| Acta constitutiva o registro legal | Documento legal de la empresa | ☐ |
| Identificación oficial | INE/Pasaporte del representante legal | ☐ |
| Comprobante de domicilio | Receipte de servicios reciente (luz/agua/teléfono) | ☐ |
| Página web funcional | Con aviso de privacidad visible | ☐ |
| Acceso a Meta Business Manager | Credenciales de administrador | ☐ |
| Número telefónico exclusivo | No conectado a WhatsApp normal | ☐ |
| Tarjeta bancaria | Para cobros de Meta (si aplica) | ☐ |

### Sistema de Reseñas 5 Estrellas

| Requisito | Descripción | Estado |
|-----------|-------------|--------|
| Acceso administrador a Google Business Profile | Credenciales completas | ☐ |
| Dominio propio | Dominio registrado y accesible | ☐ |
| Acceso al proveedor de dominio | Para configurar DNS | ☐ |
| Logotipo en PNG | Logo en formato de imagen | ☐ |
| Colores corporativos | Hex codes o branding guide | ☐ |
| Mensaje aprobado | Template para solicitud de reseña | ☐ |
| Base de datos de clientes | Lista de clientes (opcional) | ☐ |

---

## SECCIÓN 2: TIEMPOS ESTIMADOS DE IMPLEMENTACIÓN

### WhatsApp Business API

| Etapa | Tiempo Estimado |
|-------|-----------------|
| Verificación Meta Business | 1-5 días hábiles |
| Aprobación de plantillas | 1-2 días |
| Configuración técnica | 1 día |
| **Tiempo total** | **3-7 días hábiles** |

### Sistema de Reseñas 5 Estrellas

| Etapa | Tiempo Estimado |
|-------|-----------------|
| Configuración DNS | 10-30 minutos |
| Propagación DNS | hasta 24 horas |
| Activación SSL automática | 5-30 minutos |
| Verificación Google Business (si no está verificada) | 3-14 días |
| **Tiempo total (sin verificación Google)** | **1-2 días** |
| **Tiempo total (con verificación Google)** | **3-14 días** |

---

## SECCIÓN 3: SOP OPERATIVO INTERNO

### Flujo de Trabajo

```
┌─────────────────────────────────────────────────────────────────┐
│                    MESSAGE DESIGN - FLUJO DE ONBOARDING        │
└─────────────────────────────────────────────────────────────────┘

    ┌──────────┐
    │  PAGO    │─────────────┐
    │RECIBIDO  │             │
    └──────────┘             ▼
                    ┌──────────────────┐
                    │  ENVIAR          │
                    │  CHECKLIST AL    │
                    │  CLIENTE         │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  ESPERAR         │
                    │  DOCUMENTACIÓN   │
                    │  (1-3 días)      │
                    └────────┬─────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
     ┌────────────────┐           ┌────────────────┐
     │  DOCUMENTACIÓN │           │ DOCUMENTACIÓN  │
     │  INCOMPLETA    │           │ COMPLETA       │
     │                │           │                │
     │  Solicitar     │           │  CONTINUAR     │
     │  faltantes     │           │  AL PASO 3    │
     └────────────────┘           └────────────────┘
```

---

### DETALLE DE PASOS

#### Paso 1: Validar pago y enviar checklist al cliente

**Responsable:** Equipo de ventas / Soporte

**Acciones:**
1. Verificar recepción del pago en Stripe/Transferencia
2. Confirmar plan contratado (Visibilidad / Crecimiento / Aceleración)
3. Enviar checklist de requisitos al cliente por email
4. Agregar tag `onboarding-iniciado` al contacto en GHL

**Template de email:**
```
Hola [Nombre],

¡Bienvenido a Message Design! 🎉

Para comenzar con la implementación de tu servicio, necesitamos que nos proporciones la siguiente documentación:

[Adjuntar checklist]

Por favor, completa y envías la información en los próximos 3 días para comenzar tu configuración.

Cualquier duda, estamos aquí para ayudarte.

Saludos,
Equipo Message Design
```

---

#### Paso 2: Confirmar recepción completa de documentación

**Responsable:** Equipo de soporte

**Acciones:**
1. Revisar documentos recibidos
2. Verificar que todos los requisitos estén completos
3. Si falta algo, documentar y solicitar
4. Si está completo, confirmar al cliente

** checklist de verificación:**
- [ ] Acta constitutiva legible
- [ ] ID del representante vigente
- [ ] Comprobante de domicilio reciente (<3 meses)
- [ ] URL de página web funcional
- [ ] Acceso a Meta Business Manager verificado
- [ ] Número telefónico confirmado (no tiene WhatsApp)
- [ ] Acceso a Google Business Profile
- [ ] Dominio registrado
- [ ] Logo en PNG recibido

---

#### Paso 3: Crear o verificar Meta Business Manager

**Responsable:** Equipo técnico

**Acciones:**
1. Si el cliente NO tiene Business Manager:
   - Crear nuevo Business Manager
   - Agregar cuenta publicitaria
   - Agregar cuenta de WhatsApp
2. Si el cliente SÍ tiene Business Manager:
   - Verificar acceso de administrador
   - Agregar cuenta de WhatsApp si no existe
3. Documentar ID de Business Manager

**Ubicación en GHL:**
- Settings → Integrations → WhatsApp
- O ir a Facebook Developer Console

---

#### Paso 4: Iniciar verificación empresarial en Meta

**Responsable:** Equipo técnico

**Acciones:**
1. Ir a Business Settings → Business Info
2. Completar información empresarial
3. Subir documentos requeridos
4. Seleccionar método de verificación (email/phone/SMS)
5. Esperar aprobación (1-5 días hábiles)

**Información requerida:**
- Nombre legal exacto
- Dirección física
- Teléfono de contacto
- Sitio web
- Categoría de negocio

---

#### Paso 5: Configurar número WhatsApp y enviar plantillas

**Responsable:** Equipo técnico

**Acciones:**
1. Configurar número de teléfono en WhatsApp Manager
2. Verificar que el número no tenga WhatsApp activo
3. Crear plantillas de mensaje iniciales:
   - Bienvenida
   - Confirmación de cita
   - Seguimiento
   - Notificación de pago

**Plantillas estándar:**

```
Bienvenida:
¡Hola! 👋
Bienvenido a [Nombre del negocio]. 
Gracias por contactarnos.
¿En qué podemos ayudarte hoy?

Confirmación de Cita:
Tu cita ha sido confirmada para el [fecha] a las [hora].
Responder "CONFIRMAR" para confirmar o "CAMBIAR" para modificar.

Seguimiento:
¡Hola! Solo wantedíamos saber si tienes alguna duda sobre nuestro servicio.
Estamos aquí para ayudarte. 😊
```

**Ubicación en GHL:**
- Settings → WhatsApp → WhatsApp Manager
- Conversations → Templates

---

#### Paso 6: Configurar dominio y DNS para reseñas

**Responsable:** Equipo técnico

**Acciones:**
1. Obtener registros DNS de GoHighLevel
2. Enviar instrucciones al cliente para configurar en su registrador
3. O realizar configuración si se tiene acceso
4. Verificar propagación

**Registros DNS a configurar:**

| Tipo | Host | Valor |
|------|------|-------|
| A | @ | 142.251.134.17 |
| CNAME | www | connect.highlevel.com |
| CNAME | funnel | funnel.highlevel.com |
| CNAME | store | store.highlevel.com |

**Cliente sin acceso a DNS:**
- Enviar instrucciones paso a paso
- Proporcionar screenshot de configuración
- Ofrecer llamada para guiar

---

#### Paso 7: Verificar SSL y funcionamiento del formulario

**Responsable:** Equipo técnico

**Acciones:**
1. Verificar que SSL esté activo (https://)
2. Probar formulario de contacto
3. Probar que leads lleguen a GHL
4. Configurar notificaciones de nuevos leads

**Verificaciones:**
- [ ] Dominio carga correctamente
- [ ] SSL activo (candado verde)
- [ ] Formulario de contacto funciona
- [ ] Lead llega a GHL
- [ ] Email de notificación llega

---

#### Paso 8: Realizar pruebas internas completas

**Responsable:** Equipo técnico

** checklist de pruebas:**

**WhatsApp:**
- [ ] Enviar mensaje de prueba desde GHL
- [ ] Recibir respuesta del cliente
- [ ] Plantillas aprobadas funcionan
- [ ] Notificaciones activas

**Reseñas:**
- [ ] Widget de reseñas visible
- [ ] Link de Google Review funciona
- [ ] Flujo de solicitud activa
- [ ] Encuestas configuradas

**Sitio/Funnels:**
- [ ] Página carga correctamente
- [ ] Formularios submiten correctamente
- [ ] Pagos configuran (si aplica)
- [ ] CRM recibe leads

---

#### Paso 9: Entregar capacitación breve al cliente

**Responsable:** Equipo de soporte

**Contenido de capacitación:**

1. **WhatsApp Business**
   - Cómo responder mensajes
   - Cómo usar plantillas
   - Cómo vedere métricas

2. **Reseñas**
   - Cómo monitorear reseñas
   - Cómo responder reseñas
   - Cómo ver métricas

3. **Dashboard**
   - Navigación básica
   - Dónde ver leads
   - Cómo agendar citas

**Duración:** 30-60 minutos

---

#### Paso 10: Activar soporte post-implementación

**Responsable:** Equipo de soporte

**Acciones:**
1. Cambiar tag a `cliente-activo`
2. Configurar soporte según plan
3. Agendar primera llamada de seguimiento (7 días)
4. Documentar en CRM

---

## SECCIÓN 4: HANDOFFS Y RESPONSABILIDADES

| Paso | Responsable Primary | Responsable Backup |
|------|---------------------|---------------------|
| 1-2 | Ventas | Soporte |
| 3-4 | Técnico | Soporte |
| 5-7 | Técnico | Técnico senior |
| 8 | Técnico | Soporte |
| 9-10 | Soporte | Ventas |

---

## SECCIÓN 5: TIEMPOS DE RESPUESTA (SLAs)

| Tipo de Solicitud | Tiempo de Primera Respuesta |
|-------------------|----------------------------|
| Onboarding general | 24 horas hábiles |
| Documentación faltante | 24 horas hábiles |
| Issues técnicos | 4 horas hábiles |
| Urgencias | 2 horas hábiles |

---

## SECCIÓN 6: ESCALAMIENTOS

### Nivel 1: Equipo de soporte
- Preguntas básicas
- Issues menores
- Dudas de uso

### Nivel 2: Técnico senior
- Problemas de configuración
- Integraciones fallidas
- Issues de DNS/SSL

### Nivel 3: Manager
- Problemas de facturación
- Issues con Meta/Google
- Clientes en riesgo de churn

---

## ANEXO: TEMPLATES DE COMUNICACIÓN

### Template: Recordatorio de documentación
```
Hola [Nombre],

Hope you're doing well! 👋

Solo te recordamos que aún necesitamos la siguiente documentación para completar tu onboarding:

[Faltantes]

Por favor, envíalos a la brevedad para que podamos continuar con la configuración.

Gracias,
Equipo Message Design
```

### Template: Onboarding completado
```
🎉 ¡Tu sistema está listo!

Hola [Nombre],

¡Tenemos buenas noticias! Tu sistema está completamente configurado y listo para usar.

Puedes encontrar tu acceso aquí:
- WhatsApp: [Link]
- Dashboard: [Link]
- Reseñas: [Link]

Próximamente te contactaremos para agendar tu capacitación.

¡Gracias por confiar en Message Design!

Equipo Message Design
```

---

## REVISIONES

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | [Fecha] | Creación inicial |

---

**Documento creado por:** SST México
**Para:** Message Design
