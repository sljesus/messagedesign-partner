"""
API del Agente de Onboarding para GoHighLevel
Endpoints REST para integrar con widgets de chat web

Uso: uvicorn api_agente:app --reload
"""
import os
import sys
from threading import Lock
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Agregar path
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, base_dir)
sys.path.insert(0, os.path.join(base_dir, "agents", "onboarding"))

env_path = os.path.join(base_dir, "agents", ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

# Optional RAG (local index over docs/)
try:
    import rag
except Exception:
    rag = None

# Importar herramientas del agente
try:
    from agents.onboarding.onboarding_tools import (
        calcular_tiempo_optimizado,
        clasificar_tipo_cliente,
        generar_checklist,
        obtener_preguntas_calificacion,
        validar_documento,
    )
except ImportError:
    # Para despliegue en server, intentar importacion directa
    from onboarding_tools import (
        calcular_tiempo_optimizado,
        clasificar_tipo_cliente,
        generar_checklist,
        obtener_preguntas_calificacion,
        validar_documento,
    )

app = FastAPI(
    title="API Agente Onboarding - Message Design",
    description="API para integrar con GoHighLevel Chat Widget",
    version="1.1.0",
)

# Configurar CORS para permitir conexiones desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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


class KbQueryRequest(BaseModel):
    query: str
    top_k: int = 4


# Memoria simple por sesion (en proceso).
# Nota: en multiples replicas/reinicios, migrar esta memoria a Redis/DB.
SESSION_MEMORY = {}
SESSION_LOCK = Lock()


def _norm(texto: str) -> str:
    return (texto or "").lower().strip()


def _is_affirmative(texto: str) -> bool:
    t = _norm(texto)
    return t in {"si", "sí", "ok", "claro", "adelante", "continuar"} or "si, continuar" in t or "sí, continuar" in t


def _is_more_info(texto: str) -> bool:
    t = _norm(texto)
    return "mas informacion" in t or "más información" in t or "paso a paso" in t or "pasos" in t


def _service_from_message(texto: str) -> Optional[str]:
    t = _norm(texto)
    if "reseña" in t or "resena" in t or "reseñas" in t or "resenas" in t:
        return "resenas"
    if "whatsapp" in t:
        return "whatsapp_api"
    if "suite" in t or "completa" in t:
        return "suite"
    if "calendario" in t:
        return "calendario"
    return None


def _service_label(service_key: Optional[str]) -> str:
    labels = {
        "resenas": "Reseñas",
        "whatsapp_api": "WhatsApp Business API",
        "suite": "Suite Completa",
        "calendario": "Calendario",
    }
    return labels.get(service_key, "el servicio")


def _service_steps(service_key: Optional[str]) -> str:
    if service_key == "whatsapp_api":
        return (
            "Paso a paso para conectar WhatsApp Business API:\n"
            "1. Validar documentos y numero dedicado\n"
            "2. Verificar/crear Meta Business Manager\n"
            "3. Iniciar verificacion empresarial (1-5 dias)\n"
            "4. Configurar numero y plantillas\n"
            "5. Conectar en CRM y hacer pruebas\n\n"
            "Tiempo total estimado: 3-7 dias habiles."
        )
    if service_key == "resenas":
        return (
            "Paso a paso para activar Reseñas:\n"
            "1. Acceso admin a Google Business Profile\n"
            "2. Configurar dominio y DNS\n"
            "3. Activar widget y solicitudes automaticas\n"
            "4. Probar flujo de solicitud y seguimiento\n\n"
            "Tiempo total estimado: 1-2 dias."
        )
    if service_key == "suite":
        return (
            "Paso a paso para Suite Completa:\n"
            "1. Validar documentos y accesos\n"
            "2. Configurar Reseñas y dominio\n"
            "3. Implementar WhatsApp Business API\n"
            "4. Calendario + CRM + funnels\n"
            "5. Pruebas end-to-end y capacitacion\n\n"
            "Tiempo total estimado: 3-7 dias habiles."
        )
    return (
        "Paso a paso general:\n"
        "1. Confirmar servicio\n"
        "2. Recolectar documentos y accesos\n"
        "3. Configuracion tecnica\n"
        "4. Pruebas y entrega"
    )


def _rag_answer(query: str, top_k: int = 4) -> Optional[dict]:
    if rag is None:
        return None
    try:
        hits = rag.search(query, top_k=top_k)
    except Exception:
        return None
    if not hits:
        return None
    bullets = []
    sources = []
    for h in hits:
        snippet = h.text.strip().replace("\n", " ")
        if len(snippet) > 350:
            snippet = snippet[:347] + "..."
        bullets.append(f"- {snippet}")
        sources.append(h.source)
    return {
        "respuesta": "Encontre en la documentacion:\n" + "\n".join(bullets),
        "fuentes": list(dict.fromkeys(sources)),
    }


def _get_session(session_id: str) -> dict:
    with SESSION_LOCK:
        session = SESSION_MEMORY.setdefault(
            session_id,
            {
                "selected_service": None,
                "stage": "menu",
                "last_intent": None,
                "turns": 0,
            },
        )
        session["turns"] += 1
        return session


# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/")
def root():
    return {
        "status": "online",
        "agente": "Message Design Onboarding",
        "version": "1.1.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/kb_query")
def kb_query(request: KbQueryRequest):
    """
    Consulta el indice local de docs/ (RAG).
    """
    result = _rag_answer(request.query, top_k=request.top_k)
    if result is None:
        return {"success": False, "data": [], "message": "No hay indice o no hay resultados"}
    return {"success": True, "data": result}


@app.post("/chat")
def chat(request: MensajeRequest):
    """
    Endpoint principal para chat con memoria simple por session_id.
    """
    mensaje = _norm(request.mensaje)
    session_id = request.session_id or "default"
    session = _get_session(session_id)

    # Continuidad por etapa
    if _is_affirmative(mensaje) and session.get("stage") == "awaiting_service_decision":
        with SESSION_LOCK:
            session["stage"] = "awaiting_docs_confirmation"
            session["last_intent"] = "continue_after_service"
        return {
            "respuesta": (
                f"Excelente, continuamos con {_service_label(session.get('selected_service'))}. "
                "Siguiente paso: validar documentacion y accesos. "
                "¿Ya cuentas con acta/RFC, identificacion, comprobante y accesos necesarios?"
            ),
            "opciones": ["Sí, tengo todo", "Me falta documentación"],
            "session_state": session,
        }

    if _is_more_info(mensaje) and session.get("selected_service"):
        with SESSION_LOCK:
            session["stage"] = "awaiting_service_decision"
            session["last_intent"] = "more_info"
        return {
            "respuesta": _service_steps(session.get("selected_service")),
            "opciones": ["Sí, continuar", "Qué documentos necesito"],
            "session_state": session,
        }

    # Seleccion de servicio (hilo principal)
    selected_service = _service_from_message(mensaje)
    if selected_service == "resenas":
        try:
            resultado = generar_checklist(["resenas"])
        except Exception:
            resultado = None
        with SESSION_LOCK:
            session["selected_service"] = "resenas"
            session["stage"] = "awaiting_service_decision"
            session["last_intent"] = "service_overview"
        return {
            "respuesta": (
                "Perfecto. El sistema de reseñas incluye:\n"
                "- Conexión con Google Business\n"
                "- Widgets de solicitud de reseñas\n"
                "- Automatización de seguimiento\n\n"
                "Tiempo: 1-2 días.\n\n"
                "¿Te interesa proceder?"
            ),
            "opciones": ["Sí, continuar", "Más información"],
            "checklist": resultado,
            "session_state": session,
        }

    if selected_service == "whatsapp_api":
        try:
            resultado = generar_checklist(["whatsapp_api"])
            num_clientes = request.contexto.get("num_clientes") if request.contexto else 1
            tiempo = calcular_tiempo_optimizado(["whatsapp_api"], num_clientes or 1)
            tiempo_str = tiempo.get("tiempo_estimado_dias", "2-3") if tiempo else "2-3"
        except Exception:
            resultado = None
            tiempo_str = "2-3"
        with SESSION_LOCK:
            session["selected_service"] = "whatsapp_api"
            session["stage"] = "awaiting_service_decision"
            session["last_intent"] = "service_overview"
        return {
            "respuesta": (
                "WhatsApp Business API incluye:\n"
                "- Número dedicado\n"
                "- Chatbots automatizados\n"
                "- CRM integrado\n"
                "- Multimedia y respuestas rápidas\n\n"
                f"Tiempo estimado: {tiempo_str} días"
            ),
            "opciones": ["Sí, continuar", "Más información"],
            "checklist": resultado,
            "session_state": session,
        }

    if selected_service == "suite":
        try:
            resultado = generar_checklist(["resenas", "whatsapp_api", "calendario", "funnels", "crm"])
            num_clientes = request.contexto.get("num_clientes") if request.contexto else 1
            tiempo = calcular_tiempo_optimizado(
                ["resenas", "whatsapp_api", "calendario", "funnels", "crm"],
                num_clientes or 1,
            )
            tiempo_str = tiempo.get("tiempo_estimado_dias", "3-5") if tiempo else "3-5"
        except Exception:
            resultado = None
            tiempo_str = "3-5"
        with SESSION_LOCK:
            session["selected_service"] = "suite"
            session["stage"] = "awaiting_service_decision"
            session["last_intent"] = "service_overview"
        return {
            "respuesta": (
                "Suite Completa incluye:\n"
                "- Sistema de reseñas 5 estrellas\n"
                "- WhatsApp Business API\n"
                "- Calendario de citas\n"
                "- Funnels y páginas\n"
                "- CRM completo\n\n"
                f"Tiempo estimado: {tiempo_str} días"
            ),
            "opciones": ["Sí, continuar", "Solicitar cotización"],
            "checklist": resultado,
            "session_state": session,
        }

    if selected_service == "calendario":
        with SESSION_LOCK:
            session["selected_service"] = "calendario"
            session["stage"] = "awaiting_service_decision"
            session["last_intent"] = "service_overview"
        return {
            "respuesta": (
                "Calendario de citas incluye:\n"
                "- Configuración de disponibilidad\n"
                "- Recordatorios automáticos\n"
                "- Integración con CRM\n\n"
                "Tiempo estimado: 1 día."
            ),
            "opciones": ["Sí, continuar", "Más información"],
            "session_state": session,
        }

    if "hola" in mensaje or "buenos" in mensaje:
        with SESSION_LOCK:
            session["stage"] = "menu"
            session["last_intent"] = "greeting"
        return {
            "respuesta": (
                "Hola. Soy el asistente de Message Design. "
                "¿Qué servicio te interesa? (Reseñas, WhatsApp, Calendario, Suite Completa)"
            ),
            "opciones": ["Reseñas", "WhatsApp", "Calendario", "Suite Completa"],
            "session_state": session,
        }

    if "tiempo" in mensaje or "cuánto" in mensaje or "cuanto" in mensaje:
        return {
            "respuesta": (
                "El tiempo depende de los servicios:\n\n"
                "- Reseñas: 1-2 días\n"
                "- WhatsApp: 2-3 días\n"
                "- Calendario: 1 día\n"
                "- Suite completa: 3-5 días\n\n"
                "¿Quieres que calcule para tu caso específico?"
            ),
            "opciones": ["Calcular mi caso"],
            "session_state": session,
        }

    if "documentos" in mensaje or "qué necesito" in mensaje or "que necesito" in mensaje:
        with SESSION_LOCK:
            session["stage"] = "awaiting_docs_confirmation"
            session["last_intent"] = "docs_request"
        return {
            "respuesta": (
                "Para iniciar necesitamos:\n\n"
                "1. Acta constitutiva o RFC\n"
                "2. Identificación del representante\n"
                "3. Comprobante de domicilio\n"
                "4. Acceso a Google Business (si tienes)\n"
                "5. Número de WhatsApp dedicado\n\n"
                "¿Te falta alguno de estos?"
            ),
            "opciones": ["Tengo todo", "Necesito ayuda con uno"],
            "session_state": session,
        }

    if "necesito ayuda con uno" in mensaje or ("me falta" in mensaje and "doc" in mensaje):
        with SESSION_LOCK:
            session["stage"] = "awaiting_missing_doc_detail"
            session["last_intent"] = "missing_doc_help"
        return {
            "respuesta": (
                "Te ayudo con eso. Dime cuál te falta para darte el siguiente paso exacto:\n"
                "1) Acta/RFC\n2) Identificación\n3) Comprobante\n4) Google Business\n5) Número WhatsApp"
            ),
            "opciones": ["Acta/RFC", "Identificación", "Comprobante", "Google Business", "Número WhatsApp"],
            "session_state": session,
        }

    # Fallback con continuidad de hilo
    if session.get("selected_service") and session.get("stage") in {
        "awaiting_service_decision",
        "awaiting_docs_confirmation",
        "awaiting_missing_doc_detail",
    }:
        return {
            "respuesta": (
                f"Seguimos con {_service_label(session.get('selected_service'))}. "
                "¿Quieres paso a paso, documentos requeridos o tiempo estimado?"
            ),
            "opciones": ["Paso a paso", "Documentos", "Tiempo estimado"],
            "session_state": session,
        }

    rag_result = _rag_answer(mensaje, top_k=4)
    if rag_result:
        return {
            "respuesta": rag_result["respuesta"],
            "opciones": ["Reseñas", "WhatsApp", "Calendario", "Suite"],
            "fuentes": rag_result.get("fuentes", []),
            "session_state": session,
        }

    with SESSION_LOCK:
        session["stage"] = "menu"
        session["last_intent"] = "fallback_menu"
    return {
        "respuesta": (
            "Entendido. ¿Te gustaría información sobre:\n\n"
            "- Reseñas Google\n"
            "- WhatsApp Business API\n"
            "- Calendario de citas\n"
            "- Suite completa\n\n"
            "Responde con el servicio que te interese."
        ),
        "opciones": ["Reseñas", "WhatsApp", "Calendario", "Suite"],
        "session_state": session,
    }


@app.post("/checklist")
def get_checklist(request: ChecklistRequest):
    """
    Genera checklist segun servicios
    """
    try:
        resultado = generar_checklist(request.servicios)
        return {"success": True, "data": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tiempo")
def get_tiempo(request: TiempoRequest):
    """
    Calcula tiempo de implementacion
    """
    try:
        resultado = calcular_tiempo_optimizado(
            servicios=request.servicios,
            num_clientes=request.num_clientes,
            complejidad=request.complejidad,
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
