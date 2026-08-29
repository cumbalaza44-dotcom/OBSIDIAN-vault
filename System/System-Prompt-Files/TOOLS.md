# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## QMD — Motor de Búsqueda del Vault

**Instalado:** `@tobilu/qmd` v2.5.3
**Modelo embedding:** `embeddinggemma-300M-Q8_0.gguf` (local, CPU)
**Índice:** `/root/.cache/qmd/index.sqlite`

### Colecciones
| Colección | Ruta | Contexto |
|-----------|------|----------|
| `vault` | `obsidian-vault/` | Sistema personal de Mr. Jair — tareas, proyectos, notas |
| `memory` | `memory/` + `MEMORY.md` | Memoria a largo plazo, preferencias, decisiones |

### Comandos clave
```bash
qmd search "query" --json -n 5    # Búsqueda rápida (BM25)
qmd vsearch "query" --json -n 5   # Semántica (embeddings)
qmd query "query" --json -n 5     # Híbrido (BM25 + vector + reranking)
qmd get "qmd://vault/path"        # Retrieve documento específico
qmd ls vault                      # Listar colección
qmd status                        # Status del índice
qmd update && qmd embed           # Re-indexar + re-generar embeddings
```

### Regla de uso
- **SIEMPRE** usar `qmd search` antes de `grep` o `find` en el vault
- `--json` para output procesable por el agente
- `-n 5` para limitar resultados (ahorrar tokens)
- `qmd get` para leer documento completo después de encontrarlo

---

Add whatever helps you do your job. This is your cheat sheet.
