---
created: 2026-05-13
type: template-script
purpose: Generate System/JARVIS/daily-context.md
---
# 📖 Manual de uso — Sistema de contexto diario

## 🎯 ¿Qué es?

Un sistema que genera automáticamente un archivo **markdown 100% plano** (`daily-context.md`) desde Obsidian, que JARVIS lee en cada sesión para tener el contexto completo del vault.

**Reemplaza:** el antiguo snapshot + Hoy.md (Dataview no legible en texto plano).

## 📂 Archivos involucrados





| Archivo | Rol |
|---------|-----|
| `System/JARVIS/daily-context.md` | 📄 **Salida** — lo que lee JARVIS |
| `System/JARVIS/Plantilla - daily-context.md` | 🏗️ **Generador** — script Templater que produce el archivo |
| `System/Instrucción agente.md` | 📋 Copia de AGENTS.md para estudio |

## ✅ Requisitos

- Plugin **Templater** instalado y activo en Obsidian iOS
- Plugin **Dataview** instalado y activo (el script lo usa internamente)
- Carpetas `System/JARVIS/` dentro del vault

## 🚀 Cómo usarlo (iOS)

### Cada vez que quieras actualizar el contexto:

```
1. Abre Obsidian en iOS
2. Crea/edita tus tareas normalmente (con 📅 YYYY-MM-DD)
3. Presiona Cmd/Ctrl + P → "Templater: Insert Template"
4. Selecciona "Plantilla - daily-context"
5. ✅ Listo — el archivo se genera al instante
```

### Opcional: Asignar atajo de teclado

```
Settings → Hotkeys → Templater: Insert Template
→ Asigna un hotkey (ej: Cmd + Shift + D)
```

## 📋 ¿Qué genera exactamente?

```markdown
# Contexto Diario — 13/05/2026

> 📊 33 notas — 12 carpetas — 2 pendientes hoy

## 🏋️ Tareas de hoy

### ⏳ Pendientes
- [ ] Crear rutina de ejercicio  — *GYM.md*
- [ ] Terminar prueba  — *Notas somos.md*

## 📁 Estructura del vault

├── 📄 Hoy.md
├── 📁 FINANZAS Y PROYECTOS/
│   ├── 📁 Bot mt5/
│   │   └── Bot MT5.md
│   └── ...

## 🆕 Modificados recientemente
- GYM.md — *2026-05-13*
- Notas somos.md — *2026-05-12*
```

## 🔄 Flujo completo

```
1. Editas tareas en iOS (con 📅 fecha) → instantáneo en Obsidian
2. Ejecutas plantilla Templater → se genera daily-context.md → push a GitHub
3. Próxima vez que hablas con JARVIS:
   → git fetch --dry-run (detecta cambios)
   → git pull --ff-only
   → Lee daily-context.md
   → Ya tiene contexto completo
```

## 🧪 Verificación rápida

Después de generar el archivo:
1. Abre `System/JARVIS/daily-context.md`
2. Verifica que veas:
   - Tareas del día con sus rutas
   - Estructura de carpetas
   - Archivos modificados recientemente
3. Si ves "Esperando primera generación..." → la plantilla no se ha ejecutado aún

## ⚠️ Notas importantes

- **Ejecuta la plantilla cada vez que agregues/edites tareas del día** para mantener el contexto fresco
- El script excluye `Hoy.md`, `_VAULT-*` y el propio `System/JARVIS/` para evitar loops
- Si no hay tareas para hoy, el archivo se genera igual con stats y estructura
- Si olvidas ejecutar la plantilla, JARVIS tendrá la versión anterior (posiblemente desactualizada)

---

*Documentación del sistema de contexto diario — v1.0*
