# 📋 Entrega General de Turno — Datacenter

> Formato estándar. Se llena SIEMPRE al cerrar, aunque "no pasó nada".
> La ronda + validación + rack del día cuentan como evidencia.

---
**Fecha:** ___/___/___ | **Turno:** M / T / N | **Hora inicio-fin:** ___–___
**Técnico:** Jair Cumbalaza | **Racks asignados:** ___
**Entrega anterior leída:** Sí / No | **Tickets revisados:** ___

---

## 1. Ronda inicial (15 min)

- Hora ronda: ___
- LEDs / ruido / temp / basura / cables: ___
- Foto panorámica: Sí / No | Hallazgo: ___

## 2. Maniobras del turno (7 pasos c/u)

| # | Ticket | Qué se hizo | Ventana | Verificación | Estado |
|---|--------|-------------|---------|--------------|--------|
| 1 | | | | | |
| 2 | | | | | |

_Si no hubo maniobras: "Sin maniobras — turno de línea base (ver §3-4)."_

## 3. Rack documentado hoy

- Rack: ___ | Ficha: `Datacenter/06-Racks/Rack-___.md`
- Equipos: ___ | Seriales: ___/___ | Etiquetado OK: Sí/No (faltantes: ___)
- Fotos: ___

## 4. Validación cruzada del día

- Dato Zabbix/DCIM: ___
- Validación campo (CLI/LED/serial): ___
- ¿Coincide? Sí / No → Hallazgo: ___

## 5. Estado de infraestructura (semáforo NOC)

> Inspirado en formato oficial NOC Infraestructura Cómputo 23/11/2026.
> Marcar estado de cada dominio. Si no es Normal → detallar en observaciones.

| Dominio | Estado | Observaciones |
|---------|--------|---------------|
| Infraestructura general | Normal / Alerta / Crítico | ___ |
| Servidores / cómputo | Normal / Alerta / Crítico | ___ |
| Red / conectividad | Normal / Alerta / Crítico | ___ |
| Almacenamiento | Normal / Alerta / Crítico | ___ |
| Energía (PSU/PDU/UPS) | Normal / Alerta / Crítico | ___ |
| Temperatura / ambiente | Normal / Alerta / Crítico | ___ |
| GPU / aceleradores | Normal / Alerta / Crítico | ___ |
| Monitoreo Zabbix | Normal / Alerta / Crítico | ___ |

## 5b. Validaciones técnicas realizadas

| Componente | Validación | Resultado |
|------------|------------|----------|
| Servidores cómputo | Estado operativo / hardware / sensores | ___ |
| NIC / HCA | Link, errores, flaps, puertos | ___ |
| GPU / aceleradores | Disponibilidad, temp, errores | ___ |
| Almacenamiento | Capacidad, latencia, I/O | ___ |
| Red | Conectividad, interfaces, pérdida | ___ |
| Energía | PSU, PDU, UPS / alarmas | ___ |
| Temperatura | Sensores, ambiente | ___ |
| Zabbix | Triggers, hosts, agentes | ___ |

## 5c. Hallazgos para otros equipos

- Cómputo: ___
- Facility: ___
- Fibra: ___

## 6. Pendientes para siguiente turno

1. ___
2. ___

## 7. Qué monitorear

- ___
- ___

## 8. Métrica del turno

- Prohibidos: ___/5 (detalle si >0: ___)
- Maniobras con 7 pasos: ___/___
- Entrega escrita: Sí
- Turno perfecto: Sí / No

---
`🦾 Si está aquí, está priorizado.`
