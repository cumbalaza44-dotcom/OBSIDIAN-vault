# 📘 Manual de Procesos DC — Playbook Operativo

> Misión: **manual (playbook) de los 16 equipos** — observar equipo → definir proceso → redactar cómo hacerlo.
> Fuentes: 10 PDFs OEM (16/10/2026) + Estándar de Etiquetado SOMOS-DC-EST-001 + XLSX Troubleshooting_plan_APN.
> Complementa: Playbook-Runbook-DC.md (troubleshooting R/M/G) · Planes-Soporte-*.md (operación).
> Creado: 16/10/2026.

---

## 🧩 Estructura canónica de todo proceso (plantilla SOP)

Todo proceso del manual usa estas 8 secciones — sin excepción:

1. **IDENTIFICACIÓN** — equipo + modelo/SKU · ID (`P-<equipo>-<componente>-<nn>`) · versión · fecha.
2. **OBJETIVO Y ALCANCE** — qué logra (1 frase) · cuándo aplica · cuándo NO.
3. **PREREQUISITOS** — ticket/ventana · ESD · herramientas · repuesto validado (P/N vs autorizado).
4. **RIESGO Y SEGURIDAD** — severidad (P1-P4) · blast radius · peligros del equipo (líquido, 240VAC, 84 kg).
5. **PROCEDIMIENTO** — pasos numerados, 1 acción por paso, con checkpoint ✅ verificable.
6. **VALIDACIÓN** — checklist de cierre (POST, enlaces, sensores, firmware, prueba funcional).
7. **ROLLBACK** — cómo volver atrás o "no aplica".
8. **REGISTRO** — bitácora + DCIM + ticket con evidencia. **Cambio físico = DCIM en el mismo turno.**

---

## 📋 Procesos por equipo

### 🟢 P-422 — SYS-422GS-NB3RT-LCC (GPU ×144) — EQUIPO 1 ✅

#### Procesos detallados (notas propias)
- **P-422-PSU-01 — Reemplazo de PSU 6.6kW en caliente (2+2)** → ver `P-422-PSU-01.md`
- **P-422-FAN-02 — Reemplazo de fan externo (4× hot-swap)** → ver `P-422-FAN-02.md`
- *(Siguientes P-422: DIMM §3.4 · E1.S §3.6 · GPU drawer — confirmar MOP de líquido en sitio antes de redactar.)*

#### 🗺️ Ruta P-422 — los 20 procesos extraíbles del manual OEM MNL-2917
**Hechos:** ✅ 01 PSU §3.9 · ✅ 02 FAN §3.8
- **A. Desmontaje (3):** 03 rails/rack §2.3-2.4 (2 personas) · 04 retiro de energía §3.1 · 05 acceso/chasis §3.2
- **B. FRU (6):** 06 DIMM §3.4 · 07 E1.S §3.6 · 08 M.2 §3.6 · 09 PCIe/risers §3.7 · 10 batería §3.5 · 11 GPU drawer ⚠️ (requiere MOP líquido en sitio — NO redactar aún)
- **C. Configuración (4):** 12 CMOS clear §4.2/7.4 · 13 VROC RAID §6.3 · 14 update BIOS/BMC §8 · 15 TPM §6.1
- **D. Troubleshooting (3):** 16 árbol §7.3 + beep codes Anexo A · 17 crash dump BMC §7.4 · 18 interpretación Information LED §1.2
- **E. Operación (2):** 19 checklist diario · 20 commissioning (→ vive en Playbook-Runbook-DC, solo enlazar)

**Prioridad sugerida:** B (FRUs que toca a diario) → D (diagnóstico) → A → C → E.

---

### 📎 Proceso transversal — Etiquetado (SOMOS-DC-EST-001 v3.2)

#### P-TRX-LBL-01 — Etiquetado de cable nuevo / reparcheo
1. **IDENTIFICACIÓN:** todos los equipos · estándar SOMOS-DC-EST-001 v3.2 · TIA-606-C / ISO-IEC 14763-2.
2. **OBJETIVO:** que con solo leer la etiqueta se sepa dónde está cada punta y a qué circuito (CTO) pertenece.
3. **PREREQUISITOS:** registro de circuitos actualizado · Panduit Easy-Mark Plus · sala conocida (G/F/N/E).
4. **RIESGO:** P4 directo; etiqueta equivocada = P2 futuro (troubleshooting ciego).
5. **PROCEDIMIENTO:**
   1. Determinar sala+rack+U+puerto de AMBAS puntas: `SALA/RACK/POSICIÓN_U/PUERTO` (ej. `G01/R01/U05-08/IB0`).
   2. Etiqueta por posición (origen/destino por posición, sin prefijos F:/T:) — 3 líneas con ID de circuito si pasa por ODF.
   3. Troncales: `TR-<sala><rack>_<sala><rack>-nn`; lectura de la bandera de adentro hacia afuera.
   4. Imprimir desde el Registro; verificar rango U del chasis (ej. U05-08) y nombres de puerto por equipo (BMC desde 0, twin-port = P01.1/P01.2).
   5. ✅ **Checkpoint:** ambas puntas legibles desde el pasillo · coincide con el Registro de circuitos.
6. **VALIDACIÓN:** revisión visual cruzada etiqueta ↔ registro ↔ DCIM.
7. **ROLLBACK:** reetiquetar (nunca "dejar para después").
8. **REGISTRO:** Registro de circuitos + DCIM actualizados el mismo turno.

---

## 🗺️ Ruta — 16 equipos → manual completo

| # | Equipo | Fuente PDF | Estado |
|---|---|---|---|
| 1 | SYS-422GS (GPU) | ✅ manual OEM MNL-2917 | **procesos listos: P-422-PSU-01 · P-422-FAN-02 (notas propias)** |
| 2 | SYS-122H (CPU) | ✅ PDF local + PPTX 47 slides | pendiente |
| 3 | ASG-1115S (Storage) | ✅ manual OEM | pendiente |
| 4 | Switches SN2201/SN4700/MQM3400 | ✅ troubleshooting + Q32xx/Q34xx manual | pendiente |
| 5 | NICs/DPU (BF3/CX-7/CX-8/CX-6Dx) | ✅ 4 PDFs NVIDIA | pendiente |
| 6 | UFM MUA9702H | ✅ manual Gen 3.5 | pendiente |
| 7 | XE9680 | ✅ (indicadores) | pendiente |
| 8-16 | NVL72SW, Power Shelf, CDU, ODF, Opengear, routers, rack | ❌ sin datasheets | esperando docs |

**Dinámica por sesión:** observar 1 equipo (qué es/FRUs/LEDs) → elegir 1-2 procesos críticos → redactar SOP 8 secciones con fuente OEM → auto-test → siguiente.
