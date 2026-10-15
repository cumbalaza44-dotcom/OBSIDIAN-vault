# 📋 Planes de Soporte — Red, Appliances y Otros (Switches / NICs-DPU / UFM / XE9680)

> Fuente: Troubleshooting_plan_APN.xlsx (13 hojas, verificado 15/10/2026).
> Complementa: Planes-Soporte-3-Servidores.md (servidores) y Playbook-Runbook-DC.md (troubleshooting R/M/G).
> Plantilla: Perfil → Plan de soporte → Troubleshooting por LED → Checklist → Puntos de control.

---

## 1. Switches de fabric (4 modelos)

### Perfil comparado
| Modelo | Rol probable | Software | LED sistema | LED fan/PSU |
|---|---|---|---|---|
| **MSN5610-WS2RC** | Leaf/spine 400G (InfiniBand/Ethernet) | MLNX-OS/Onyx | ámbar = fallo crítico (CPU/firmware) o alta temp | ámbar = FRU swap |
| **MSN2201-CB2RC** | Leaf compacto (Spectrum-4) | Onyx/NOS | **rojo** = fallo crítico o alta temp | rojo = FRU swap |
| **MSN4700-WS2RC** | Spine 800G (Spectrum-4) | **NVIDIA Onyx (MLNX-OS)** | ámbar = fallo crítico o alta temp | fan ámbar / PSU **rojo** |
| **SSE-MQM3400-RA** | Fabric box (NVL72 / Q3400 family) | — | ámbar = fallo crítico o alta temp | ámbar/rojo = FRU swap |

### Troubleshooting unificado (patrón común de los 4)
1. **LED sistema parpadea >5 min** → el SO/NOS no arrancó, solo vive el firmware → **consola (RS-232/management)** y revisar estado del software. Reinicio primero; si persiste → firmware/reinstall.
2. **LED sistema ámbar/rojo** → ① verificar ambiente (inlet temp) ② si ambiente OK → fallo CPU/firmware → logs + caso.
3. **LED fan ámbar/rojo** → verificar inserción completa + nada bloquea airflow → **swap FRU ventilador**.
4. **LED PSU ámbar/rojo** → revisar cable/entrada → **swap PSU** (2+N: cambiar en caliente sin caída).

### Checklist diario (switches)
□ LEDs sistema verde · □ Enlaces sin CRC/discards nuevos · □ Velocidad negociada = diseño · □ Fans/PSU verde · □ Temp inlet en rango · □ Firmwares vs baseline

### ⚠️ Puntos de control
- **NO tocar config desde hardware** — config/fabric es de Network Operations; tú: FRU, LEDs, consola para diagnóstico.
- LED parpadeando ≠ LED rojo: parpadeo = SO caído (software); sólido = fallo crítico/temps (hardware/ambiente).
- Swap de fan/PSU en caliente OK; **dejar de PSU o fan tras el swap = deuda**, reparar el mismo turno.

---

## 2. NICs / DPUs (3 componentes PCIe)

### Perfil
- **BlueField-3 BF3230** — DPU (offload RedHat/NVIDIA): 2× 400G o configurable; PCIe 5.0 x16.
- **ConnectX-7 900-9X766-003N** — NIC 400G NDR; PCIe 5.0.
- **AOC-623106AN-CDAT** — cable/AOC activo (attach cable); mismo patrón de falla que NIC.

### Troubleshooting (mismo árbol para los 3)
1. **No detectada** → asentar en ranura → compatibilidad ranura/tarjeta → **probar otra ranura PCIe** → drivers originales/actualizados → **BIOS actualizado** → reboot.
2. **Deja de funcionar** → reseat → **otro cable** → reinstalar drivers (archivos corruptos) → reboot.
3. **Falló tras instalar otra tarjeta** → retirar y reinstalar TODAS → verificar cables → BIOS latest.
4. **LED link OFF** → **otro puerto en el switch** → cable bien conectado y de longitud válida → compatibilidad switch↔puerto.
5. **LED ON sin tráfico** → driver cargado → **misma velocidad y dúplex en adaptador y enlace**.

### Checklist (tras cualquier swap NIC/DPU)
□ Detectada en BIOS/OS · □ Driver versión correcta · □ LED link ON · □ Velocidad = diseño · □ Sin CRC en el enlace · □ DCIM: serial/P/N/ranura actualizados

### ⚠️ Puntos de control
- ESD obligatorio; **cambio físico = actualización DCIM en el mismo turno**.
- Solo 1 cambio a la vez (aislar causa).
- Link ON ≠ comunicación — validar velocidad/dúplex siempre.

