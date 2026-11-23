---
created: 2026-11-16
updated: 2026-11-23
version: v2.0
estado: plantilla viva — mejorar con cada turno
tags: [datacenter, operatividad, RMA, commissioning, disciplina]
---

# 🧩 Estándar Mínimo de Operatividad — Técnico DC

> Plantilla viva. Cada turno que aprendas algo, se agrega aquí.
> Si está aquí, está priorizado.
> v2.0 (23/11): Disciplina Operativa integrada como sección 0.

## 0. Disciplina operativa — toda maniobra

### 7 pasos obligatorios
1. Autorización — ticket / quién autoriza / ventana hora inicio-fin
2. Impacto — qué se afecta si sale mal, quién debe saber (NetOps, cómputo)
3. Pre-check — LEDs, link, errores, foto + captura monitoreo real
4. Maniobra — solo lo autorizado, un cambio a la vez, paso a paso escrito
5. Verificación — link UP, velocidad, CRC/flaps 5 min, lado remoto confirma + monitoreo valida dato real
6. Registro — ticket, DCIM, fotos antes/después, seriales/PNs, repuestos a bodega con acta
7. Lección — qué falló en el orden, no solo en el fierro

### 5 prohibidos
1. Apagar desde PDU sin shutdown controlado confirmado
2. Mezclar UTP en organizadores de potencia
3. Dejar repuestos tirados
4. Basura/comida en rack
5. Cerrar turno sin entrega escrita

### Mínimo medible por turno
- Inicio 15 min: leer entrega anterior + tickets + ronda visual (LEDs, ruido, temp, basura, cables) — foto si hay hallazgo
- Durante: 7 pasos siempre. Sin autorización escrita no se toca
- Cierre 15 min: tickets + DCIM al día, repuestos a bodega, fotos cargadas, entrega escrita (hecho / pendiente / monitorear)
- Métrica: turno perfecto = 0 prohibidos + 100% maniobras con 7 pasos + entrega escrita

## 1. Gestión (80% del cargo)

- [ ] Tickets al día: abiertos, en curso y cerrados con evidencia
- [ ] DCIM / inventario actualizado (serial, ubicación, estado)
- [ ] SOP/MOP leído y entendido ANTES de tocar fierros
- [ ] Ventana de mantenimiento validada antes de intervenir

## 2. Fierros (20% del cargo)

- [ ] Reemplazo FRU: disco, fuente, DIMM, ventilador
- [ ] Diagnóstico básico: POST, LEDs, SEL iDRAC/iLO, dmesg
- [ ] Validación post-cambio (ver checklist abajo)

## 3. RMA — flujo cuando toque

1. Apertura: serial, falla, logs, fotos → caso con fabricante
2. Tracking: # caso, SLA, estado
3. Recepción retorno: verificar serial/modelo/físico
4. Validación en cuarentena (NO directo a producción):
   - Encendido + POST limpio
   - iDRAC/iLO accesible + firmware estándar site
   - Discos/CPU/RAM visibles
   - Red link up
   - Sensores temp/voltaje en rango
   - Burn-in 2-4h + revisar logs (SEL, dmesg)
5. Si falla → reabrir caso con evidencia. Si pasa → programar ventana + commissioning

## 4. CLI mínimo

- [ ] SSH + PuTTY, IPMI/iDRAC/iLO
- [ ] Logs: `journalctl`, `dmesg`, SEL iDRAC
- [ ] Estado servicios + salud hardware por consola
- [ ] Red: ping, puertos switch, VLAN

## 5. Cierre obligatorio

Todo cambio deja: ticket + inventario + monitoreo actualizado.

---

# ✅ Checklist Commissioning Post-Mantenimiento

Usar cada vez que un equipo vuelve de RMA o se interviene.

## Físico
- [ ] Rack + rieles firmes
- [ ] Cableado potencia (doble fuente, PDU balanceada)
- [ ] Cableado datos (puertos correctos)
- [ ] Etiquetado TIA-606

## Energía
- [ ] Doble fuente activa
- [ ] Consumo esperado

## Gestión
- [ ] IPMI / iDRAC / iLO responde
- [ ] Credenciales estándar
- [ ] NTP + DNS OK
- [ ] Firmware en versión estándar del site

## Red
- [ ] Puertos en switch correcto (S4048/Z9664)
- [ ] VLAN correcta
- [ ] Ping + SSH OK

## Sistema
- [ ] SO / firmware versión estándar
- [ ] RAID sano
- [ ] Sin errores en logs (SEL, dmesg, journalctl)

## Monitoreo
- [ ] Aparece en DCIM
- [ ] Aparece en monitoreo + alertas configuradas

## Documentación y entrega
- [ ] Ticket cerrado: qué se hizo, serial, hora, responsable
- [ ] Inventario marcado como OPERATIVO
- [ ] Evidencia guardada (fotos/logs si aplica)

---

## 📌 Anexo: Lección 15/11 → 17/11 (MPO leaf)

Reportados puertos 5 y 7 caídos → falsos, estaban OK. Real: puertos 3-17 movidos antes sin gestión en switch → Zabbix ciego. Fierro quedó bien (peinado MPO, fracturas fuera, radios corregidos). Falló orden: PDU sin shutdown confirmado, sin ventana fija, repuestos tirados, UTP en potencia, sin paso a paso, entrega sin detalle, servilletas en rack.
Regla: todo cambio físico de puerto exige validación lógica + monitoreo/DCIM el mismo día.
Caso base de la disciplina operativa (origen 17/11, integrada 23/11).

---

## 📝 Mejoras pendientes (agregar con la práctica)
- [ ] Versiones firmware estándar del site (anotar cuando las tengas)
- [ ] Contactos / portal RMA por fabricante (Dell, HPE, etc.)
- [ ] Rack de cuarentena disponible (ubicación)
- [ ] Comandos exactos que uses en turno
