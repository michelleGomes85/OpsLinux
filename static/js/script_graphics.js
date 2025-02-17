// Constantes para valores importantes
const CHART_WIDTH = 650;
const CHART_HEIGHT = 500;

// Definição de cores para os gráficos
const BLUE_COLORS = {
    MEMORY: ['rgb(17 46 81)', 'rgb(46 113 191)'], 
    
    CPU: {
        HIGH: 'rgb(17 46 81)',
        LOW: 'rgb(46 113 191)'  
    },

    DISK: ['rgb(17 46 81)', 'rgb(46 113 191)'],  // Cor para Disco Usado e Livre (mais saturada)
};

// Função para atualizar o gráfico de uso de CPU
function updateCpuUsageChart(cpuUsage) {

    const colors = cpuUsage.map((usage, index) => `Core ${index + 1}`);
    const totalCpuUsage = cpuUsage.reduce((acc, usage) => acc + usage, 0);
    const totalCpuPercentage = (totalCpuUsage / (cpuUsage.length * 100)) * 100;

    // Encontrando o valor máximo de CPU
    const maxUsage = Math.max(...cpuUsage);

    // As cores variam de acordo com o valor da CPU
    const cpuColors = cpuUsage.map(usage => {
        return usage === maxUsage ? BLUE_COLORS.CPU.HIGH : BLUE_COLORS.CPU.LOW; // Cores iguais ao máximo recebem a cor escura
    });

    const pizzaData = [{
        values: cpuUsage,
        labels: colors,
        type: 'pie',
        hoverinfo: 'label+percent',
        textinfo: 'value+percent',
        textposition: 'inside',
        marker: {
            colors: cpuColors
        },
        textfont: { color: 'white' }
    }];
    
    const barData = [{
        x: ['Total CPU Usage'],
        y: [totalCpuPercentage],
        type: 'bar',
        marker: {
            color: BLUE_COLORS.CPU.HIGH
        },
        text: [`${totalCpuPercentage.toFixed(2)}%`],
        textposition: 'auto',
        textfont: { color: 'white' },
        hoverinfo: 'text',
    }];
    
    const pizzaLayout = {
        title: 'Uso da CPU por Core',
        height: CHART_HEIGHT,
        width: CHART_WIDTH,
        showlegend: true,
        paper_bgcolor: 'rgb(5, 20, 40)',  
        plot_bgcolor: 'rgb(5, 20, 40)',   
        legend: {
            x: 0.8, 
            y: 0.5, 
            traceorder: 'normal',
            orientation: 'v',
            font: { color: '#FFFFFF' }  
        },
        titlefont: { color: 'white' },
        xaxis: {
            tickfont: { color: 'white' },
            title: { text: 'Cores', font: { color: 'white' } }
        },
        yaxis: {
            tickfont: { color: 'white' },
            titlefont: { color: 'white' },
            title: { text: 'Uso (%)', font: { color: 'white' } }
        }
    };
    
    const barLayout = {
        title: 'Uso Total da CPU (Percentual)',
        height: CHART_HEIGHT,
        width: CHART_WIDTH,
        yaxis: {
            title: 'Percentual',
            range: [0, 100],
            tickfont: { color: 'white' },
            titlefont: { color: 'white' }
        },
        xaxis: {
            title: 'Uso Total',
            tickfont: { color: 'white' },
            titlefont: { color: 'white' }
        },
        paper_bgcolor: 'rgb(5, 20, 40)',
        plot_bgcolor: 'rgb(5, 20, 40)',   
        legend: {
            x: 0.8,
            y: 1,
            traceorder: 'normal',
            orientation: 'v',
            font: { color: '#FFFFFF' }
        },
        titlefont: { color: 'white' }
    };

    Plotly.newPlot('cpu-usage-pie-chart', pizzaData, pizzaLayout);
    Plotly.newPlot('cpu-usage-bar-chart', barData, barLayout);
}

