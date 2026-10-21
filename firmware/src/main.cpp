#include <Arduino.h>
#include "config.h"

// State Machine Definition
enum DeviceState {
    STANDBY,
    INHALATION_NEBULIZING,
    EXHALATION_PEP_STENTING,
    BAROTRAUMA_ALARM,
    ERROR_FAULT
};

DeviceState currentState = STANDBY;
unsigned long nebulizationStartTime = 0;
float currentPressure_cmH2O = 0.0f;

// Forward declarations
float readPressureCmH2O();
void setPiezoState(bool enable);
void setPepValve(bool engage);

void setup() {
    Serial.begin(115200);
    analogReadResolution(12);

    pinMode(PIN_PIEZO_PWM, OUTPUT);
    pinMode(PIN_SOLENOID_PULLIN, OUTPUT);
    pinMode(PIN_SOLENOID_PWM_HOLD, OUTPUT);

    digitalWrite(PIN_PIEZO_PWM, LOW);
    digitalWrite(PIN_SOLENOID_PULLIN, LOW);
    digitalWrite(PIN_SOLENOID_PWM_HOLD, LOW);

    // Initialize LEDC PWM for 110 kHz Piezo on ESP32
    ledcAttach(PIN_PIEZO_PWM, PIEZO_FREQ_HZ, PIEZO_PWM_RES_BITS);
    ledcWrite(PIN_PIEZO_PWM, 0);

    Serial.println(F("[AERO-STENT] Firmware Initialized. Ready for breathing sync."));
}

void loop() {
    currentPressure_cmH2O = readPressureCmH2O();

    switch (currentState) {
        case STANDBY:
            // Check for inhalation trigger
            if (currentPressure_cmH2O <= INHALE_TRIGGER_CMH2O) {
                currentState = INHALATION_NEBULIZING;
                nebulizationStartTime = millis();
                setPiezoState(true);
                setPepValve(false);
                Serial.printf("[EVENT] Inhale Detected (%.2f cmH2O) -> Piezo ON (110kHz)\n", currentPressure_cmH2O);
            }
            break;

        case INHALATION_NEBULIZING:
            // Check for exhalation cutoff or maximum timeout
            if (currentPressure_cmH2O >= EXHALE_TRIGGER_CMH2O || (millis() - nebulizationStartTime > MAX_INHALATION_TIMEOUT_MS)) {
                setPiezoState(false);
                currentState = EXHALATION_PEP_STENTING;
                setPepValve(true);
                Serial.printf("[EVENT] Exhale Switch (%.2f cmH2O) -> Piezo OFF (<3.2ms), PEP Active\n", currentPressure_cmH2O);
            }
            break;

        case EXHALATION_PEP_STENTING:
            // Barotrauma safety check
            if (currentPressure_cmH2O >= BAROTRAUMA_LIMIT_CMH2O) {
                currentState = BAROTRAUMA_ALARM;
                setPepValve(false);
                Serial.printf("[ALARM] Over-Pressure (%.2f cmH2O)! Disengaging Solenoid & Venting\n", currentPressure_cmH2O);
            } 
            else if (fabs(currentPressure_cmH2O) < 0.05f) {
                // Return to standby during respiratory pause
                setPepValve(false);
                currentState = STANDBY;
            }
            break;

        case BAROTRAUMA_ALARM:
            // Wait for pressure to drop safely
            if (currentPressure_cmH2O < 15.0f) {
                currentState = STANDBY;
                Serial.println(F("[RECOVERY] Pressure Normalized. Resuming Normal Loop."));
            }
            break;

        default:
            setPiezoState(false);
            setPepValve(false);
            break;
    }

    delayMicroseconds(SENSOR_SAMPLE_INTERVAL_US);
}

float readPressureCmH2O() {
    int raw = analogRead(PIN_PRESSURE_ADC);
    float voltage = (raw / 4095.0f) * PRESSURE_VREF;
    float deltaV = voltage - PRESSURE_OFFSET_V;
    float pressure_kPa = deltaV / PRESSURE_SENSITIVITY;
    // 1 kPa = 10.1972 cmH2O
    return pressure_kPa * 10.1972f;
}

void setPiezoState(bool enable) {
    if (enable) {
        ledcWrite(PIN_PIEZO_PWM, PIEZO_DEFAULT_DUTY);
    } else {
        ledcWrite(PIN_PIEZO_PWM, 0);
    }
}

void setPepValve(bool engage) {
    if (engage) {
        // High-energy pull-in pulse (4.0 ms)
        digitalWrite(PIN_SOLENOID_PULLIN, HIGH);
        delayMicroseconds(4000);
        digitalWrite(PIN_SOLENOID_PULLIN, LOW);
        // Continuous low-power PWM hold
        analogWrite(PIN_SOLENOID_PWM_HOLD, (SOLENOID_HOLD_DUTY_PCT * 255) / 100);
    } else {
        digitalWrite(PIN_SOLENOID_PULLIN, LOW);
        analogWrite(PIN_SOLENOID_PWM_HOLD, 0);
    }
}
