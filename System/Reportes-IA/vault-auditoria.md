# 🗂️ Auditoría del Vault de Obsidian — Mr. Jair

**Fecha:** 09/08/2026
**Vault:** `/root/.openclaw/workspace/obsidian-vault/`
**Objetivo:** Mapear la estructura real, detectar problemas (duplicados, carpetas espejo, huérfanos) y proponer una reorganización práctica que no rompa `tasks.md` ni los enlaces existentes.

---

## 1. Mapa actual de la estructura

### 1.1 Resumen general

| Métrica | Valor |
|---------|-------|
| Total de archivos (sin `.git`/`__pycache__`) | **233** |
| Total de archivos `.md` | **164** |
| Carpetas de primer nivel | **13** |
| Carpetas espejo detectadas | **2 pares** |
| Proyectos de código embebidos (carpeta `assistentLLM-master`) | **1** (≈60 archivos Python) |

### 1.2 Árbol de carpetas (con conteo de archivos)

```
obsidian-vault/  (raíz)
├── tasks.md  ⭐ FUENTE DE VERDAD de tareas (1)
├── FINANZAS Y PROYECTOS/  (32 archivos)  ← CARPETA PRINCIPAL
│   ├── Bot mt5/  (5 .md + ~60 código)
│   │   ├── assistentLLM-master/  ← CÓDIGO PYTHON EMBEBIDO (proyecto completo)
│   │   ├── Análisis assistentLLM.md
│   │   ├── Arquitectura Ghost Trader.md
│   │   ├── Evolución MT5.md
│   │   ├── Plan de Construcción Ghost Trader.md
│   │   └── 🌀 Ghost Trader — Flujo de Datos (Arquitectura Limpia).md
│   ├── EMPRESA TECNOLÓGICA/  (9)
│   │   ├── BANCO DE IDEAS.md, ESTAPA 1.md, ETAPA 2.md
│   │   ├── HERRAMIENTAS Y RECURSOS CONNTENIDO.md  ← typo "CONNTENIDO"
│   │   ├── Innovación en cada paso.md, META ADS.md
│   │   └── PROTOTIPO X/  (3: Perifericos, Plataformas, prototipo X)
│   │   └── tintura de THC/  (1)
│   ├── Finanzas y proyectos/  (7)  ← CARPETA ANIDADA con nombre duplicado
│   │   ├── Búsqueda de plataformas..., Conocimientos financieros.md
│   │   ├── GASTOS Y FIJOS.md, Plan de Acción.md
│   │   ├── Plan de negocios 300MCop.md, Recordatorios.md
│   │   └── Semillas y trabajos automatizados.md
│   ├── Ghost mode/  (1: identidad y objetivos.md)
│   ├── lista de compras/  (1: lista de objetos.md)
│   └── Prestamos.md  (sueltos)
│
├── FINANZAS-Y-PROYECTOS/  (2)  ← CARPETA ESPEJO (con guiones)
│   └── Bot-mt5/
│       ├── Ghost-Trader-Elevator-Pitch.md
│       └── Ghost-Trader-Plan-Construccion.md  ← DUPLICADO (2004 líneas)
│
├── HABITOS Y DESARROLLO AVANZADO/  (60)
│   ├── Habilidades-conocimiento (intereses)/  (4)
│   ├── habito -lectura/  (1: .gitkeep)  ← CARPETA VACÍA (placeholder)
│   ├── Mente (ser)/  (49)
│   │   ├── habito -lectura/  (37 notas diarias 2026-06-01 → 07-07)  ← CARPETA ACTIVA
│   │   ├── FLUJO 3 P.md, Habilidad (mentales).md
│   │   ├── Hábitos mente.md, Mente.md, Notas mentales.md
│   ├── MODO FANTASMA/  (26)
│   │   ├── 2026-07/  (20 notas diarias)
│   │   ├── Habilidades/  (4: comunicacion, fotografia, storytelling, video)
│   │   ├── Reportes/  (0 — VACÍA)
│   │   └── README.md
│   └── Yo y pendientes personales/  (3: Cuidado personal, Hábitos, Objetivo)
│
├── HOGAR/  (2)
│   ├── Mantenimiento moto/  (Mantenimiento Moto.md)
│   └── Mantenimiento y mejoras hogar/  (Mantenimiento y mejoras hogar.md)
│
├── LECTURAS-DIARIAS/  (14)  ← SUCESOR de "registro de progreso diario"
│   ├── Plan-Lecturas.md  ⭐ ÍNDICE/CATÁLOGO de leyes
│   └── 2026-07-27.md → 2026-08-09.md  (13 notas)
│
├── PROTOTIPO X/  (3)  ← CÓDIGO/HARDWARE (raíz)
│   ├── circuit/DIAGRAMA.md
│   ├── docs/ARQUITECTURA.md
│   └── firmware/prototipo_x.ino
│
├── registro de progreso diario/  (28)  ← CARPETA LEGACY (abandonada en junio)
│   ├── 2026-05-02.md → 2026-06-20-agenda.md  (27 notas)
│   └── README.md
│
├── Filosofía/  (1: Los 7 Principios Herméticos.md)
├── System/configObsidian/  (2: _INFRA-RESTORE.md, Flujo de sincronización.md)
│
├── ARCHIVOS SUELTOS EN RAÍZ  (8)
│   ├── Go Kart.md, MIL Cosas por hacer antes de morir 🔥😼.md
│   ├── Notas somos.md, Tutorial-OpenClaw-iOS.md
│   ├── backup-obsidian.sh, check-flag.sh, sync-push.sh, watcher.sh
│   └── _INFRA-crontab.txt, _INFRA-watcher.service
```