// Função para atualizar o gráfico de uso de disco
function updateDiskUsageChart(diskUsage) {
    const labelsPercent = ['Usado (%)', 'Livre (%)'];

    const pieValues = [diskUsage.used_percent, diskUsage.free_percent];
    const pieData = [{
        values: pieValues,
        labels: labelsPercent,
        type: 'pie',
        hoverinfo: 'label+percent',
        textinfo: 'value+percent',
        textposition: 'inside',
        marker: {
            colors: BLUE_COLORS.DISK
        },
        textfont: { color: 'white' }
    }];
    
    const barData = [
        {
            x: ['Usado (GB)'],
            y: [diskUsage.used_gb],
            type: 'bar',
            name: 'Usado (GB)',
            marker: {
                color: BLUE_COLORS.DISK[0]
            },
            text: [`${diskUsage.used_gb.toFixed(2)} GB`],
            textposition: 'auto',
            textfont: { color: 'white' },
            hoverinfo: 'text',
        },
        {
            x: ['Livre (GB)'],
            y: [diskUsage.free_gb],
            type: 'bar',
            name: 'Livre (GB)',
            marker: {
                color: BLUE_COLORS.DISK[1]
            },
            text: [`${diskUsage.free_gb.toFixed(2)} GB`],
            textposition: 'auto',
            textfont: { color: 'white' },
            hoverinfo: 'text',
        }
    ];
    
    const pieLayout = {
        title: 'Uso do Disco (Percentual)',
        height: CHART_HEIGHT,
        width: CHART_WIDTH,
        showlegend: true,
        paper_bgcolor: 'rgb(5, 20, 40)',  
        plot_bgcolor: 'rgb(5, 20, 40)',   
        legend: {
            x: 0.8, 
            y: 0.5, 
            traceorder: 'normal',
            orientation: 'v',
            font: { color: '#FFFFFF' }
        },
        titlefont: { color: 'white' },
        xaxis: {
            tickfont: { color: 'white' },
            title: { text: 'Espaço', font: { color: 'white' } }
        },
        yaxis: {
            tickfont: { color: 'white' },
            titlefont: { color: 'white' },
            title: { text: 'Espaço (%)', font: { color: 'white' } }
        }
    };
    
    const barLayout = {
        title: 'Uso do Disco (GB)',
        height: CHART_HEIGHT,
        width: CHART_WIDTH,
        xaxis: {
            title: 'Espaço',
            tickvals: [0, 1],
            ticktext: ['Usado', 'Livre'],
            tickfont: { color: 'white' },
            titlefont: { color: 'white' }
        },
        yaxis: {
            title: 'Espaço em GB',
            range: [0, diskUsage.total_gb],
            tickfont: { color: 'white' },
            titlefont: { color: 'white' }
        },
        showlegend: true,
        paper_bgcolor: 'rgb(5, 20, 40)',
        plot_bgcolor: 'rgb(5, 20, 40)',   
        legend: {
            x: 0.8,
            y: 1,
            traceorder: 'normal',
            orientation: 'v',
            font: { color: '#FFFFFF' }
        },
        titlefont: { color: 'white' }
    };

    Plotly.newPlot('disk-usage-pie-chart', pieData, pieLayout);
    Plotly.newPlot('disk-usage-bar-chart', barData, barLayout);
}

// Função para atualizar o gráfico de uso de memória
function updateMemoryUsageChart(memoryUsage) {
    const labelsPercent = ['Usado (%)', 'Livre (%)'];

    const pieValues = [memoryUsage.used_percent, memoryUsage.free_percent];
    const pieData = [{
        values: pieValues,
        labels: labelsPercent,
        type: 'pie',
        hoverinfo: 'label+percent',
        textinfo: 'value+percent',
        textposition: 'inside',
        marker: {
            colors: BLUE_COLORS.MEMORY
        },
        textfont: { color: 'white' }
    }];
    
    const barData = [
        {
            x: ['Usado (GB)'],
            y: [memoryUsage.used_gb],
            type: 'bar',
            name: 'Usado (GB)',
            marker: {
                color: BLUE_COLORS.MEMORY[0]
            },
            text: [`${memoryUsage.used_gb.toFixed(2)} GB`],
            textposition: 'auto',
            textfont: { color: 'white' },
            hoverinfo: 'text',
        },
        {
            x: ['Livre (GB)'],
            y: [memoryUsage.free_gb],
            type: 'bar',
            name: 'Livre (GB)',
            marker: {
                color: BLUE_COLORS.MEMORY[1]
            },
            text: [`${memoryUsage.free_gb.toFixed(2)} GB`],
            textposition: 'auto',
            textfont: { color: 'white' },
            hoverinfo: 'text',
        }
    ];
    
    const pieLayout = {
        title: 'Uso da Memória (Percentual)',
        height: CHART_HEIGHT,
        width: CHART_WIDTH,
        showlegend: true,
        paper_bgcolor: 'rgb(5, 20, 40)',  
        plot_bgcolor: 'rgb(5, 20, 40)',   
        legend: {
            x: 0.8, 
            y: 0.5, 
            traceorder: 'normal',
            orientation: 'v',
            font: { color: '#FFFFFF' }
        },
        titlefont: { color: 'white' },
        xaxis: {
            tickfont: { color: 'white' },
            title: { text: 'Espaço', font: { color: 'white' } }
        },
        yaxis: {
            tickfont: { color: 'white' },
            titlefont: { color: 'white' },
            title: { text: 'Espaço (%)', font: { color: 'white' } }
        }
    };
    
    const barLayout = {
        title: 'Uso da Memória (GB)',
        height: CHART_HEIGHT,
        width: CHART_WIDTH,
        xaxis: {
            title: 'Espaço',
            tickvals: [0, 1],
            ticktext: ['Usado', 'Livre'],
            tickfont: { color: 'white' },
            titlefont: { color: 'white' }
        },
        yaxis: {
            title: 'Espaço em GB',
            range: [0, memoryUsage.total_gb],
            tickfont: { color: 'white' },
            titlefont: { color: 'white' }
        },
        showlegend: true,
        paper_bgcolor: 'rgb(5, 20, 40)',
        plot_bgcolor: 'rgb(5, 20, 40)',   
        legend: {
            x: 0.8,
            y: 1,
            traceorder: 'normal',
            orientation: 'v',
            font: { color: '#FFFFFF' }
        },
        titlefont: { color: 'white' }
    };

    Plotly.newPlot('memory-usage-pie-chart', pieData, pieLayout);
    Plotly.newPlot('memory-usage-bar-chart', barData, barLayout);
}

// Exemplo de uso
const cpuUsage = [50, 70, 60];
const diskUsage = { used_percent: 65, free_percent: 35, used_gb: 200, free_gb: 1000, total_gb: 1200 };
const memoryUsage = { used_percent: 70, free_percent: 30, used_gb: 8, free_gb: 2, total_gb: 10 };

updateCpuUsageChart(cpuUsage);
updateDiskUsageChart(diskUsage);
updateMemoryUsageChart(memoryUsage);
