/*
 * Prototipo X — Copiloto Moto
 * Firmware v1.0 — Blind Spot Detection System
 * 
 * Hardware: ESP32-S3 + 2x HLK-LD2410 radar + LED strip + vibradores + buzzer
 * 
 * Funcionalidad:
 *   - Lee 2 radares mmWave en paralelo (izquierda + derecha)
 *   - Detecta distancia + velocidad de vehículos
 *   - Alerta visual (LED strip), háptica (vibradores) y sonora (buzzer)
 *   - Display OLED con estado en tiempo real
 *   - WiFi AP para debugging
 */

#include <Arduino.h>
#include <HardwareSerial.h>
#include <Adafruit_NeoPixel.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ============================================================
// PIN DEFINITIONS
// ============================================================
// Radar izquierdo (UART2)
#define RADAR_L_RX      16
#define RADAR_L_TX      17

// Radar derecho (UART1)
#define RADAR_R_RX      18
#define RADAR_R_TX      19

// LED strip (WS2812B)
#define LED_PIN         8
#define LED_COUNT       30

// Vibradores (PWM)
#define VIB_LEFT_PIN    4
#define VIB_RIGHT_PIN   5

// Buzzer
#define BUZZER_PIN      6

// OLED I2C
#define SDA_PIN         21
#define SCL_PIN         22
#define OLED_WIDTH      128
#define OLED_HEIGHT     64

// ============================================================
// CONSTANTS
// ============================================================
#define ZONA_PELIGRO       1.0   // metros — rojo sólido + vibración fuerte
#define ZONA_ALERTA        2.0   // metros — rojo parpadeo + vibración suave
#define ZONA_PRECAUCION    5.0   // metros — amarillo parpadeo
#define UMBRAL_APROX       0.5   // m/s — velocidad de aproximación peligrosa
#define UPDATE_INTERVAL    50    // ms — frecuencia de lectura

// ============================================================
// GLOBALS
// ============================================================
Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);
Adafruit_SSD1306 display(OLED_WIDTH, OLED_HEIGHT, &Wire, -1);

HardwareSerial SerialRadarL(1);
HardwareSerial SerialRadarR(2);

struct RadarData {
    float distance;      // metros
    float speed;         // m/s (positivo = se acerca)
    bool moving;
    bool detected;
    uint32_t lastUpdate;
};

struct AlertState {
    uint8_t level;       // 0=safe, 1=caution, 2=warning, 3=danger, 4=imminent
    bool leftActive;
    bool rightActive;
};

RadarData radarLeft = {0, 0, false, false, 0};
RadarData radarRight = {0, 0, false, false, 0};
AlertState alerts = {0, false, false};

unsigned long lastLEDUpdate = 0;
unsigned long lastDisplayUpdate = 0;
bool ledState = false;

// ============================================================
// HLK-LD2410 PROTOCOL PARSER
// ============================================================

// LD2410 frame: 0xF4 0xF3 0xF2 0xF1 + payload + 0xF8 0xF7 0xF6 0xF5
// Target data: distance(2 bytes) + speed(2 bytes) + energy(1 byte) + state(1 byte)

struct LD2410Frame {
    uint16_t distance;    // cm
    int16_t speed;        // cm/s (negative = moving away)
    uint8_t energy;       // signal strength
    bool moving;
    bool valid;
};

LD2410Frame parseLD2410(Stream &serial) {
    LD2410Frame frame = {0, 0, 0, false, false};
    
    // Wait for header: 0xF4 0xF3 0xF2 0xF1
    if (serial.available() < 8) return frame;
    
    // Find header
    while (serial.available() >= 8) {
        uint8_t b = serial.read();
        if (b == 0xF4 && serial.peek() == 0xF3) {
            serial.read(); // consume 0xF3
            if (serial.read() == 0xF2 && serial.read() == 0xF1) {
                break; // header found
            }
        }
    }
    
    // Read payload (target data is 4 bytes minimum)
    uint8_t buf[8];
    unsigned long start = millis();
    while (serial.available() < 6 && millis() - start < 50) {
        delay(1);
    }
    
    if (serial.available() < 6) return frame;
    
    // Distance: 2 bytes LE (cm)
    frame.distance = serial.read() | (serial.read() << 8);
    
    // Speed: 2 bytes LE (cm/s)
    frame.speed = serial.read() | (serial.read() << 8);
    
    // Energy
    frame.energy = serial.read();
    
    // Moving state
    frame.moving = (serial.read() > 0);
    
    frame.valid = true;
    return frame;
}