---

## 2. Problemas detectados

### 🔴 CRÍTICOS — Duplicados y carpetas espejo

#### 2.1 Carpetas espejo de FINANZAS (duplicación de todo el dominio)
- **`FINANZAS Y PROYECTOS/`** (con espacios) → carpeta principal, 32 archivos
- **`FINANZAS-Y-PROYECTOS/`** (con guiones) → carpeta espejo, solo 2 archivos
- **Causa probable:** se creó la segunda carpeta con guiones (quizá por un fallo al escribir rutas con espacios), y solo se movieron 2 archivos antes de abandonarla.

#### 2.2 Carpetas espejo del Bot MT5
- **`FINANZAS Y PROYECTOS/Bot mt5/`** (con espacio) → principal, 5 .md + código
- **`FINANZAS-Y-PROYECTOS/Bot-mt5/`** (con guiones) → espejo, 2 .md

#### 2.3 DUPLICADO DE CONTENIDO — Plan de Construcción Ghost Trader
- **`FINANZAS Y PROYECTOS/Bot mt5/Plan de Construcción Ghost Trader.md`** (595 líneas)
- **`FINANZAS-Y-PROYECTOS/Bot-mt5/Ghost-Trader-Plan-Construccion.md`** (2004 líneas)
- **Son el MISMO documento en distintos estados de evolución.** El de 2004 líneas es la versión más completa (Fases 1-6 con código). El de 595 es una versión anterior. **Riesgo:** editar el equivocado y perder trabajo.

#### 2.4 DUPLICADO — identidad de Ghost
- **`FINANZAS Y PROYECTOS/Ghost mode/identidad y objetivos.md`** contiene las tareas "musical / aventura / estilo dark colorido vivido"
- **`tasks.md` → sección "👤 IDENTIDAD / GHOST"** contiene las mismas 3 tareas
- **Fuente única rota:** el mismo dato vive en 2 lugares.

### 🟠 ALTOS — Fragmentación de proyectos

