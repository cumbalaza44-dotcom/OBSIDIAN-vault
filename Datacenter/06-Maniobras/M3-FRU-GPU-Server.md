# M3 — FRU servidor GPU (SYS-422GS ×144)

> FRUs: 4× PSU 6.6kW Titanium (2+2) · 4× fan 80mm · 32× DIMM DDR5 · 8× E1.S NVMe · GPU tray.
> Peso 84.6kg — requiere 2 personas / rail kit. Refrigeración D2C cold plate.

## Pre-check
- ¿Qué falla? POST / LED / SEL iDRAC / `dmesg` / temp / throttling
- Autorización + ventana escrita (apagado controlado, no desde PDU)
- Repuesto en mano: mismo PN, serial anotado
- Foto del antes (LED + ubicación + etiqueta)

## Maniobra (1 FRU a la vez)
- PSU: hot-swap permitido, verificar redundancia 2+2 antes de sacar
- DIMM/NVMe/fan: shutdown controlado → confirmar apagado → reemplazar → encender desde botón del equipo
- GPU tray: solo con MOP formal + 2 personas

## Verificación
- [ ] POST limpio, sin errores
- [ ] iDRAC/BMC accesible, SEL sin nuevos errores
- [ ] Discos/CPU/RAM/GPU visibles (`lscpu`, `nvme list`, `nvidia-smi` si aplica)
- [ ] Red link up + SSH OK
- [ ] Temp/voltaje en rango, burn-in 2-4h si fue RMA
- [ ] DCIM actualizado + ticket con serial viejo/nuevo + hora + responsable
