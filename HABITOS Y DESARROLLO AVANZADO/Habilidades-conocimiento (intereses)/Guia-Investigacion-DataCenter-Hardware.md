# Guía de Investigación — Técnico Especialista Data Center Hardware (IA)

> Complemento del Plan-Estudio-DataCenter-Hardware.md. Por cada punto del plan: título, qué aprender y 4 búsquedas en inglés listas para YouTube/Google.

---

## Semana 1 (28 Sep – 4 Oct) — Fundamentos físicos + Energía

### Lun 28 — Rack y energía

#### 1. Rack 19", unidad U y servidores DGX 8U
Aprende qué es 1U (1.75"), cómo se mide un rack de 42U y por qué un DGX ocupa 8U.
- "19 inch server rack units explained"
- "What is rack unit U 42U datacenter"
- "NVIDIA DGX server rack installation 8U"
- "Server rack setup tutorial datacenter"

#### 2. PDU básica vs switched/monitored, UPS y EPO
Aprende tipos de PDU, qué hace un UPS y cuándo se usa el botón de apagado de emergencia EPO.
- "Basic vs switched vs metered PDU datacenter"
- "Datacenter UPS system explained"
- "EPO emergency power off datacenter"
- "Server rack PDU installation guide"

#### 3. Monofásica vs trifásica, PDU 22 kW y regla del 80%
Aprende diferencia entre potencia mono/trifásica, capacidad de una PDU de 22 kW y por qué no pasar del 80% de carga.
- "Single phase vs three phase power datacenter"
- "22kW PDU datacenter power explained"
- "80 percent rule electrical load PDU"
- "Three phase PDU power calculation servers"

### Mar 29 — Clima y airflow

#### 4. Pasillo frío/caliente, CFM y blanks en U vacíos
Aprende contención de pasillos, qué es CFM y por qué tapar los espacios vacíos del rack.
- "Hot aisle cold aisle containment datacenter"
- "Datacenter airflow management CFM explained"
- "Blanking panels empty rack units airflow"
- "Cold aisle containment installation guide"

#### 5. Sensores de temperatura/humedad, umbrales y alertas
Aprende dónde van los sensores, rangos normales ASHRAE y cómo se configuran las alertas.
- "Datacenter temperature humidity sensors placement"
- "ASHRAE temperature humidity datacenter thresholds"
- "Environmental monitoring datacenter alert setup"
- "Temp humidity sensor rack installation"

#### 6. Throttling térmico en GPU y consecuencias
Aprende qué es el thermal throttling en GPUs, cómo detectarlo y qué daño causa al rendimiento.
- "GPU thermal throttling explained datacenter"
- "NVIDIA GPU overheating throttling fix"
- "GPU temperature limit performance drop server"
- "Datacenter GPU cooling failure consequences"

### Mié 30 — Cableado cobre y fibra

#### 7. Cat6A vs fibra OM4/OS2 y cuándo usar cada uno
Aprende diferencias entre cobre Cat6A y fibra multimodo/monomodo, distancia y velocidad de cada uno.
- "Cat6A vs fiber optic datacenter cabling"
- "OM4 vs OS2 fiber difference explained"
- "When to use copper vs fiber datacenter"
- "Datacenter cabling types tutorial"

#### 8. Patch panels, MPO y limpieza de conectores
Aprende qué es un patch panel, conectores MPO y cómo limpiar fibra sin dañarla.
- "Fiber patch panel installation datacenter"
- "MPO connector explained datacenter"
- "Fiber optic connector cleaning procedure"
- "MPO trunk cable polarity explained"

#### 9. Etiquetado TIA-606 y colores estándar
Aprende la norma TIA-606 para etiquetar cables y el código de colores de fibra y cobre.
- "TIA-606 cable labeling standard explained"
- "Datacenter cable labeling best practices"
- "Fiber optic cable color code chart"
- "Cable labeling machine datacenter tutorial"

### Jue 1 — Seguridad física y ESD

#### 10. ESD: pulsera, tapete y empaque antiestático
Aprende qué es la descarga electrostática y cómo usar pulsera, tapete y bolsas antiestáticas.
- "ESD protection server hardware replacement"
- "Anti static wrist strap how to use"
- "ESD mat grounding datacenter procedure"
- "ESD safe handling electronic components"

#### 11. EPO, extinción por gas y bitácora de acceso
Aprende el botón EPO, sistemas de extinción por gas limpio y cómo llevar el registro de accesos.
- "Datacenter gas suppression fire system explained"
- "EPO button datacenter emergency procedure"
- "Datacenter physical access log best practices"
- "Clean agent fire suppression server room"

#### 12. SOP y MOP: qué son y cuándo aplican
Aprende qué es un procedimiento operativo estándar (SOP) y un método de procedimiento (MOP) y cuándo exigirlos.
- "SOP vs MOP datacenter explained"
- "Method of procedure MOP datacenter example"
- "Datacenter standard operating procedure template"
- "MOP approval process maintenance window"

### Vie 2 — Repaso + validación semanal

#### 13. Repaso 20 preguntas semana 1 y cierre de huecos
Repasa energía, airflow, cableado y seguridad con 20 preguntas y refuerza los temas flojos.
- "Datacenter fundamentals quiz questions"
- "Server rack power cooling basics test"
- "Datacenter technician interview questions"
- "Datacenter infrastructure basics review"

#### 14. Dibujar un rack completo de memoria (PDU, UPS, ToR, airflow)
Practica dibujar de memoria un rack con energía, red y flujo de aire sin mirar notas.
- "Server rack diagram PDU UPS ToR"
- "Datacenter rack elevation drawing example"
- "Top of rack switch diagram explained"
- "How to document server rack layout"

#### 15. Actualizar notas de campo con lo visto en sitio
Aprende a registrar marcas, modelos, PDUs y observaciones reales del sitio en tus notas.
- "Datacenter site survey documentation template"
- "Field notes datacenter technician example"
- "Server hardware inventory documentation"
- "Datacenter walkthrough checklist template"

### Sáb 3 / Dom 4 — Simulacro + lectura

#### 16. Simulacro: 2x DGX 8 kW en PDU 22 kW, ¿tercer servidor?
Practica el cálculo de carga: 2 servidores de 8 kW en PDU de 22 kW y por qué un tercero sobrecarga.
- "PDU load calculation server rack example"
- "Datacenter power capacity planning tutorial"
- "Server power draw calculation DGX"
- "PDU overload risk datacenter power"

#### 17. Lectura diaria y planeación de la semana 2
Organiza lecturas de FRUs y prepara herramientas y objetivos para la semana 2.
- "Server FRU field replaceable unit overview"
- "Datacenter technician study guide hardware"
- "Server hardware maintenance basics book"
- "How to study datacenter hardware technician"

---

## Semana 2 (5 – 11 Oct) — FRUs y diagnóstico

### Lun 5 — Fuentes y ventiladores

#### 18. PSU hot-swap 1+1/2+2, LEDs y validación post-reemplazo
Aprende redundancia de fuentes, significado de LEDs y cómo validar después de un reemplazo en caliente.
- "Server hot swap power supply replacement"
- "PSU redundancy 1+1 vs 2+2 explained"
- "Server PSU LED status meanings Dell HPE"
- "Power supply failure server troubleshooting"

#### 19. Fans: zonas, reemplazo sin apagado y curvas
Aprende zonas de ventiladores, reemplazo hot-swap y cómo funcionan las curvas de velocidad.
- "Server hot swap fan replacement procedure"
- "Server fan failure troubleshooting Dell HPE"
- "Server fan zones cooling explained"
- "Fan speed curve server BMC control"

### Mar 6 — RAM ECC y discos

#### 20. ECC corregible vs no corregible, reseat y canales
Aprende memoria ECC, errores CE vs UE, cómo reasentar DIMMs y reglas de canales.
- "ECC memory correctable vs uncorrectable error"
- "Server RAM reseat procedure troubleshooting"
- "Memory channel population rules server"
- "ECC memory error server log diagnosis"

#### 21. NVMe/SAS/SATA, hot-swap y RAID 0/1/5/6/10 conceptual
Aprende tipos de disco, reemplazo en caliente y niveles RAID más usados en servidores.
- "NVMe vs SAS vs SATA server drives explained"
- "Server hard drive hot swap replacement"
- "RAID 0 1 5 6 10 explained servers"
- "Failed drive RAID rebuild procedure server"

### Mié 7 — NICs, GPUs, DPUs (identificación)

#### 22. NICs 25/100/200/400G, DAC vs transceiver, link/flap
Aprende velocidades de tarjetas de red, cables DAC vs ópticos y qué es link flap.
- "Datacenter NIC 25G 100G 200G 400G explained"
- "DAC vs fiber transceiver datacenter"
- "Network link flapping troubleshooting server"
- "NIC link down server troubleshooting"

#### 23. GPU vs DPU: qué hace cada una e identificación física
Aprende a distinguir una GPU de una DPU físicamente y qué función cumple cada una en IA.
- "GPU vs DPU difference explained datacenter"
- "NVIDIA BlueField DPU explained identification"
- "AI server GPU identification guide"
- "What is DPU datacenter networking"

### Jue 8 — Aislamiento de falla

#### 24. Flujo síntoma → LED/post → SEL → swap mínimo → validar
Aprende el flujo de diagnóstico ordenado desde el síntoma hasta validar el reemplazo mínimo.
- "Server hardware troubleshooting methodology"
- "Server fault isolation step by step"
- "Server POST codes LED diagnosis"
- "Minimum to POST server troubleshooting"

#### 25. BMC: iDRAC/iLO/IPMI, KVM y lectura de logs
Aprende a entrar al BMC, usar consola KVM remota y leer logs de hardware.
- "iDRAC vs iLO vs IPMI BMC explained"
- "Remote KVM server management tutorial"
- "How to read server SEL logs BMC"
- "BMC remote management server setup"

### Vie 9 — Checklist FRU propio + repaso

#### 26. Checklist FRU: apagar, ESD, foto, swap, validar, documentar, DCIM
Crea tu checklist personal: ¿apagar?, ESD, foto previa, reemplazo, validación, registro y DCIM.
- "Server FRU replacement checklist procedure"
- "Field replaceable unit best practices server"
- "Server hardware replacement documentation"
- "ESD photo documentation server repair"

#### 27. Repaso 20 preguntas semana 2
Repasa PSUs, fans, RAM, discos, NICs, GPUs y diagnóstico con 20 preguntas.
- "Server hardware technician quiz FRU"
- "Server troubleshooting interview questions"
- "FRU replacement technician test questions"
- "Datacenter hardware basics review test"

### Sáb 10 / Dom 11 — Simulacro

#### 28. Simulacro: LED ámbar en PSU + temperatura alta, paso a paso
Practica el diagnóstico combinado de fuente en falla más sobretemperatura, en orden.
- "Server amber LED PSU troubleshooting"
- "Server high temperature alert troubleshooting"
- "Server PSU failure overheating diagnosis"
- "Dell HPE server warning LED guide"

---

## Semana 3 (12 – 18 Oct) — Servidores IA a fondo

#### 29. Arquitectura CPU + 8x GPU, NVLink/NVSwitch, PCIe Gen5
Aprende cómo se conectan CPU y 8 GPUs, qué es NVLink/NVSwitch y el rol de PCIe Gen5.
- "NVIDIA DGX H100 architecture explained NVLink"
- "NVLink vs NVSwitch AI server explained"
- "PCIe Gen5 server explained bandwidth"
- "8 GPU server architecture deep learning"

#### 30. TDP por GPU (700W H100), consumo total y nvidia-smi básico
Aprende el TDP de la H100, cómo sumar el consumo del servidor y comandos básicos de nvidia-smi.
- "NVIDIA H100 TDP power consumption explained"
- "nvidia-smi commands tutorial GPU monitoring"
- "GPU power draw monitoring datacenter"
- "AI server total power consumption calculation"

#### 31. BMC a fondo, SEL logs, firmware y KVM remoto
Aprende a exprimir el BMC: leer SEL, actualizar firmware y tomar consola KVM remota.
- "BMC SEL log analysis server troubleshooting"
- "Server firmware update iDRAC iLO tutorial"
- "Remote KVM BMC server console guide"
- "IPMI commands server management tutorial"

#### 32. Cableado de alta potencia, fases y validación de carga
Aprende a cablear servidores de alto consumo, balancear fases y validar carga con pinza/medición.
- "High power server rack cabling best practices"
- "Three phase load balancing datacenter rack"
- "Server rack power load validation procedure"
- "High density rack power cable management"

#### 33. Repaso + 20 preguntas servidores IA
Repasa arquitectura GPU, potencia, BMC y cableado de alta densidad con 20 preguntas.
- "AI server hardware quiz questions"
- "GPU server troubleshooting interview questions"
- "NVIDIA DGX maintenance basics test"
- "High density server rack quiz"

#### 34. Leer un SEL log real e identificar la causa
Practica abrir un System Event Log real y rastrear la causa raíz del evento.
- "How to read SEL system event log server"
- "SEL log error decoding tutorial"
- "Server hardware log analysis example"
- "IPMI SEL list troubleshooting guide"

---

## Semana 4 (19 – 25 Oct) — RMA y commissioning

#### 35. RMA: apertura, seriales, fotos, empaque y seguimiento
Aprende el flujo RMA completo: abrir el caso, seriales, evidencia fotográfica, empaque y tracking.
- "Server RMA process explained datacenter"
- "Hardware RMA request procedure Dell HPE"
- "How to pack server parts RMA shipping"
- "RMA tracking warranty claim server hardware"

#### 36. Validación de equipo reparado: burn-in, stress y pre/post
Aprende a validar un equipo que vuelve de RMA con burn-in, pruebas de estrés y comparativa antes/después.
- "Server burn in test procedure new hardware"
- "Server stress test CPU GPU RAM tools"
- "Post repair server validation checklist"
- "Memtest Prime95 server burn in tutorial"

#### 37. Commissioning: rack → cablear → energizar → BMC → firmware → test → entrega
Aprende la secuencia de puesta en servicio desde el rack vacío hasta la entrega al cliente interno.
- "Server commissioning process datacenter step by step"
- "New server rack installation commissioning checklist"
- "Server provisioning BMC firmware setup guide"
- "Datacenter server deployment procedure"

#### 38. Checklist de puesta en servicio + documentación obligatoria
Crea tu checklist de commissioning y aprende qué documentos son obligatorios al entregar.
- "Server commissioning checklist template datacenter"
- "Datacenter handover documentation requirements"
- "Server installation acceptance test procedure"
- "Datacenter deployment documentation best practices"

#### 39. Simular un RMA completo en papel
Practica en papel un RMA de inicio a fin: ticket, seriales, fotos, empaque y cierre.
- "RMA ticket example server hardware failure"
- "Server warranty claim documentation example"
- "Hardware failure report template datacenter"
- "RMA packing slip serial number documentation"

#### 40. Simulacro commissioning de un DGX ficticio
Practica comisionar un DGX imaginario: rack, energía, red, BMC, firmware y tests.
- "NVIDIA DGX setup installation guide"
- "DGX server initial setup BMC network"
- "GPU server commissioning checklist AI"
- "DGX H100 firmware update setup tutorial"

---

## Semana 5 (26 Oct – 1 Nov) — DCIM, inventarios y red física

#### 41. DCIM: altas, bajas, movimientos y ubicación U exacta
Aprende a registrar en DCIM cada alta, baja y movimiento con su posición U exacta.
- "DCIM software tutorial asset management"
- "Datacenter asset move add change procedure"
- "Rack U location tracking DCIM best practices"
- "What is DCIM datacenter infrastructure management"

#### 42. Inventario: seriales, FRUs, spares y ciclo de vida
Aprende a llevar inventario de seriales, repuestos críticos y ciclo de vida del hardware.
- "Datacenter hardware inventory management best practices"
- "Server serial number asset tracking"
- "Spare parts management datacenter FRU stock"
- "IT hardware lifecycle management process"

#### 43. Red física: ToR, agregación, MPO y OTDR conceptual
Aprende switch ToR, capa de agregación, troncales MPO y qué mide un OTDR en fibra.
- "Top of rack ToR switch explained datacenter"
- "Datacenter aggregation layer network explained"
- "MPO trunk fiber datacenter cabling guide"
- "OTDR fiber testing explained tutorial"

#### 44. Coordinación: Network Ops, Physical Connectivity y Datacenter Ops
Aprende con quién coordinar cada tarea entre los equipos de red, conectividad física y operaciones.
- "Datacenter operations team roles explained"
- "Network operations vs datacenter operations"
- "Physical connectivity team datacenter role"
- "Datacenter cross team coordination maintenance"

#### 45. SOP/MOP, ventanas de mantenimiento y rollback
Aprende a ejecutar SOPs/MOPs en ventana de mantenimiento y cómo hacer rollback si algo falla.
- "Datacenter maintenance window procedure MOP"
- "Rollback plan server maintenance example"
- "Change management datacenter MOP approval"
- "Datacenter MOP execution step by step"

#### 46. Auditar un rack ficticio y dejarlo cuadrado en formato DCIM
Practica auditar un rack imaginario: seriales, Us, cables y déjalo registrado como en DCIM.
- "Server rack audit checklist datacenter"
- "DCIM rack audit procedure tutorial"
- "Datacenter asset audit best practices"
- "Rack inventory audit template excel"

---

## Semana 6 (2 – 8 Nov) — Incidentes críticos y cierre

#### 47. Severidades P1/P2/P3, tiempos y comunicación
Aprende a clasificar incidentes P1/P2/P3, sus SLAs y cómo comunicar cada uno.
- "P1 P2 P3 incident severity levels explained"
- "Datacenter incident response SLA priorities"
- "Incident communication template major outage"
- "Severity levels IT incident management"

#### 48. Recuperación: aislar, mitigar, reemplazar, validar y post-mortem
Aprende el ciclo de recuperación: aislar falla, mitigar, reemplazar, validar y hacer post-mortem.
- "Datacenter incident recovery procedure steps"
- "IT post mortem template major incident"
- "Server outage mitigation troubleshooting steps"
- "Root cause analysis datacenter outage example"

#### 49. Herramientas: multímetro, probador de fibra, etiquetadora y kit ESD
Aprende a usar multímetro, VFL/probador de fibra, etiquetadora y kit antiestático en campo.
- "Multimeter basics server technician tutorial"
- "Fiber optic tester VFL how to use"
- "Cable label printer datacenter tutorial"
- "ESD kit server repair tools list"

#### 50. Repaso 40 preguntas semanas 1-5
Repasa todo lo de las semanas 1 a 5 con 40 preguntas integrales antes del simulacro final.
- "Datacenter technician final exam questions"
- "Server hardware comprehensive review test"
- "Datacenter operations interview questions senior"
- "AI datacenter hardware basics full review"

#### 51. Simulacro final: GPU caída en hora pico, paso a paso
Practica la respuesta a una GPU caída en producción: detección, aislamiento, reemplazo y validación.
- "GPU failure troubleshooting datacenter server"
- "NVIDIA GPU failure diagnosis nvidia-smi"
- "Failed GPU replacement server procedure"
- "GPU server emergency maintenance datacenter"

#### 52. Validación final: explicar el flujo completo en voz alta sin notas
Cierra explicando sin notas el flujo completo: energía, FRU, IA, RMA, DCIM e incidentes.
- "Datacenter hardware workflow end to end explained"
- "Server lifecycle datacenter rack to decommission"
- "Explain datacenter operations technician role"
- "AI datacenter hardware support full workflow"

---

*Total: 52 temas · 208 queries · Generado 2026-09-29*
