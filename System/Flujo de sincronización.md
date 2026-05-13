# Flujo de Sincronización — Obsidian Vault ↔ OpenClaw (v2)

> **Modelo: Bajo Demanda — Sin cron. Sin heartbeat. Sin snapshot.**

## 📡 Visión general

Pipeline 100% reactivo a la conversación. JARVIS sincroniza el vault automáticamente al inicio de cada sesión directa. No hay procesos en segundo plano, no hay archivos intermedios, no hay flags.

```
┌──────────────┐     ┌────────────┐     ┌──────────────┐
│  Mr. Jair    │────→│  GitHub    │────→│  Servidor    │
│  (iOS)       │     │  Repo      │     │  (VPS)       │
└──────────────┘     └────────────┘     └──────────────┘
       │                                     │
       │ (edita en Obsidian)                 │ (inicia sesión directa)
       ▼                                     ▼
  ┌──────────┐                     ┌─────────────────────┐
  │ Hoy.md   │                     │ git fetch --dry-run  │
  │ Dataview │                     │ ¿cambios remotos?    │
  │ nativo   │                     └─────────┬───────────┘
  └──────────┘                               │
       │                           ┌─────────┴─────────┐
       │                           │                   │
       │                           ▼                   ▼
       │                    ┌────────────┐    ┌────────────────┐
       │                    │ No → leer  │    │ Sí → git pull  │
       │                    │ Hoy.md     │    │ → leer Hoy.md  │
       │                    │ directo    │    │                │
       │                    └────────────┘    └────────────────┘
       │                           │                   │
       └───────────────────────────┴───────────────────┘
                                   ▼
                        ┌──────────────────────┐
                        │  JARVIS tiene el     │
                        │  contexto del día    │
                        └──────────────────────┘
```

## 🔄 Flujo completo

### 📥 Mr. Jair edita → JARVIS se entera

1. **Mr. Jair** edita/crea/checkea tareas en Obsidian (iOS)
   - `Hoy.md` con queries **Tasks + Dataview** nativos renderiza instantáneo
   - Sin esperar al servidor
2. Plugin **Obsidian Git** sincroniza a GitHub cada ~3 min
3. **JARVIS** inicia una sesión directa → ejecuta automáticamente:
   - `git fetch --dry-run` para detectar cambios remotos (<2s)
   - Si hay cambios → `git pull --ff-only`
   - Lee `Hoy.md` para contexto diario (~50-200 tokens)
4. El usuario no pide nada. Ocurre automático en cada interacción.
5. Costo en idle: **0** (nada corriendo). Costo por interacción: **~150 tokens**.

### 📤 JARVIS edita → Mr. Jair lo ve

1. **JARVIS** modifica archivos en `obsidian-vault/`
2. Al terminar, ejecuta **sync-push.sh**:
   - `git add -A` → `git commit` → `git push --force-with-lease`
3. **Mr. Jair** recibe los cambios vía plugin Obsidian Git en iOS
4. Costo: **0 tokens**.

### 🏠 Hoy.md — Nativo Obsidian (Dataview + Tasks)

```tasks
due today
not done
group by filename
sort by priority
```

Hoy.md se renderiza automáticamente en Obsidian iOS usando Dataview y Tasks. No depende del servidor para nada. JARVIS lo lee directamente desde el sistema de archivos en cada sesión.

## 🧩 Scripts involucrados

| Script | Trigger | Función |
|--------|---------|---------|
| `sync-push.sh` | Manual (JARVIS al editar) | Commit + push forzado de ediciones locales |

**Eliminados (v1 → v2):**

| ~~Script/Archivo~~ | ~~Razón~~ |
|-------------------|-----------|
| ~~sync-pull.sh~~ | Reemplazado por `git fetch --dry-run` bajo demanda |
| ~~sync-snapshot.sh~~ | Reemplazado por lectura directa de `Hoy.md` |
| ~~sync-today.sh~~ | Reemplazado por Dataview nativo en Obsidian |
| ~~check-flag.sh~~ | Eliminado: sin flags que verificar |
| ~~_VAULT-SNAPSHOT.md~~ | Eliminado: sin snapshot que leer |
| ~~/tmp/obsidian-vault-flag~~ | Eliminado: sin señal reactiva |
| ~~Cron cada 5 min~~ | Eliminado: sin heartbeat |

## 📊 Costos

| Concepto | Antes (v1) | Ahora (v2) |
|----------|-----------|------------|
| Idle | 0 tokens (pero proceso cada 5 min) | **0 tokens + 0 procesos** |
| Startup (cambios) | ~200 tok (snapshot) | ~150 tok (Hoy.md) |
| Startup (sin cambios) | ~200 tok (flag + snapshot) | ~50 tok (Hoy.md solo) |
| Escritura | 0 tokens | 0 tokens |
| Latencia cambios iOS→JARVIS | Hasta 8 min (cron 5 + push 3) | **~3 min** (solo push de iOS) |

## ✅ Cumplimiento de requisitos

| Requisito | Cumplimiento |
|-----------|-------------|
| Sin cron (no heartbeat) | ✅ No hay procesos en segundo plano |
| Detección reactiva | ✅ JARVIS detecta cambios en cada interacción automáticamente |
| Cero costo idle | ✅ El servidor no hace nada entre conversaciones |
| Alta sincronía | ✅ Latencia máxima de un `git fetch` (~2s) al hablar |
| Sin snapshot | ✅ Eliminado por completo |
| Estructura del vault en iOS | ✅ El vault ya existe en iOS; servidor solo clona |
| Mantener sync-push.sh | ✅ Se conserva para escrituras de JARVIS |

---

*Documentación del pipeline v2 — Cero overhead, máxima eficiencia. Actualizado 2026-05-13.*