#### 2.5 Prototipo X dividido en 2 carpetas
- **`PROTOTIPO X/`** (raíz) → código real: circuit/, docs/, firmware/ (`.ino`)
- **`FINANZAS Y PROYECTOS/EMPRESA TECNOLÓGICA/PROTOTIPO X/`** → documentación markdown (Perifericos, Plataformas, prototipo X)
- Mismo proyecto, 2 ubicaciones, sin conexión entre sí.

#### 2.6 "Finanzas y proyectos" anidada dentro de "FINANZAS Y PROYECTOS"
- `FINANZAS Y PROYECTOS/Finanzas y proyectos/` repite el nombre de la carpeta padre. Confuso y redundante.

### 🟡 MEDIOS — Inconsistencias de nombres

#### 2.7 Nombres inconsistentes / typos
- `HERRAMIENTAS Y RECURSOS CONNTENIDO.md` → typo "CONNTENIDO" (doble N)
- `ESTAPA 1.md` → typo "ESTAPA" (debería ser ETAPA, y existe `ETAPA 2.md`)
- `Habilidades y conocimientos ( intereses).md` → espacio raro antes de "(intereses)"
- `habito -lectura` (con espacios) → inconsistente con `LECTURAS-DIARIAS` (con guiones)
- `Bot mt5` vs `Bot-mt5` (espacio vs guión)

#### 2.8 Carpetas vacías / muertas
- `HABITOS Y DESARROLLO AVANZADO/habito -lectura/.gitkeep` → **carpeta placeholder vacía** (la activa con notas está en `Mente (ser)/habito -lectura/`)
- `HABITOS Y DESARROLLO AVANZADO/MODO FANTASMA/Reportes/` → **vacía** (el reporte semanal de MODO FANTASMA nunca se generó)

### 🟡 MEDIOS — Archivos huérfanos / desorganizados

#### 2.9 Archivos sueltos en la raíz (sin categorizar)
- `Go Kart.md` (proyecto mecánico — debería estar en HOGAR o Proyectos)
- `MIL Cosas por hacer, antes de morir 🔥😼.md` (lista de vida — huérfano)
- `Notas somos.md` (¿notas personales? sin categoría)
- `Tutorial-OpenClaw-iOS.md` (documentación técnica — debería estar en System/)
- `Filosofía/` (solo 1 archivo — huérfano de un sistema mayor)

#### 2.10 Sistema de registro diario fragmentado en 3 sistemas
- **`registro de progreso diario/`** → notas de **Mayo–Junio** (abandonado)
- **`LECTURAS-DIARIAS/`** → notas de **Julio–Agosto** (sucesor activo)
- **`MODO FANTASMA/2026-07/`** → notas de desarrollo integral (julio)
- **3 sistemas de diario que no se comunican entre sí.** El registro de progreso se abandonó; LECTURAS-DIARIAS solo cubre lectura; MODO FANTASMA cubre desarrollo integral (pero solo tiene julio, no agosto).

#### 2.11 Código fuente dentro del vault
- `assistentLLM-master/` (~60 archivos Python: app/, tests/, scripts/) está **embebido dentro del vault de notas**.
- **Problema:** contamina el vault de markdown, infla el repo git, y no es el lugar natural para código (debería ser un repo separado).

### 🟢 BAJOS — Otros

#### 2.12 MODO FANTASMA desactualizado
- Solo existe `2026-07/`, no `2026-08/`. El sistema diario de agosto no se está documentando (aunque tasks.md sí registra hábitos).

#### 2.13 `.obsidian` sin plugins
- Solo tiene `github-sync-metadata.json`. No hay plugins de plantillas, índices, ni dashboards instalados (oportunidad, ver Sección 5).

---

## 3. Estructura reorganizada propuesta

**Principios:**
1. **No romper `tasks.md`** — es la fuente de verdad y se mantiene en la raíz.
2. **Un proyecto = una carpeta** — eliminar espejos y fragmentación.
3. **Agrupar por dominio** (Proyectos, Hábitos, Finanzas, Desarrollo, Registros).
4. **Separar código de notas** — el código Python sale del vault.
5. **Convención de nombres única** — espacios consistentes, sin typos.

