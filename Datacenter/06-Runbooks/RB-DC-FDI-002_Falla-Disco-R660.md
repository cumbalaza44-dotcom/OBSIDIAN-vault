---
created: 2026-11-25
tipo: runbook-correctivo
codigo: RB-DC-FDI-002
equipo: Dell PowerEdge R660
tags: [runbook, R660, disco, hot-swap, EDSFF, PERC, iDRAC9]
version: "1.0"
---

# 🔴 RB-DC-FDI-002 — FALLA DE DISCO · Dell PowerEdge R660

> **Control documental:** RB-DC-FDI-002 · v1.0 · Nov 2026 · Autor: Jair Cumbalaza — Técnico Especialista Hardware · Área: NOC Cómputo / DC Hardware · Equipo: Dell PowerEdge R660 (E83S) — iDRAC9 OOB.
> **Fuente técnica:** Dell PowerEdge R660 Manual de instalación y servicio Rev. A00 (Cap. 7 Disassembly, Cap. 10 Diagnósticos, Cap. 11 Uso de diagnósticos).
> **Confidencialidad:** uso interno. La versión vigente es la publicada en el repositorio documental.

---

## 1. Propósito y alcance

Aplica ante falla, degradación o daño de discos del **Dell PowerEdge R660** — LED carrier ámbar, RAID degradado, rebuild detenido o disco ausente en iDRAC.

**Configuraciones cubiertas:**

| Bahía | Formato | Cantidad |
|-------|---------|----------|
| Frontal 2.5" | SAS/SATA/NVMe | 8× o 10× |
| Frontal EDSFF | E3.S NVMe | 14× o 16× |
| Posterior 2.5" | SAS/SATA | 2× (módulo posterior) |
| Posterior EDSFF | E3.S NVMe | 2× (módulo posterior) |
| Boot interno | BOSS-N1 (M.2 RAID1) / M.2 NVMe | 2× M.2 |

**Criterio de trabajo:** una alerta de disco requiere identificar primero el **estado RAID** antes de tocar. Verificar en iDRAC (Storage) y en el LED del carrier:

| LED carrier | Significado | Decisión |
|-------------|-------------|----------|
| 🟠 Ámbar 4 parpadeos/seg | Disco fallido | → **F1** |
| 🟢+🟠 que se apaga | Falla inesperada / rebuild detenido | → **F2** |
| 🟢 parpadeo lento | Rebuild en curso — **NO tocar** | → **F3** |
| ⚫ Apagados con equipo encendido | Backplane / RAID / no detectado | → **F4** |
| 🟠 en 2+ discos mismo array | Riesgo pérdida de datos | → **F5** |
| Daño físico / formato dudoso | 2.5" vs E3.S | → **F6** |

---

## 2. Prerrequisitos y permisos

- [ ] Ticket y **ventana aprobada NOC**; equipo identificado (rack, U, Service Tag).
- [ ] iDRAC9 y PERC accesibles; estado del RAID y **backup verificado** antes de tocar cualquier disco.
- [ ] Repuesto mismo tipo, capacidad y P/N; drive blank disponible para slots vacíos.
- [ ] **EPP:** manilla antiestática + calzado dieléctrico. El R660 tiene DIMMs y boards sensibles — antiestática obligatoria incluso en hot-swap de disco.
- [ ] **Ventana:** reemplazo hot-swap de 1 disco con RAID sano = ventana estándar. 2+ discos o backplane = ventana mayor + N2 en sitio o en línea.
- [ ] Credenciales iDRAC con rol Operator o superior (para preparar extracción y ver Storage).

---

## 3. Tabla de fallas y decisión rápida (F1–F6)

