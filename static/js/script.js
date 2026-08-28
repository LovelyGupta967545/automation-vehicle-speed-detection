async function refreshStats() {
    const res = await fetch("/stats");
    const data = await res.json();
    document.getElementById("in-count").textContent = data.in_count;
    document.getElementById("out-count").textContent = data.out_count;
}
setInterval(refreshStats, 1000);
refreshStats();