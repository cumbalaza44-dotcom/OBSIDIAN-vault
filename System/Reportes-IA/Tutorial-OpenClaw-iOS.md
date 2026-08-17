# 📱 Tutorial Completo: App Oficial OpenClaw iOS

> **Última actualización:** Julio 2026 | **Versión referenciada:** v2026.7.1
>
> Guía paso a paso para instalar, configurar y sacar el máximo provecho de la app oficial de OpenClaw en iPhone y Apple Watch.

---

## 📋 Índice

1. [Requisitos Previos](#1-requisitos-previos)
2. [Instalación](#2-instalación)
3. [Emparejamiento (Pairing)](#3-emparejamiento-pairing)
4. [Configuración Inicial](#4-configuración-inicial)
5. [Uso Diario](#5-uso-diario)
6. [Apple Watch](#6-apple-watch)
7. [Solución de Problemas Comunes](#7-solución-de-problemas-comunes)
8. [Tips Avanzados](#8-tips-avanzados)

---

## 1. Requisitos Previos

### 📲 Dispositivo iOS

| Requisito | Detalle |
|-----------|---------|
| **Dispositivo** | iPhone con iOS 17+ (recomendado) |
| **Apple Watch** (opcional) | watchOS 10+ |
| **Conexión** | Wi-Fi o datos móviles activos |
| **Almacenamiento** | ~50 MB libres para la app |

### 🖥️ Gateway (Servidor)

Tu **Gateway** debe estar corriendo y accesible desde tu iPhone. El Gateway es el cerebro de OpenClaw — la app iOS es solo un cliente que se conecta a él.

**Verificar versión del Gateway (mínimo v2026.7.1+):**

```bash
openclaw gateway status
```

Si necesitas actualizar:

```bash
openclaw update
openclaw gateway restart
```

**Verificar que el Gateway escucha en el puerto correcto (por defecto `18789`):**

```bash
openclaw gateway status
# Deberías ver algo como:
# Gateway: listening on port 18789
```

### 🌐 Conexión de Red

Tu iPhone necesita poder alcanzar el Gateway. Hay tres caminos principales:

| Método | Cuándo usarlo | Configuración |
|--------|---------------|---------------|
| **Tailscale (recomendado)** | Gateway remoto / VPS / nube | Instala Tailscale en ambos dispositivos |
| **Misma LAN (Bonjour)** | Gateway en tu casa/oficina | Ambos en la misma red Wi-Fi |
| **Host manual (fallback)** | Cualquier otro caso | IP pública + puerto expuesto |

#### Configurar Tailscale (recomendado para uso remoto)

```bash
# En el servidor donde corre el Gateway:
openclaw gateway --port 18789 --tailscale serve
```

Esto expone el Gateway a través de tu tailnet. El iPhone se conectará automáticamente si tiene Tailscale instalado y activo.

#### Configurar acceso LAN

Si el Gateway y el iPhone están en la misma red:

```json5
// En tu openclaw.json:
{
  gateway: {
    bind: "lan"  // En vez del default "loopback"
  }
}
```

> ⚠️ **Importante:** El bind por defecto es `loopback`, que **no es accesible** desde el teléfono. Debes cambiarlo a `lan` o usar Tailscale.

Reinicia después del cambio:

```bash
openclaw gateway restart
```

### 🔐 Autenticación

El Gateway debe tener autenticación configurada (token o contraseña). Si aún no lo has hecho:

```bash
openclaw onboard
# Sigue el asistente para configurar token/contraseña
```

---

## 2. Instalación

### 📥 Descargar la App

La app oficial de OpenClaw iOS se distribuye a través de **Apple App Store** cuando está habilitada para una release.

**Pasos:**

1. Abre la **App Store** en tu iPhone
2. Busca **"OpenClaw"**
3. Toca **Obtener** / **Instalar**
4. Espera a que se descargue e instale
5. Abre la app

> 💡 **Nota:** Las builds locales de desarrollo también pueden ejecutarse desde código fuente, pero para uso normal la App Store es el camino recomendado.

---

## 3. Emparejamiento (Pairing)

El emparejamiento vincula tu iPhone con tu Gateway de forma segura. Es el paso más importante de toda la configuración.

### 🔄 Método 1: Desde Control UI (Recomendado)

Este es el camino más fácil. Necesitas acceso administrativo al Gateway.

#### Paso 1: Generar el código QR en Control UI

1. Abre el **Control UI** en tu navegador (`openclaw dashboard`)
2. Navega a **Nodes** → **Devices**
3. Haz clic en **Pair mobile device**
4. Selecciona el nivel de acceso:
   - **Full access** (recomendado) — acceso completo administrativo
   - **Limited access** — solo funciones básicas del chat
5. Haz clic en **Create setup code**
6. Se mostrará un código QR y un código de texto

#### Paso 2: Escanear desde el iPhone

1. En la app OpenClaw de iPhone, ve a **Settings** → **Gateway**
2. Toca **Scan QR Code** (o **Paste setup code**)
3. Apunta la cámara al código QR
4. Espera la conexión

> 🔒 **Seguridad:** El código QR es de un solo uso y expira después de un tiempo. Si expira, genera uno nuevo desde Control UI.

#### Paso 3: Aprobar la conexión

Si la app muestra **"Pending approval"**:

1. **Desde Control UI:** La solicitud aparecerá automáticamente. Revísala y apruébala.
2. **Desde Terminal:**

```bash
openclaw devices list
# Busca el requestId del dispositivo pendiente
openclaw devices approve <requestId>
```

> ⚠️ **Nota:** Si el app reintentó el pairing con datos de autenticación diferentes (rol/alcances/llave pública), la solicitud anterior queda invalidada. Ejecuta `openclaw devices list` de nuevo antes de aprobar.

### 🔄 Método 2: Descubrimiento Automático (LAN/Bonjour)

Si estás en la misma red local, la app puede descubrir el Gateway automáticamente:

1. Abre la app → **Settings** → **Gateway**
2. La app busca automáticamente gateways en `_openclaw-gw._tcp` vía Bonjour
3. Selecciona tu gateway de la lista
4. Aprueba la conexión desde el Gateway

### 🔄 Método 3: Host Manual (Fallback)

Si Bonjour y Tailscale no funcionan:

1. Ve a **Settings** → **Gateway**
2. Habilita **Manual Host**
3. Ingresa la IP y puerto del Gateway (ej: `192.168.1.100:18789`)
4. Conéctate y aprueba desde el Gateway

### 🔧 Auto-Aprobación (Opcional, Avanzado)

Si tu iPhone siempre se conecta desde una subred controlada, puedes habilitar auto-aprobación:

```json5
// En openclaw.json:
{
  gateway: {
    nodes: {
      pairing: {
        autoApproveCidrs: ["192.168.1.0/24"]
      }
    }
  }
}
```

> ⚠️ Esto solo aplica a emparejamientos nuevos de tipo `role: node` sin alcances solicitados. El pairing de operadores/browsers siempre requiere aprobación manual.

### ✅ Verificar Conexión

```bash
openclaw nodes status
openclaw gateway call node.list --params "{}"
```

Deberías ver tu iPhone listado como nodo conectado.

---

## 4. Configuración Inicial

Al abrir la app por primera vez, verás un asistente de permisos y configuración.

### 🔐 Permisos que Solicita la App

| Permiso | Para qué se usa | Obligatorio |
|---------|-----------------|-------------|
| **Cámara** | Capturar fotos para enviar al agente | No |
| **Micrófono** | Talk mode (voz) y dictado | No |
| **Ubicación** | Funciones de geolocalización | No |
| **Notificaciones** | Alertas push del Gateway | No |
| **Fotos** | Acceder a imágenes existentes | No |
| **Contactos** | Funciones de contactos | No |
| **Calendario** | Acceso a eventos | No |
| **Recordatorios** | Acceso a recordatorios | No |

> 💡 Todos los permisos son **opcionales**. Puedes cambiarlos después en **Settings** → **Permissions** o en la app **Configuración** de iOS.

**Permisos recomendados para una experiencia completa:**
- ✅ **Cámara** — para enviar fotos al agente
- ✅ **Micrófono** — para Talk mode y dictado por voz
- ✅ **Notificaciones** — para recibir alertas importantes
- ✅ **Ubicación** — para que el agente pueda ayudarte con información contextual

### 🎙️ Configuración de Talk Mode

El Talk mode permite interactuar por voz con tu agente en tiempo real.

**Para activarlo:**

1. Ve a **Chat** en la app
2. Busca el control **Talk** (ícono de micrófono)
3. Mantén presionado para hablar (push-to-talk) o toca para activar/desactivar
4. El control se anima con el nivel de audio mientras escuchas o hablas

**Configuración avanzada de Talk:**

1. Ve a **Settings** → **OpenClaw** (requiere conexión operator.admin)
2. Configura el proveedor de voz, transporte y nivel de razonamiento
3. Puedes elegir o actualizar el micrófono desde la configuración de Talk

### 🖼️ Configuración de Canvas

Canvas permite al agente mostrar contenido visual en tu iPhone (gráficos, imágenes, interfaces).

**Verificar Canvas está habilitado:**

1. En **Settings** → **OpenClaw**, verifica que Canvas esté activo
2. El Gateway debe soportar comandos `node.invoke` para Canvas
3. El agente puede enviar contenido a Canvas cuando lo necesite

### ⚙️ Configurar Gateway desde la App (Avanzado)

Si tienes permisos de `operator.admin` y el Gateway soporta `openclaw.chat`:

1. Ve a **Settings** → **OpenClaw**
2. Se abrirá un **asistente dedicado de configuración del Gateway**
3. La conversación de setup es separada del chat normal
4. Las respuestas con secretos se redactan localmente
5. Cuando termines, toca **Open Chat** para volver al chat normal

---

## 5. Uso Diario

### 💬 Chatear desde la App

1. Abre la app → pestaña **Chat**
2. Escribe tu mensaje en el compositor
3. Toca **Enviar** (o usa el atajo de teclado)
4. El agente responde en la conversación

**Características del chat:**
- Las conversaciones se preservan en caché y se abren inmediatamente
- Las conversaciones recientes se pueden navebar mientras estás desconectado
- La app refresca automáticamente cuando el Gateway responde

### 🎙️ Talk Mode (Push-to-Talk)

Para interactuar por voz:

1. En **Chat**, busca el control **Talk**
2. **Mantén presionado** para hablar (push-to-talk)
3. **Libera** para enviar tu mensaje de voz
4. El agente procesa y responde por voz o texto

**Alternativas de voz:**
- **Dictado:** Toca el ícono de micrófono para dictar un mensaje de texto
- **Nota de voz:** Abre el menú del micrófono para grabar una nota de voz completa
- **Reproducir respuesta:** Mantén presionado un mensaje del agente y elige **Listen** para escucharlo

### 📸 Enviar Fotos y Videos

1. En el chat, toca el ícono de **adjuntar** 📎
2. Elige:
   - **Cámara** — tomar una foto/video nuevo
   - **Galería** — seleccionar una imagen existente
3. Selecciona o captura el contenido
4. Se envía al agente junto con tu mensaje

> 💡 Las imágenes enviadas se procesan por el agente. Puedes preguntar sobre lo que la imagen muestra, pedir análisis, etc.

### 📴 Cola Offline

Si el Gateway está temporalmente inaccesible, la app maneja una **cola de mensajes offline**:

- **Hasta 50 mensajes** pueden encolarse
- Los mensajes encolados se muestran en la transcripción con un indicador
- Se envían **en orden** al reconectar
- Incluyen reintentos con backoff y controles de retry/delete
- Los mensajes **expiran después de 48 horas** offline (no se envían)
- **Reinicio de app** no borra la cola

**Controles de la cola:**
- **Retry** — reintentar envío de un mensaje fallido
- **Delete** — eliminar un mensaje de la cola

### 📂 Explorar Archivos del Workspace

Desde la app puedes navegar el workspace del agente (solo lectura):

1. Ve a **Agents** → **Files**
2. Explora directorios con drill-down
3. Vista previa con syntax highlighting para archivos de texto
4. Vista previa de imágenes
5. Opción de compartir (share sheet) para exportar

---

## 6. Apple Watch

### ⌚ Emparejar el Watch (Relay por iPhone — Por Defecto)

Por defecto, el Apple Watch funciona como **relay** a través del iPhone:

1. Abre la app **Watch** en tu iPhone
2. Ve a **My Watch** → **Available Apps**
3. Instala **OpenClaw**
4. Abre OpenClaw una vez en ambos dispositivos

**Qué puede hacer en este modo:**
- ✅ Dictar mensajes y escuchar respuestas
- ✅ Enviar mensajes al agente
- ✅ Recibir notificaciones
- ✅ Revisar aprobaciones de comandos (allow/deny)

### ⌚ Conexión Directa al Gateway (Avanzado)

El modo **Direct** le da al Watch su propia conexión al Gateway, sin depender del iPhone.

**Requisitos:**
- iPhone conectado al Gateway con `operator.admin`
- Gateway con endpoint `wss://` con certificado confiable por watchOS
- Watch con Wi-Fi o celular activo
- OpenClaw activo en el Watch

**Setup:**

1. En iPhone: **Settings** → **Apple Watch**
2. Toca **Enable Direct Gateway Connection**
3. Abre OpenClaw en el Watch antes de que el código expire
4. Verifica con `openclaw nodes status`

**Comandos disponibles en modo Direct:**

| Superficie | Comandos | Notas |
|------------|----------|-------|
| Device | `device.info`, `device.status` | Identidad, batería, almacenamiento, red |
| Notifications | `system.notify` | Mientras la app esté activa |

> ⚠️ **Limitación:** Chat, Talk, aprobaciones y el flujo de notificaciones `watch.*` siguen siendo features de relay iPhone. El Watch directo solo cubre comandos de dispositivo y notificaciones.

### 🎙️ Dictar y Escuchar

1. **Dictar:** En el Watch, mantén presionado o usa el botón de voz
2. **Habla tu mensaje**
3. El Watch envía el dictado al iPhone → Gateway → agente
4. **Escuchar respuesta:** El Watch reproduce la respuesta del agente por audio

**Controles disponibles:**
- **Silent send** — enviar sin sonido
- **Cancel** — cancelar la dictado
- **Stop** — detener la reproducción

---

## 7. Solución de Problemas Comunes

### ❌ "Gateway no encontrado" / "Gateway unreachable"

**Causas más frecuentes:**

1. **El Gateway no está corriendo:**
   ```bash
   openclaw gateway status
   # Si no está activo:
   openclaw gateway restart
   ```

2. **El bind es `loopback` (el más común):**
   - El Gateway solo escucha en `127.0.0.1`
   - Solución: cambia a `lan` o usa Tailscale
   ```json5
   { gateway: { bind: "lan" } }
   ```

3. **Firewall bloquea el puerto 18789:**
   ```bash
   # En Linux:
   sudo ufw allow 18789/tcp
   # O verifica con:
   ss -tlnp | grep 18789
   ```

4. **El iPhone no está en la misma red o Tailscale no está activo**
   - Verifica que Tailscale esté conectado en ambos dispositivos
   - O usa host manual con IP pública

5. **Certificado SSL inválido (wss://):**
   - El Gateway debe usar un certificado válido para `wss://`
   - Certificados autofirmados no funcionan para Watch directo

### ❌ "Pending approval" / Pairing falla

1. **Código expirado:**
   - Los códigos de pairing tienen vida corta
   - Genera uno nuevo desde Control UI o `openclaw qr`

2. **Aprobación pendiente:**
   ```bash
   openclaw devices list
   openclaw devices approve <requestId>
   ```

3. **Cambio de autenticación:**
   - Si el app reintentó con datos diferentes, la solicitud anterior se invalida
   - Ejecuta `openclaw devices list` de nuevo antes de aprobar

4. **Acceso limitado:**
   - Si el pairing fue en `ws://` (LAN sin TLS), el acceso es automáticamente limitado
   - Para acceso full: configura `wss://` o Tailscale Serve
   - Escanea un nuevo código de acceso completo

### ❌ La app se desconecta frecuentemente

1. **iOS suspende conexiones en background:**
   - Es comportamiento normal de iOS
   - La app intenta reconectar automáticamente al volver a foreground
   - Las notificaciones push ayudan a despertar la app

2. **Gateway reinicia:**
   ```bash
   openclaw gateway status
   # Si está en crash loop:
   openclaw doctor
   ```

3. **Red inestable:**
   - La app tiene reconexión automática con backoff
   - Los mensajes se encolan durante desconexiones temporales

4. **Memory pressure en el Gateway:**
   - v2026.7.1 reduce el uso de memoria en reconexiones
   - Verifica con `openclaw gateway status` si hay warnings de memoria

### ❌ Problemas con permisos

1. **Micrófono no funciona en Talk mode:**
   - Ve a **Configuración** de iOS → **OpenClaw** → **Micrófono** → activar
   - En la app: **Settings** → **Permissions** → verificar micrófono

2. **Cámara no funciona:**
   - Misma solución: verificar permisos en Configuración de iOS

3. **Notificaciones no llegan:**
   - Verificar que las notificaciones estén habilitadas en iOS
   - Verificar que el push relay esté configurado (builds oficiales usan `ios-push-relay.openclaw.ai`)

4. **Foto no se envía:**
   - Verificar permiso de Fotos en iOS
   - Intentar con una imagen más pequeña

### ❌ Error de conexión "Pairing required" en Control UI

Desde v2026.7.1, los errores de conexión muestran mensajes accionables en vez de genéricos:

- **"Pairing required"** — necesitas emparejar el dispositivo
- **"Protocol incompatible"** — actualiza el Gateway o la app
- **"Authentication failed"** — verifica credenciales

### ❌ Watch no conecta directamente

1. **Certificado no confiable:**
   - watchOS no acepta certificados autofirmados
   - Usa un certificado Let's Encrypt o similar

2. **Loopback o rutas solo iPhone:**
   - El Watch necesita una ruta accesible independiente
   - Loopback y rutas solo iPhone no funcionan

3. **Sin Wi-Fi ni celular:**
   - El Watch directo necesita conectividad propia

---

## 8. Tips Avanzados

### 🔄 Combinar con Telegram (Uso Complementario)

Puedes usar **Telegram** y la **app iOS** en paralelo. Ambos se conectan al mismo Gateway:

- **Telegram** → ideal para mensajes rápidos, notificaciones, uso desde escritorio
- **App iOS** → ideal para voz (Talk mode), fotos, Canvas, Apple Watch

**Configurar Telegram** (si aún no lo tienes):

```bash
# Necesitas un Bot Token de @BotFather
openclaw configure
# Selecciona Telegram y sigue las instrucciones
```

> 💡 Ambos canales comparten las mismas sesiones del agente. Puedes empezar una conversación en Telegram y continuarla en la app iOS.

### 🖼️ Canvas y Capacidades Nativas

Canvas permite al agente mostrar contenido visual interactivo en tu iPhone:

- **Gráficos e interfaces** — el agente puede generar y mostrar dashboards
- **Imágenes procesadas** — análisis visual en tiempo real
- **Contenido dinámico** — se actualiza con la conversación

**Para habilitar Canvas:**
1. Verificar que el Gateway soporte comandos `node.invoke`
2. En la app: **Settings** → verificar Canvas activo

### 📱 Múltiples Gateways

La app puede emparejarse con **múltiples Gateways**:

1. Ve a **Settings** → **Gateways**
2. Verás la lista de gateways emparejados
3. El ✓ indica el gateway activo
4. Toca otro para cambiar (se desconecta del actual y reconecta al nuevo)

**Características:**
- Cada gateway tiene sus propias credenciales, preferencias e historial
- Cambiar gateway nunca mezcla estado entre gateways
- El push registration sigue al gateway activo
- Swipe → **Forget** para eliminar un gateway (borra credenciales, tokens, caché)

### 🔒 Seguridad: Acceso Full vs Limited

| Nivel | Acceso | Cuándo usar |
|-------|--------|-------------|
| **Full** | Chat, configuración, upgrades, aprobaciones, terminal | Uso personal, administrador |
| **Limited** | Solo chat y funciones básicas | Dispositivos compartidos, invitados |

- El acceso `ws://` (LAN sin TLS) se limita automáticamente
- Para acceso full con red remota: usa `wss://` o Tailscale Serve

### 📊 Monitoreo de Uso

Desde la app puedes ver:
- **Costo estimado** por sesión y por proveedor
- **Tokens** usados en cada respuesta
- **Contexto** usado vs disponible
- **Modelo activo** y nivel de razonamiento

### 🛠️ Terminal desde la App

Desde v2026.7.1, puedes abrir un terminal del workspace directamente desde la app:

1. Ve a **Control Hub** → **Terminal**
2. Se abre una sesión de shell en el workspace del agente
3. Las sesiones persisten entre cambios de pantalla
4. Si el Gateway no está conectado, muestra guía de setup

### 🔄 Actualizar la App

Las actualizaciones de la app se distribuyen vía App Store:

1. Abre **App Store** → **Perfil** → **Available Updates**
2. Busca actualizaciones de OpenClaw
3. Actualiza

> 💡 Las builds oficiales de App Store usan un push relay en `ios-push-relay.openclaw.ai`. No necesitas configurar credenciales APNs manualmente — el relay lo maneja.

### 🧹 Limpiar y Reconfigurar

Si necesitas empezar de cero:

1. **Olvidar gateway:** Settings → Gateways → swipe → **Forget**
2. **Borrar caché:** Settings → Reset (borra caché, credenciales, cola)
3. **Re-pairing:** genera un nuevo código QR y repite el proceso de pairing

---

## 📚 Recursos Adicionales

| Recurso | URL |
|---------|-----|
| Documentación oficial | https://docs.openclaw.ai |
| Plataformas | https://docs.openclaw.ai/platforms |
| iOS app docs | https://docs.openclaw.ai/platforms/ios |
| Release notes v2026.7.1 | https://docs.openclaw.ai/releases/2026.7.1 |
| GitHub | https://github.com/openclaw/openclaw |
| Gateway config | https://docs.openclaw.ai/gateway/configuration |

---

## ❓ FAQ Rápida

**¿Necesito un Gateway corriendo para usar la app?**
Sí. La app es un cliente — el Gateway es el servidor. Sin Gateway, la app no funciona.

**¿Puedo usar la app sin Tailscale?**
Sí, pero necesitas que el Gateway sea accesible desde tu iPhone (misma LAN con bind `lan`, o IP pública con puerto expuesto).

**¿La app funciona en background?**
Sí, pero iOS puede suspender conexiones WebSocket. La app se reconecta automáticamente al volver a foreground. Las notificaciones push ayudan a despertarla.

**¿Puedo tener múltiples iPhones conectados al mismo Gateway?**
Sí. Cada iPhone se empareja independientemente y recibe su propio nodo.

**¿Qué pasa si el Gateway se cae?**
La app encola mensajes (hasta 50, 48h max), muestra conversaciones en caché, y se reconecta automáticamente cuando el Gateway vuelve.

**¿La app iOS es de código abierto?**
Las builds oficiales se distribuyen vía App Store. El código fuente está disponible para desarrollo local.

---

> 🎉 **¡Listo!** Con esta guía deberías tener tu app OpenClaw iOS funcionando. Si encuentras problemas, consulta la sección de [Solución de Problemas](#7-solución-de-problemas-comunes) o visita la documentación oficial.