### Árbol propuesto

```
obsidian-vault/
├── tasks.md  ⭐ (se mantiene en la raíz — NO se mueve)
│
├── 00-INBOX/                     ← NUEVO: captura rápida (notas sin categorizar)
│
├── 10-PROYECTOS/                 ← Un proyecto = una carpeta
│   ├── Ghost-Trader/             ← (fusión de Bot mt5 + Bot-mt5)
│   │   ├── docs/                 ← .md: Plan, Arquitectura, Flujo, Elevator Pitch, Análisis
│   │   └── (código → repo git externo, ver migración)
│   ├── Prototipo-X/              ← (fusión de PROTOTIPO X/ + EMPRESA/PROTOTIPO X)
│   │   ├── docs/                 ← .md: ARQUITECTURA, Perifericos, Plataformas, prototipo X
│   │   ├── circuit/DIAGRAMA.md
│   │   └── firmware/prototipo_x.ino
│   ├── Meta-Ads/
│   ├── E-commerce/
│   ├── Empresa-Tecnologica/      ← (BANCO DE IDEAS, ETAPA 1/2, HERRAMIENTAS, META ADS, Innovación)
│   └── tintura-THC/
│
├── 20-FINANZAS/                  ← (fusión de Finanzas y proyectos/ + Prestamos + lista de compras)
│   ├── GASTOS Y FIJOS.md
│   ├── Plan de Acción.md
│   ├── Plan de negocios 300MCop.md
│   ├── Conocimientos financieros.md
│   ├── Búsqueda de plataformas.md
│   ├── Semillas y trabajos automatizados.md
│   ├── Recordatorios.md
│   ├── Prestamos.md
│   └── lista-de-compras/
│
├── 30-HABITOS/                   ← (fusión de HABITOS Y DESARROLLO AVANZADO)
│   ├── lectura/                  ← (mueve habito -lectura activa aquí)
│   ├── gym/
│   ├── mente/                    ← (FLUJO 3 P, Habilidad mental, Hábitos mente, Mente, Notas mentales)
│   ├── habilidades-intereses/    ← (carburador, DOHC, Habilidades y conocimientos)
│   └── yo-pendientes/            ← (Cuidado personal, Hábitos, Objetivo)
│
├── 40-DESARROLLO/                ← (MODO FANTASMA + Filosofía)
│   ├── MODO-FANTASMA/
│   │   ├── 2026-07/  (y futuros 2026-08/...)
│   │   ├── Habilidades/
│   │   └── Reportes/
│   └── Filosofia/                ← (Los 7 Principios Herméticos)
│
├── 50-REGISTROS/                 ← (fusión de registro de progreso + LECTURAS-DIARIAS)
│   ├── progreso-diario/          ← (2026-05 → 2026-06, histórico)
│   ├── lecturas/                 ← (Plan-Lecturas.md + 2026-07-27 → agosto)
│   └── (futuro: 2026-08-progreso.md por día)
│
├── 60-HOGAR/                     ← (HOGAR + Go Kart)
│   ├── moto/
│   ├── hogar/
│   └── go-kart/
│
├── 90-SISTEMA/                   ← (System + Tutorial + scripts)
│   ├── configObsidian/
│   ├── Tutorial-OpenClaw-iOS.md
│   ├── backup-obsidian.sh, sync-push.sh, watcher.sh, check-flag.sh
│   └── _INFRA-*.txt/.service
│
├── MIL Cosas por hacer antes de morir 🔥😼.md   ← (vida, se mantiene en raíz — es icónico)
└── Notas somos.md  ← (se mantiene o va a 00-INBOX)
```

**Nota sobre numeración:** El prefijo numérico (`00-`, `10-`, `20-`...) fuerza el orden lógico en Obsidian (que ordena alfabéticamente). Es opcional pero muy recomendable.

---

## 4. Plan de migración paso a paso (sin romper nada)

