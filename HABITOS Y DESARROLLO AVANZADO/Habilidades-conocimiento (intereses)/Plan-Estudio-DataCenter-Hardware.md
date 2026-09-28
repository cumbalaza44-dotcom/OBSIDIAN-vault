# Plan de Estudio — Técnico Especialista Data Center Hardware (IA)

> Rol: disponibilidad y operatividad del hardware crítico en datacenters de IA.
> Sesiones: 30-45 min/noche (6:30-9:30 PM). 6 semanas, una capa por semana.
> Regla: teoría 40% + práctica mental/checklist 60%. Cada semana cierra con validación.

## Semana 1 — Fundamentos físicos del DC
- [ ] Rack 19": U, rieles, PDU básica vs switched, UPS, top-of-rack
- [ ] Energía: monofásica vs trifásica, fuentes redundantes 1+1 / 2+2, power draw GPU
- [ ] Clima: pasillo frío/caliente, CFM fans, sensores temp/humedad, alertas
- [ ] Cableado: cobre Cat6A vs fibra OM4/OS2, patch panels, etiquetado TIA-606
- [ ] Seguridad: ESD (pulsera, tapete), EPO, extinción, bitácora de acceso
- ✅ Validación: dibujar de memoria un rack con PDU, UPS, ToR y flujo de aire

## Semana 2 — FRUs y diagnóstico
- [ ] Fuentes (PSU): hot-swap, LEDs, validación post-reemplazo
- [ ] Ventiladores: zonas, curvas, reemplazo sin apagado
- [ ] RAM ECC: canales, errores corregibles vs no corregibles, reseat
- [ ] Discos: NVMe/SAS/SATA, hot-swap, RAID 0/1/5/6/10 a nivel conceptual
- [ ] NICs: 25/100/200/400G, DAC vs transceiver, link/flap
- [ ] Aislamiento de falla: síntoma → LED/post → swap mínimo → validar
- ✅ Validación: checklist propio de reemplazo FRU (apagar? ESD? validar? documentar?)

## Semana 3 — Servidores IA y GPUs
- [ ] Arquitectura: CPU + GPUs (H100/A100 o similar), NVLink/NVSwitch, PCIe Gen5
- [ ] DPUs: qué descargan (red, storage, seguridad), diferencia vs NIC
- [ ] Termales y potencia: TDP por GPU, airflow, throttling, nvidia-smi básico
- [ ] BMC: iDRAC / iLO / IPMI, KVM remoto, SEL logs, firmware
- [ ] Cableado alta potencia: conectores, fases, validación de carga
- ✅ Validación: leer un SEL log de ejemplo e identificar causa probable

## Semana 4 — RMA y commissioning
- [ ] RMA: apertura de caso, seriales, fotos, empaque antiestático, seguimiento
- [ ] Validación de equipo reparado: burn-in básico, stress, comparación pre/post
- [ ] Commissioning: rack → cablear → energizar → BMC → firmware → test → entrega
- [ ] Checklist puesta en servicio: torque, etiquetado, DCIM, fotos, firma
- [ ] Documentación: qué registrar siempre (serial, parte, hora, técnico, resultado)
- ✅ Validación: simular un RMA completo en papel con un caso ficticio

## Semana 5 — DCIM, inventarios y red física
- [ ] DCIM: altas/bajas/movimientos, ubicación U exacta, auditoría
- [ ] Inventario: seriales, FRUs, spares, ciclo de vida
- [ ] Red física: ToR, agregación, fibra MPO, limpieza de conectores, OTDR conceptual
- [ ] Coordinación: Network Ops, Physical Connectivity, Datacenter Ops — quién hace qué
- [ ] Procedimientos: SOP, MOP, ventanas de mantenimiento, rollback
- ✅ Validación: auditar un rack ficticio y dejarlo cuadrado en formato DCIM

## Semana 6 — Incidentes críticos y puesta a punto
- [ ] Severidades: P1/P2/P3, tiempos de respuesta, comunicación
- [ ] Recuperación: aislar, mitigar, reemplazar, validar, post-mortem
- [ ] Herramientas: multímetro, probador de fibra, etiquetadora, kit ESD
- [ ] Repaso: 20 preguntas de las semanas 1-5, cerrar huecos
- [ ] Simulacro: incidente GPU caída en hora pico — paso a paso
- ✅ Validación final: explicar en voz alta el flujo completo sin mirar notas

## Progreso
| Semana | Estado | Fecha cierre |
|--------|--------|--------------|
| 1 Físico | ⬜ | |
| 2 FRUs | ⬜ | |
| 3 GPUs | ⬜ | |
| 4 RMA | ⬜ | |
| 5 DCIM | ⬜ | |
| 6 Incidentes | ⬜ | |

## Notas de campo
- Marcas vistas en sitio: _
- Modelo de servidor más común: _
- Sistema DCIM usado: _
- Contacto RMA principal: _
