#pragma once

#include <stdint.h>

// ==========================================
// AERO-STENT Hardware Pin Definitions & Config
// ==========================================

// --- Piezo Atomizer PWM (HRTIM STM32 / ESP32 LEDC) ---
#define PIN_PIEZO_PWM           18      // Output pin to MOSFET gate driver
#define PIEZO_FREQ_HZ           110000  // 110.0 kHz Resonant Frequency
#define PIEZO_PWM_RES_BITS      10      // 10-bit PWM resolution
#define PIEZO_DEFAULT_DUTY      512     // 50% duty cycle

// --- MPXV7002DP Differential Pressure Sensor ---
#define PIN_PRESSURE_ADC        34      // ADC pin connected to MPXV7002DP Vout
#define PRESSURE_VREF           3.3f    // Reference voltage
#define PRESSURE_SENSITIVITY    1.0f    // 1.0 V / kPa
#define PRESSURE_OFFSET_V       1.65f   // 1.65 V at zero differential pressure (Vcc/2)

// --- Operating Pressure Thresholds (cmH2O) ---
#define INHALE_TRIGGER_CMH2O    -0.20f  // Trigger nebulization on inhale
#define EXHALE_TRIGGER_CMH2O     0.15f  // Cutoff nebulization on exhale
#define PEP_TARGET_MIN_CMH2O     5.0f   // Minimum therapeutic PEP resistance
#define PEP_TARGET_MAX_CMH2O    15.0f   // Maximum therapeutic PEP resistance
#define BAROTRAUMA_LIMIT_CMH2O  20.0f   // Hard safety threshold for alarm / blow-off

// --- PEP Solenoid Valve Driver Pins ---
#define PIN_SOLENOID_PULLIN     25      // 12V Boost Enable (4 ms pulse)
#define PIN_SOLENOID_PWM_HOLD   26      // 3.3V PWM Holding pin
#define SOLENOID_HOLD_DUTY_PCT  28      // 28% Duty Cycle to minimize heat

// --- Timing Constants ---
#define SENSOR_SAMPLE_INTERVAL_US 1000  // 1 kHz sampling rate (1000 µs)
#define MAX_INHALATION_TIMEOUT_MS 3500  // Max aerosol burst duration safety limit
