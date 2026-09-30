# Plan de Estudio — Técnico Especialista Data Center Hardware (IA)

> Rol: disponibilidad y operatividad del hardware crítico en datacenters de IA.
> Modo: intensivo — usa todo el tiempo disponible.
> Ventanas: Mañana 5:10-8:00 AM (lectura + repaso) | Noche 6:30-9:30 PM (bloque principal 2-3h) | Finde (simulacros + validación)
> Regla: teoría 30% + práctica/checklist 70%. Cada día cierra con 3 preguntas de auto-test.

## Semana 1 (28 Sep – 4 Oct) — Fundamentos físicos + Energía
### Lun 28 — Rack y energía
- [ ] Rack 19": U = 1.75", rack 42U, DGX 8U (visto hoy)
- [ ] PDU básica vs switched/monitored, UPS, EPO
- [ ] Monofásica vs trifásica, PDU 22 kW, regla 80% carga
- Auto-test: ¿cuántos servers 8 kW en PDU 22 kW? ¿por qué no el tercero?

### Mar 29 — Clima y airflow
- [ ] Pasillo frío/caliente, CFM, blanks en U vacíos
- [ ] Sensores temp/humedad, umbrales, alertas
- [ ] Throttling térmico en GPU, consecuencias
- Auto-test: dibujar flujo de aire de memoria

### Mié 30 — Cableado cobre y fibra
- [ ] Cat6A vs fibra OM4/OS2, cuándo usar cada uno
- [ ] Patch panels, MPO, limpieza de conectores
- [ ] Etiquetado TIA-606, colores estándar
- Auto-test: etiquetar un enlace ficticio completo

### Jue 1 — Seguridad física y ESD
- [ ] ESD: pulsera, tapete, empaque antiestático
- [ ] EPO, extinción por gas, bitácora de acceso
- [ ] SOP/MOP: qué son, cuándo aplican
- Auto-test: checklist ESD antes de tocar un server

### Vie 2 — Repaso + validación semanal
- [ ] 20 preguntas semana 1, cerrar huecos
- [ ] Dibujar rack completo de memoria (PDU, UPS, ToR, airflow)
- [ ] Actualizar notas de campo con lo visto en sitio

### Sáb 3 / Dom 4 — Simulacro + SSH + lectura
- [ ] Simulacro: rack con 2× DGX 8 kW en PDU 22 kW — ¿qué pasa si agregan un tercero?
- [ ] 🔐 SSH a servidores: conexión, llaves, config/alias, hardening básico
- [ ] Lectura diaria + planear semana 2

## Semana 2 (5 – 11 Oct) — FRUs y diagnóstico
### Lun 5 — Fuentes y ventiladores
- [ ] PSU hot-swap 1+1/2+2, LEDs, validación post-reemplazo
- [ ] Fans: zonas, reemplazo sin apagado, curvas

### Mar 6 — RAM ECC y discos
- [ ] ECC corregible vs no corregible, reseat, canales
- [ ] NVMe/SAS/SATA, hot-swap, RAID 0/1/5/6/10 conceptual

### Mié 7 — NICs, GPUs, DPUs (identificación)
- [ ] NICs 25/100/200/400G, DAC vs transceiver, link/flap
- [ ] GPU vs DPU: qué hace cada una, cómo identificarlas físicamente

### Jue 8 — Aislamiento de falla
- [ ] Flujo: síntoma → LED/post → SEL → swap mínimo → validar
- [ ] BMC: iDRAC/iLO/IPMI, KVM, lectura de logs

### Vie 9 — Checklist FRU propio + repaso
- [ ] Checklist: apagar? ESD? foto pre? swap? validar? documentar? DCIM?
- [ ] 20 preguntas semana 2

### Sáb 10 / Dom 11 — Simulacro
- [ ] Simulacro: server con LED ámbar en PSU + temp alta — paso a paso

## Semana 3 (12 – 18 Oct) — Servidores IA a fondo
- [ ] Lun: arquitectura CPU + 8× GPU, NVLink/NVSwitch, PCIe Gen5
- [ ] Mar: TDP por GPU (700W H100), power draw total, nvidia-smi básico
- [ ] Mié: BMC a fondo, SEL logs, firmware, KVM remoto
- [ ] Jue: cableado alta potencia, fases, validación de carga
- [ ] Vie: repaso + 20 preguntas
- [ ] Finde: leer un SEL log real e identificar causa

## Semana 4 (19 – 25 Oct) — RMA y commissioning
- [ ] Lun: RMA — apertura, seriales, fotos, empaque, seguimiento
- [ ] Mar: validación equipo reparado — burn-in, stress, pre/post
- [ ] Mié: commissioning — rack → cablear → energizar → BMC → firmware → test → entrega
- [ ] Jue: checklist puesta en servicio + documentación obligatoria
- [ ] Vie: repaso + simular RMA completo en papel
- [ ] Finde: simulacro commissioning de un DGX ficticio

## Semana 5 (26 Oct – 1 Nov) — DCIM, inventarios y red física
- [ ] Lun: DCIM — altas/bajas/movimientos, ubicación U exacta
- [ ] Mar: inventario — seriales, FRUs, spares, ciclo de vida
- [ ] Mié: red física — ToR, agregación, MPO, OTDR conceptual
- [ ] Jue: coordinación — Network Ops, Physical Connectivity, Datacenter Ops
- [ ] Vie: SOP/MOP, ventanas de mantenimiento, rollback
- [ ] Finde: auditar un rack ficticio y dejarlo cuadrado en formato DCIM

## Semana 6 (2 – 8 Nov) — Incidentes críticos y cierre
- [ ] Lun: severidades P1/P2/P3, tiempos, comunicación
- [ ] Mar: recuperación — aislar, mitigar, reemplazar, validar, post-mortem
- [ ] Mié: herramientas — multímetro, probador fibra, etiquetadora, kit ESD
- [ ] Jue: repaso 40 preguntas semanas 1-5
- [ ] Vie: simulacro final — GPU caída en hora pico, paso a paso
- [ ] Finde: validación final — explicar flujo completo en voz alta sin notas

## Progreso
| Semana | Foco | Estado | Cierre |
|--------|------|--------|--------|
| 1 (28 Sep–4 Oct) | Físico + energía | 🔄 en curso | |
| 2 (5–11 Oct) | FRUs | ⬜ | |
| 3 (12–18 Oct) | Servidores IA | ⬜ | |
| 4 (19–25 Oct) | RMA + commissioning | ⬜ | |
| 5 (26 Oct–1 Nov) | DCIM + red | ⬜ | |
| 6 (2–8 Nov) | Incidentes + cierre | ⬜ | |

## Notas de campo
- Marcas vistas en sitio: _
- Modelo de servidor más común: _
- Sistema DCIM usado: _
- Contacto RMA principal: _
- PDU estándar del sitio: _