| ID | Condición | Acción |
|----|-----------|--------|
| **F1** | Disco fallido (ámbar 4 Hz) | Preparar en software → extraer carrier → reemplazar hot-swap |
| **F2** | Falla inesperada / rebuild detenido (verde+ámbar que se apaga) | ePSA + SEL → reasentar → reemplazar si persiste |
| **F3** | Rebuild en curso (verde lento) | **NO extraer ningún disco del array.** Solo monitorear |
| **F4** | Disco no detectado / backplane / RAID (LEDs apagados) | Reasentar carrier → revisar PERC → escalar si persiste |
| **F5** | 2+ discos caídos mismo array | **No intervenir solo. Escalar de inmediato** |
| **F6** | Daño físico / confusión formato (2.5" vs E3.S) | Verificar tipo y tornillería → RMA con fotos |

---

## 4. Procedimiento + Reversión

### Caso A — Disco fallido con RAID sano (F1)

**1 solo disco afectado, RAID en verde, reemplazo hot-swap:**

1. Confirmar en iDRAC (Storage > Physical Disks) qué disco falla: **slot, serial, capacidad** y que el RAID está en verde. Anotar índice del slot.
   - *Resultado esperado:* disco en estado `Failed`, resto del array `Online`.
2. Preparar el disco para extracción desde el management software (iDRAC > Storage > Prepare for Removal). Esperar a que los LED del carrier se apaguen.
   - *Resultado esperado:* LEDs apagados = listo para extraer.
3. Presionar botón de liberación, abrir manija, deslizar carrier fuera del slot.
4. Insertar repuesto (**mismo tipo 2.5" o E3.S, misma capacidad**) hasta conectar con backplane. Cerrar manija.
   - ⚠️ **E3.S vs 2.5" no son intercambiables.** Verificar formato del slot antes de insertar (F6).
5. Verificar LED verde sólido + estado `Online` en iDRAC. El rebuild arranca automáticamente.
6. Etiquetar disco extraído con RMA/ticket. Registrar serial y slot en DCIM.
7. Monitorear rebuild hasta verde sólido. Verificar que no haya nuevas fallas en el array.
8. Instalar drive blank en cualquier slot vacío (mantener airflow).

> **🔙 REVERSIÓN Caso A:** si el rebuild no arranca en 10 min → reasentar el repuesto → si persiste, verificar en PERC que el disco es reconocido (tamaño/tipo) → si el PERC no lo ve, probar otro slot del mismo backplane → si tampoco, escalar a N2/Dell (posible backplane). **No extraer otro disco del mismo array.**

### Caso B — Falla inesperada / rebuild detenido / no detectado (F2/F4)

**Verificar antes de reemplazar:**

1. Registrar patrón exacto del LED con **foto** + exportar logs iDRAC/SEL.
2. Correr diagnóstico **ePSA online** (Lifecycle Controller > Hardware Diagnostics) y revisar System Event Log.
3. Reasentar el carrier (extraer 10 seg → reinsertar firme hasta clic de manija).
   - *Si el disco reaparece y el RAID reconstruye:* no hay reemplazo — registrar causa como intermitencia.
4. Si es RAID: entrar a utilidad del adaptador **PERC** (F2 > Device Settings > PERC) → verificar estado del array y del rebuild.
5. Si persiste → reemplazar con pasos del Caso A. Si el problema es backplane o PERC → escalar a N2/Dell.

> **🔙 REVERSIÓN Caso B:** si tras reasentar el disco desaparece de iDRAC por completo → NO reinsertar repetidamente (máx 2 intentos) → dejar el slot con blank → escalar a N2 con foto + SEL. Reasentados repetidos pueden dañar el conector del backplane.

### Caso C — 2+ discos caídos o daño físico (F5/F6)

**Riesgo de pérdida de datos:**

1. **NO extraer ningún otro disco del array.** Detener cualquier cambio y escalar de inmediato a Líder DC / N2.
2. Confirmar con el responsable que el **backup existe** antes de cualquier intervención adicional.
3. Si el RAID no tolera más fallas → validar con Hardware si procede conmutar el servicio al nodo redundante.
4. Daño físico visible (conector dañado, rieles rotos, E3.S forzado en slot 2.5"): no instalar → aislar → registrar con fotos → RMA.
5. Confusión de formato: verificar etiqueta del slot (2.5" vs E3.S) y tornillería del carrier. El E3.S usa portaunidades distinto al 2.5" — no forzar.

> **🔙 REVERSIÓN Caso C:** no hay reversión a nivel técnico — la reversión es **organizacional**: detener, escalar, no tocar. Cualquier extracción adicional puede destruir el array. El rollback lo define el Líder DC (restore desde backup o failover).

---

## 5. Matriz de escalamiento

| Nivel | Contacto | Cuándo |
|-------|----------|--------|
| **N1** | Técnico de turno (tú) | F1, F2, F4 con 1 disco aislado y RAID sano |
| **N2** | Líder DC / Hardware senior | F5 (2+ discos), backplane, PERC, rebuild que no arranca |
| **Dell ProSupport** | Service Tag + contrato | Falla de backplane, PERC, E3.S con error de firmware, RMA |
| **Líder servicio** | Dueño de la aplicación | F5 con riesgo de datos — decisión de failover |

**Registro obligatorio:** ticket + DCIM (serial, slot, P/N repuesto) + foto del LED + hora inicio/fin rebuild.

---

<div align="center">

`🦾 RB-DC-FDI-002 v1.0 — R660: identifica RAID primero, toca después.`

</div>
