window.onload = function () {
    const TIME_LIMIT_MINUTES = 1;
    const SECONDS_IN_MINUTE = 60;
    const totalSecondsInTimeLimit = TIME_LIMIT_MINUTES * SECONDS_IN_MINUTE;

    let uptimeSeconds = 0;
    let update_graphic = 0;

    // Variável para armazenar os dados mais recentes
    let latestData = null; 

    // Seleciona elementos do DOM
    const update = document.getElementById('uptime-display');
    const ipDisplay_ipv4 = document.getElementById("ip-display-ipv4");
    const ipDisplay_ipv6 = document.getElementById("ip-display-ipv6");
    const donut_time = document.getElementById("donut");
    const toggle_icon_ip = document.getElementById("ip-toggle-icon");
    const ipText = document.getElementById('ip-display-ip-text');

    if (!update || !ipDisplay_ipv4 || !ipDisplay_ipv6 || !donut_time) return;

    function formatTime(seconds) {
        let hours = Math.floor(seconds / 3600);
        let minutes = Math.floor((seconds % 3600) / SECONDS_IN_MINUTE);
        let secs = Math.floor(seconds % SECONDS_IN_MINUTE);
        return `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }

    function update_data_initial() {

        fetch("/system-info/")

            .then(response => response.json())
            .then(data => {
                
                uptimeSeconds = Math.floor(data.uptime.seconds);
                ipDisplay_ipv4.innerText = data.ip_address.ipv4;
                ipDisplay_ipv6.innerText = data.ip_address.ipv6;

                // Armazena os dados mais recentes
                latestData = data;

                // Atualiza os gráficos com os novos dados
                updateCharts(data);
            })

            .catch(error => console.error('Erro ao buscar dados:', error));
    }

    function updateUptimeLocal() {
        uptimeSeconds++;
        update.innerText = formatTime(uptimeSeconds);
        updateChartTimeUpdate();
    }

    function updateChartTimeUpdate() {
        update_graphic++;
        const elapsedInCurrentCycle = update_graphic % totalSecondsInTimeLimit;
        const percentage = (elapsedInCurrentCycle / totalSecondsInTimeLimit) * 100;
        const adjustedPercentage = percentage / 2;

        if (update_graphic >= totalSecondsInTimeLimit) {
            update_graphic = 0;
            update_data_initial();
        }

        donut_time.style.background = `conic-gradient(
            #367cdd 0% ${adjustedPercentage}%,
            #A3D5FF ${adjustedPercentage}% 100%
        )`;
    }

    function updateCharts(data) {

        updateCpuUsageChart(data.cpu_usage_per_core);
        updateDiskUsageChart(data.disk_usage);
        updateMemoryUsageChart(data.memory_usage);

    }

    update_data_initial();
    setInterval(updateUptimeLocal, 1000);
    setInterval(update_data_initial, totalSecondsInTimeLimit * 1000);

    if (toggle_icon_ip) {
        let isIPv4Visible = true;

        toggle_icon_ip.addEventListener("click", function() {
            isIPv4Visible = !isIPv4Visible;
            ipText.textContent = isIPv4Visible ? "IPV4" : "IPV6";
            ipDisplay_ipv4.style.display = isIPv4Visible ? 'block' : 'none';
            ipDisplay_ipv6.style.display = isIPv4Visible ? 'none' : 'block';
        });
    }
};