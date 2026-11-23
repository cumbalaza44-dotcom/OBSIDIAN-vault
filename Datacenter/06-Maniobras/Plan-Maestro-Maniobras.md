---
created: 2026-11-23
updated: 2026-11-23
version: v1.0
estado: plan maestro — cada maniobra real lo alimenta
tags: [datacenter, maniobras, comprobaciones, validacion, topologia-fabricato]
---

# 🛠️ Plan Maestro de Maniobras y Comprobaciones — DC Fabricato

> Toda maniobra y comprobación existe para 4 cosas: trazabilidad, validación cruzada, proactividad, dinamismo en equipo.
> Si una maniobra no deja rastro, no valida nada, no adelanta línea base ni sirve a otro equipo → no se hace así.
> Fuente topología: 74 racks · 637 equipos · 10.049 cables (Fabricato_Topologia_XIO).

## 0. Dos sitios — no mezclar

| | 🏭 HARD (actual) | 🏗️ FABRICATO (nuevo, en construcción) |
|---|---|---|
| Estado | Operativo, tú estás de turno ahí | Casi finaliza construcción, pendiente entrega |
| Evidencia | INC-001 (S4048), INC-002 (COL-MDE-HARD-APD-FIBR01), CLI 17/11 | Topología XIO export (74/637/10049), sin campo aún |
| Switches | S4048-ON / Z9664 (Dell) | Q3400, SN5610, SN2201, SN4700 (NVIDIA) |
| Servidores | XE2_NIC7/8, Dell XE9680 (capacitación) | SYS-422GS ×144, ARS-121GL ×144 |
| Qué hacer | Operar + documentar línea base real | Estudiar topología + preparar playbooks + exigir inventario de entrega |
| Handover esperado | — | Inventario rack x rack: equipos, seriales, ubicaciones, puertos, etiquetas (validar contra topología XIO) |

> Regla: toda ficha M1–M8 lleva etiqueta de sitio. Si aplica a ambos, se marca. Si es solo uno, se dice explícito.

## 1. Mapa maniobra → topología → utilidad

| # | Familia maniobra | Dónde en Fabricato | Qué dolor resuelve | Tangible que deja |
|---|---|---|---|---|
| M1 | Link caído / flap (cobre-fibra) | SN5610 ×12, SN2201 ×52, ODF ×84, 10.049 cables | Entrenamiento o gestión caídos sin causa clara | Ticket + contadores antes/después + causa raíz |
| M2 | Fibra MPO degradada / fracturada | ODF ×84, GPU Fabric Q3400 ×24, mazo MPO-12 | Carriles desiguales >2.26 dB, riesgo cascada | Fotos + dB por lane + reemplazo 1x1 validado |
| M3 | FRU servidor GPU (PSU/fan/DIMM/NVMe) | SYS-422GS ×144 (PSU 6.6kW 2+2, 4 fans, 32 DIMM, 8 E1.S) | GPU fuera, throttling, POST fail | Serial viejo+nuevo + POST limpio + SEL limpio |
| M4 | FRU switch / PSU / fan | Q3400 ×24, SN5610 ×12, SN2201 ×52, SN4700 ×4 | Switch degradado, LED ámbar/rojo | LED verde + `show environment` + uptime |
| M5 | Energía busbar DC 50V | Power Shelf 33kW ×64 (32L+32R), CDU ×8 | Rack sin potencia, desbalance fases | Medición por riel + balance L/R + temp CDU |
| M6 | OOB / BMC inaccesible | SN2201 ×52 + SN4700 ×2, Opengear ×2, BMC todos los equipos | "No puedo entrar al equipo" = ciego | SSH BMC OK + ruta OOB trazada + puerto mapeado |
| M7 | Validación cruzada monitor vs campo | Zabbix vs CLI/LED/serial (cualquiera de los 637) | Zabbix ciego (lección 15/11) | 1 discrepancia/día registrada como hallazgo |
| M8 | Rack línea base (proactivo) | 74 racks (GR 24, NR 36, NW 8, MMR 6) | Nadie conoce el DC completo | 1 ficha rack/turno → 15 turnos = DC mapeado |

## 2. Rutina mínima por maniobra (hereda los 7 pasos del Estándar v2.2)

Toda M1–M8 corre con: Autorización → Impacto → Pre-check → Maniobra (1 cambio) → Verificación → Registro → Lección.
Lo que cambia por familia es el **pre-check** y la **verificación**. Eso está en cada ficha M1–M8.

## 3. Comprobaciones que NUNCA faltan (checklist universal)

Antes de decir "quedó bien", estas 5:
- [ ] Link UP en ambos extremos (no solo uno)
- [ ] Errores/CRC no creciendo 5 min (`show interfaces counters errors` / `ethtool -S`)
- [ ] LED verde/actividad normal (foto si hubo cambio)
- [ ] Monitoreo muestra lo real (Zabbix/DCIM actualizado el mismo día)
- [ ] Etiqueta TIA-606 en ambos extremos (si falta → hallazgo, no improvisación)

## 4. Orden de aprendizaje (de lo que más ves a lo raro)

1. **M6 OOB/BMC** — es tu herramienta diaria, sin esto estás ciego. Dominar SSH vía SN2201 + consola Opengear.
2. **M1 Link caído** — INC-001 ya lo tienes practicado. Repetir hasta que salga sin notas.
3. **M7 Validación cruzada** — 1 por turno. Es lo que te hace confiable frente a cómputo.
4. **M2 Fibra MPO** — INC-002 real. Fotos + dB + reemplazo 1x1.
5. **M3 FRU GPU** — PSU 6.6kW, fans, DIMM, E1.S del SYS-422GS. Con manual + checklist.
6. **M4 FRU switch** — PSU/fan de Q3400, SN5610, SN2201.
7. **M5 Energía busbar** — Power Shelf 33kW + CDU. Medir, no adivinar.
8. **M8 Rack línea base** — 1 por turno tranquilo. Acumula.

## 5. Cómo cada maniobra alimenta los 4 objetivos permanentes

- **Trazabilidad:** toda M deja ticket + ficha/entrega + fotos. Nada en la cabeza.
- **Validación cruzada:** toda M incluye M7 (monitor vs campo). Mínimo 1/día.
- **Proactividad:** sin incidentes → M8 (1 rack) + M7 (1 validación) + ronda con foto.
- **Dinamismo:** hallazgo útil → sección 5 de la Entrega General (cómputo/facility/fibra).

## 6. Métrica semanal

- Maniobras con 7 pasos: ___/___
- Validaciones cruzadas: ___/7 (meta: 1/día)
- Racks documentados: ___/74 (acumulado: ___)
- Playbooks nuevos o mejorados: ___
- Turnos perfectos (0 prohibidos + entrega): ___/___

---
*Alimenta: Estándar v2.2 §0.1 + Entrega General + Ficha Rack + Playbooks Mar 24 22:00.*
*Origen: INC-001 + INC-002 + CLI 17/11 + topología Fabricato 74/637/10049.*
