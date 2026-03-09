"""
API del Agente de Onboarding para GoHighLevel
Endpoints REST para integrar con widgets de chat web

Uso: uvicorn api_agente:app --reload
"""
import os
import sys
from typing import Optional

# Agregar path
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)
sys.path.insert(0, os.path.join(base_dir, 'agents', 'onboarding'))

from dotenv import load_dotenv
env_path = os.path.join(base_dir, "agents", ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Importar herramientas del agente
try:
    from agents.onboarding.onboarding_tools import (
        clasificar_tipo_cliente,
        generar_checklist,
        calcular_tiempo_optimizado,
        obtener_preguntas_calificacion,
        validar_documento
    )
except ImportError:
    # Para despliegue en server, intentar importación directa
    from onboarding_tools import (
        clasificar_tipo_cliente,
        generar_checklist,
        calcular_tiempo_optimizado,
        obtener_preguntas_calificacion,
        validar_documento
    )

app = FastAPI(
    title="API Agente Onboarding - Message Design",
    description="API para integrar con GoHighLevel Chat Widget",
    version="1.0.0"
)

# Modelos de solicitud
class MensajeRequest(BaseModel):
    mensaje: str
    session_id: Optional[str] = "default"
    contexto: Optional[dict] = {}

class ChecklistRequest(BaseModel):
    servicios: list

class TiempoRequest(BaseModel):
    servicios: list
    num_clientes: int = 1
    complejidad: str = "media"

# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/")
def root():
    return {
        "status": "online",
        "agente": "Message Design Onboarding",
        "version": "1.0.0"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/chat")
def chat(request: MensajeRequest):
    """
    Endpoint principal para chat con el agente
    """
    mensaje = request.mensaje.lower()
    
    # Lógica simple de respuestas
    if "hola" in mensaje or "buenos" in mensaje:
        return {
            "respuesta": "Hola! Soy el asistente de Message Design. ¿Qué servicio te interesa? (Reseñas, WhatsApp, Calendario, Suite Completa)",
            "opciones": ["Reseñas", "WhatsApp", "Calendario", "Suite Completa"]
        }
    
    elif "reseñas" in mensaje or "resenas" in mensaje:
        try:
            resultado = generar_checklist(["resenas"])
        except:
            resultado = None
        return {
            "respuesta": "Perfecto! El sistema de reseñas incluye:\n• Conexión con Google Business\n• Widgets de solicitud de reseñas\n• Automatización de seguimiento\n\nTiempo: 1-2 días\n\n¿Te interesa proceder?",
            "opciones": ["Sí, continuar", "Más información"],
            "checklist": resultado
        }
    
    elif "whatsapp" in mensaje:
        try:
            resultado = generar_checklist(["whatsapp_api"])
            num_clientes = request.contexto.get("num_clientes") if request.contexto else 1
            tiempo = calcular_tiempo_optimizado(["whatsapp_api"], num_clientes or 1)
            tiempo_str = tiempo.get('tiempo_estimado_dias', '2-3') if tiempo else '2-3'
        except:
            resultado = None
            tiempo_str = "2-3"
        return {
            "respuesta": f"WhatsApp Business API incluye:\n• Número dedicado\n• Chatbots automatizados\n• CRM integrado\n• Multimedia y respuestas rápidas\n\nTiempo estimado: {tiempo_str} días",
            "opciones": ["Sí, continuar", "Más información"],
            "checklist": resultado
        }
    
    elif "suite" in mensaje or "completa" in mensaje:
        try:
            resultado = generar_checklist(["resenas", "whatsapp_api", "calendario", "funnels", "crm"])
            num_clientes = request.contexto.get("num_clientes") if request.contexto else 1
            tiempo = calcular_tiempo_optimizado(
                ["resenas", "whatsapp_api", "calendario", "funnels", "crm"],
                num_clientes or 1
            )
            tiempo_str = tiempo.get('tiempo_estimado_dias', '3-5') if tiempo else '3-5'
        except:
            resultado = None
            tiempo_str = "3-5"
        return {
            "respuesta": f"Suite Completa incluye TODO:\n• Sistema de reseñas 5 estrellas\n• WhatsApp Business API\n• Calendario de citas\n• Funnels y páginas\n• CRM completo\n\nTiempo estimado: {tiempo_str} días",
            "opciones": ["Sí, continuar", "Solicitar cotización"],
            "checklist": resultado
        }
    
    elif "tiempo" in mensaje or "cuánto" in mensaje or "cuanto" in mensaje:
        return {
            "respuesta": "El tiempo depende de los servicios:\n\n• Reseñas: 1-2 días\n• WhatsApp: 2-3 días\n• Calendario: 1 día\n• Suite completa: 3-5 días\n\n¿Quieres que calcule para tu caso específico?",
            "opciones": ["Calcular mi caso"]
        }
    
    elif "documentos" in mensaje or "qué necesito" in mensaje or "que necesito" in mensaje:
        return {
            "respuesta": "Para iniciar necesitamos:\n\n1. Acta constitutiva o RFC\n2. Identificación del representante\n3. Comprobante de domicilio\n4. Acceso a Google Business (si tienes)\n5. Número de WhatsApp dedicado\n\n¿Te falta alguno de estos?",
            "opciones": ["Tengo todo", "Necesito ayuda con uno"]
        }
    
    else:
        return {
            "respuesta": "Entendido. ¿Te gustaría información sobre:\n\n• Reseñas Google\n• WhatsApp Business API\n• Calendario de citas\n• Suite completa\n\nResponde con el servicio que te interese.",
            "opciones": ["Reseñas", "WhatsApp", "Calendario", "Suite"]
        }


@app.post("/checklist")
def get_checklist(request: ChecklistRequest):
    """
    Genera checklist según servicios
    """
    try:
        resultado = generar_checklist(request.servicios)
        return {"success": True, "data": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tiempo")
def get_tiempo(request: TiempoRequest):
    """
    Calcula tiempo de implementación
    """
    try:
        resultado = calcular_tiempo_optimizado(
            servicios=request.servicios,
            num_clientes=request.num_clientes,
            complejidad=request.complejidad
        )
        return {"success": True, "data": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clasificar")
def clasificar(request: MensajeRequest):
    """
    Clasifica tipo de cliente
    """
    try:
        contexto = request.contexto or {}
        resultado = clasificar_tipo_cliente(contexto)
        return {"success": True, "data": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# EJEMPLO DE INTEGRACIÓN CON GHL
# ============================================================

"""
INSTRUCCIONES PARA GHL:

1. Despliega esta API en Render/Vercel (gratis)
2. En GHL, crea un Custom Chatbot
3. Configura Webhook en el chatbot:
   - URL: https://tu-api.onrender.com/chat
   - Método: POST
   - Body: {"mensaje": "{{message}}"}

O alternativamente, usa el widget HTML personalizado:

<script>
async function sendMessage(msg) {
    const response = await fetch('https://your-api.onrender.com/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({mensaje: msg})
    });
    const data = await response.json();
    return data.respuesta;
}
</script>
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
