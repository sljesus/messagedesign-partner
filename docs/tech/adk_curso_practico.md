# GUÍA DEFINITIVA: Google ADK para Principiantes
## "Como si tuvieras 15 años" 🎮

---

## ¿Qué es Google ADK? (Explicación para gamers)

Imagina que creas un **NPC (Personaje No Jugador)** para un juego, pero en lugar de seguir un script fijo, este personaje puede:

- 🧠 **Pensar** (usando IA)
- 💬 **Hablar** contigo naturalmente
- 🔧 **Usar herramientas** (como un personaje que puede abrir puertas, recoger items)
- 👥 **Trabajar con otros agentes** (como un equipo de NPCs)

**ADK = Agent Development Kit** = Kit para crear agentes de IA

---

## NIVEL 1: Instalación y Primer Agente 🎯

### Paso 1: Instala Python

1. Ve a: https://www.python.org/downloads/
2. Descarga la versión más reciente
3. **IMPORTANTE:** Durante la instalación, marca ✅ "Add Python to PATH"
4. Click en "Install Now"

### Paso 2: Verifica que Python funcione

Abre tu terminal (Command Prompt en Windows) y escribe:

```bash
python --version
```

Debería mostrar algo como `Python 3.11.5` (o similar)

### Paso 3: Instala Google ADK

En la misma terminal:

```bash
pip install google-adk
```

**(pip es como el "Play Store" de Python - donde bajas apps)**

### Paso 4: Consigue tu API Key (Gratis)

1. Ve a: https://aistudio.google.com/app/apikey
2. Inicia sesión con tu Gmail
3. Click en "Create API Key"
4. Copia la clave (se ve como: `AIzaSy...`)
5. **Guárdala en un bloc de notas** - ¡No la pierdas!

---

## NIVEL 2: Tu Primer Agente 🚀

### Estructura de carpetas

Vas a crear una carpeta así:

```
mi_primer_agente/
├── agent.py        ← El código
└── .env           ← Tu API key
```

### Paso 1: Crea la carpeta

```bash
mkdir mi_primer_agente
cd mi_primer_agente
```

### Paso 2: Crea el archivo .env

Crea un archivo llamado `.env` y pon esto:

```
GOOGLE_API_KEY=AQUI_TU_API_KEY
```

(Reemplaza `AQUI_TU_API_KEY` con tu clave real)

### Paso 3: Crea agent.py

Crea un archivo llamado `agent.py` y copia este código:

```python
from google.adk.agents.llm_agent import Agent

# Esta es tu "herramienta" - una función que el agente puede usar
def saludar():
    """Esta función hace que el agente salude"""
    return "¡Hola! Soy tu primer agente de IA. 🎉"

# Aquí creas al agente
mi_agente = Agent(
    model='gemini-2.0-flash',  # El "cerebro" del agente
    name='mi_primer_agente',
    instruction='Eres un agente amigable que saluda a las personas.',
    tools=[saludar],  # Le das la herramienta
)

# Esto hace que el archivo sea ejecutable
root_agent = mi_agente
```

### Paso 4: Ejecuta tu agente

En tu terminal:

```bash
adk run mi_primer_agente
```

¡Ahora puedes chatear con tu agente! 🎮

---

## NIVEL 3: Agente con Funciones Reales 🔧

Ahora vamos a hacer un agente que haga cosas útiles

### Código completo (cópialo):

```python
from google.adk.agents.llm_agent import Agent
from datetime import datetime

# --- HERRAMIENTAS (Lo que el agente puede hacer) ---

def obtener_hora():
    """Retorna la hora actual"""
    ahora = datetime.now()
    return f"Son las {ahora.strftime('%H:%M')} horas"

def obtener_fecha():
    """Retorna la fecha actual"""
    ahora = datetime.now()
    return f"Hoy es {ahora.strftime('%d de %B de %Y')}"

def calcular_doble(numero: int) -> str:
    """Duplica un número"""
    resultado = numero * 2
    return f"El doble de {numero} es {resultado}"

# --- CREAR EL AGENTE ---

agente_util = Agent(
    model='gemini-2.0-flash',
    name='agente_util',
    instruction='''
    Eres un asistente útil llamado "Utilín".
    Sempre que te pregunten la hora, usa la herramienta obtener_hora.
    Sempre que te pregunten la fecha, usa la herramienta obtener_fecha.
    Sempre que te pidan calcular algo, usa la herramienta calcular_doble.
    Sé amable y conversacional.
    ''',
    tools=[obtener_hora, obtener_fecha, calcular_doble]
)

root_agent = agente_util
```

### Ejecútalo:

```bash
adk run mi_primer_agente
```

**Prueba diciendo:**
- "¿Qué hora es?"
- "¿Qué fecha es hoy?"
- "Calcula el doble de 25"

---

## NIVEL 4: Agente de Soporte (El que necesitas para tu negocio) 📞

Este es el que usarás para dar soporte a clientes de Message Design:

