---
created: 2026-06-09
updated: 2026-06-09
tags: [mapa, vault, visual, mermaid]
---

# 🗺️ Mapa del Vault

> Diagrama visual de la estructura del vault. Renderizado con Mermaid.

## 📋 Estructura General

```mermaid
graph TB
    VAULT[📁 VAULT PRINCIPAL]

    VAULT --> TASKS[tasks.md<br/>Fuente única de tareas]
    VAULT --> FINANZAS[💰 FINANZAS Y PROYECTOS]
    VAULT --> HABITOS[🧠 HÁBITOS Y DESARROLLO]
    VAULT --> HOGAR[🏍️ HOGAR Y MOTO]
    VAULT --> REGISTRO[📅 Registro de Progreso]

    FINANZAS --> MT5[🤖 Bot MT5]
    FINANZAS --> META[📢 Meta Ads]
    FINANZAS --> PROTOTIPO[🏍️ Prototipo X]
    FINANZAS --> EMPRESA[🏢 Empresa Tecnológica]
    FINANZAS --> GHOST[👤 Ghost Mode]

    HABITOS --> GYM[🏋️ Rutinas Gym]
    HABITOS --> LECTURA[📖 Lectura Diaria]
    HABITOS --> HABILIDADES[🎓 Habilidades]
    HABITOS --> IDENTIDAD[👤 Identidad]

    HOGAR --> MOTO[🔧 Mantenimiento Moto]
    HOGAR --> CASA[🏠 Mejoras Hogar]

    TASKS --> EOD[🌙 End-of-Day]
    TASKS --> ARYA[⏰ Arya Recordatorios]
    TASKS --> BRIEF[☀️ Morning Brief]
```

## 🔥 Flujo Diario

```mermaid
flowchart LR
    IOS[iOS Obsidian<br/>Editas tasks.md]
    IOS --> GIT[Git Push<br/>~3 min]
    GIT --> HELEN[H.E.L.E.N.<br/>Detección automática]

    HELEN --> CAMBIO{¿Cambió<br/>tasks.md?}

    CAMBIO -->|Sí| COMPARA[Comparar snapshot]
    CAMBIO -->|No| ESPERA[Esperar próximo turno]

    COMPARA --> NUEVA{Nueva tarea?}
    NUEVA -->|Con ⏰| CRON[Crear recordatorio]
    NUEVA -->|Sin hora| REVERSE[Reverse prompting]
    NUEVA -->|✅ marcada| PROGRESO[Registrar progreso]

    CRON --> TELEGRAM[📱 Te llega el recordatorio]
    REVERSE --> TELEGRAM2[📱 Pregunta: ¿hora/desglose?]
    PROGRESO --> REGISTRO2[📅 Registro de progreso]
```

## 🏋️ Rutina Semanal

```mermaid
gantt
    title Rutina Gym — Junio 2026
    dateFormat HH:mm
    axisFormat %H:%M

    section Lunes
    Tren Superior Completo    :lun, 07:00, 90m

    section Martes
    Pierna 1 (Cuádriceps)     :mar, 07:00, 80m

    section Miércoles
    Espalda + Bíceps          :mie, 07:00, 85m

    section Jueves
    Pecho + Tríceps           :jue, 07:00, 85m

    section Viernes
    Pierna 2 (Isquiotibiales) :vie, 07:00, 85m
```

## 📊 Proyectos Activos

```mermaid
pie title Distribución del Foco
    "Bot MT5" : 25
    "Meta Ads" : 20
    "Prototipo X" : 15
    "Gym Junio" : 15
    "Hoja de Vida Mamá" : 10
    "Hogar/Moto" : 10
    "Hábitos" : 5
```

---

*Mapa generado el 09/06/2026. Actualizar cuando cambie la estructura del vault.*
