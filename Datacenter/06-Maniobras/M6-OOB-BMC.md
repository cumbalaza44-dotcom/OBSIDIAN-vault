# M6 — OOB / BMC inaccesible

> Tu red diaria: SN2201 ×52 leaf + SN4700 ×2 spine. Emergencia: Opengear CM8132 ×2 (32 serie c/u).
> Sin OOB estás ciego. Esta es la primera que se domina.

## Pre-check
- ¿Llega ping a la IP OOB? ¿SSH responde? ¿BMC web responde?
- Trazar ruta: tu estación → SN2201 leaf → SN4700 spine → BMC destino
- `show interfaces status` en el SN2201 del rack (¿puerto BMC UP?)
- Etiqueta del cable OOB (formato OOB-nnn) — si falta, hallazgo

## Escalera (en este orden)
1. SSH al BMC por OOB → si OK, era ruta o credencial, no fierro
2. SSH al SN2201 → `show interfaces status` del puerto BMC → flap si aplica
3. SSH al Opengear → consola serie al equipo → acceso aunque no haya IP
4. Físico: LED BMC + cable OOB + puerto switch (ventana si hay que re-cablear)

## Verificación
- [ ] SSH BMC OK + credenciales estándar
- [ ] Puerto OOB mapeado (rack/U/puerto switch ↔ BMC equipo)
- [ ] NTP + DNS OK en BMC, firmware estándar site
- [ ] DCIM: IP OOB + ubicación actualizadas
