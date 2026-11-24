---
created: 2026-11-24
tags: [datacenter, fierros, FRU, diagnóstico, hardware]
---

# 🔧 Fierros 20% — FRUs + Diagnóstico

> **Principio:** El 80% de tu trabajo es gestión. Este 20% es cuando tocas fierros. Cada FRU que cambias sin procedimiento es un riesgo; cada uno con procedimiento es evidencia de que sabes.

---

## 1. Qué es un FRU

**FRU = Field Replaceable Unit.** Componente diseñado para reemplazarse en sitio, sin llevar el equipo al laboratorio. Si necesitas soldar, desarmar la board o usar herramientas especiales — no es FRU, es reparación de taller.

### FRUs por equipo (tu sitio)

| Equipo | FRUs | Hot-swap | Notas |
|--------|------|----------|-------|
| **SYS-422GS GPU** ×144 | 4× PSU 6.6kW, 4× fan 80mm, 32× DIMM DDR5, 8× E1.S NVMe, GPU tray | PSU sí / resto no | 84.6kg — 2 personas + rail kit. D2C cold plate |
| **Q3400 fabric** ×24 | 8× PSU, fans, supervisor | PSU/fan sí | Fat-tree 16+8 — no tumbar 2 del mismo pod |
| **SN5610** ×12 | PSU, fan | Sí | Ver M4 |
| **SN2201** ×52 | PSU, fan | Sí | OOB — si lo tumbas pierdes consola remota |
| **SN4700** ×4 | PSU, fan | Sí | Core OOB |
| **Power Shelf 33kW** ×8 | Módulos rectificadores | Sí | Coordinar con facility siempre |
| **CDU** ×8 | Sensores, válvulas | No | Líquido — MOP formal obligatorio |

---

## 2. Diagnóstico antes de tocar

**Regla de oro:** Ningún FRU se reemplaza por sospecha. Se reemplaza por evidencia. El orden es:

```
1. LED → ¿qué color? ¿cuál componente? (foto)
2. Consola → ¿qué dice el log? (captura)
3. BMC/iDRAC → ¿qué dice el SEL? (exportar)
4. Validación cruzada → ¿Zabbix dice lo mismo que el campo?
5. Decisión → ¿FRU específico o es otra cosa?
```

### Tabla de diagnóstico rápido

| Síntoma | Revisar primero | Comando / lugar | FRU probable |
|---------|----------------|-----------------|--------------|
| LED PSU ámbar | Redundancia + input | `show environment` / iDRAC power | PSU |
| LED fan rojo | RPM + temp | `show environment` / `ipmitool sdr` | Fan |
| DIMM error POST | Slot específico | SEL / `dmidecode -t memory` | DIMM ese slot |
| NVMe no aparece | Bahía + PCIe | `nvme list` / `lspci` | E1.S esa bahía |
| GPU throttling | Temp + power | `nvidia-smi` | Cold plate / pasta (no FRU simple) |
| Switch no arranca | Consola serie | Opengear → boot log | No es FRU — es firmware/config |
| Link caído | Ambos extremos | `show interfaces status` ambos lados | Cable/transceiver (no FRU del equipo) |

### Lo que NO es FRU (no lo toques como FRU)

- Firmware corrupto → reinstalación, no reemplazo
- Config errónea → rollback, no reemplazo
- Cable/transceiver dañado → cambiar cable, no el equipo
- Problema de energía del rack → facility, no FRU
- Bug de software → ticket al vendor, no FRU

---

## 3. Procedimiento de reemplazo

### Antes (pre-check)
- [ ] Autorización escrita con ventana (hora inicio/fin)
- [ ] Repuesto en mano: mismo Part Number, serial anotado
- [ ] Foto del antes (LED + ubicación + etiqueta)
- [ ] Baseline: captura de `show environment` / SEL / `dmesg`
- [ ] Si no es hot-swap: shutdown controlado confirmado

### Durante (1 FRU a la vez)
- [ ] Sacar → foto del slot vacío → insertar nuevo → confirmar click/asiento
- [ ] NO tocar otro FRU hasta verificar este
- [ ] Si algo no encaja: parar, no forzar. Verificar PN.

### Después (verificación)
- [ ] LED verde en el FRU nuevo
- [ ] Equipo reconoce el FRU (`show environment` / iDRAC / `dmidecode`)
- [ ] Sin errores nuevos en log/SEL
- [ ] Burn-in 2-4h si fue RMA o GPU
- [ ] DCIM actualizado (serial viejo → serial nuevo)
- [ ] Ticket con: serial viejo, serial nuevo, hora, responsable, fotos

---

## 4. RMA — cuando el FRU sale al vendor

| Paso | Acción |
|------|--------|
| 1 | Confirmar falla con evidencia (log + foto + serial) |
| 2 | Abrir caso con vendor (número de caso anotado) |
| 3 | Empacar FRU fallado (antiestático + etiqueta con caso) |
| 4 | Recibir reemplazo → verificar PN + serial |
| 5 | Instalar → burn-in → cerrar caso con evidencia |
| 6 | Actualizar DCIM + inventario de spares |

**Spares mínimos en sitio:** 2× PSU por modelo crítico, 4× fan, 4× DIMM, 2× NVMe, 2× transceiver por velocidad. Si bajas de eso → pedir reposición.

---

## 5. Errores comunes (no los cometas)

1. **Cambiar FRU por sospecha** → siempre con evidencia de log/LED/SEL
2. **Cambiar 2 FRUs a la vez** → si se arregla no sabes cuál era; si empeora no sabes qué rompiste
3. **No anotar seriales** → repuesto al piso = repuesto perdido
4. **Forzar conector** → si no entra suave, está mal orientado o es PN equivocado
5. **Olvidar DCIM** → si no está escrito, no pasó
6. **Hot-swap lo que no es hot-swap** → DIMM/NVMe/GPU tray con equipo encendido = daño seguro

---

<div align="center">

`🦾 H.E.L.E.N. — Toca fierros con evidencia, no con sospecha.`

</div>
