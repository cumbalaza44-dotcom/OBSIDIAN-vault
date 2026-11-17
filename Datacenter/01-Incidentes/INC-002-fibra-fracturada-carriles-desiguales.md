# INC-002 — Fibra MPO fracturada + carriles desiguales (COL-MDE-HARD-APD-FIBR01)

> Fecha: 2026-11-11 | Caso REAL reportado por Mr. Jair | Estado: en curso
> Guía completa: ubicación física → evidencia → escalamiento → reemplazo

## 1. Contexto experto: qué significa este incidente

**Carriles desiguales (lane skew / imbalance):** un cable MPO-12 lleva 8-12 hilos (lanes). Cada lane debe atenuar parecido. Cuando uno se fractura, su potencia cae distinto a los demás → el delta entre lanes sube. Umbral: **2.26 dB**. Valor actual: **2.2694 dB** → ya lo superó en Eth1/8/1 y Eth1/8/2.

**Lectura del caso:** no es degradación gradual, es daño mecánico agudo (foto: fibra prensada por tornillo). Los 2 puertos caídos (Eth1/17:1, 17:2) son probablemente el mismo mazo o consecuencia en cascada. 4 cables en riesgo = el mazo completo que pasa por ese punto.

**Riesgo:** si ese mazo alimenta NICs de GPU (XE2_NIC7, NIC8 según Zabbix), el entrenamiento distribuido se cae o se degrada. Prioridad alta.

## 2. Ubicación física: dónde están esos puertos

Zabbix dice host `COL-MDE-HARD-APD-FIBR01`. Eso es el nombre del equipo en monitoreo — puede ser un switch o el patch panel. Para ubicarlo:

1. **En Zabbix:** click al host → ver IP de gestión + descripción (suele tener rack/fila).
2. **En DCIM o plano:** buscar `COL-MDE-HARD-APD-FIBR01` → te da sala, fila, rack, U.
3. **En campo:** el puerto `Eth1/8/1` = slot 1, módulo/panel 8, puerto 1. `Eth1/17:1` = puerto breakout 17, sub-puerto 1 (cable breakout MPO→4xLC o similar).
4. **Trazar el mazo:** desde el transceiver del switch, seguir el cable aqua hasta el patch panel. El punto de fractura (foto del tornillo) es donde los 4 cables pasan juntos — ese es el punto a documentar con foto panorámica + close-up.

**Qué observar en hardware:**
- Transceiver: LED del puerto (ámbar/rojo = fault, apagado = down, verde parpadeante = actividad).
- Cable: punto de presión, radio de curvatura (mínimo 10x diámetro en OM3/OM4 ≈ 3 cm), peladura, conector MPO con guía (pins) doblados.
- Etiquetas: leer ambos extremos (origen→destino). Si no hay etiqueta, ese ya es un hallazgo para el reporte.

## 3. Evidencia (formato que sirve para escalar y RMA)

Por cada cable afectado, registrar:
- [ ] Foto panorámica del rack con el punto de daño visible
- [ ] Close-up del punto de fractura (como las que mandaste)
- [ ] Foto de etiqueta origen + etiqueta destino
- [ ] Captura Zabbix: host, puerto, valor dB, duración
- [ ] Solo lectura en nodo/switch (no cambios):
```
show interfaces transceiver      # RX/TX por lane
show interfaces status           # up/down/admin
show lldp neighbors              # vecino vivo o no
```
- [ ] En servidor si aplica: `ethtool -S <iface> | grep -i "err\|crc\|drop"`, `dmesg | grep -i link | tail`

**Etiquetado (TIA-606):** si el cable no tiene etiqueta o está borrada, anotarlo. En el reemplazo, etiquetar ambos extremos: `ORIGEN-RACK/U/PTO → DESTINO-RACK/U/PTO + fecha`.

## 4. Escalamiento: a quién y con qué texto

**A quién:** Network Ops (dueños del enlace) + DC Ops / coordinador de turno (dueños de ventana y MOP). Tu rol reporta y prepara, no ejecuta cambio sin MOP.

**Contenido mínimo del ticket:**
1. Host + puertos + valores (2.2694 vs umbral 2.26) + duración Zabbix
2. Causa probable: daño físico por aplastamiento (fotos adjuntas)
3. Impacto: 2 puertos down, 2 degradados, 4 cables en riesgo, servicio afectado (NICs XE2)
4. Acción solicitada: ventana + MOP reemplazo de mazo + re-ruteo
5. Ubicación física exacta (sala/fila/rack/U) + etiquetas

## 5. Procedimiento de reemplazo (con ventana + MOP aprobado)

**Pre-requisitos:** repuesto igual (MPO-12 OM3/OM4 aqua, mismo largo o mayor), etiquetas, limpiadores MPO, medidor si hay. Nunca empezar sin repuesto en mano.

1. Identificar y etiquetar los 4 cables (origen→destino de cada uno).
2. Reemplazar **uno por uno**, nunca los 4 a la vez:
   a. Desconectar solo el cable objetivo (los otros quedan quietos).
   b. Instalar el nuevo por ruta libre (lejos del tornillo, con radio de curvatura correcto, con velcro no bridas plásticas apretadas).
   c. Etiquetar ambos extremos.
   d. Validar antes de seguir con el siguiente:
```
show interfaces transceiver   # carriles < 2.26 dB
show interfaces status        # up
show interfaces counters errors  # CRC en 0 o no creciendo
```
3. Al final: verificar los 4, fotos del nuevo ruteo, cerrar ticket con causa raíz (mal ruteo por soporte metálico) + acción preventiva (protector/gancho + re-etiquetado).
4. Dejar el cable dañado embolsado y etiquetado como evidencia (no botarlo hasta cierre del caso).

## Lecciones
- Umbral 2.26 dB = alerta temprana de fibra dañada, no ignorarlo.
- Foto del daño físico vale más que 10 comandos para el MOP.
- Nunca manipular fibra fracturada sin ventana y repuesto en mano.
- Un tornillo mal puesto puede tumbar entrenamiento de GPUs — planta física manda.

---
## Plantilla para próximo incidente
Copiar esta estructura: Contexto → Ubicación → Evidencia → Escalamiento → Reemplazo → Lecciones.
