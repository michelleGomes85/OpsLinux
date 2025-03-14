
const btn_memory = document.getElementById('btnMemory');
const btn_disk = document.getElementById('btnDisk');
const btn_cpu = document.getElementById('btnCPU');

btn_memory.addEventListener('click', function() {
    document.getElementById('cpu-usage-chart').classList.add('hidden');
    document.getElementById('disk-usage-chart').classList.add('hidden');
    document.getElementById('memory-usage-chart').classList.remove('hidden');

    btn_memory.classList.add('select');
    btn_disk.classList.remove('select');
    btn_cpu.classList.remove('select');

});

btn_disk.addEventListener('click', function() {
    document.getElementById('cpu-usage-chart').classList.add('hidden');
    document.getElementById('disk-usage-chart').classList.remove('hidden');
    document.getElementById('memory-usage-chart').classList.add('hidden');

    btn_memory.classList.remove('select');
    btn_disk.classList.add('select');
    btn_cpu.classList.remove('select');
});

btn_cpu.addEventListener('click', function() {
    document.getElementById('cpu-usage-chart').classList.remove('hidden');
    document.getElementById('disk-usage-chart').classList.add('hidden');
    document.getElementById('memory-usage-chart').classList.add('hidden');

    btn_memory.classList.remove('select');
    btn_disk.classList.remove('select');
    btn_cpu.classList.add('select');
});

const btns = document.querySelectorAll(".btn-success");

btns.forEach(btn => {
    btn.addEventListener("click", function () {
        
        document.querySelectorAll(".tip-text").forEach(span => span.classList.add("hidden"));

        btns.forEach(b => b.classList.remove("select"));

        this.classList.add("select");

        this.nextElementSibling.classList.remove("hidden");
    });
});