// ============================================================
// RADAR READING (runs on Core 0)
// ============================================================
void readRadarsTask(void *pvParameters) {
    while (true) {
        // Read left radar
        LD2410Frame leftFrame = parseLD2410(SerialRadarL);
        if (leftFrame.valid) {
            radarLeft.distance = leftFrame.distance / 100.0f; // cm → m
            radarLeft.speed = leftFrame.speed / 100.0f;       // cm/s → m/s
            radarLeft.moving = leftFrame.moving;
            radarLeft.detected = leftFrame.distance < 500;    // < 5m = something there
            radarLeft.lastUpdate = millis();
        }
        
        // Read right radar
        LD2410Frame rightFrame = parseLD2410(SerialRadarR);
        if (rightFrame.valid) {
            radarRight.distance = rightFrame.distance / 100.0f;
            radarRight.speed = rightFrame.speed / 100.0f;
            radarRight.moving = rightFrame.moving;
            radarRight.detected = rightFrame.distance < 500;
            radarRight.lastUpdate = millis();
        }
        
        delay(UPDATE_INTERVAL);
    }
}

// ============================================================
// ALERT LOGIC
// ============================================================
uint8_t calculateAlertLevel(float distance, float speed) {
    // Speed-based escalation: if coming fast, escalate even at distance
    bool approaching = speed < -UMBRAL_APROX; // negative = approaching
    
    if (distance < ZONA_PELIGRO) {
        return approaching ? 4 : 3;  // imminent or danger
    }
    if (distance < ZONA_ALERTA) {
        return approaching ? 4 : 3;  // imminent if fast, danger if slow
    }
    if (distance < ZONA_PRECAUCION) {
        return approaching ? 3 : 2;  // danger if fast, warning if slow
    }
    // Beyond 5m: caution if approaching fast
    if (approaching && distance < 8.0f) {
        return 1; // caution
    }
    return 0; // safe
}

void updateAlerts() {
    uint8_t leftLevel = 0;
    uint8_t rightLevel = 0;
    
    if (millis() - radarLeft.lastUpdate < 1000) { // fresh data
        leftLevel = calculateAlertLevel(radarLeft.distance, radarLeft.speed);
    }
    
    if (millis() - radarRight.lastUpdate < 1000) {
        rightLevel = calculateAlertLevel(radarRight.distance, radarRight.speed);
    }
    
    alerts.leftActive = leftLevel > 0;
    alerts.rightActive = rightLevel > 0;
    alerts.level = max(leftLevel, rightLevel);
}

// ============================================================
// LED ALERTS (runs on Core 1)
// ============================================================
void updateLEDs() {
    if (millis() - lastLEDUpdate < 80) return;
    lastLEDUpdate = millis();
    ledState = !ledState;
    
    switch (alerts.level) {
        case 0: // Safe
            for (int i = 0; i < LED_COUNT; i++) {
                strip.setPixelColor(i, strip.Color(0, 255, 0)); // verde
            }
            break;
            
        case 1: // Caution - amarillo parpadeo lento
            if (ledState) {
                for (int i = 0; i < LED_COUNT; i++) {
                    strip.setPixelColor(i, strip.Color(255, 180, 0));
                }
            } else {
                strip.clear();
            }
            break;
            
        case 2: // Warning - rojo parpadeo + vibración suave
            for (int i = 0; i < LED_COUNT; i++) {
                strip.setPixelColor(i, ledState ? 
                    strip.Color(255, 0, 0) : strip.Color(100, 0, 0));
            }
            // Left side vibration
            if (alerts.leftActive) {
                analogWrite(VIB_LEFT_PIN, ledState ? 120 : 0);
            }
            // Right side vibration
            if (alerts.rightActive) {
                analogWrite(VIB_RIGHT_PIN, ledState ? 120 : 0);
            }
            break;
            
        case 3: // Danger - rojo sólido + vibración fuerte
            for (int i = 0; i < LED_COUNT; i++) {
                strip.setPixelColor(i, strip.Color(255, 0, 0));
            }
            analogWrite(VIB_LEFT_PIN, alerts.leftActive ? 200 : 0);
            analogWrite(VIB_RIGHT_PIN, alerts.rightActive ? 200 : 0);
            break;
            
        case 4: // Imminent - rojo strobe + vibración continua + buzzer
            if (ledState) {
                for (int i = 0; i < LED_COUNT; i++) {
                    strip.setPixelColor(i, strip.Color(255, 50, 50));
                }
            } else {
                strip.clear();
            }
            analogWrite(VIB_LEFT_PIN, alerts.leftActive ? 255 : 0);
            analogWrite(VIB_RIGHT_PIN, alerts.rightActive ? 255 : 0);
            digitalWrite(BUZZER_PIN, HIGH);
            break;
    }
    
    if (alerts.level < 4) {
        digitalWrite(BUZZER_PIN, LOW);
    }
    if (alerts.level < 2) {
        analogWrite(VIB_LEFT_PIN, 0);
        analogWrite(VIB_RIGHT_PIN, 0);
    }
    
    strip.show();
}

