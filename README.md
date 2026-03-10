# Message Design Partner Project

Repositorio mixto con dos frentes:

1. Runtime del agente de onboarding (API desplegada en Render).
2. Base documental y material de investigacion/comercial.

## Runtime (produccion)

- [api_agente.py](api_agente.py): API FastAPI principal (`/chat`, `/checklist`, `/tiempo`, `/clasificar`).
- [agents/onboarding/onboarding_tools.py](agents/onboarding/onboarding_tools.py): logica de checklist, tiempos y clasificacion.
- [chat_widget.html](chat_widget.html): cliente web simple para probar el endpoint `/chat`.
- [requirements.txt](requirements.txt): dependencias de ejecucion.

## Documentacion principal

- [docs/agency/onboarding_sop.md](docs/agency/onboarding_sop.md)
- [docs/agency/servicios_ghl.md](docs/agency/servicios_ghl.md)
- [docs/workflows/automatizacion_resenas.md](docs/workflows/automatizacion_resenas.md)
- [docs/guides/conexion_dominios.md](docs/guides/conexion_dominios.md)
- [docs/tech/dns_sstmexico.md](docs/tech/dns_sstmexico.md)
- [docs/tech/adk_curso_practico.md](docs/tech/adk_curso_practico.md)
- [docs/tech/guia_crear_agente_soporte.md](docs/tech/guia_crear_agente_soporte.md)
- [docs/market_study/messagedesign.md](docs/market_study/messagedesign.md)
- [docs/challenges/retos.md](docs/challenges/retos.md)
- [docs/platform/estructura_plataforma_message_design.md](docs/platform/estructura_plataforma_message_design.md)
- [docs/platform/settings_message_design.md](docs/platform/settings_message_design.md)
- [docs/partnership/comprehensive_proposal.md](docs/partnership/comprehensive_proposal.md)
- [docs/partnership/message_design_support_plan.md](docs/partnership/message_design_support_plan.md)
- [docs/partnership/message_design_speech.md](docs/partnership/message_design_speech.md)
- [docs/partnership/conversation_updates.md](docs/partnership/conversation_updates.md)

## Investigacion y soporte

- [scripts/transcribe.py](scripts/transcribe.py): script utilitario de transcripcion.
- [transcripts/696f99eeeb392b34c9fb4c9e.txt](transcripts/696f99eeeb392b34c9fb4c9e.txt)
- [transcripts/transcripcion_con_tiempo.txt](transcripts/transcripcion_con_tiempo.txt)
- `videos/`: activos pesados de video (no versionados por defecto).

## Seguridad y secretos

- No subir credenciales reales al repo.
- Usar `.env` local y plantillas `.env.example`.
