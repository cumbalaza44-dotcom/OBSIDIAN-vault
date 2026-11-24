---
created: 2026-11-24
version: v1.0
tipo: SOP/MOP formal
origen: Estandar-Operatividad-DC v2.2 (experiencia 15-23/11)
tags: [datacenter, SOP, MOP, procedimiento, ventana-mantenimiento]
---

# 📋 SOP-001 — Maniobra Estándar en Datacenter

> **Alcance:** Toda intervención física o lógica en equipos del datacenter (servidores, switches, energía, fibra).
> **Aplica a:** Técnico Especialista DC Hardware + cualquier rol que toque fierros.
> **Revisión:** Cada incidente alimenta este documento (sección 8).

---

## 1. Definiciones

| Término | Significado |
|---------|-------------|
| **SOP** | Standard Operating Procedure — procedimiento estándar, siempre igual |
| **MOP** | Method of Procedure — paso a paso específico para UNA maniobra puntual |
| **Ventana** | Periodo autorizado con hora inicio/fin exacta para intervenir |
| **FRU** | Field Replaceable Unit — componente reemplazable en sitio |
| **Baseline** | Estado previo documentado (foto + captura + valores) |
| **Rollback** | Plan para revertir si la maniobra falla |

---

## 2. Cuándo se necesita SOP vs MOP

| Situación | Documento | Ejemplo |
|-----------|-----------|---------|
| Tarea repetitiva y conocida | **SOP** (este documento) | Reemplazo FRU, revisión de rack, ronda |
| Cambio puntual con riesgo | **MOP** específico | Migración de fibra, apagado de pod, firmware masivo |
| Emergencia (equipo caído) | **SOP** + ticket post | Restaurar link, reemplazar PSU fallada |
| Cambio que toca producción | **MOP** obligatorio | Cualquier cosa que pueda tumbar servicio |

**Regla:** Si la maniobra puede afectar entrenamiento distribuido, GPUs o más de 1 rack → MOP formal, no basta este SOP.

---

## 3. Roles y autorizaciones

| Rol | Autoriza | No autoriza |
|-----|----------|-------------|
| **DC Ops / Supervisor** | Ventanas, MOPs, cambios en producción | — |
| **NetOps** | Cambios en enlaces de red | Cambios físicos en servidores |
| **Cómputo** | Ventanas en sus racks/GPUs | Cambios en fabric/red |
| **Facility** | Todo lo de energía/clima (PDU, UPS, CDU) | Cambios en equipos IT |
| **Técnico DC (tú)** | Ejecuta con autorización escrita | Nada sin ticket + ventana |

**Autorización verbal NO vale.** Si te dicen "hágale" de palabra → pides que lo escriban en ticket o chat del turno. Sin excepción.

---

## 4. Procedimiento — 7 fases obligatorias

### FASE 1 — Autorización
- [ ] Ticket creado con: qué, dónde (rack/U/equipo), por qué
- [ ] Quién autoriza (nombre + rol) registrado por escrito
- [ ] Ventana con hora inicio/fin exacta (no "cuando se pueda")
- [ ] Rollback definido: ¿qué hago si sale mal?

### FASE 2 — Análisis de impacto
- [ ] ¿Qué servicio cuelga de este equipo?
- [ ] ¿Qué pasa si lo tumbo 5 minutos?
- [ ] ¿A quién le duele? (NetOps / cómputo / facility avisados)
- [ ] Si toca GPUs/entrenamiento → escalar a MOP formal

### FASE 3 — Pre-check (baseline)
- [ ] Foto: LEDs + ubicación + etiquetas (antes)
- [ ] Captura: `show interfaces status` / `ethtool` / SEL / `dmesg`
- [ ] Valores base: errores, CRC, temp, voltaje (anotados)
- [ ] Monitoreo: captura Zabbix/DCIM con timestamp
- [ ] Si Zabbix contradice al CLI → desconfiar de Zabbix, anotar discrepancia

### FASE 4 — Ejecución
- [ ] Paso a paso escrito ANTES de empezar (no improvisar en campo)
- [ ] Un cambio a la vez (si son 4 cables → uno por uno con validación)
- [ ] Solo lo autorizado (lo demás se anota, no se toca)
- [ ] Fibra: seguro del conector, radio ≥3cm, velcro no bridas
- [ ] Energía: shutdown controlado confirmado antes de tocar PDU

### FASE 5 — Verificación
- [ ] Link UP + velocidad correcta (comparar con baseline)
- [ ] Errores/CRC en 0 o no creciendo (5 min mínimo)
- [ ] Lado remoto confirma (ambos extremos UP)
- [ ] Monitoreo muestra estado real (actualizar DCIM/Zabbix si es necesario)
- [ ] FRU nuevo reconocido por el sistema

### FASE 6 — Registro
- [ ] Ticket: qué se hizo, serial viejo/nuevo, hora real, responsable
- [ ] DCIM actualizado el mismo día
- [ ] Fotos antes/después en ticket (no en celular)
- [ ] Repuestos a bodega con acta (no al piso)
- [ ] Etiquetado TIA-606 en ambos extremos si hubo recableado

### FASE 7 — Lección aprendida
- [ ] ¿Qué fase se saltó o se hizo a medias?
- [ ] Documentar en este SOP (sección 8) o crear MOP específico
- [ ] Si se repite la misma lección 2 veces → crear checklist dedicado

---

## 5. Prohibiciones (5)

| # | Prohibido | Por qué | Forma correcta |
|---|-----------|---------|----------------|
| 1 | Apagar desde PDU sin shutdown | Corrompe filesystem, mata RAID, GPUs inconsistentes | Shutdown OS/iDRAC → confirmar → recién ahí PDU |
| 2 | UTP en organizadores de potencia | Inducción EM, calentamiento, tracing imposible | Potencia y datos separados siempre |
| 3 | Repuestos tirados en piso/rack | Se pierden seriales, se dañan, nadie sabe si sirven | Bodega con acta el mismo turno |
| 4 | Basura/comida en rack | Plagas, obstruye airflow, riesgo corto | Solo fierro/cable dentro del rack |
| 5 | Cerrar turno sin entrega escrita | Siguiente turno a ciegas, repite diagnósticos | Hecho/pendiente/monitorear, siempre |

---

## 6. Métrica de cumplimiento

**Turno perfecto =**
- 0 prohibiciones violadas
- 100% maniobras con 7 fases
- Entrega escrita al cierre

---

## 7. Documentos relacionados

| Doc | Ubicación |
|-----|-----------|
| Estándar personal (origen) | `00-Disciplina/Estandar-Operatividad-DC.md` |
| FRUs + diagnóstico | `03-Fierros-FRUs/FRU-Diagnostico-Reemplazo.md` |
| Maniobras M1–M8 | `06-Maniobras/M*.md` |
| Ficha de rack | `05-Turnos/Ficha-Rack-Template.md` |
| Entrega de turno | `05-Turnos/Entrega-General-Turno.md` |
| Incidentes INC-001/002 | `01-Incidentes/` |

---

## 8. Historial de cambios

| Fecha | Versión | Cambio | Origen |
|-------|---------|--------|--------|
| 15/11 | — | Caso base: MPO leaf, falló orden no técnica | INC-002 |
| 16/11 | v1.0 | Estándar personal creado | Turno |
| 23/11 | v2.2 | 4 objetivos + 7 pasos detallados + entrega | Turno |
| 24/11 | SOP v1.0 | Formalización a SOP (este documento) | B1+B2 |

---

<div align="center">

`🦾 SOP-001 v1.0 — Si no está escrito, no pasó.`

</div>