### Fase 0 — Preparación (seguridad primero)
1. **Hacer backup completo** del vault (correr `backup-obsidian.sh` o `git tag` antes de tocar nada).
2. **Confirmar con Mr. Jair** el árbol propuesto (Sección 3) antes de ejecutar — decisiones irreversibles de estructura.
3. **Verificar que no hay sesión activa** escribiendo en el vault (evitar conflictos con el watcher).

### Fase 1 — Resolver duplicados (mayor valor, menor riesgo)
1. **Ghost Trader:** comparar `Plan de Construcción Ghost Trader.md` (595L) vs `Ghost-Trader-Plan-Construccion.md` (2004L). **Fusionar en la versión de 2004 líneas** (la más completa). Eliminar la de 595 tras confirmar que no tiene contenido único.
2. **Eliminar carpetas espejo:** mover los 2 archivos de `FINANZAS-Y-PROYECTOS/Bot-mt5/` a `FINANZAS Y PROYECTOS/Bot mt5/` (o a la nueva estructura). Borrar `FINANZAS-Y-PROYECTOS/` vacía.
3. **Ghost mode:** decidir si `identidad y objetivos.md` o la sección de `tasks.md` es la fuente. Recomendado: **tasks.md es la fuente de verdad** → borrar `Ghost mode/` o convertirlo en referencia.

### Fase 2 — Crear la nueva estructura (migración por dominio)
4. **Crear las carpetas nuevas** (`10-PROYECTOS`, `20-FINANZAS`, etc.) con `mkdir`.
5. **Mover archivos con `git mv`** (preserva historial) en lotes pequeños:
   - Proyectos → `10-PROYECTOS/`
   - Finanzas → `20-FINANZAS/`
   - Hábitos → `30-HABITOS/`
   - Desarrollo → `40-DESARROLLO/`
   - Registros → `50-REGISTROS/`
   - Hogar → `60-HOGAR/`
   - Sistema → `90-SISTEMA/`
6. **Después de cada lote:** correr `sync-push.sh` (push dual: submodule + parent) y verificar que el watcher no revierta nada.

### Fase 3 — Sacar el código del vault
7. **`assistentLLM-master/`:** mover el código Python a un **repo git separado** (p.ej. `~/repos/ghost-trader/`). En el vault dejar solo un enlace/README apuntando al repo. Esto limpia el vault y el git.

### Fase 4 — Unificar los sistemas de registro
8. **Registros:** mover `registro de progreso diario/` (histórico) y `LECTURAS-DIARIAS/` (activo) bajo `50-REGISTROS/`. Decidir un sistema único para agosto (recomendar retomar el formato de "registro de progreso diario" pero unificado con MODO FANTASMA).

### Fase 5 — Actualizar referencias y validar
9. **Buscar enlaces rotos:** tras mover, usar Obsidian "unresolved links" o `qmd search` para detectar referencias a rutas antiguas. Actualizar.
10. **Verificar `tasks.md`:** confirmar que las tareas siguen apuntando a las notas correctas (tasks.md usa nombres, no rutas completas, así que el riesgo es bajo — solo verificar que los "write-back" a notas originales sigan funcionando).
11. **Commit final + push dual** y confirmar sync con el dispositivo iOS de Mr. Jair.

---

## 5. Mejoras de funcionalidad recomendadas

### 5.1 Índices automáticos (Dashboard)
- **Crear un `00-INICIO.md` / Dashboard** en la raíz que agregue automáticamente (con Dataview):
  - Tareas de hoy (leídas de tasks.md)
  - Proyectos activos y su estado
  - Hábitos de la semana
  - Últimas notas de cada dominio
- **Recomendación:** instalar el plugin **Dataview** (o **DataviewJS**) en `.obsidian`. Es el que más valor aporta con menos riesgo.

