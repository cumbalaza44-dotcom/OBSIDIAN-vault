---
created: 2026-11-24
tags: [datacenter, DCIM, inventario, validacion-cruzada, documentacion]
---

# 🗂️ DCIM — Inventario + Validación Cruzada

> **DCIM = Data Center Infrastructure Management.** El sistema que dice qué hay, dónde está y cómo está. Si el DCIM miente, todos operan a ciegas (lección 15/11: Zabbix ciego).
> Tu trabajo: que el DCIM diga la verdad. Cada validación cruzada es un dato corregido.

---

## 1. Qué registra el DCIM

| Campo | Ejemplo | Fuente verdad |
|-------|---------|---------------|
| Ubicación | Rack B12, U22-24 | Placa del rack (físico) |
| Equipo | SYS-422GS | Etiqueta del equipo |
| Serial | SV-422GS-0144 | Sticker trasero / `dmidecode -s system-serial-number` |
| Modelo / PN | SYS-422GS-NV | Placa + `dmidecode` |
| Estado | Operativo / RMA / Cuarentena / Baja | Ticket + verificación |
| Puertos red | Eth1→Leaf-03:P12, Eth2→Leaf-04:P12 | Etiqueta cable + `lldpctl` / `show lldp neighbors` |
| Energía | PDU-A:C14, PDU-B:C15 | Etiqueta + trazado físico |
| Firmware | BMC 2.1.4 / BIOS 3.2 | `ipmitool mc info` / `show version` |
| Fecha instalación | 2026-09-15 | Ticket commissioning |
| Responsable | Jair Cumbalaza | Quien lo instaló/validó |

---

## 2. Validación cruzada — el método

**Principio:** ningún dato del sistema se da por cierto hasta verlo en campo. Mínimo 1 por turno.

### Procedimiento (5 min por equipo)

```
1. Elige un dato del DCIM/Zabbix (ej: "servidor X en rack B12 U22")
2. Ve al rack físico
3. Verifica: ¿está ahí? ¿el serial coincide? ¿los LEDs están verdes?
4. CLI: ¿el hostname/serial por consola coincide con el físico?
5. Resultado:
   ✅ Coincide → anota "validado [fecha]" (confianza +1)
   ❌ No coincide → hallazgo, corrige DCIM + ticket
```

### Qué validar (rotación semanal)

| Día | Foco | Comando campo |
|-----|------|---------------|
| Lun | Seriales (5 equipos) | `dmidecode -s system-serial-number` vs sticker |
| Mar | Puertos red (1 rack) | `show lldp neighbors` vs etiqueta cable |
| Mié | Energía (1 rack) | Trazado PDU físico vs DCIM |
| Jue | Firmware (5 equipos) | `show version` / `ipmitool mc info` vs DCIM |
| Vie | Temperatura (sensores) | `ipmitool sdr` vs Zabbix |

---

## 3. Discrepancias comunes (y qué hacer)

| Discrepancia | Causa típica | Acción |
|--------------|--------------|--------|
| Equipo no está donde dice DCIM | Movido sin registrar | Actualizar DCIM + ticket + buscar quién lo movió |
| Serial no coincide | Typo al ingresar o equipo reemplazado | Verificar físico 2 veces, corregir DCIM |
| Puerto dice UP pero LED apagado | Zabbix ciego / polling caído | Validar por CLI, reportar a monitoreo |
| Firmware desactualizado en DCIM | Actualizado sin registrar | Actualizar DCIM con versión real |
| Cable sin etiqueta | Instalación sin TIA-606 | Etiquetar + registrar (hallazgo) |
| Equipo en DCIM pero dado de baja físico | Baja sin registrar | Marcar baja en DCIM + acta |

---

## 4. Formato de registro de validación

Copiar al llenar ficha de rack o entrega de turno:

```
Validación [fecha] — Rack ___ U___:
- DCIM dice: [equipo] SN:[serial] FW:[versión] Puerto:[origen→destino]
- Campo muestra: [equipo] SN:[serial] FW:[versión] Puerto:[origen→destino]
- Resultado: ✅ coincide / ❌ discrepancia: [detalle]
- Acción: [ninguna / DCIM actualizado / ticket #___ / hallazgo para ___]
```

---

## 5. Meta: línea base en 15 turnos

| Turno | Rack | Validación | Estado |
|-------|------|------------|--------|
| 1 | ___ | ___ | ⏳ |
| 2 | ___ | ___ | ⏳ |
| 3 | ___ | ___ | ⏳ |
| ... | ... | ... | ... |
| 15 | ___ | ___ | ⏳ |

> 1 rack + 1 validación por noche tranquila. En 15 turnos el DC queda mapeado. Nadie más lo tiene. Ese es tu diferencial como operador.

---

<div align="center">

`🦾 DCIM que miente = operación a ciegas. Valida uno por turno.`

</div>
