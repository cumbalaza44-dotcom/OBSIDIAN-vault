---
created: 2026-06-08
type: automatización
tags: [productividad, automatización, decisiones]
---

# 🤖 Matriz de Puntuación de Automatización

## ¿Qué es?

Una herramienta para decidir si una tarea vale la pena automatizar. Evalúa 4 dimensiones de 0-3 puntos cada una.

## Fórmula

```
Puntuación = Frecuencia + Tiempo + Impacto + Complejidad
```

| Dimensión | 0 | 1 | 2 | 3 |
|-----------|---|---|---|---|
| **Frecuencia** | Mensual | Semanal | Diario | Varias veces/día |
| **Tiempo** | <5 min | 5-15 min | 15-60 min | >1 hora |
| **Impacto error** | Sin impacto | Inconveniente | Requiere corrección | Pérdida $/reputación |
| **Complejidad** | 5+ decisiones | 3-4 decisiones | 1-2 decisiones | Solo reglas |

## Interpretación

| Puntuación | Recomendación |
|------------|---------------|
| 10-12 | 🟢 Automatizar ya |
| 7-9 | 🟡 Automatizar pronto |
| 4-6 | 🟠 Considerar |
| 0-3 | 🔴 No automatizar |

## Tareas Evaluadas

| Tarea | F | T | I | C | Total | Decisión |
|-------|---|---|---|---|-------|----------|
| *Ejemplo: Enviar recordatorios* | 3 | 1 | 2 | 3 | **9** | 🟡 Automatizar |

---

*Usar script: `bash skills/productivity-automation-kit/scripts/auto-score.sh "nombre"`*
