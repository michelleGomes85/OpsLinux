document.addEventListener('DOMContentLoaded', function() {

    var modal = document.querySelectorAll('.modal');

    M.Modal.init(modal, {
        opacity: 0.8,
        inDuration: 300,
        outDuration: 200,
        startingTop: '10%',
        endingTop: '10%',
        onOpenEnd: function() {
            var textarea = document.getElementById('pergunta');
            textarea.value = ''; 
            textarea.focus(); 
        }
    });

    var sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);

    var tooltips = document.querySelectorAll('.tooltipped');
    M.Tooltip.init(tooltips, {
        position: 'bottom'
    });

    document.querySelectorAll('.icon-link').forEach(function(link) {
        link.addEventListener('click', function() {
            var pergunta = this.getAttribute('data-pergunta');
            document.getElementById('pergunta').value = pergunta;
        });
    });

    let clearQuestion = document.getElementById('limparPergunta');
    
    if (clearQuestion) {
        clearQuestion.addEventListener('click', function() {
            document.getElementById('pergunta').value = '';
        });
    }

    let sendQuestion = document.getElementById('enviarPergunta');

    if (sendQuestion) {
        
        document.getElementById('enviarPergunta').onclick = async function () {

            const question = document.getElementById('pergunta').value;
            var loadingEffect = document.getElementById('loadingEffect');
        
            if (!question) {
                alert("Por favor, insira uma pergunta.");
                return;
            }
        
            try {
                loadingEffect.style.display = 'block';
                const response = await fetch('/generate-response', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question: question })
                });
        
                if (!response.ok) {
                    throw new Error('Erro ao fazer a requisição');
                }
        
                const data = await response.json();
    
                loadingEffect.style.display = 'none';
    
                alert("Pergunta enviada com sucesso: " + pergunta);
    
                M.Modal.getInstance(document.getElementById('modalPergunta')).close();
        
                console.log(data); 
        
            } catch (error) {
                console.error('Erro:', error);
            }
        };
    }

    // Carrega os dados da API ao iniciar
    updateChartData();

    // Atualiza os dados a cada 5 minutos (300.000 milissegundos)
    setInterval(updateChartData, 300000);
});

const memoryData = {
    title: 'Consumo de Memória', 
    chartType: 'bar',    

    datasets: {
        label: 'Memória',
        data: [20, 30], 
        backgroundColor: generateColors(2),
        labels: ['Usada', 'Livre']
    }
};

const diskData = {
    title: 'Consumo de Disco', 
    chartType: 'bar',     

    datasets: {
        label: 'Disco',
        data: [30, 80],
        backgroundColor: generateColors(2),
        labels: ['Usada', 'Livre']
    }
};

const cpuData = {
    title: 'Consumo de CPU',
    chartType: 'bar',       
    
    datasets: {
        label: 'CPU',
        data: [25, 35, 20, 20], 
        backgroundColor: generateColors(4),
        labels: ['CPU 1', 'CPU 2', 'CPU 3', 'CPU 4'], 
    }
};