```python
from google.adk.agents.llm_agent import Agent

# --- BASE DE CONOCIMIENTO (FAQ) ---
# Aquí pones todas las preguntas y respuestas que tu agente debe saber

FAQ_SOPORTE = """
Eres el agente de soporte de Message Design.

PREGUNTAS FRECUENTES:

1. ¿Cómo configuro Google Business?
   Respuesta: Ve a Reputation → Settings → Conecta tu cuenta de Google Business

2. ¿Cómo conecto un dominio?
   Respuesta: Ve a Settings → Domains → Agrega tu dominio → Configura los DNS en Cloudflare

3. ¿Cómo activo las reseñas automáticas?
   Respuesta: Ve a Reputation → Requests → Crea una campaña → Configura timing

4. ¿Cómo configuro el calendario?
   Respuesta: Ve a Calendars → Create Calendar → Configura disponibilidad

5. ¿Cómo conecto WhatsApp?
   Respuesta: Ve a Settings → WhatsApp → Connect your business account

INSTRUCCIONES:
- Responde siempre de forma amable
- Si no sabes la respuesta, pide paciencia y dice que transferirás a un técnico
- Usa emojis para hacer la conversación más amigable
"""

# --- CREAR EL AGENTE ---

agente_soporte = Agent(
    model='gemini-2.0-flash',
    name='soporte_message_design',
    instruction=FAQ_SOPORTE,
    description="Agente de soporte para clientes de Message Design"
)

root_agent = agente_soporte
```

### Ejecútalo:

```bash
adk run mi_primer_agente
```

**Prueba diciendo:**
- "Hola, necesito ayuda para configurar Google Business"
- "¿Cómo activo las reseñas automáticas?"
- "No puedo conectar mi dominio"

---

## NIVEL 5: Interfaz Web (Para que clientes hablen con él) 🌐

### Ejecutar con interfaz web:

```bash
adk web --port 8000
```

1. Abre tu navegador
2. Ve a: http://localhost:8000
3. Selecciona tu agente
4. ¡Chatea con él!

### Para uso real (producción):

Necesitarás:
- Un servidor (puede ser Render, Railway, o tu propia PC)
- Un dominio
- Configuración de WhatsApp (Twilio o Botpress)

---

## NIVEL 6: Conectar a Herramientas Externas (MCP) 🔗

MCP = Model Context Protocol

Esto es como añadir "items" a tu personaje que le dan superpoderes:

```python
from google.adk.tools.mcp_tool import McpToolset
from google.adk.agents.llm_agent import Agent

# Ejemplo: Conectar a Google Maps
agente_con_mapa = Agent(
    model='gemini-2.0-flash',
    name='agente_con_mapa',
    instruction='Ayudas a encontrar lugares y dar direcciones',
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command='npx',
                    args=["-y", "@modelcontextprotocol/server-google-maps"],
                    env={"GOOGLE_MAPS_API_KEY": "TU_KEY_DE_MAPS"}
                )
            )
        )
    ]
)
```

---

## Comandos Útiles 📋

| Comando | Para qué sirve |
|---------|----------------|
| `pip install google-adk` | Instalar ADK |
| `adk create mi_agente` | Crear nuevo agente |
| `adk run mi_agente` | Ejecutar en terminal |
| `adk web --port 8000` | Ejecutar con interfaz web |
| `adk web` | Web UI en puerto 8000 por defecto |

---

## Estructura de Proyecto Completo

```
mi_proyecto/
├── agent.py           ← Código principal
├── .env              ← API keys
├── __init__.py       ← Necesario para ADK
└── tools/            ← Carpeta de herramientas
    ├── __init__.py
    └── mis_herramientas.py
```

---

## Próximos Pasos (Roadmap de Aprendizaje)

| Nivel | Lo que aprenderás |
|-------|------------------|
| 1-3 | ✅ Lo básico - Ya lo tienes |
| 4 | Añadir más preguntas al FAQ |
| 5 | Conectar a WhatsApp |
| 6 | Conectar a GoHighLevel (vía API) |
| 7 | Agente de voz (con Vapi/Bland AI) |
| 8 | Multi-agentes (equipo de agentes) |
| 9 | Desplegar en producción |

---

## Preguntas Frecuentes (FAQ) ❓

**P: ¿Cuánto cuesta esto?**
R: La API de Gemini es gratis para empezar (tiene crédito gratis). Después~$0.01/mensaje.

**P: ¿Necesito saber programar?**
R: No mucho. Solo copiar y pegar código. Pero sí ayuda entender lógica básica.

**P: ¿Puedo hacer un agente que habla por voz?**
R: Sí, con Vapi.ai o Bland AI. Pero eso es nivel avanzado.

**P: ¿Puedo conectar a mi cuenta de GoHighLevel?**
R: Sí, usando la API de GHL. ¡Eso sería muy útil para tu negocio!

---

## ¿Qué sigue?

1. **Copia el código del Nivel 3 o 4**
2. **Ejecútalo en tu computadora**
3. **Prueba chatear con él**
4. **Añade más preguntas al FAQ**

Cuando lo pruebes y funcione, dime y te ayudo con el siguiente nivel: **Conectar a WhatsApp** 📱
