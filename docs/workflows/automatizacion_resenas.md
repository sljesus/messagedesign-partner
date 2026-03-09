# Workflows de Automatización - GoHighLevel

## Información

- **Agencia:** Message Design
- **Prestador de servicios:** SST México
- **Plataforma:** GoHighLevel (cuenta staff)

---

## Workflow 1: Solicitud de Reseña (5 Estrellas)

### Nombre
`Review Request Flow`

### Trigger
- **Tipo:** Appointment Completed / Tag Added
- **Configuración:** Etiqueta `servicio-completado` o `compra-finalizada`

### Pasos del Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Wait                                              │
│  ─────────────────────────────────────────────────────────  │
│  Duration: 3 days                                          │
│  (después del trigger)                                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Send SMS/Email                                    │
│  ─────────────────────────────────────────────────────────  │
│  Channel: SMS + Email                                      │
│  Template: Review Request                                  │
│                                                            │
│  SMS:                                                       │
│  "¡Hola {{contact.first_name}}! 👋                         │
│  Gracias por confiar en nosotros.                          │
│  Tu opinión nos ayuda a mejorar.                           │
│  ¿Podrías tomarte 30 segundos para dejarnos una reseña?   │
│  {{business.google_review_link}}                          │
│                                                            │
│  Si te generó valor, una ⭐⭐⭐⭐⭐ sería genial!"          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Survey - Rating                                   │
│  ─────────────────────────────────────────────────────────  │
│  Question: "¿Cómo calificarías tu experiencia?"            │
│  Type: Rating (1-5 stars)                                  │
│  Field: rating_experiencia                                 │
│                                                            │
│  Note: Incluir en mensaje anterior:                        │
│  "Responde con un número del 1 al 5"                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
         ┌─────────────────┴─────────────────┐
         │              ▼                     │
         │  ┌───────────────────────────┐    │
         │  │  STEP 4: Condition        │    │
         │  │  ─────────────────────── │    │
         │  │  rating_experiencia = 5   │    │
         │  └───────────┬───────────────┘    │
         │              │                    │
         │    ┌─────────┴─────────┐          │
         │    ▼                   ▼          │
         │  YES                  NO           │
         │   │                    │           │
         ▼   ▼                    ▼            │
┌──────────────────┐   ┌──────────────────┐   │
│  STEP 5a:        │   │  STEP 5b:        │   │
│  Redirect to     │   │  Add Tag:        │   │
│  Google Review   │   │  review-1-4      │   │
│                  │   │                  │   │
│  Send SMS:       │   │  Go to Workflow: │   │
│  "¡Excelente!    │   │  Salvamento Flow  │   │
│  Aquí puedes     │   │                  │   │
│  dejarnos tu     │   │                  │   │
│  reseña:         │   │                  │   │
│  [Google Link]"  │   │                  │   │
└──────────────────┘   └──────────────────┘
```

---

## Workflow 2: Flujo de Salvamento

### Nombre
`Salvamento Review Flow`

### Trigger
- **Tipo:** Tag Added
- **Tag:** `review-1-4`

### Pasos del Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Update Contact                                     │
│  ─────────────────────────────────────────────────────────  │
│  Add Tags:                                                  │
│  - review-salvamento                                        │
│  - awaiting-resolution                                     │
│                                                            │
│  Set Custom Field:                                          │
│  - salvage_date: Current Date                              │
│  - salvage_status: pending                                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Send SMS - Acknowledgment                         │
│  ─────────────────────────────────────────────────────────  │
│  "Hola {{contact.first_name}},                             │
│  Gracias por tu retroalimentación.                          │
│  Lamentamos que no hayas tenido la mejor experiencia.     │
│  Nos encantaría resolver esto personalmente.              │
│  Un miembro de nuestro equipo te contactará hoy.          │
│  ¡Gracias por给我们机会弥补!"                               │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Create Internal Task                              │
│  ─────────────────────────────────────────────────────────  │
│  Title: "🔴 Salvamento: {{contact.first_name}}"           │
│  Description:                                              │
│  "Cliente reportó rating: {{custom_fields.rating_experiencia}} ⭐    │
│  Contactar dentro de 24 horas.                             │
│  Teléfono: {{contact.phone}}"                              │
│                                                            │
│  Assign to: [Tu equipo de atención]                        │
│  Priority: High                                            │
│  Due Date: Today                                           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Create Opportunity                                 │
│  ─────────────────────────────────────────────────────────  │
│  Pipeline: Salvamento                                       │
│  Stage: Nuevo Lead (Salvamento)                            │
│  Name: "Salvamento - {{contact.first_name}}"               │
│  Value: $0                                                  │
│  Contact: {{contact}}                                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: Send Internal Notification                        │
│  ─────────────────────────────────────────────────────────  │
│  Channel: Email / SMS a equipo interno                    │
│  "🚨 NUEVO SALVAMENTO                                      │
│  Cliente: {{contact.first_name}}                           │
│  Rating: {{custom_fields.rating_experiencia}}/5            │
│  Tel: {{contact.phone}}                                    │
│  Revisar pipeline: Salvamento"                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 6: Wait                                              │
│  ─────────────────────────────────────────────────────────  │
│  Duration: 24 hours                                         │
│  (Tiempo para que el equipo contacte)                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 7: Condition                                          │
│  ─────────────────────────────────────────────────────────  │
│  Check Custom Field: salvage_status                        │
│                                                            │
│  IF salvage_status = "resolved" →                         │
│      Go to STEP 8 (Request 5 Stars)                       │
│                                                            │
│  IF salvage_status = "pending" →                          │
│      Wait 24h and check again                              │
│      (Max 3 iterations)                                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Workflow 3: Resolución y Nueva Solicitud

### Nombre
`Salvamento - Request 5 Stars`

### Trigger
- **Tipo:** Tag Added
- **Tag:** `salvamento-resuelto`

### Pasos

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Send SMS - Thank You + Request                   │
│  ─────────────────────────────────────────────────────────  │
│  "¡Hola {{contact.first_name}}! 🎉                        │
│  Gracias por给我们机会 demostrar nuestro compromiso.     │
│  Nos alegra que hayamos resuelto tu preocupación.         │
│  ¿Podrías actualizar tu reseña a 5 estrellas?              │
│  {{business.google_review_link}}"                         │
│                                                            │
│  Remove Tag: review-salvamento                             │
│  Add Tag: review-resuelto                                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Wait                                              │
│  ─────────────────────────────────────────────────────────  │
│  Duration: 2 days                                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Survey - New Rating                               │
│  ─────────────────────────────────────────────────────────  │
│  Question: "¿Cómo calificarías ahora tu experiencia?"     │
│  Type: Rating (1-5 stars)                                  │
│  Field: rating_final                                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
         ┌─────────────────┴─────────────────┐
         │              ▼                     │
         │  ┌───────────────────────────┐    │
         │  │  Condition: rating_final │    │
         │  │  = 5                      │    │
         │  └───────────┬───────────────┘    │
         │              │                    │
         │    ┌─────────┴─────────┐          │
         │    ▼                   ▼          │
         │  YES                  NO           │
         ▼   │                    │           │
┌──────────────────┐   ┌──────────────────┐   │
│  STEP 4a:        │   │  STEP 4b:        │   │
│  Redirect to     │   │  Add Tag:        │   │
│  Google Review   │   │  needs-followup  │   │
│                  │   │                  │   │
│  Remove Tag:     │   │  Note: Escalar  │   │
│  review-1-4     │   │  a manager      │   │
│  Add Tag:        │   │                  │   │
│  happy-customer  │   │                  │   │
└──────────────────┘   └──────────────────┘
```

