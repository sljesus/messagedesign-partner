"""
Herramientas del Agente de Onboarding para Message Design
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ============================================================
# HERRAMIENTAS DEL AGENTE
# ============================================================

def clasificar_tipo_cliente(contexto: Dict) -> Dict:
    """
    Clasifica el tipo de cliente basado en la información proporcionada
    """
    tipo = contexto.get("tipo", "")
    num_empleados = contexto.get("num_empleados", 0)
    sector = contexto.get("sector", "")
    
    # Lógica de clasificación
    if "agencia" in tipo.lower():
        return {
            "tipo": "Agencia",
            "complejidad_estimada": "alta",
            "servicios_recomendados": ["suite_completa"],
            "nota": "Agencias requieren múltiples cuentas y automaciones complejas"
        }
    elif "pyme" in tipo.lower() or "negocio" in tipo.lower():
        return {
            "tipo": "PYME",
            "complejidad_estimada": "media",
            "servicios_recomendados": ["whatsapp_api", "resenas"],
            "nota": "PYMEs típicamente necesitan WhatsApp y reseñas"
        }
    elif "startup" in tipo.lower():
        return {
            "tipo": "Startup",
            "complejidad_estimada": "media-alta",
            "servicios_recomendados": ["suite_completa", "funnels"],
            "nota": "Startups necesitan escalabilidad desde el inicio"
        }
    else:
        return {
            "tipo": "General",
            "complejidad_estimada": "baja",
            "servicios_recomendados": ["whatsapp_api"],
            "nota": "Evaluación adicional necesaria"
        }


def generar_checklist(servicios: List[str]) -> Dict:
    """
    Genera un checklist personalizado según los servicios solicitados
    """
    # Definición de requisitos por servicio
    requisitos_por_servicio = {
        "resenas": [
            {"id": "google_business", "nombre": "Acceso a Google Business Profile", "tipo": "acceso", "obligatorio": True},
            {"id": "logo", "nombre": "Logo de la empresa en alta calidad", "tipo": "archivo", "obligatorio": True},
            {"id": "fotos", "nombre": "Fotos del negocio (opcional)", "tipo": "archivo", "obligatorio": False},
        ],
        "whatsapp_api": [
            {"id": "acta_constitutiva", "nombre": "Acta constitutiva o registro legal", "tipo": "documento", "obligatorio": True},
            {"id": "id_representante", "nombre": "Identificación oficial del representante legal", "tipo": "documento", "obligatorio": True},
            {"id": "domicilio", "nombre": "Comprobante de domicilio empresarial", "tipo": "documento", "obligatorio": True},
            {"id": "sitio_web", "nombre": "Página web con aviso de privacidad", "tipo": "url", "obligatorio": True},
            {"id": "meta_bm", "nombre": "Acceso a Meta Business Manager", "tipo": "acceso", "obligatorio": True},
            {"id": "telefono_exclusivo", "nombre": "Número telefónico exclusivo para WhatsApp API", "tipo": "informacion", "obligatorio": True},
            {"id": "tarjeta_bancaria", "nombre": "Tarjeta bancaria para cobros de Meta", "tipo": "informacion", "obligatorio": False},
            {"id": "opcion_whatsapp", "nombre": "Opción: Conectar app existente o número nuevo", "tipo": "decision", "obligatorio": True},
        ],
        "calendario": [
            {"id": "horarios", "nombre": "Horarios de atención", "tipo": "informacion", "obligatorio": True},
            {"id": "servicios", "nombre": "Lista de servicios/duración", "tipo": "informacion", "obligatorio": True},
            {"id": "empleados", "nombre": "Nombres de empleados/responsables", "tipo": "informacion", "obligatorio": False},
        ],
        "funnels": [
            {"id": "logo", "nombre": "Logo de la empresa", "tipo": "archivo", "obligatorio": True},
            {"id": "colores", "nombre": "Colores品牌", "tipo": "informacion", "obligatorio": True},
            {"id": "textos", "nombre": "Textos para páginas (opcional)", "tipo": "documento", "obligatorio": False},
        ],
        "crm": [
            {"id": "pipelines", "nombre": "Definición de pipelines de venta", "tipo": "informacion", "obligatorio": True},
            {"id": "campos", "nombre": "Campos personalizados necesarios", "tipo": "informacion", "obligatorio": False},
        ]
    }
    
    # Agregar también lo que otros servicios requieren
    todos_requisitos = {}
    
    for servicio in servicios:
        if servicio in requisitos_por_servicio:
            for req in requisitos_por_servicio[servicio]:
                todos_requisitos[req["id"]] = req
    
    # Clasificar requisitos
    documentos = []
    informacion = []
    accesos = []
    archivos = []
    decisiones = []
    
    for req in todos_requisitos.values():
        if req["tipo"] == "documento":
            documentos.append(req)
        elif req["tipo"] == "informacion":
            informacion.append(req)
        elif req["tipo"] == "acceso":
            accesos.append(req)
        elif req["tipo"] == "archivo":
            archivos.append(req)
        elif req["tipo"] == "decision":
            decisiones.append(req)
    
    # Calcular tiempo estimado
    tiempo_base = {
        "resenas": "1-2 días",
        "whatsapp_api": "1-5 días (verificación Meta) + 1-2 días (plantillas)",
        "calendario": "1 día",
        "funnels": "2-3 días",
        "crm": "1-2 días"
    }
    
    tiempo_total = []
    for s in servicios:
        if s in tiempo_base:
            tiempo_total.append(tiempo_base[s])
    
    return {
        "fecha_generacion": datetime.now().isoformat(),
        "servicios": [{"id": s, "nombre": s.replace("_", " ").title()} for s in servicios],
        "requisitos_totales": list(todos_requisitos.values()),
        "documentos_requeridos": [r["nombre"] for r in documentos],
        "informacion_requerida": [r["nombre"] for r in informacion],
        "accesos_requeridos": [r["nombre"] for r in accesos],
        "archivos_requeridos": [r["nombre"] for r in archivos],
        "decisiones_requeridas": [r["nombre"] for r in decisiones],
        "tiempo_estimado_total": ", ".join(tiempo_total) if tiempo_total else "1-3 días"
    }


def calcular_tiempo_optimizado(servicios: List[str], num_clientes: int = 1, complejidad: str = "media") -> Dict:
    """
    Calcula el tiempo de implementación usando metodología IEEE
    """
    # Puntos de función por servicio
    puntos_por_servicio = {
        "resenas": 8,
        "whatsapp_api": 21,
        "calendario": 8,
        "funnels": 15,
        "crm": 13,
    }
    
    # Calcular puntos totales
    pf_total = sum(puntos_por_servicio.get(s, 5) for s in servicios)
    
    # Factor de ajuste por complejidad
    factores = {
        "baja": 0.8,
        "media": 1.0,
        "alta": 1.3,
        "muy_alta": 1.5
    }
    
    factor = factores.get(complejidad, 1.0)
    pf_ajustado = pf_total * factor
    
    # Factor de volumen (clientes adicionales)
    factor_volumen = 1 + (num_clientes - 1) * 0.1
    pf_final = pf_ajustado * factor_volumen
    
    # Convertir a días (asumiendo 8 horas/día y velocidad de 10 PF/día)
    dias_base = pf_final / 10
    dias_min = int(dias_base * 0.8)
    dias_max = int(dias_base * 1.2)
    
    # Ruta crítica
    ruta_critica = []
    if "whatsapp_api" in servicios:
        ruta_critica.extend(["verificacion_meta", "aprobacion_plantillas"])
    if "resenas" in servicios:
        ruta_critica.append("verificacion_google")
    if "funnels" in servicios:
        ruta_critica.append("propagacion_dns")
    
    return {
        "servicios": servicios,
        "num_clientes": num_clientes,
        "complejidad": complejidad,
        "puntosFuncion": int(pf_final),
        "factorVolumen": round(factor_volumen, 2),
        "tiempo_estimado_dias": f"{dias_min}-{dias_max}",
        "tiempo_optimo_dias": int(dias_base),
        "ruta_critica": ruta_critica,
        "nota": "Tiempos incluye verificación de Meta (variable)"
    }


def obtener_preguntas_calificacion(tipo_cliente: str) -> List[Dict]:
    """
    Obtiene las preguntas de calificación según el tipo de cliente
    """
    preguntas_base = [
        {"id": "nombre", "pregunta": "¿Cuál es el nombre de tu empresa?", "tipo": "texto"},
        {"id": "sector", "pregunta": "¿En qué sector opera tu negocio?", "tipo": "opcion", "opciones": ["Retail", "Servicios", "Salud", "Educación", "Tecnología", "Otro"]},
        {"id": "empleados", "pregunta": "¿Cuántos empleados tiene tu empresa?", "tipo": "numero"},
    ]
    
    preguntas_whatsapp = [
        {"id": "whatsapp_actual", "pregunta": "¿Ya tienes WhatsApp Business?", "tipo": "si_no"},
        {"id": "numero_dedicado", "pregunta": "¿Tienes un número dedicado para la API?", "tipo": "si_no"},
    ]
    
    if tipo_cliente == "whatsapp":
        return preguntas_base + preguntas_whatsapp
    
    return preguntas_base


def validar_documento(tipo_documento: str, archivo_contenido: str) -> Dict:
    """
    Valida un documento cargado por el cliente
    """
    # Simulación de validación
    validaciones = {
        "acta_constitutiva": {"valido": True, "nota": "Documento看起来 válido"},
        "id_representante": {"valido": True, "nota": "ID verificado"},
        "domicilio": {"valido": True, "nota": "Comprobante válido"},
    }
    
    resultado = validaciones.get(tipo_documento, {"valido": False, "nota": "Tipo de documento no reconocido"})
    
    return {
        "tipo": tipo_documento,
        "valido": resultado["valido"],
        "nota": resultado["nota"],
        "timestamp": datetime.now().isoformat()
    }


# ============================================================
# EXPORTAR HERRAMIENTAS PARA EL AGENTE
# ============================================================

HERRAMIENTAS = [
    {
        "name": "clasificar_tipo_cliente",
        "description": "Clasifica el tipo de cliente (agencia, PYME, startup, etc.)",
        "function": clasificar_tipo_cliente
    },
    {
        "name": "generar_checklist", 
        "description": "Genera checklist de requisitos según servicios solicitados",
        "function": generar_checklist
    },
    {
        "name": "calcular_tiempo_optimizado",
        "description": "Calcula tiempo de implementación con algoritmo optimizado",
        "function": calcular_tiempo_optimizado
    },
    {
        "name": "obtener_preguntas_calificacion",
        "description": "Obtiene preguntas de calificación para el cliente",
        "function": obtener_preguntas_calificacion
    },
    {
        "name": "validar_documento",
        "description": "Valida documentos cargados por el cliente",
        "function": validar_documento
    }
]
