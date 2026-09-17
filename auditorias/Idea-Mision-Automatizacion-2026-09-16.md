# 🤖 MISION.md como Super-Sistema con IA — Automatización Sostenible

> **Origen:** Idea-Mision-Canon-2026-09-13 · **Reescritura:** 2026-09-16
> **Enfoque:** de asistencia puntual → sistemas que corren solos 24/7
> **Premisa:** cada idea = loop autónomo (cron + pipeline + auto-monitoreo + recuperación sin intervención).

## CAPA 1 — mision.md como cañón autónomo

| # | Idea original (1 línea) | Sistema autónomo que corre solo |
|---|---|---|
| 1 | MIT auto diario (1 tarea 🏆) | Cron 5:00 AM lee HOY+PROYECTOS, marca 🏆, si ayer MIT falló auto-ajusta criterio y lo registra. |
| 2 | Time-blocking auto por ventanas | Cron 5:10 AM genera bloques desde horas+SEMANA, si bloque se solapa re-planifica solo y avisa. |
| 3 | Carry-forward con contador ×N | Pipeline reactivo: detecta `[ ]` 2+ días vía snapshot, re-escribe con `(×N)`, escala a alerta si ×3. |
| 4 | Recordatorios con hora (HOY/MAÑANA/SEMANA) | Cron detector cada turno crea `cron add` por cada `— HH:MM` nuevo, se auto-limpia al completarse. |
| 5 | Scoring del día X/9 + racha | Cron 9:30 PM calcula score, escribe en registro-diario, si falla el write reintenta y guarda backlog. |
| 6 | Briefing pre-trabajo 7:45 AM | Cron 7:45 AM lee HOY+ayer, envía 3 líneas; si Telegram falla guarda en registro para reenvío. |
| 7 | Cierre P&L de tiempo 9:30 PM | Cron 9:30 PM compara plan vs real, escribe P&L, alimenta al briefing de mañana (loop cerrado). |
| 8 | Detector arrastres crónicos (≥3 días) | Job diario compara snapshots, marca 🔴 crónico y propone eliminar/delegar solo. |
| 9 | Streak hábitos (Gym/Lectura/Creatina) | Cron Vie lee HÁBITOS+registros, calcula racha, si hay gap auto-inserta recordatorio en HOY. |
| 10 | Micro-decisión nocturna 30 min (Ghost o Meta) | Cron 18:30 lee avance+energía SEMANA, decide 1 foco; aprende de cierres previos (feedback loop). |
| 11 | Pre-mortem matutino (2 riesgos) | Cron 6:30 AM cruza HOY+horario L-V, lista 2 riesgos y pre-crea plan B como subtarea. |
| 12 | Compresión semanal auto (Dom 9 PM) | Cron Dom archiva completadas, crea HOY/MAÑANA nuevos; si falla hace backup antes de editar. |
| 13 | Balance carga mañana vs noche | Monitor por turno cuenta tareas/bloque, si noche >3 auto-propone mover 1 y lo deja listo. |
| 14 | Costo oportunidad ($/meta 300M) | Pipeline etiqueta `💰/🧱/🧹` cada tarea nueva, reporte semanal auto de % en 💰directo. |
| 15 | Check 2-min (desglosar >2h) | Detector: tarea proyecto sin sub-pasos → genera 3 sub-pasos y los deja encolados para aprobar. |
| 16 | Anti-duplicados HOY vs PROYECTOS | Job por turno compara strings, fusiona duplicados y deja 1 SSOT con link. |
| 17 | Ventana libre detector (huecos SEMANA) | Cron diario escanea celdas vacías, auto-llena con backlog priorizado por 💰. |
| 18 | Revisión Vie 18 pre-llenada | Cron Vie 5 PM agrega Lun-Vie, genera borrador revisión y lo deja en registro listo. |
| 19 | Hábito→tarea (si Gym ❌ forzar en HOY) | Loop: si HÁBITOS falla ayer, auto-inserta en HOY hoy con hora sugerida. |
| 20 | Identidad check (¿alimenta IDENTIDAD?) | Cron noche: 1 línea "hoy alimentas X", acumula score identidad semanal auto. |

