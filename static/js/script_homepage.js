document.addEventListener('DOMContentLoaded', function() {

    var modal = document.querySelectorAll('.modal');

    M.Modal.init(modal, {
        opacity: 0.8,
        inDuration: 300,
        outDuration: 200,
        startingTop: '10%',
        endingTop: '10%',
        onOpenEnd: function() {
            var textarea = document.getElementById('question');
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
            var question = this.getAttribute('data-question');
            document.getElementById('question').value = question;
        });
    });

    let clearQuestion = document.getElementById('clear-question');
    
    if (clearQuestion) {
        clearQuestion.addEventListener('click', function() {
            document.getElementById('question').value = '';
        });
    }

    let sendQuestion = document.getElementById('send-question');

    if (sendQuestion) {
        
        sendQuestion.onclick = async function () {

            const question = document.getElementById('question').value;
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
    
                alert("Pergunta enviada com sucesso: " + question);
    
                M.Modal.getInstance(document.getElementById('modal-question')).close();
        
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
        data: [], 
        backgroundColor: generateColors(2),
        labels: ['Usada', 'Livre']
    }
};

const diskData = {
    title: 'Consumo de Disco', 
    chartType: 'bar',     

    datasets: {
        label: 'Disco',
        data: [],
        backgroundColor: generateColors(2),
        labels: ['Usada', 'Livre']
    }
};

const cpuData = {
    title: 'Consumo de CPU',
    chartType: 'bar',       
    
    datasets: {
        label: 'CPU',
        data: [], 
        backgroundColor: [],
        labels: [], 
    }
};

const card_ip = document.querySelector('.card-ip');
const card_time = document.querySelector('.card-time');
const graphics = document.querySelector('.graphics');
const card_question = document.querySelector('.card-question');

// Variável para controlar o carregamento inicial
let isInitialLoad = true; 

function formatUptime(seconds) {

    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);

    // Adiciona um zero à esquerda se necessário
    const time = (num) => (num < 10 ? `0${num}` : num);

    return `${time(hours)}:${time(minutes)}:${time(secs)}`;
}

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
    const ip_system = document.getElementById('ip-system');
    const time_system = document.getElementById('time-system');

    if (systemInfo) {

        // Atualiza o endereço IP
        ip_system.textContent = systemInfo.ip_address;

        if (isInitialLoad) {
            card_ip.classList.remove('hidden');
            card_ip.classList.add('visible');
        }

        // Inicia a contagem do tempo de atividade
        startUptimeCounter(systemInfo.uptime.seconds, time_system);

        if (isInitialLoad) {
            card_time.classList.remove('hidden');
            card_time.classList.add('visible');
        }

        if (isInitialLoad) {
            card_question.classList.remove('hidden');
            card_question.classList.add('visible');
        }

        // Atualiza os dados de memória
        memoryData.datasets.data = [
            systemInfo.memory_usage.used_percent,
            systemInfo.memory_usage.free_percent
        ];

        // Atualiza os dados de disco
        diskData.datasets.data = [
            systemInfo.disk_usage.used_percent,
            systemInfo.disk_usage.free_percent
        ];

        // Atualiza os dados de CPU
        cpuData.datasets.data = systemInfo.cpu_usage_per_core;
        cpuData.datasets.labels = systemInfo.cpu_usage_per_core.map((_, index) => `CPU ${index + 1}`);
        cpuData.datasets.backgroundColor = generateColors(systemInfo.cpu_usage_per_core.length); 

        // Re-renderiza o gráfico atual
        renderGraphic(currentData);

        if (isInitialLoad) {
            graphics.classList.remove('hidden');
            graphics.classList.add('visible');
        }
    }
}

function startUptimeCounter(initialSeconds, element) {
    
    let seconds = initialSeconds;

    element.textContent = formatUptime(seconds);
    const interval = setInterval(() => {
        seconds += 1; 
        element.textContent = formatUptime(seconds);
    }, 1000);

    window.addEventListener('beforeunload', () => {
        clearInterval(interval);
    });
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
const btnLineChart = document.getElementById('btnLineChart');
const btnPieChart = document.getElementById('btnPieChart');

if (btnBarChart) {
    btnBarChart.addEventListener('click', () => {
        updateChartType('bar');

        btnBarChart.style.backgroundColor = '#215341';
        btnLineChart.style.backgroundColor = 'transparent';
        btnPieChart.style.backgroundColor = 'transparent';


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

        btnBarChart.style.backgroundColor = '#215341';
        btnLineChart.style.backgroundColor = 'transparent';
        btnPieChart.style.backgroundColor = 'transparent';

        cpuData.chartType = 'bar';
        currentData = cpuData; 
        renderGraphic(currentData); 
    });
}