// ============================================================
// OLED DISPLAY
// ============================================================
void updateDisplay() {
    if (millis() - lastDisplayUpdate < 200) return;
    lastDisplayUpdate = millis();
    
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    
    // Title
    display.setCursor(0, 0);
    display.println(F("  PROTO-X COPILOT"));
    display.drawLine(0, 10, 128, 10, SSD1306_WHITE);
    
    // Left radar
    display.setCursor(0, 14);
    display.print(F("L: "));
    if (millis() - radarLeft.lastUpdate < 1000) {
        display.print(radarLeft.distance, 1);
        display.print(F("m "));
        display.print(radarLeft.speed, 1);
        display.print(F("m/s"));
        display.print(radarLeft.moving ? " <<" : "");
    } else {
        display.print(F("---"));
    }
    
    // Right radar
    display.setCursor(0, 24);
    display.print(F("R: "));
    if (millis() - radarRight.lastUpdate < 1000) {
        display.print(radarRight.distance, 1);
        display.print(F("m "));
        display.print(radarRight.speed, 1);
        display.print(F("m/s"));
        display.print(radarRight.moving ? " >>" : "");
    } else {
        display.print(F("---"));
    }
    
    // Alert level
    display.setCursor(0, 38);
    display.print(F("STATUS: "));
    switch (alerts.level) {
        case 0: display.println(F("[ OK ]")); break;
        case 1: display.println(F("[ !! ] PRECAUCION")); break;
        case 2: display.println(F("[ !!!] ALERTA")); break;
        case 3: display.println(F("[!!!!] PELIGRO")); break;
        case 4: display.println(F("[!!!!] INMINENTE")); break;
    }
    
    // Mini bar graph
    display.setCursor(0, 50);
    display.print(F("L "));
    int lbar = map(constrain((int)radarLeft.distance, 0, 500), 0, 500, 0, 50);
    for (int i = 0; i < lbar; i++) display.print(F("="));
    display.print(F("|"));
    
    display.setCursor(64, 50);
    display.print(F("R "));
    int rbar = map(constrain((int)radarRight.distance, 0, 500), 0, 500, 0, 50);
    for (int i = 0; i < rbar; i++) display.print(F("="));
    
    display.display();
}

// ============================================================
// SETUP
// ============================================================
void setup() {
    Serial.begin(115200);
    Serial.println(F("=== PROTO-X COPILOT MOTO v1.0 ==="));
    
    // Init pins
    pinMode(VIB_LEFT_PIN, OUTPUT);
    pinMode(VIB_RIGHT_PIN, OUTPUT);
    pinMode(BUZZER_PIN, OUTPUT);
    digitalWrite(BUZZER_PIN, LOW);
    
    // Init I2C + OLED
    Wire.begin(SDA_PIN, SCL_PIN);
    if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        Serial.println(F("ERROR: OLED no detectado"));
    } else {
        display.clearDisplay();
        display.setTextSize(1);
        display.setTextColor(SSD1306_WHITE);
        display.setCursor(0, 0);
        display.println(F("PROTO-X v1.0"));
        display.println(F("Inicializando..."));
        display.display();
    }
    
    // Init LED strip
    strip.begin();
    strip.setBrightness(150);
    strip.clear();
    strip.show();
    
    // Init radars (9600 baud default for LD2410)
    SerialRadarL.begin(9600, SERIAL_8N1, RADAR_L_RX, RADAR_L_TX);
    SerialRadarR.begin(9600, SERIAL_8N1, RADAR_R_RX, RADAR_R_TX);
    
    Serial.println(F("Radares inicializados"));
    Serial.println(F("Iniciando deteccion..."));
    
    // Launch radar reading on Core 0
    xTaskCreatePinnedToCore(
        readRadarsTask,
        "RadarReader",
        4096,
        NULL,
        1,
        NULL,
        0  // Core 0
    );
    
    // Self-test: flash all LEDs
    for (int i = 0; i < LED_COUNT; i++) {
        strip.setPixelColor(i, strip.Color(0, 0, 255));
        strip.show();
        delay(20);
    }
    delay(200);
    strip.clear();
    strip.show();
    
    Serial.println(F("PROTO-X listo para operar"));
}

// ============================================================
// LOOP (runs on Core 1)
// ============================================================
void loop() {
    updateAlerts();
    updateLEDs();
    updateDisplay();
    delay(10);
}