async function fetchSystemInfo() {
    try {
        const response = await fetch('/system-info');
        if (!response.ok) {
            throw new Error(`Erro na requisição: ${response.statusText}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Erro ao buscar dados da API:', error);
        return null;
    }
}

async function updateChartData() {

    const systemInfo = await fetchSystemInfo();

    if (systemInfo) {
        // Atualiza os dados de memória
        memoryData.datasets.data = [
            systemInfo.memory_usage.used_percent,
            systemInfo.memory_usage.free_percent
        ];

        memoryData.datasets.labels = ['Usada', 'Livre'];

        // Atualiza os dados de disco
        diskData.datasets.data = [
            systemInfo.disk_usage.used_percent,
            systemInfo.disk_usage.free_percent
        ];

        diskData.datasets.labels = ['Usada', 'Livre'];

        // Atualiza os dados de CPU
        cpuData.datasets.data = systemInfo.cpu_usage_per_core;
        cpuData.datasets.labels = systemInfo.cpu_usage_per_core.map((_, index) => `CPU ${index + 1}`);

        // Re-renderiza o gráfico atual
        renderGraphic(currentData);
    }
}

function generateColors(length) {

    const colors = [];
    const greenShades = [
        'rgba(32, 178, 170, 0.5)', // cor base
        'rgba(38, 188, 177, 0.5)', // mais claro
        'rgba(24, 168, 153, 0.5)', // mais escuro
        'rgba(20, 150, 135, 0.5)', // mais escuro ainda
        'rgba(28, 140, 125, 0.5)'  // tom intermediário
    ]; 
    
    const blueShades = [
        'rgba(17, 132, 137, 0.5)', // cor base (azul)
        'rgba(23, 145, 150, 0.5)', // mais claro
        'rgba(12, 120, 130, 0.5)', // mais escuro
        'rgba(10, 110, 120, 0.5)', // mais escuro ainda
        'rgba(18, 135, 140, 0.5)'  // tom intermediário
    ];

    for (let i = 0; i < length; i++) {
        if (i % 2 === 0) {
            colors.push(greenShades[i % greenShades.length]);
        } else {
            colors.push(blueShades[i % blueShades.length]); 
        }
    }
    return colors;
}

const title_graphic = document.querySelector('.title-graphic');
const btnMemory = document.querySelector('#btnMemory');
const btnDisk = document.querySelector('#btnDisk');
const btnCPU = document.querySelector('#btnCPU');

let currentChart = null; 
let currentData = memoryData; 

function renderGraphic(dataGraphic) {

    var ctx = document.getElementById('memoryChart');

    if (!ctx)
        return;

    var ctx = ctx.getContext('2d');

    if (currentChart) {
        currentChart.destroy();
    }

    currentChart = new Chart(ctx, {
        type: dataGraphic.chartType,
        data: {
            labels: dataGraphic.datasets.labels,
            datasets: [{
                data: dataGraphic.datasets.data,
                backgroundColor: dataGraphic.datasets.backgroundColor, 
                borderColor: dataGraphic.datasets.backgroundColor, 
                borderWidth: 1
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            },
        }
    });
}

function updateChartType(type) {
    currentData.chartType = type; 
    renderGraphic(currentData);
}

const btnBarChart = document.getElementById('btnBarChart');
const btnLineChart = document.getElementById('btnLineChart');
const btnPieChart = document.getElementById('btnPieChart');

if (btnBarChart) {
    btnBarChart.addEventListener('click', () => {
        updateChartType('bar');

        btnBarChart.style.backgroundColor = '#215341';
        btnLineChart.style.backgroundColor = 'transparent';
        btnPieChart.style.backgroundColor = 'transparent';

    });
}

if (btnLineChart) {
    btnLineChart.addEventListener('click', () => {
        updateChartType('line');

        btnBarChart.style.backgroundColor = 'transparent';
        btnLineChart.style.backgroundColor = '#215341';
        btnPieChart.style.backgroundColor = 'transparent';
    });
}


if (btnPieChart) {
    btnPieChart.addEventListener('click', () => {
        updateChartType('pie');

        btnBarChart.style.backgroundColor = 'transparent';
        btnLineChart.style.backgroundColor = 'transparent';
        btnPieChart.style.backgroundColor = '#215341';
    });
}

if (btnMemory) {
    document.getElementById('btnMemory').addEventListener('click', () => {
        title_graphic.textContent = 'Gráfico Consumo de Memória';
        btnMemory.style.backgroundColor = '#215341';
        btnDisk.style.backgroundColor = 'transparent';
        btnCPU.style.backgroundColor = 'transparent';

        btnBarChart.style.backgroundColor = '#215341';
        btnLineChart.style.backgroundColor = 'transparent';
        btnPieChart.style.backgroundColor = 'transparent';

        memoryData.chartType = 'bar';
        currentData = memoryData; 
        renderGraphic(currentData);
    });
}

if (btnDisk) {
    document.getElementById('btnDisk').addEventListener('click', () => {
        title_graphic.textContent = 'Gráfico Consumo de Disco';
        btnMemory.style.backgroundColor = 'transparent';
        btnDisk.style.backgroundColor = '#215341';
        btnCPU.style.backgroundColor = 'transparent';

        btnBarChart.style.backgroundColor = '#215341';
        btnLineChart.style.backgroundColor = 'transparent';
        btnPieChart.style.backgroundColor = 'transparent';

        diskData.chartType = 'bar';
        currentData = diskData;
        renderGraphic(currentData); 
    });
}

if (btnCPU) {
    document.getElementById('btnCPU').addEventListener('click', () => {
        title_graphic.textContent = 'Gráfico Consumo de CPU em cada núcleo';
        btnMemory.style.backgroundColor = 'transparent';
        btnDisk.style.backgroundColor = 'transparent';
        btnCPU.style.backgroundColor = '#215341';

        btnBarChart.style.backgroundColor = '#215341';
        btnLineChart.style.backgroundColor = 'transparent';
        btnPieChart.style.backgroundColor = 'transparent';

        cpuData.chartType = 'bar';
        currentData = cpuData; 
        renderGraphic(currentData); 
    });
}

renderGraphic(currentData);