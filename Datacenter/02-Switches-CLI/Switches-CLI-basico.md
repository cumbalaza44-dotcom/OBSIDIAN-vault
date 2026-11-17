# Switches — Gestión por CLI (PuTTY)
Fecha: 2026-11-17 | S4048 / Z9664

## Conexión
- PuTTY → Serial o SSH a IP gestión del switch
- Usuario/contraseña: según credenciales sitio (no guardar en claro)
- Consola: 9600-8-N-1

## Comandos base practicados 17/11
- `show interfaces status` — estado UP/DOWN por puerto
- `show interfaces <puerto>` — detalle, velocidad, errores, CRC, flaps
- `show port` / `show interfaces description` — qué hay conectado por puerto
- `show version` / `show system` — modelo, firmware, uptime
- `show logs` — eventos recientes (caídas, flaps)

## Rutina antes de tocar fierro
1. `show interfaces status` → foto/captura
2. Identificar puerto físico vs lógico (validar que monitoreo dice la verdad — lección Zabbix ciego 15/11)
3. Si hay cambio físico de puerto → validar en CLI el mismo día + actualizar monitoreo/DCIM

## Pendiente
- Agregar comandos exactos S4048-ON / Z9664 según captures del turno
- Mapeo puerto físico → puerto lógico → servidor/NIC
