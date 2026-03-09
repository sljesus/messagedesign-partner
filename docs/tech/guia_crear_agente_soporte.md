# Guía Simple: Crear un Agente de Soporte con Google ADK

## ¿Qué es un Agente de Soporte?

Es como un empleado virtual que:
- Responde preguntas de tus clientes
- Está disponible 24/7
- Nunca se cansa
- Siempre responde con la misma información

```
Cliente pregunta: "Cómo configuro mi Google Business?"
       │
       ▼
   🤖 Tu Agente
       │
       ▼
Cliente recibe: "Ve a Reputation → Settings → Conecta Google..."
```

---

## Lo que necesitas (Lista simple)

| Qué necesitas | Para qué sirve |
|---------------|----------------|
| Computadora con Python | Para crear el agente |
| Google AI API Key | Para que el agente "piense" |
| Cuenta de Google (Gmail) | Para obtener la API key |
| WhatsApp (opcional) | Para que te hablen por ahí |

---

## Paso 1: Obtener tu API Key de Google

1. Ve a: **https://aistudio.google.com/app/apikey**
2. Inicia sesión con tu cuenta de Google
3. Click en "Create API Key"
4. Copia la clave (se ve algo como `AIza...`)
5. **Guárdala en un lugar seguro**

---

## Paso 2: Instalar Google ADK

Abre tu terminal (Command Prompt o PowerShell en Windows):

```bash
pip install google-adk
```

*(Si no tienes pip, primero instala Python desde python.org)*

---

## Paso 3: Crear tu primer agente

### Estructura de carpetas

```
mi_agente/
├── agent.py
└── .env
```

### Archivo 1: .env (la configuración)

Crea un archivo llamado `.env` y pon esto:

```
GOOGLE_API_KEY=AIzaTuClaveAqui
```

*(Reemplaza con tu API key real)*

### Archivo 2: agent.py (el código)

```python
from google.adk.agents import LlmAgent

# Este es tu agente de soporte
agente_soporte = LlmAgent(
    name="soporte_message_design",
    model="gemini-2.0-flash",
    instruction="""
    Eres el agente de soporte de Message Design.
    
    Ayudas a clientes con estas preguntas frecuentes:
    
    1. ¿Cómo configuro Google Business?
       Respuesta: Ve a Reputation → Settings → Conecta tu cuenta de Google Business
    
    2. ¿Cómo连接 un dominio?
       Respuesta: Ve a Settings → Domains → Agrega tu dominio y configura los DNS
    
    3. ¿Cómo activo las reseñas automáticas?
       Respuesta: Ve a Reputation → Requests → Crea una campaña de reseñas
    
    4. ¿Cómo configuro el calendario?
       Respuesta: Ve a Calendars → Create Calendar → Configura disponibilidad
    
    Si no sabes la respuesta, dice que contactarás al equipo técnico.
    """
)

# Esto es para probar el agente
if __name__ == "__main__":
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    
    # Crear una sesión de prueba
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name="soporte")
    
    # Hacer una pregunta
    pregunta = "¿Cómo configuro Google Business?"
    
    # Ejecutar el agente
    runner = Runner(agent=agente_soporte, app_name="soporte", session_service=session_service)
    respuesta = runner.run(session_id=session.id, user_message=pregunta)
    
    print("Cliente:", pregunta)
    print("Agente:", respuesta.text)
```

---

## Paso 4: Probar tu agente

En tu terminal, ejecuta:

```bash
python agent.py
```

Debería mostrar algo como:

```
Cliente: ¿Cómo configuro Google Business?
Agente: Ve a Reputation → Settings → Conecta tu cuenta de Google Business
```

---

## Paso 5: Hacerlo más útil (opcional)

### Añadir más preguntas frecuentes

Edita la parte de `instruction` y agrega más respuestas:

```python
instruction="""
Eres el agente de soporte de Message Design.

Ayudas a clientes con estas preguntas frecuentes:

1. ¿Cómo configuro Google Business?
   Respuesta: Ve a Reputation → Settings → Conecta tu cuenta de Google Business

2. [AGREGA MÁS AQUÍ...]
"""
```

### Conectar a WhatsApp (avanzado)

Esto es más complejo. Necesitas:
- Twilio ($15/mes)
- O usar Botpress (más fácil)

---

## Estructura básica resumida

```
CREAR AGENTE DE SOPORTE
│
├── 1. Obtener API Key de Google AI
├── 2. Instalar: pip install google-adk
├── 3. Crear archivo .env (poner API key)
├── 4. Crear agent.py (escribir el código)
└── 5. Ejecutar: python agent.py
```

---

## Próximos pasos (cuando domines lo básico)

| Nivel | Qué hacer |
|-------|-----------|
| **2** | Añadir más preguntas frecuentes |
| **3** | Conectar a WhatsApp |
| **4** | Agregar acceso a la cuenta del cliente |
| **5** | Hacerlo hablar por voz |

---

## ¿Necesitas ayuda?

Si algo no funciona, dime:
1. Qué error te aparece
2. Qué paso seguiste
3. Tu sistema operativo (Windows/Mac)
