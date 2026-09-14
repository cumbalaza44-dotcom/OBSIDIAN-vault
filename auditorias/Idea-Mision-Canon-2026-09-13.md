# 🎯 IDEA: mision.md como Cañón + Vault como Sistema Operativo
**Fecha:** 2026-09-13 | **Autor:** H.E.L.E.N. (subagente) | **Para:** Mr. Jair
**Premisa:** un agente frontera + una nota central + 341 notas = OS personal.

## Notas clave detectadas
| # | Nota | Uso |
|---|------|-----|
| 1 | `mision.md` | Tasks central, SSOT (HOY 5, MAÑANA 4, SEMANA, HÁBITOS, 6 PROYECTOS) |
| 2 | `Ghost-Trader-Plan-Construccion-v2.2.md` | Plan maestro Ghost Trader |
| 3 | `FINANZAS-Y-PROYECTOS/Bot-mt5/Arquitectura-Ghost-Trader.md` | Arquitectura técnica GT |
| 4 | `LECTURAS-DIARIAS/` (40+ notas) | Corpus lectura diaria desde Jul |
| 5 | `registro-de-progreso-diario/` | Log diario de completados |

---
## CAPA 1 — mision.md como cañón (20 usos, solo nota → máximo jugo)
Formato: qué + cómo (lee/escribe/cron-tool).

| # | Uso | Cómo |
|---|-----|------|
| 1 | **MIT auto diario** (1 tarea que mueve 300M COP/año) | Lee HOY+PROYECTOS → marca 1 con 🏆. Escribe prefijo en mision. Cron 5:00 AM, solo lectura+edit. |
| 2 | **Time-blocking auto** (mapear tareas a ventanas 5:10-8 / 8-17 / 18:30-21:30) | Lee horas + SEMANA → propone bloques. Escribe tabla en respuesta Telegram, no toca vault. |
| 3 | **Carry-forward inteligente** (arrastres → MAÑANA con contador `×N`) | Lee HOY archivo + snapshot → si `[ ]` 2+ días, re-escribe con `(arrastre ×N)`. Edit mision. |
| 4 | **Recordatorios con hora** (ya existe, extender a SEMANA) | Lee `— HH:MM` en HOY/MAÑANA/SEMANA → `openclaw cron add`. Sistema reactivo actual. |
| 5 | **Scoring del día** (X/9 + % + racha) | Lee `[x]/[ ]` HOY+MAÑANA al cierre → escribe score en `registro-de-progreso-diario/YYYY-MM-DD.md`. Cron 9:30 PM. |
| 6 | **Briefing pre-trabajo 7:45 AM** | Lee HOY → Telegram 3 líneas: MIT + horario laboral + riesgo. Cron, solo lectura. |
| 7 | **Cierre P&L de tiempo 9:30 PM** | Lee completadas vs plan SEMANA → escribe P&L (ganado/perdido por bloque). Cron + write registro. |
| 8 | **Detector arrastres crónicos** (ITM lleva 7+ días) | Compara snapshot actual vs archivo Sáb/Dom → si tarea repite ≥3 días, alerta "🔴 crónico". Solo lectura. |
| 9 | **Streak hábitos** (Gym/Lectura/Creatina) | Lee tabla HÁBITOS + `[x]` diarios → calcula racha, escribe en respuesta. Cron semanal Vie. |
| 10 | **Micro-decisión 30 min** (noche: ¿Ghost o Meta?) | Lee HOY noche + PROYECTOS avance → recomienda 1 foco según energía/día SEMANA. Solo lectura. |
| 11 | **Pre-mortem matutino** (qué puede fallar hoy) | Lee HOY + horario L-V 8-17 → lista 2 riesgos (ej: ITM 06:00 antes del trabajo). Solo lectura. |
| 12 | **Compresión semanal auto** (Dom: archivar HOY→🗂️) | Lee HOY+MAÑANA completadas → mueve a sección archivo, crea nuevo HOY/MAÑANA. Edit mision, cron Dom 9 PM. |
| 13 | **Balance carga día** (mañana vs noche) | Cuenta tareas por bloque → si noche >3, sugiere mover 1 a mañana. Solo lectura. |
| 14 | **Costo oportunidad** (cada tarea → $/meta 300M) | Lee tarea + PROYECTOS Ingresos → etiqueta `💰directo / 🧱base / 🧹mante`. Solo lectura. |
| 15 | **Check 2-minutos** (¿tarea >2h? desglosar) | Si tarea sin sub-pasos y es proyecto (Ghost/Meta) → propone 3 sub-pasos. Respuesta, no escribe. |
| 16 | **Anti-duplicados** (misma tarea en HOY+PROYECTOS) | Compara strings HOY vs PROYECTOS/HOGAR → alerta duplicado. Solo lectura. |
| 17 | **Ventana libre detector** (huecos sin tarea) | Lee SEMANA tabla → encuentra celdas vacías/flex → sugiere backlog. Solo lectura. |
| 18 | **Revisión Vie 18 automática** (pre-llena revisión semanal) | Lee `[x]` Lun-Vie de registros → genera borrador revisión en respuesta. Cron Vie 5 PM. |
| 19 | **Hábito→tarea vinculación** (si Gym en HÁBITOS ❌, forzar en HOY) | Lee HÁBITOS último registro vs HOY → si falta, propone insertar. Solo lectura+pregunta. |
| 20 | **Identidad check** (¿tarea alimenta IDENTIDAD/GHOST?) | Lee HOY vs IDENTIDAD (Musical/Aventura/Estilo) → 1 línea "hoy alimentas X". Solo lectura. |

