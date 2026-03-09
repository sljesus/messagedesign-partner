import os
os.environ["OLLAMA_API_BASE"] = "http://localhost:11434"

from google.adk.agents.llm_agent import Agent
from google.adk.models import LiteLlm

# ============================================================
# CONTEXTO COMPLETO DEL NEGOCIO
# ============================================================

CONTEXTO_NEGOCIO = """
# CONTEXTO: SST México - Message Design

## INFORMACIÓN DEL NEGOCIO

- **Agencia:** Message Design (cuenta staff de GoHighLevel)
- **Prestador de servicios:** SST México
- **Servicios:** Soporte técnico, ventas y gestión de la plataforma

## SERVICIOS OFRECIDOS (Priorizados)

1. ⭐ SISTEMA DE RESEÑAS 5 ESTRELLAS (PRIORIDAD #1)
   - Google Business Profile
   - Automatización de solicitud de reseñas
   - Flujo de salvamento (reviews < 4 estrellas → llamada interna)
   - Widgets y enlaces de reseñas

2. AUTOMATIZACIÓN DE CITAS
   - Configuración de calendarios
   - Agentes de IA para agendamiento
   - Confirmaciones y recordatorios automáticos

3. CONEXIÓN DE DOMINIOS
   - Configuración DNS en Cloudflare
   - Dominios para funnels y sitios web

4. FUNNELS Y SITES/WEB
   - Páginas web
   - Funnels de ventas

## MODELO DE NEGOCIO

SST México → Message Design (cuenta agencia GHL) → Clientes finales (PYMEs México)

## PRECIOS (MXN)

- Básico (solo reseñas): $800-$1,000/mes
- Intermedio (+ WhatsApp + Calendario): $1,200-$1,500/mes
- Completo: $1,800-$2,500/mes

## PROCESO DE VENTA

1. Identificar el problema (reseñas, llamadas perdidas, agenda)
2. Demo del sistema
3. Propuesta
4. Cierre

## PROCESO DE ONBOARDING

1. Checklist de requisitos
2. Configuración técnica (1-3 días)
3. Pruebas internas
4. Capacitación al cliente
5. Soporte continuo
"""

# ============================================================
# PRIORIDADES Y OBJETIVOS ACTUALES
# ============================================================

PRIORIDADES_ACTUALES = """
## PRIORIDADES Y OBJETIVOS DE SST MÉXICO

### Objetivo Principal
Vender servicios de Message Design a pequeños negocios en México

### Prioridades Actuales (en orden):

1. CONFIGURAR AGENTE DE SOPORTE
   - Agentede IA con Google ADK
   - Para responder preguntas de clientes
   - Conectado a WhatsApp (futuro)

2. IMPLEMENTAR SISTEMA DE RESEÑAS 5 ESTRELLAS
   - Flujo de salvamento automático
   - Widget de reseñas
   - Configuración Google Business

3. CONFIGURAR WHATSAPP BUSINESS
   - Conexión con GoHighLevel
   - Chatbots
   - Automatizaciones

4. CREAR MATERIALES DE VENTA
   - Presentaciones
   - Videos demo
   - Propuestas comerciales

5. CAPTAR PRIMEROS CLIENTES
   - Prospectar negocios locales
   - Ofrecer demo gratuita
   - Cerrar primeros contratos
"""

# ============================================================
# AGENTE PROJECT MANAGER
# ============================================================

agente_pm = Agent(
    model=LiteLlm(model="ollama_chat/llama3.2"),
    name='sst_mexico_pm',
    instruction=f"""
Eres el "Project Manager" de SST México. Tu trabajo es AYUDAR a priorizar tareas y recordar qué acciones tomar.

## QUIÉN ERES

Eres un asistente de productividad que conoce:
- El negocio de SST México (servicios de GoHighLevel)
- Los servicios que se ofrecen
- Los precios y proceso de venta
- Las prioridades actuales

## TU TRABAJO

Cuando el usuario te pregunte sobre qué hacer, tú debes:

1. **Recordar el contexto**: Usa la información de CONTEXTO_NEGOCIO
2. **Saber las prioridades**: Usa PRIORIDADES_ACTUALES
3. **Sugerir siguiente paso**: Basado en lo que ya se ha hecho
4. **Ayudar a planificar**: Qué hacer primero, segundo, tercero

## PREGUNTAS QUE DEBES SABER RESPONDER

- ¿Cuáles son los servicios que ofrece SST México?
- ¿Cuáles son los precios?
- ¿Cuál es el proceso de venta?
- ¿Qué debo hacer primero para empezar?
- ¿Cómo configuro el sistema de reseñas?
- ¿Cómo conecto un dominio?
- ¿Qué es el flujo de salvamento?

## CÓMO RESPONDER

- Sé práctico y directo
- Da solo la información necesaria
- Si hay varias tareas, ayuda a priorizar
- Si el usuario pregunta por algo técnico, consulta la documentación

## IMPORTANTE

- Cuando te pregunte "¿qué hago?" o "¿por dónde empiezo?", recommienda la siguiente acción basada en PRIORIDADES_ACTUALES
- Si ya hizo algo, ayúdele a identificar el siguiente paso
- Sé motivador pero realista
""",
    description="Agente Project Manager para SST México"
)

root_agent = agente_pm
