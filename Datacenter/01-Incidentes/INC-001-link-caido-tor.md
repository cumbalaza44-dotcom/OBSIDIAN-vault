# INC-001 — Link caído servidor ↔ ToR (S4048-ON)

> Fecha: 2026-11-11 | Caso real practicado | Estado: ruta validada

## Síntoma
Servidor sin conectividad, eth0 DOWN. Switch S4048-ON puerto Te1/0/22.

## Ruta de diagnóstico (en este orden)

### 1. Servidor (sesión Linux)
```bash
ethtool eth0                        # ¿Link detected yes/no? Speed/Duplex
ethtool -S eth0 | grep -i "err\|crc\|drop"   # errores físicos
dmesg | grep -i link | tail -10     # historial link up/down
```
- Si `ethtool -m` dice "not supported" → normal en VM o cobre/DAC. Ir a plan B (dmesg + contadores).

### 2. Switch (sesión SSH aparte — NO en Linux)
```
show interfaces status
show interfaces transceiver         # RX Power: ¿llega luz?
show lldp neighbors                  # ¿hay vecino al otro lado?
```

### 3. Decisión
| RX Power | LLDP | Acción |
|----------|------|--------|
| Bajo/N/A | vacío | Físico → revisar fibra/transceiver (ventana) |
| Normal | vacío | Lógico → `show running-config interface Te1/0/22`, verificar shutdown/VLAN |
| Normal | ok | Flap: `shutdown` → `no shutdown`, luego contadores CRC |

### 4. Cierre
```
show interfaces counters errors     # CRC/drops post-fix
```
Documentar: puerto, causa raíz, acción, tiempo.

## Lecciones del caso
- Linux y switch = 2 sesiones distintas. `show` nunca va en Linux.
- OS9 S4048: `show interfaces transceiver` (no existe `show fiber-optic`).
- Con RX ok → no tocar hardware primero, revisar config.
- Calificación Mr. Jair: 8.5/10.

---
## Plantilla para próximo incidente
Copiar esta estructura: Síntoma → Ruta → Decisión → Cierre → Lecciones.
