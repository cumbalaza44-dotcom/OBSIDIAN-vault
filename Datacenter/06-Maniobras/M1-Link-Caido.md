# M1 — Link caído / flap (cobre-fibra)

> Dónde: SN5610 ×12, SN2201 ×52, ODF ×84, 10.049 cables.
> Origen: INC-001 (ruta validada 8.5/10).

## Pre-check (foto del antes)
- `show interfaces status` → captura (puerto, estado, velocidad)
- `show interfaces transceiver` → RX Power por lane (fibra) o N/A (DAC/cobre)
- `show lldp neighbors` → ¿hay vecino?
- Servidor: `ethtool <iface>` + `ethtool -S <iface> | grep -i "err\|crc\|drop"` + `dmesg | grep -i link | tail -10`
- Zabbix: valor + timestamp del puerto

## Decisión
| RX Power | LLDP | Acción |
|---|---|---|
| Bajo/N/A | vacío | Físico → ventana, revisar fibra/transceiver |
| Normal | vacío | Lógico → `show running-config interface <pto>`, shutdown/VLAN |
| Normal | ok | Flap → `shutdown` → `no shutdown`, luego CRC |

## Verificación (5 obligatorias)
- [ ] Link UP ambos extremos
- [ ] CRC/drops en 0 o no creciendo 5 min
- [ ] LED verde/actividad
- [ ] Zabbix/DCIM actualizado mismo día
- [ ] Etiqueta TIA-606 ambos extremos

## Registro
Ticket: puerto, causa raíz, acción, hora ini-fin, responsable. Fotos antes/después.
