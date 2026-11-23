# M2 — Fibra MPO degradada / fracturada

> Dónde: ODF ×84, GPU Fabric Q3400 ×24, mazos MPO-12.
> Origen: INC-002 real (umbral 2.26 dB, 4 cables en riesgo).

## Pre-check
- Zabbix: host, puerto, valor dB por lane, duración
- `show interfaces transceiver` → RX/TX por lane, delta entre carriles
- `show interfaces status` + `show lldp neighbors`
- Fotos: panorámica rack + close-up daño + etiquetas origen/destino

## Regla de oro
Umbral **2.26 dB** entre carriles = alerta temprana. Superado → ventana + MOP, no tocar sin repuesto en mano.
Reemplazo **uno por uno**, nunca el mazo completo a la vez. Validar cada uno antes de seguir.

## Verificación por cable reemplazado
- [ ] Carriles < 2.26 dB
- [ ] `show interfaces status` UP
- [ ] CRC en 0 o no creciendo
- [ ] Nuevo ruteo: radio curvatura OK, velcro (no bridas), lejos del punto de daño
- [ ] Etiquetado TIA-606 ambos extremos + fecha

## Registro
Ticket: causa raíz (ej. mal ruteo por soporte metálico) + acción preventiva. Cable dañado embolsado y etiquetado como evidencia.
