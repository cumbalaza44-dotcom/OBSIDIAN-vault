---
created: 2026-11-16
updated: 2026-11-16
version: v1.0
estado: plantilla viva — mejorar con cada turno
tags: [datacenter, operatividad, RMA, commissioning]
---

# 🧩 Estándar Mínimo de Operatividad — Técnico DC

> Plantilla viva. Cada turno que aprendas algo, se agrega aquí.
> Si está aquí, está priorizado.

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

## 📝 Mejoras pendientes (agregar con la práctica)
- [ ] Versiones firmware estándar del site (anotar cuando las tengas)
- [ ] Contactos / portal RMA por fabricante (Dell, HPE, etc.)
- [ ] Rack de cuarentena disponible (ubicación)
- [ ] Comandos exactos que uses en turno
