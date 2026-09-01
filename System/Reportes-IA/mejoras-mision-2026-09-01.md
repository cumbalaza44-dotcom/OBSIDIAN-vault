# 10 Mejoras para mision.md
**Fecha:** 2026-09-01 | **Generado por:** H.E.L.E.N. (sub-agente)

---

## 1. Separar archivo histórico de sección activa
El documento acumula días cerrados con tablas completas, lo que infla el archivo cada semana y dificulta encontrar lo urgente. **Propuesta:** mover días cerrados a `historial/` y mantener solo la semana actual y la siguiente en `mision.md`.

## 2. Eliminar redundancia de tablas semanales duplicadas
La semana del 3 Ago–9 Ago aparece dos veces — una completa y otra parcialmente duplicada. **Propuesta:** agregar un mecanismo de validación al escribir o un comentario tipo `<!-- dups-check -->` para evitar esta acumulación.

## 3. Implementar estados con semáforo
Los estados actuales (✅ ⬜ 🔄 ❌) son insuficientes. **Propuesta:** 🔴 Bloqueado, 🟡 En progreso, 🟢 Completado, ⬜ Pendiente, ⏸️ Pospuesto. Permite filtrar rápidamente qué está detenido versus qué simplemente no empezó.

## 4. Agregar bloque "Contexto del día" con 3 prioridades
El encabezado de cada día tiene una nota descriptiva inconsistente. **Propuesta:** formato fijo:
```
> Foco: [X] | Energía: [Alta/Baja] | Tiempo disponible: [Xh]
```
Fuerza a priorizar antes de planificar el día.

## 5. Crear sección "Decisiones pendientes" independiente
Elementos estratégicos mezclados con tareas operativas (ej: "Definir plataforma hardware"). **Propuesta:** sección dedicada para decisiones que requieren input del usuario, separada de tareas ejecutables.

## 6. Formato estándar para cada proyecto con campos obligatorios
Algunos proyectos tienen "Siguiente" y "Esfuerzo" pero no todos. **Propuesta de plantilla fija:**
```
**Objetivo:** ... | **Siguiente paso:** ... | **Bloqueado por:** ... | **Deadline:** ... | **Esfuerzo:** ...
```

## 7. Métricas de seguimiento de hábitos con ventanas de rendimiento
La tabla de hábitos solo muestra el último registro. **Propuesta:** agregar columnas de `Racha actual`, `Mejor racha`, y `Tasa cumplimiento último mes`. Convierte un tracker pasivo en un sistema de rendimiento que permite detectar tendencias.

## 8. Separar tareas recurrentes de tareas únicas
Lectura diaria, gym y creatina se repiten cada día en cada tabla semanal, consumiendo espacio innecesario. **Propuesta:** bloque fijo `## 🔄 Recurrentes` que se liste una sola vez con su programa, y que las tablas semanales solo contengan tareas únicas o variables.

## 9. Sección de "Revisión semanal" estructurada
El Viernes ya tiene "📋 Revisión semanal" como tarea, pero no hay template. **Propuesta:** checklist:
```
> □ Hábitos completados ≥80% | □ Proyectos avanzaron ≥1 paso | □ Gasto vs presupuesto | □ Próxima semana definida
```

## 10. Frontmatter YAML extendido con metadatos de seguimiento
El frontmatter actual solo tiene `created`, `updated` y `source`. **Propuesta agregar:** `week_number`, `habit_streak_gym`, `habit_streak_lectura`, `projects_blocked`, `tasks_completed_this_week`. Permite automatizar reportes, gráficas de progreso, y alertas.

---

## Resumen de Impacto

| Categoría | Mejoras | Beneficio |
|-----------|---------|-----------|
| Legibilidad | 1, 2, 8 | Reducen tamaño del archivo |
| Decisiones | 3, 4, 6 | Mejoran la toma de decisiones |
| Estrategia | 5, 9 | Evitan que tareas estratégicas se pierdan |
| Medición | 7, 10 | Permiten medir y automatizar seguimiento |
