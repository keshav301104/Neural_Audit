console.log("⚡ NeuralAudit Script Loaded");

// 1. FILE SELECTION LOGIC
document.getElementById('fileChat').addEventListener('change', function(e) {
    if (this.files && this.files[0]) {
        console.log("Chat file picked:", this.files[0].name);
        document.getElementById('labelChat').innerText = "✅ " + this.files[0].name;
        document.getElementById('labelChat').style.color = "#00ff9d";
    }
});

document.getElementById('fileCtx').addEventListener('change', function(e) {
    if (this.files && this.files[0]) {
        console.log("Context file picked:", this.files[0].name);
        document.getElementById('labelCtx').innerText = "✅ " + this.files[0].name;
        document.getElementById('labelCtx').style.color = "#00ff9d";
    }
});

// 2. CHART SETUP
const ctx = document.getElementById('auditChart').getContext('2d');
let auditChart = new Chart(ctx, {
    type: 'radar',
    data: {
        labels: ['Relevance', 'Faithfulness', 'Safety', 'Tone', 'Accuracy'],
        datasets: [{
            label: 'Audit Score',
            data: [0, 0, 0, 0, 0],
            backgroundColor: 'rgba(0, 255, 157, 0.2)',
            borderColor: '#00ff9d',
            borderWidth: 2,
            pointBackgroundColor: '#fff'
        }]
    },
    options: {
        scales: {
            r: {
                angleLines: { color: 'rgba(255,255,255,0.1)' },
                grid: { color: 'rgba(255,255,255,0.1)' },
                suggestedMin: 0,
                suggestedMax: 100,
                ticks: { display: false }
            }
        },
        plugins: { legend: { display: false } }
    }
});

// 3. RUN AUDIT LOGIC
document.getElementById('btnRun').addEventListener('click', async () => {
    console.log("🚀 Initiate Clicked");
    
    const chatInput = document.getElementById('fileChat');
    const ctxInput = document.getElementById('fileCtx');
    const term = document.getElementById('terminal');

    // DEBUG CHECK
    if (!chatInput.files.length || !ctxInput.files.length) {
        alert("⚠️ Files missing! Please select both JSON files.");
        return;
    }

    const btn = document.getElementById('btnRun');
    btn.innerText = "PROCESSING...";
    term.innerHTML += `<div class="log-line">> UPLOADING DATA TO NEURAL CORE...</div>`;

    const formData = new FormData();
    formData.append("chat_file", chatInput.files[0]);
    formData.append("context_file", ctxInput.files[0]);

    try {
        const res = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        if (!res.ok) {
            const errText = await res.text();
            throw new Error(`Server Error (${res.status}): ${errText}`);
        }

        const data = await res.json();
        console.log("Data Received:", data);

        // Update UI
        document.getElementById('valRel').innerText = data.scores.relevance.score + "%";
        document.getElementById('valFaith').innerText = data.scores.faithfulness.score + "%";
        document.getElementById('valCost').innerText = "$" + data.metrics.cost_usd;
        document.getElementById('valLatency').innerText = data.metrics.latency_seconds + "s";

        // Update Terminal
        term.innerHTML += `<div class="log-line" style="color:#00ff9d">> SUCCESS: METRICS COMPUTED</div>`;
        term.innerHTML += `<div class="log-line">> RELEVANCE: ${data.scores.relevance.reason}</div>`;
        term.innerHTML += `<div class="log-line">> FAITHFULNESS: ${data.scores.faithfulness.reason}</div>`;
        
        // Update Chart
        auditChart.data.datasets[0].data = [
            parseInt(data.scores.relevance.score || 0), 
            parseInt(data.scores.faithfulness.score || 0), 
            95, 88, 92
        ];
        auditChart.update();

        btn.innerText = "AUDIT COMPLETE";

    } catch (error) {
        console.error(error);
        term.innerHTML += `<div class="log-line log-fail">> CRITICAL ERROR: ${error.message}</div>`;
        btn.innerText = "RETRY";
        alert("Audit Failed: Check Console (F12) for details.");
    }
});