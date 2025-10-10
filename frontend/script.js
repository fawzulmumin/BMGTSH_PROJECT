document.addEventListener('DOMContentLoaded', function() {
    const predictButton = document.querySelector('button[type="submit"]');
    const resultDiv = document.getElementById('predictionResult');

    // Cek apakah predictButton dan resultDiv ada di DOM
    if (predictButton && resultDiv) {
        predictButton.addEventListener('click', async (event) => {
            event.preventDefault(); // Mencegah form submit default

            const data = {
                Provinsi: document.getElementById('Provinsi').value,
                Tahun: document.getElementById('Tahun').value,
                Luas_Panen: document.getElementById('Luas Panen').value,
                Curah_hujan: document.getElementById('Curah hujan').value,
                Kelembapan: document.getElementById('Kelembapan').value,
                Suhu_rata_rata: document.getElementById('Suhu rata-rata').value
            };

            try {
                const response = await fetch('http://127.0.0.1:5000/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                if (response.ok) {
                    resultDiv.innerHTML = `Prediksi produksi padi: ${result.prediction} ton`;
                } else {
                    resultDiv.innerHTML = `Error: ${result.error}`;
                }
            } catch (error) {
                console.error('Error:', error);
                resultDiv.innerHTML = `Error: ${error.message}`;
            }
        });
    } else {
        console.error('Predict button or result div not found.');
    }

    async function loadVisualizationData() {
        try {
            const response = await fetch('http://127.0.0.1:5000/visualization_data');
            const data = await response.json();
            
            if (response.ok) {
                updateBarChart(data.barChart);
                updateLineChart(data.lineChart);
                updateCorrelationMatrix(data.correlationMatrix);
            } else {
                console.error('Error fetching visualization data:', data.error);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    function updateBarChart(chartData) {
        const ctx = document.getElementById('barChart').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: 'Average Production by Province',
                    data: chartData.data,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    function updateLineChart(chartData) {
        const ctx = document.getElementById('lineChart').getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: 'Average Production by Year',
                    data: chartData.data,
                    fill: false,
                    borderColor: 'rgba(75, 192, 192, 1)',
                    tension: 0.1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }

    function updateCorrelationMatrix(matrixData) {
        const ctx = document.getElementById('correlationMatrix').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: matrixData.labels,
                datasets: matrixData.data.map((row, rowIndex) => ({
                    label: matrixData.labels[rowIndex],
                    data: row,
                    backgroundColor: (context) => {
                        const value = context.dataset.data[context.dataIndex];
                        const alpha = (value + 1) / 2; // Example mapping
                        return `rgba(255, 99, 132, ${alpha})`;
                    }
                }))
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    // Load visualization data on page load
    loadVisualizationData();
});