---

## 3. UFM MUA9702H-2SFS — "El gerente de tráfico"

### Perfil
Appliance UFM Enterprise (gestión del fabric InfiniBand): 2 fuentes, disks RAID, management Ethernet, LED de sistema con botón de encendido integrado.

### Troubleshooting por LED
| Señal | Significado | Acción |
|---|---|---|
| **LED sistema ROJO** | fallo crítico | **desenchufar y llamar a NVIDIA support** |
| **PSU off/ROJO** | energía | verificar tomacorriente, rango 100-240VAC, reseat del cable |
| **Botón encendido se apaga** | térmica/obstrucción | verificar airflow, limpiar polvo de orificios y paneles (aspiradora) |
| **Link Ethernet OFF** | cable/firmware | ambos extremos + seguros → firmware HCA/appliance → apretar adaptadores de medios |
| **Link ON sin tráfico** | driver/config | driver cargado → velocidad/dúplex |
| **LEDs actividad OFF** | servicio caído | **verificar que UFM esté iniciado** |
| **Disco ámbar SÓLIDO** | SSD defectuoso | **reemplazar SSD** |
| **Disco ámbar PARPADEANDO** | RAID rebuild | **esperar hasta 48 h** — NO extraer disco |
| **Apagado/no responde** | — | botón → si no: desenchufar, **esperar 5 min**, enchufar, encender → si no enciende: PSU → si enciende: revisar logs UFM (causa del apagado) + temp + fans → aún sin respuesta: **soporte NVIDIA Networking** |

### Checklist diario (UFM)
□ LED sistema verde · □ Servicio UFM up · □ Disks sin ámbar · □ Enlaces activos · □ Temp/fans OK · □ Último firmware

### ⚠️ Puntos de control
- **Ámbar parpadeante ≠ ámbar sólido**: parpadeo = rebuild en curso (tocar = perder horas de reconstrucción); sólido = SSD muerto.
- LED rojo sistema = escalar a NVIDIA, no improvisar.
- Si el fabric se cae, UFM te dice dónde — es tu primera consulta en incidentes de red.

---

## 4. XE9680 — Dell PowerEdge XE9680 (GPU, fuera de topología — verificar origen)

### Perfil
Servidor GPU Dell 6U, 8× GPU, diseño para IA; aquí aparece en el XLSX con matriz de **indicadores frontales** (no de sistema).

### Tabla de indicadores
| Indicador | Significa ámbar/amarillo sólido cuando... | Acción |
|---|---|---|
| **Conducción (disco)** | error de transmisión en disco | Sistema Event Log → diagnóstico online → **reiniciar y ePSA** → si RAID: config del adaptador HBA |
| **Temperatura** | error térmico (inlet fuera de rango o fan fallido) | verificar: fan retirado/fallido · cubierta/airflow covers puestos · inlet OK · flujo externo libre |
| **Eléctrico** | voltaje fuera de rango, PSU o VR fallido | event log → **LED de la PSU** → reseat PSU |
| **Memoria** | error de módulo de memoria | event log → ubicación del DIMM → **reseat del módulo** |
| **PCIe** | error de tarjeta PCIe | reboot → actualizar drivers → **reseat de la tarjeta** |

### ⚠️ Puntos de control
- **XLSX lo marca "fuera de topología"** — primer paso en sitio: confirmar si realmente está en el DC o es de otra villa/cliente.
- Cada ámbar pide: log → reseat → si persiste, escalar/RMA (nunca saltar a swap sin diagnóstico).

---

## 🔗 Dónde encaja cada uno en tu cargo
| Equipo | Rol de ti (Hardware) | Escala a |
|---|---|---|
| Switches | LEDs, FRU fan/PSU, consola diagnóstica | **Network Ops** (config, fabric, rutas) |
| NICs/DPUs | reseat, swap, drivers, validación | Network Ops si enlace caído persiste |
| UFM | SSD swap, power cycle, airflow | **NVIDIA support** (LED rojo); NetOps (servicio) |
| XE9680 | diagnóstico indicadores, reseat | N3/plataforma si persiste |

---

## ✅ Commissioning general (igual que servidores)
□ POST/boot completo · □ Enlaces a velocidad de diseño sin CRC · □ Sensores en rango · □ Firmware vs baseline · □ Prueba funcional del FRU tocado · □ Bitácora · □ DCIM actualizado · □ Ticket con evidencia
