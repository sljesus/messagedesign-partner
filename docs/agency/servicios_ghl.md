# Servicios de Agencia GoHighLevel - Message Design

## Información del Negocio

- **Agencia:** Message Design (cuenta staff de GoHighLevel)
- **Prestador de servicios:** SST México
- **Servicios:** Soporte técnico, ventas y gestión de la plataforma

---

## Descripción General

Agencia especializada en GoHighLevel ofreciendo servicios de:
- Creación de páginas web y funnels
- Conexión de dominios
- Automatizaciones de marketing
- Sistema de gestión de reseñas de Google Business

---

## 1. Páginas Web y Funnels

### Proceso de Creación

1. **Planificación**
   - Definir objetivo del funnel (Lead Magnet, Venta, Cita)
   - Identificar audiencia objetivo
   - Crear estructura de páginas

2. **Configuración en GHL**
   - Ir a **Sites → Funnels** o **Websites**
   - Seleccionar template o iniciar desde cero
   - Configurar secciones con editor drag-and-drop

3. **Elementos comunes**
   - Header con logo y navegación
   - Hero section con CTA
   - Formularios de captura
   - Testimonios
   - Footer con contacto

---

## 2. Conexión de Dominios

### Pasos para Conectar Dominio

1. **En el registrador (Namecheap, GoDaddy, etc.)**
   - Iniciar sesión
   - Ir a DNS Management
   - Agregar registros CNAME y A

2. **Registros DNS típicos para GHL**

| Tipo | Host | Valor |
|------|------|-------|
| A | @ | 142.251.134.17 |
| CNAME | www | connect.highlevel.com |
| CNAME | funnel | funnel.highlevel.com |
| CNAME | store | store.highlevel.com |

3. **En GoHighLevel**
   - Ir a **Settings → Domains & URL Redirects**
   - Agregar dominio propio
   - Verificar SSL (automático)

4. **Verificación**
   - Esperar 24-48 horas para propagación
   - Probar que el dominio carga correctamente

---

## 3. Automatización de Reseñas de Google Business

### Flujo Completo

```
┌──────────────────┐
│  Cliente compra  │
│   o termina      │
│   servicio        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Esperar X días  │  (Configurable: 1-7 días)
│  post-servicio   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Enviar SMS/Email│
│  pidiendo        │
│  reseña          │
└────────┬─────────┘
         │
         ▼
    ┌────┴────┐
    │ Rating? │
    └────┬────┘
   5★     │    1-4★
   │      │      │
   ▼      │      ▼
┌─────┐   │  ┌─────────┐
│Ir a │   │  │FLUJO DE │
│Google│   │  │SALVAMENTO│
│Review│   │  │ (llamada│
│Link │   │  │ interna)│
└─────┘   │  └─────────┘
          │
          ▼
   ┌──────────────────┐
   │  Solicitar      │
   │  retroaliment.  │
   │  para resolver  │
   └──────────────────┘
```

### Workflow: Solicitud de Reseña (5 Estrellas)

**Trigger:** Survey Response / Appointment Completed / Tag Added

**Acciones:**

1. **Esperar** (2-7 días después del servicio)

2. **Enviar mensaje** con link de reseñas:
   ```
   ¡Hola [Nombre]! 👋
   Gracias por confiar en nosotros. 
   Tu opinión nos ayuda a mejorar.
   ¿Podrías tomarte 30 segundos para dejarnos una reseña?
   [Link de Google Review]
   
   Si te generó valor nuestro servicio, una ⭐⭐⭐⭐⭐ sería genial!
   ```

3. **Condición: Rating**
   - Si rating = 5 → Ir a Google Review Link
   - Si rating < 5 → Ir a Flujo de Salvamento

---

## 4. Flujo de Salvamento (Reviews 1-4 Estrellas)

### Propósito
Cuando un cliente indica menos de 5 estrellas, NO se le envía directamente a Google. En su lugar, se activa un flujo de salvamento para:

1. **Resolver el problema** antes de que publique una mala reseña
2. **Contactar al cliente** para arreglar la situación
3. **Redirigir a llamada interna** con el equipo

### Workflow: Flujo de Salvamento

**Trigger:** Rating < 5 estrellas

**Acciones:**

1. **Enviar mensaje de seguimiento:**
   ```
  Hola [Nombre], gracias por tu retroalimentación.
  Lamentamos que no hayas tenido la mejor experiencia.
  Nos encantaría resolver esto. 
  Un miembro de nuestro equipo te contactará hoy para arreglarlo.
   ```

2. **Crear tarea** para el equipo:
   - Título: "Salvamento de cliente: [Nombre]"
   - Asignar a: Equipo de atención al cliente
   - Prioridad: Alta
   - Fecha de vencimiento: Hoy

3. **Agregar tags:**
   - `review-salvamento`
   - `review-[X]-estrellas` (donde X es el rating)

4. **Agendar llamada:**
   - Enviar link de calendario para agendar llamada
   - O generar Opportunity en pipeline

5. **Después de la llamada:**
   - Si se resolvió → Solicitar reseña de 5 estrellas
   - Si no resolvió → Documentar para mejora interna

---

## 5. Configuración en GoHighLevel

### Reputación (Reputation)

1. **Conectar Google Business Profile**
   - Ir a **Reputation → Settings**
   - Conectar cuenta de Google Business
   - Configurar review link

2. **Configurar Review Request**
   - Ir a **Reputation → Requests**
   - Crear campaña de solicitud
   - Timing: 2-7 días post-servicio
   - Incluir pregunta de rating

3. **Configurar Widget** (opcional)
   - Personalizar mensaje
   - Configurar umbrales de rating

### Automations (Workflows)

**Workflow Principal:**
```
Name: Review Request Flow
Trigger: Appointment Completed / Tag Added
Action 1: Wait (3 days)
Action 2: Send SMS/Email with Review Link
Action 3: Survey (Rating 1-5)
Action 4: IF Rating = 5 → Redirect to Google Review
          IF Rating < 5 → Go to Workflow "Salvamento"
```

**Workflow Salvamento:**
```
Name: Salvamento Review
Trigger: Tag added (review-salvamento)
Action 1: Send SMS (mensaje de seguimiento)
Action 2: Create Task (contactar cliente)
Action 3: Add to Pipeline (seguimiento)
Action 4: Wait (24 hours)
Action 5: Send SMS (solicitar 5 estrellas si se resolvió)
```

---

## 6. Métricas a Monitorear

| Métrica | Meta |
|---------|------|
| Reseñas 5 estrellas | >80% |
| Rate de respuesta | >60% |
| Clientes salvados | >40% |
| Tiempo de respuesta (salvamento) | <24 horas |

---

## 7. Checklist de Implementación

- [ ] Conectar Google Business Profile
- [ ] Configurar Review Link personalizado
- [ ] Crear Workflow "Review Request Flow"
- [ ] Crear Workflow "Salvamento"
- [ ] Configurar tareas automáticas
- [ ] Probar flujo completo
- [ ] Configurar pipeline para seguimiento
- [ ] Entrenar equipo en atención de salvamento
