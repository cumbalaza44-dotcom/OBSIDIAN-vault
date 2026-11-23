# M4 — FRU switch / PSU / fan

> Dónde: Q3400 ×24 (8 PSU), SN5610 ×12, SN2201 ×52, SN4700 ×4.
> LED ámbar/rojo o sistema parpadeando >5min = entrar por consola.

## Pre-check
- LED sistema + PSU + fan (color + estado) + foto
- `show version` / `show system` → modelo, firmware, uptime
- `show environment` / `show logs` → temp, voltaje, eventos
- Si sistema parpadea >5min → SO no arrancó → consola serie (Opengear), no tocar PSU todavía

## Maniobra
- PSU/fan hot-swap donde el modelo lo permita; 1 a la vez
- Firmware: solo con ventana + MOP, nunca en caliente sin autorización

## Verificación
- [ ] Todos los LED verdes
- [ ] `show environment` en rango
- [ ] `show interfaces status` sin puertos caídos nuevos
- [ ] Uptime / logs sin errores nuevos
- [ ] DCIM + ticket actualizados