---

## Configuración de Campos Personalizados

### Campos necesarios en GoHighLevel

| Campo | Tipo | Descripción |
|-------|------|-------------|
| rating_experiencia | Rating (1-5) | Rating inicial |
| rating_final | Rating (1-5) | Rating después de salvamento |
| salvage_date | Date | Fecha de inicio de salvamento |
| salvage_status | Dropdown | pending / resolved / escalated |
| salvage_notes | Text | Notas del equipo sobre resolución |

---

## Configuración de Pipeline (Oportunidades)

### Pipeline: Salvamento

| Stage | Descripción |
|-------|-------------|
| Nuevo Lead | Cliente requiere contacto |
| Contactando | Equipo en proceso de llamada |
| Problema Identificado | Cliente expresó problema específico |
| En Resolución | Solución en proceso |
| Resuelto | Problema resuelto, esperando nueva reseña |
| Perdido | No se logró resolver |

---

## SMS Templates

### Template 1: Solicitud Inicial
```
¡Hola {{contact.first_name}}! 👋

Gracias por confiar en nosotros. Tu opinión nos ayuda a mejorar.

¿Podrías tomarte 30 segundos para dejarnos una reseña?
{{business.google_review_link}}

Si te generó valor, una ⭐⭐⭐⭐⭐ sería genial!

Responde con un número del 1 al 5.
```

### Template 2: Acknowledgment (Salvamento)
```
Hola {{contact.first_name}},

Gracias por tu retroalimentación.
Lamentamos que no hayas tenido la mejor experiencia.

Nos encantaría resolver esto personalmente.
Un miembro de nuestro equipo te contactará hoy.

Gracias por给我们机会弥补!
```

### Template 3: After Resolution
```
¡Hola {{contact.first_name}}! 🎉

Gracias por给我们机会 demostrar nuestro compromiso.
Nos alegra que hayamos resuelto tu preocupación.

¿Podrías actualizar tu reseña a 5 estrellas?
{{business.google_review_link}}
```

---

## Configuración de Tareas

### Task: Salvamento - Contactar Cliente
```
Title: 🔴 Salvamento: {{contact.first_name}}

Description:
Cliente reportó rating: {{custom_fields.rating_experiencia}}/5 ⭐

Teléfono: {{contact.phone}}
Email: {{contact.email}}

Última compra/servicio: [Revisar en contacto]

ACCIONES REQUERIDAS:
1. Llamar al cliente en las próximas 24 horas
2. Escuchar y documentar el problema
3. Ofrecer solución
4. Actualizar estado en custom field

Priority: High
Due: Today
Assign to: [Equipo de atención]
```

---

## Métricas del Workflow

| Métrica | Descripción | Meta |
|---------|-------------|------|
| Review Request Rate | % de clientes que reciben solicitud | 100% |
| Response Rate | % de clientes que responden | >60% |
| 5-Star Rate | % de rating 5 estrellas | >80% |
| Salvamento Rate | % de clientes <5 que se salvan | >40% |
| Resolution Time | Tiempo promedio de resolución | <48 hrs |
| Recovery Rate | % que mejora a 5 estrellas post-salvamento | >50% |
