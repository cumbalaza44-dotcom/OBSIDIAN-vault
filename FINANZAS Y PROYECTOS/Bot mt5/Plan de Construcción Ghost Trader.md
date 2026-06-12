# 🏗️ Plan de Construcción — Ghost Trader

> **Versión:** 1.0 — 11/06/2026
> **Propósito:** Hoja de ruta para construir el asistente de trading en lenguaje natural

---

## 📋 Estado General

| Componente | Estado | Notas |
|-----------|--------|-------|
| Arquitectura definida | ✅ | Documentada en *Arquitectura Ghost Trader.md* |
| Flujo de datos | ✅ | Documentado en *🌀 Ghost Trader — Flujo de Datos.md* |
| OpenCode instalado | ⏳ | Pendiente verificar |
| Backtest estrategia base | ⏳ | Siguiente paso técnico |
| Integración Deriv API | ⏳ | Pendiente |
| Risk Engine | ⏳ | Pendiente |
| Conexión Telegram → LLM → Deriv | ⏳ | Pendiente |

---

## 🪜 Fases de Construcción

### Fase 1 — Fundación (Prioridad 🔴)
- [ ] Verificar instalación OpenCode
- [ ] Backtest estrategia base con datos reales Deriv
- [ ] Definir parámetros de riesgo iniciales
- [ ] Establecer conexión LLM → sistema de órdenes

### Fase 2 — Núcleo Funcional
- [ ] Risk Engine funcional (límites, stops automáticos, drawdown)
- [ ] Integración Telegram → ejecución de análisis
- [ ] Ciclo de trabajo automatizado (cron cada X tiempo)

### Fase 3 — Optimización
- [ ] Pruebas en mercado real con capital mínimo
- [ ] Ajuste de estrategias según resultados
- [ ] Documentación de operaciones y métricas

---

## 📌 Tareas Inmediatas

- [ ] **⬆️ Prioridad:** Diseñar plan de arquitectura (bloque 45min post-gym) — *tasks.md HOY*
- [ ] Investigar N8N como alternativa de orquestación — *Evolución MT5.md*
- [ ] Ciclo de trabajo 🔁 — *Evolución MT5.md*

---

## 🔗 Notas Relacionadas

- [[Arquitectura Ghost Trader]]
- [[🌀 Ghost Trader — Flujo de Datos (Arquitectura Limpia)]]
- [[Evolución MT5]]
- [[Análisis assistentLLM]]