## CAPA 2 — Cruces mision × notas como pipelines

| # | Cruce original | Pipeline autónomo |
|---|---|---|
| 1 | HOY Ghost ↔ Plan-v2.2 (sub-paso exacto) | Cron noche trae fase+archivo exactos del plan, avanza puntero solo al completarse. |
| 2 | HOY Ghost ↔ Arquitectura (checklist noche) | Pipeline genera checklist MT5→estrategia→test, valida completados contra plan. |
| 3 | Meta nicho ↔ notas Ads (evitar re-trabajo) | `qmd search` auto trae nichos investigados a cada tarea Meta nueva, cita fuente. |
| 4 | Lectura ↔ última LECTURAS-DIARIAS | Monitor: si cron lectura falló, retoma donde quedó y reprograma solo. |
| 5 | Scoring ↔ registro-diario (loop cierre→briefing) | Loop cerrado: cierre escribe score, briefing lee ayer y ajusta MIT sin manual. |
| 6 | SEMANA ↔ registros (% avance Ghost) | Cron Dom calcula noches trabajadas/proyecto, publica % sin intervención. |
| 7 | ITM ↔ notas educación (requisitos) | Pipeline `qmd` reúne requisitos una vez, cachea y reusa en cada tarea ITM. |
| 8 | Ingresos ↔ Recordatorios finanzas | Monitor: si "proyecciones" pendiente desde Vie, escala alerta y sube prioridad solo. |
| 9 | Prototipo X ↔ carpeta sensor | Cron Mié trae estado sensor + próximo paso, actualiza puntero al cerrar. |
| 10 | HÁBITOS ↔ habito-lectura (corrige drift) | Job semanal compara declarado vs último registro real, corrige drift y reporta. |

## CAPA 3 — Vault como OS que se auto-opera

| # | Sistema original | Versión autónoma 24/7 |
|---|---|---|
| 1 | Q&A sobre vault | Servicio siempre-on: `qmd` responde con cita, log de preguntas alimenta FAQ auto. |
| 2 | Resumen semanal auto Dom 9 PM | Cron Dom agrega registros+mision → 10 líneas, si faltan datos marca hueco y estima. |
| 3 | Knowledge graph liviano | Script mensual mapea Ghost↔Finanzas↔Meta, publica qué tema alimenta 300M. |
| 4 | Memoria two-zone (RAM/disco) | Regla dura: briefing solo RAM+ayer; full-scan bloqueado, auto-audita violaciones. |
| 5 | Detector contradicciones | Job mensual `qmd` mismo tema, si 2 notas difieren abre reporte para resolver. |
| 6 | Ideas compuestas trimestrales | Pipeline trimestral cruza Fitness×Finance×E-com, propone 1 experimento con margen. |
| 7 | Archivo inteligente >90 días | Monitor lista candidatas a `archivo/`, mueve solo con aprobación, mantiene índice. |
| 8 | Dashboard Dom | Cron Dom: 1 mensaje score+rachas+P&L+MIT; si cron falla, reintenta y acumula. |

## ⚡ Priorización (loops primero)

- **P0 hoy:** C1-1,4,6,8,13 + C2-1,5 + C3-1,4 (crons lectura + Q&A, sin installs).
- **P1 semana:** C1-5,7,9,12,18 + C2-2,4,6,10 + C3-2,8 (writes registro/mision, loops cierre→briefing).
- **P2 mes:** resto (graph, contradicciones, archivo con aprobación).

*38 sistemas autónomos: C1=20, C2=10, C3=8. Regla: todo loop lleva monitor + reintento + log.*

`🦾 H.E.L.E.N. — Si está aquí, está priorizado.`
