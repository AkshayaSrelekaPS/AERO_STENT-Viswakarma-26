// AERO-STENT Live Telemetry Chart & Dynamic Feed Simulator

document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('pressureChart').getContext('2d');
    const phaseEl = document.getElementById('phase-val');
    const pressureEl = document.getElementById('pressure-val');
    const drugEl = document.getElementById('drug-val');
    const btnToggle = document.getElementById('btn-toggle-sim');

    let isRunning = true;
    let timeIndex = 0;
    let drugRemaining_mL = 4.2;

    const maxPoints = 50;
    const labels = Array.from({ length: maxPoints }, (_, i) => `${i * 0.1}s`);
    const dataPoints = Array.from({ length: maxPoints }, () => 0.0);

    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Airway Pressure (cmH₂O)',
                data: dataPoints,
                borderColor: '#00D2D3',
                backgroundColor: 'rgba(0, 210, 211, 0.1)',
                borderWidth: 2.5,
                fill: true,
                tension: 0.35,
                pointRadius: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    min: -2.0,
                    max: 18.0,
                    grid: { color: 'rgba(255, 255, 255, 0.08)' },
                    ticks: { color: '#8B949E' }
                },
                x: {
                    display: false
                }
            },
            plugins: {
                legend: { display: false }
            },
            animation: false
        }
    });

    function generateBreathingCycle(t) {
        // 4.0s breath period (1.5s inhale, 2.5s exhale with PEP)
        const cycleTime = t % 4.0;
        let pressure = 0.0;
        let phase = "PAUSE";

        if (cycleTime < 1.4) {
            // Inhalation: drops to -0.4 to -0.8 cmH2O
            pressure = -0.55 * Math.sin((cycleTime / 1.4) * Math.PI);
            phase = "INHALATION (NEBULIZING)";
            drugRemaining_mL = Math.max(0, drugRemaining_mL - 0.0004);
        } else if (cycleTime < 3.6) {
            // Exhalation: climbs to therapeutic PEP plateaux (10.0 cmH2O)
            const exTime = cycleTime - 1.4;
            pressure = 10.2 * Math.sin((exTime / 2.2) * Math.PI) + (Math.random() * 0.4 - 0.2);
            phase = "EXHALATION (PEP STENTING)";
        } else {
            // Rest pause
            pressure = 0.0;
            phase = "RESPIRATORY PAUSE";
        }

        return { pressure, phase };
    }

    setInterval(() => {
        if (!isRunning) return;

        timeIndex += 0.08;
        const { pressure, phase } = generateBreathingCycle(timeIndex);

        dataPoints.shift();
        dataPoints.push(parseFloat(pressure.toFixed(2)));
        chart.update();

        // Update DOM labels
        phaseEl.textContent = phase;
        pressureEl.textContent = `${pressure.toFixed(2)} cmH₂O`;
        drugEl.textContent = `${drugRemaining_mL.toFixed(2)} mL`;

        if (phase.includes("INHALATION")) {
            phaseEl.style.color = '#00D2D3';
        } else if (phase.includes("PEP")) {
            phaseEl.style.color = '#0A84FF';
        } else {
            phaseEl.style.color = '#8B949E';
        }
    }, 80);

    btnToggle.addEventListener('click', () => {
        isRunning = !isRunning;
        btnToggle.textContent = isRunning ? "PAUSE TELEMETRY STREAM" : "RESUME TELEMETRY STREAM";
    });
});