### 5.2 Plantillas (Templates)
- **Instalar plugin Templates** y crear plantillas para:
  - `plantilla-nota-proyecto.md` (objetivo, estado, siguiente paso, depende de)
  - `plantilla-registro-diario.md` (completadas/progreso/pendientes/métricas)
  - `plantilla-lectura-diaria.md` (concepto → ejemplo → pregunta)
  - `plantilla-modo-fantasma.md` (5 fases)
- Esto estandariza el formato y hace que H.E.L.E.N. genere notas consistentes.

### 5.3 Convenciones de nombres (naming)
- **Regla única:** usar **espacios** en nombres de carpetas (no guiones) para consistencia con Obsidian. O guiones — pero **uno solo, siempre el mismo**.
- Corregir typos: `CONNTENIDO` → `CONTENIDO`, `ESTAPA` → `ETAPA`.
- **Fechas ISO** (`YYYY-MM-DD`) para notas diarias (ya se usa — mantener).
- Prefijos numéricos (`10-`, `20-`) para forzar orden.

### 5.4 Relación con tasks.md (mejorar el flujo)
- **tasks.md como fuente de verdad** (ya es así). Mejorar:
  - Agregar **links bidireccionales** desde cada tarea a su nota de proyecto (p.ej. `[[10-PROYECTOS/Ghost-Trader]]`).
  - Que H.E.L.E.N. haga **write-back automático**: tarea ✅ en tasks.md → actualiza la nota original del proyecto.
  - **Plantilla de tarea** con metadatos YAML (prioridad, ventana, proyecto, dependencia) para que Dataview la pueda filtrar.

### 5.5 Dashboard de MODO FANTASMA
- Activar el **reporte semanal** (la carpeta `Reportes/` está vacía — el domingo H.E.L.E.N. debería generar el resumen con métricas).
- Crear `2026-08/` para retomar el registro diario de agosto.

### 5.6 Separar código de notas (higiene del repo)
- Mover `assistentLLM-master/` a un repo git dedicado. El vault debe ser **solo markdown + assets**.
- Si se quiere mantener documentación técnica, usar subcarpeta `docs/` dentro del proyecto, nunca código fuente completo.

### 5.7 Archivos de infraestructura
- Mover scripts (`backup-obsidian.sh`, `sync-push.sh`, `watcher.sh`, `check-flag.sh`, `_INFRA-*`) a `90-SISTEMA/` o fuera del vault (a `~/.openclaw/`). No son notas y ensucian la raíz.

### 5.8 Bandeja de entrada (Inbox)
- Crear `00-INBOX/` para captura rápida de notas sin categorizar. Revisar semanalmente y clasificar. Evita acumular archivos sueltos en la raíz.

---

## Resumen ejecutivo (prioridades)

| Prioridad | Acción | Valor | Riesgo |
|-----------|--------|-------|--------|
| 🔴 1 | Fusionar los 2 planes de Ghost Trader (595L vs 2004L) | Alto — evita pérdida de trabajo | Bajo |
| 🔴 2 | Eliminar carpetas espejo (`FINANZAS-Y-PROYECTOS`, `Bot-mt5`) | Alto — elimina confusión | Bajo |
| 🟠 3 | Unificar Prototipo X en una sola carpeta | Alto | Medio |
| 🟠 4 | Sacar `assistentLLM-master/` (código) del vault | Alto — higiene del repo | Medio |
| 🟡 5 | Reorganizar por dominio (Sección 3) | Medio-Alto | Medio |
| 🟡 6 | Instalar Dataview + Templates + Dashboard | Alto — funcionalidad | Muy bajo |
| 🟢 7 | Corregir typos y convención de nombres | Bajo | Muy bajo |
| 🟢 8 | Consolidar los 3 sistemas de registro diario | Medio | Medio |

**Regla de oro:** Ejecutar en orden (duplicados primero, luego estructura, luego funcionalidad). Cada fase termina con `sync-push.sh` y verificación del sync iOS. Confirmar cada fase con Mr. Jair antes de avanzar.
