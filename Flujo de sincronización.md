# Flujo de Sincronización — Obsidian Vault → OpenClaw

## 📡 Visión general

Pipeline automatizado de 0 costos en tokens. Conecta ediciones en iOS (Mr. Jair) con lecturas reactivas en OpenClaw (JARVIS), y viceversa.

```
┌──────────────┐     ┌────────────┐     ┌──────────────┐
│  Mr. Jair    │────→│  GitHub    │────→│  Servidor    │
│  (iOS)       │     │  Repo      │     │  (VPS)       │
└──────────────┘     └────────────┘     └──────┬───────┘
                                                │
                          ┌─────────────────────┘
                          ▼
              ┌──────────────────────┐
              │  sync-pull.sh        │
              │  (cron cada 5 min)   │
              └──────────┬───────────┘
                         │ ¿Cambios?
                         ▼
              ┌──────────────────────┐
              │  sync-snapshot.sh    │
              │  → _VAULT-SNAPSHOT.md│
              │  → /tmp/obsidian-    │
              │    vault-flag        │
              └──────────┬───────────┘
                         │ Señal reactiva
                         ▼
              ┌──────────────────────┐
              │  JARVIS (OpenClaw)   │
              │  Lee snapshot en     │
              │  cada sesión         │
              └──────────────────────┘
```

## 🔄 Flujo completo

### 📥 Mr. Jair edita → JARVIS se entera

1. **Mr. Jair** edita notas en Obsidian (iOS)
2. Plugin **Obsidian Git** sincroniza a GitHub cada ~3 min
3. **sync-pull.sh** (cron del VPS cada 5 min) hace `git pull --ff-only`
4. Si hay cambios → ejecuta **sync-snapshot.sh**:
   - Genera `_VAULT-SNAPSHOT.md` (resumen estático de ~20 líneas)
   - Escribe `/tmp/obsidian-vault-flag` (señal reactiva)
5. **JARVIS** en su próxima sesión detecta la flag, lee el snapshot y borra la flag
6. Costo: **0 tokens** en idle. Una lectura (~200 tokens) solo cuando hay cambios.

### 📤 JARVIS edita → Mr. Jair lo ve

1. **JARVIS** modifica archivos en `obsidian-vault/`
2. Al terminar, ejecuta **sync-push.sh**:
   - `git add -A` → `git commit` → `git push --force-with-lease`
3. También ejecuta **sync-snapshot.sh** para refresh inmediato del snapshot
4. **Mr. Jair** recibe los cambios vía plugin Obsidian Git en iOS
5. Costo: **0 tokens**. Sin esperar al cron.

### 🚦 Señal reactiva (flag)

El archivo `/tmp/obsidian-vault-flag` contiene:
- `changed_at` — timestamp de detección
- `new_commits` — cantidad de commits nuevos
- `files_changed` — archivos modificados

Se borra automáticamente después de leerlo. Sin limpieza manual.

## 🧩 Scripts involucrados

| Script | Trigger | Función |
|--------|---------|---------|
| `sync-pull.sh` | Cron cada 5 min | Git pull + detección de cambios + snapshot |
| `sync-push.sh` | Manual (JARVIS) | Commit + push forzado de ediciones locales |
| `sync-snapshot.sh` | Pull (cambio) o Push | Genera `_VAULT-SNAPSHOT.md` |
| `check-flag.sh` | Startup de JARVIS | Detecta flag, lee snapshot, verifica watcher |
| `watcher.sh` | systemd (en desuso) | Vigilancia alternativa — reemplazado por cron |

## 📊 Costos

- **Idle:** 0 tokens — solo corre cron bash
- **Lectura en startup:** ~200 tokens (snapshot de ~20 líneas)
- **Escritura (JARVIS):** 0 tokens — solo git operations

---

*Documentación del pipeline — Cero overhead, máximo control.*