---
## CAPA 2 — mision.md × notas (10 cruces concretos)

| # | Cruce | Qué produce |
|---|-------|-------------|
| 1 | HOY Ghost ↔ `Ghost-Trader-Plan-v2.2.md` | Sub-paso exacto del plan para "prototipo funcional" (qué fase, qué archivo). |
| 2 | HOY Ghost ↔ `Arquitectura-Ghost-Trader.md` | Checklist técnico noche (ej: MT5 conexión → estrategia → test). |
| 3 | MAÑANA Meta nicho ↔ `FINANZAS-Y-PROYECTOS/` notas Ads | Trae nichos ya investigados, evita re-trabajo Ad Library. |
| 4 | Lectura diaria ↔ `LECTURAS-DIARIAS/última` | Si cron lectura falló, retoma donde quedó (última fecha sin nota). |
| 5 | Scoring ↔ `registro-de-progreso-diario/` | Cierre escribe score + arrastres; briefing lee ayer para ajustar hoy. |
| 6 | SEMANA tabla ↔ registros Lun-Dom | % avance real por proyecto (Ghost × noches trabajadas). |
| 7 | ITM/pregrados ↔ notas educación (qmd "universidad") | Reúne requisitos ya consultados, evita re-consultar. |
| 8 | Ingresos $1.050.000 ↔ `Recordatorios.md` finanzas | Alerta si "ajustar proyecciones" lleva pendiente desde Vie 11. |
| 9 | Prototipo X ↔ `PROTOTIPO X/` carpeta | Mié 16: trae estado sensor ultrasónico + próximo paso. |
| 10 | HÁBITOS tabla ↔ `habito-lectura/README.md` + registros | Último registro real (Sáb 8/08 lectura) vs declarado → corrige drift. |

---
## CAPA 3 — Vault completo como OS personal (8 sistemas)

| # | Sistema | Descripción (1-2 líneas) |
|---|---------|--------------------------|
| 1 | **Q&A sobre vault** | `qmd query` como memoria externa: "¿qué decidí de nicho Meta?" → respuesta con cita. Sin installs. |
| 2 | **Resumen semanal auto** (Dom 9 PM) | Agrega registros + mision archivo → 10 líneas: avance por proyecto, hábitos %, top arrastre. Cron + lectura. |
| 3 | **Knowledge graph liviano** | qmd links entre notas (Ghost↔Finanzas↔Meta) → mapa mensual de qué tema alimenta 300M. Script simple. |
| 4 | **Memoria two-zone real** | mision.md = RAM (hoy); vault = disco (historia). Regla: briefing solo lee RAM + ayer disco, nunca full-scan. |
| 5 | **Detector contradicciones** | qmd search mismo tema (ej: "presupuesto") → si 2 notas dicen distinto, alerta. Mensual. |
| 6 | **Ideas compuestas** (Fitness×Finance×E-com) | Cruce trimestral: ¿producto fitness vía Meta Ads con margen para 300M? Solo lectura + propuesta. |
| 7 | **Archivo inteligente** | Notas >90 días sin link → mover a `archivo/` con índice. Requiere aprobación (mueve archivos). |
| 8 | **Dashboard Dom** | 1 mensaje: score semana, rachas, P&L tiempo, MIT siguiente semana. Cron Dom, solo lectura. |

---
## Priorización IMPACTO/ESFUERZO

### P0 — Hoy, sin permisos (solo prompts/crons/lecturas)
C1: 1, 4, 6, 8, 13 | C2: 1, 5 | C3: 1, 4

### P1 — Esta semana, sin installs (nuevos crons + writes a registro/mision)
C1: 2, 5, 7, 9, 12, 18 | C2: 2, 4, 6, 10 | C3: 2, 8

### P2 — Requiere aprobación o diseño (mover archivos, graph, ideas compuestas)
C1: 14, 20 | C2: 7, 8 | C3: 3, 5, 6, 7

**Sin nuevos permisos ni installs:** todo P0 + P1 (crons, edits mision, writes registro, qmd). **Requiere aprobación:** C3-7 (mover archivos), cualquier `git push` primera vez, installs nuevos.

---
## Plan de ejecución 3 fases

### FASE 1 — Hoy 30 min (verificable)
- [ ] Activar MIT auto + briefing 7:45 AM (2 crons) → verificar con `openclaw cron list`
- [ ] Activar detector arrastres crónicos en turno reactivo → verificar alerta ITM ×N
- [ ] Probar Q&A vault: `qmd query "nicho Meta Ads decidido" --json -n 3` → 1 respuesta con cita

### FASE 2 — Esta semana
- [ ] Cierre P&L 9:30 PM + scoring → 7 archivos en `registro-de-progreso-diario/` con score
- [ ] Compresión dominical (Dom 20, 9 PM) → mision.md archiva semana 14-20, crea 21-27
- [ ] Cruce Ghost nocturno (C2-1/2) → cada noche 1 sub-paso exacto del plan en briefing
- [ ] Resumen semanal Vie 18 → borrador revisión con % por proyecto

### FASE 3 — Este mes
- [ ] Dashboard dominical estable (4 domingos enviados)
- [ ] Detector contradicciones mensual (1 reporte)
- [ ] Decidir archivo inteligente (propuesta + aprobación Mr. Jair)
- [ ] 1 experimento idea compuesta (Fitness×Meta×300M)

---
*Total usos propuestos: C1=20, C2=10, C3=8 → 38. P0=9, P1=14, P2=8 (+7 solapados según contexto).*
