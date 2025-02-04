window.onload = function () {
    
    setTimeout(function() {

        update_graphic_func();
        
        const TIME_LIMIT_MINUTES = 2; 
        const SECONDS_IN_MINUTE = 60; 
        const totalSecondsInTimeLimit = TIME_LIMIT_MINUTES * SECONDS_IN_MINUTE;

        // Obtém o uptime da página
        let update = document.getElementById('uptime-display');

        if (!update)
            return;

        var uptimeSeconds = parseInt(update.getAttribute('data-uptime')) || 0;
        let update_graphic = 0;

        function update_graphic_func() {
            fetch("http://127.0.0.1:5000/api/system-info/")
                .then(response => response.json())
                .then(data => {
                    
                    if (typeof Plotly === "undefined") {
                        return;
                    }
        
                    // Cores personalizadas
                    const colors = {
                        blue: 'rgb(163, 213, 255)',
                        green: '#037a76',
                        fundo: 'rgb(5, 20, 40)', // Cor de fundo escura
                        texto: '#ffffff'  // Cor do texto branco
                    };
        
                    // Atualiza gráfico de CPU (barras horizontais)
                    const cpuUsage = data.cpu_usage_per_core || [];
                    const cpuGraph = {
                        data: [{
                            type: 'bar',
                            x: cpuUsage,
                            y: cpuUsage.map((_, i) => `Núcleo ${i + 1}`),
                            orientation: 'h', // Barras horizontais
                            marker: { color: colors.blue } // Cor das barras
                        }],
                        layout: {
                            title: {
                                text: "Uso de CPU por Núcleo",
                                x: 0.5, // Centraliza o título
                                font: { size: 18, color: colors.texto } // Cor do título
                            },
                            xaxis: {
                                title: "Uso (%)",
                                titlefont: { color: colors.texto },
                                tickfont: { color: colors.texto },
                                gridcolor: '#444', // Cor da grade
                                zerolinecolor: '#444' // Cor da linha zero
                            },
                            yaxis: {
                                title: "Núcleo",
                                titlefont: { color: colors.texto },
                                tickfont: { color: colors.texto },
                                gridcolor: '#444', // Cor da grade
                                zerolinecolor: '#444' // Cor da linha zero
                            },
                            paper_bgcolor: colors.fundo, // Fundo escuro
                            plot_bgcolor: colors.fundo,  // Área do gráfico escura
                            font: { color: colors.texto }, // Cor do texto geral
                            margin: { l: 120, r: 40, t: 80, b: 80 } // Margens para melhorar o layout
                        }
                    };
                    Plotly.react('cpu-graph', cpuGraph.data, cpuGraph.layout);
        
                    // Atualiza gráfico de memória (gráfico de rosca)
                    const memoryUsage = data.memory_usage || {};
                    const memoryGraph = {
                        data: [{
                            type: 'pie',
                            labels: ['Usado', 'Livre'],
                            values: [memoryUsage.used_percent || 0, memoryUsage.free_percent || 0],
                            marker: { colors: [colors.green, colors.blue] }, // Cores do gráfico
                            hole: 0.4 // Transforma em gráfico de rosca
                        }],
                        layout: {
                            title: {
                                text: "Uso de Memória",
                                x: 0.5, // Centraliza o título
                                font: { size: 18, color: colors.texto } // Cor do título
                            },
                            paper_bgcolor: colors.fundo, // Fundo escuro
                            plot_bgcolor: colors.fundo,  // Área do gráfico escura
                            font: { color: colors.texto }, // Cor do texto geral
                            showlegend: true, // Mostra a legenda
                            legend: {
                                x: 1.1, // Posiciona a legenda à direita
                                y: 0.5,
                                font: { color: colors.texto } // Cor do texto da legenda
                            }
                        }
                    };
                    Plotly.react('memory-graph', memoryGraph.data, memoryGraph.layout);
        
                    // Atualiza gráfico de disco (barras empilhadas)
                    const diskUsage = data.disk_usage || {};
                    const diskGraph = {
                        data: [
                            {
                                type: 'bar',
                                x: ['Disco'],
                                y: [diskUsage.used_percent || 0],
                                name: 'Usado',
                                marker: { color: colors.green } // Cor da barra "Usado"
                            },
                            {
                                type: 'bar',
                                x: ['Disco'],
                                y: [diskUsage.free_percent || 0],
                                name: 'Livre',
                                marker: { color: colors.blue } // Cor da barra "Livre"
                            }
                        ],
                        layout: {
                            title: {
                                text: "Uso de Disco",
                                x: 0.5, // Centraliza o título
                                font: { size: 18, color: colors.texto } // Cor do título
                            },
                            xaxis: {
                                title: "Disco",
                                titlefont: { color: colors.texto },
                                tickfont: { color: colors.texto },
                                gridcolor: '#444', // Cor da grade
                                zerolinecolor: '#444' // Cor da linha zero
                            },
                            yaxis: {
                                title: "Uso (%)",
                                titlefont: { color: colors.texto },
                                tickfont: { color: colors.texto },
                                gridcolor: '#444', // Cor da grade
                                zerolinecolor: '#444' // Cor da linha zero
                            },
                            paper_bgcolor: colors.fundo, // Fundo escuro
                            plot_bgcolor: colors.fundo,  // Área do gráfico escura
                            font: { color: colors.texto }, // Cor do texto geral
                            barmode: 'stack', // Barras empilhadas
                            showlegend: true, // Mostra a legenda
                            legend: {
                                x: 1.1, // Posiciona a legenda à direita
                                y: 0.5,
                                font: { color: colors.texto } // Cor do texto da legenda
                            },
                            margin: { l: 80, r: 80, t: 80, b: 80 } // Margens para melhorar o layout
                        }
                    };
                    Plotly.react('disk-graph', diskGraph.data, diskGraph.layout);
                })
                .catch(error => console.error('Erro ao buscar dados:', error));
        }

        function formatTime(seconds) {
            let hours = Math.floor(seconds / 3600);
            let minutes = Math.floor((seconds % 3600) / SECONDS_IN_MINUTE);
            let secs = seconds % SECONDS_IN_MINUTE;
            return (
                String(hours).padStart(2, '0') + ':' +
                String(minutes).padStart(2, '0') + ':' +
                String(secs).padStart(2, '0')
            );
        }

        function updateUptime() {
            uptimeSeconds++;
            localStorage.setItem("uptimeSeconds", uptimeSeconds);
            var display = document.getElementById('uptime-display');
            if (display) {
                display.innerText = formatTime(uptimeSeconds);
            }
        }

        function updateChart() {
            update_graphic++;
            
            const elapsedInCurrentCycle = update_graphic % totalSecondsInTimeLimit;
            const percentage = (elapsedInCurrentCycle / totalSecondsInTimeLimit) * 100;
            const adjustedPercentage = percentage * 2;

            if (adjustedPercentage == 50) {
                update_graphic = 0;
                update_graphic_func();
            }

            document.getElementById("donut").style.background = `conic-gradient(
                #037a76 0% ${adjustedPercentage}%, 
                #A3D5FF ${adjustedPercentage}% 100%
            )`;

            setTimeout(updateChart, 1000); 
        }

        setInterval(updateUptime, 1000); 
        updateChart(); 

        const toggle_icon = document.getElementById("ip-toggle-icon");
        const ipDisplay_ipv4 = document.getElementById("ip-display-ipv4");
        const ipDisplay_ipv6 = document.getElementById("ip-display-ipv6");
        const ipText = document.getElementById('ip-display-ip-text');

        if (toggle_icon) {

            let isIPv4Visible = true; 

            toggle_icon.addEventListener("click", function() {
                if (isIPv4Visible) {
                    // Alternar para IPv6
                    ipText.textContent = "IPV6";
                    ipDisplay_ipv6.style.display = 'block';
                    ipDisplay_ipv4.style.display = 'none';
                } else {
                    // Alternar para IPv4
                    ipText.textContent = "IPV4";
                    ipDisplay_ipv4.style.display = 'block';
                    ipDisplay_ipv6.style.display = 'none';
                }

                isIPv4Visible = !isIPv4Visible;
            });
        }

        const modal = document.getElementById("modal-question");
        const btn = document.getElementById("open-modal-btn");
        const closeModal = document.querySelector(".modal-close");

        if (btn) {
            btn.addEventListener("click", function () {
                document.getElementById('question').focus();
                modal.style.display = "block"; 
            });
        }

        if (closeModal) {
            closeModal.addEventListener("click", function () {
                modal.style.display = "none";  
                document.getElementById('question').value = '';
            });
        }

        window.addEventListener("click", function (event) {
            if (event.target === modal) {
                modal.style.display = "none";
                document.getElementById('question').value = '';
            }
        });
    
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
            
                    console.log(data); 
            
                } catch (error) {
                    console.error('Erro:', error);
                }
            };
        }

        const isSpeechRecognitionSupported = 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;

        if (!isSpeechRecognitionSupported) {
            alert('Seu navegador não suporte reconhecimento de voz. Use Chrome ou outro navegador moderno');
        } else {

            // Criando uma instância do objeto de reconhecimento de voz
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'pt-BR'; 
            recognition.interimResults = false;

            const textarea = document.getElementById('question');
            const microphone = document.getElementById('microphone');
            const microphoneContainer = document.getElementById('microphone-container');

            // Variable to track if the microphone is active
            let isListening = false;

            // Função começar a escutar
            const startListening = () => {
                recognition.start(); 
                textarea.placeholder = "Escutando ...";
                textarea.disabled = true; 
                isListening = true;

                const pulseEffect = document.createElement('div');
                pulseEffect.classList.add('pulsating-effect');
                microphoneContainer.appendChild(pulseEffect);
            };

            // Função para de escutar
            const stopListening = () => {
                recognition.stop(); 
                textarea.placeholder = "Faça uma pergunta sobre o sistema ...";
                textarea.disabled = false; 
                isListening = false;

                const pulseEffect = microphoneContainer.querySelector('.pulsating-effect');
                if (pulseEffect)
                    pulseEffect.remove();
            };

            if (microphone) {
                microphone.addEventListener('click', () => {
                    if (isListening)
                        stopListening();
                    else
                        startListening();
                });
            
                // Transcrever o resultado no textArea
                recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript;
                    textarea.value = transcript;
                    stopListening(); 
                };
            
                // Se ocorre um erro ao escutar
                recognition.onerror = (event) => {
                    textarea.placeholder = "Erro ao escutar tente novamente";
                    stopListening(); 
                };
            
                // Quando o reconhecimento de voz terminar
                recognition.onend = () => {
                    stopListening();
                };
            }

        }

    }, 1500); 
};

