async function loadOlympiads() {
    const items = await apiFetch(`/olympiads/?user_id=${USER_ID}`);
    const container = document.getElementById("olympiads-list");
    if (!items.length) {
        container.innerHTML = "<p>Олимпиад пока нет.</p>";
        return;
    }
    const rows = items.map(o => `
        <tr>
            <td>${o.name}</td>
            <td>${o.subject || "—"}</td>
            <td>${o.deadline || "—"}</td>
            <td>${o.status}</td>
            <td>${o.result || "—"}</td>
        </tr>`).join("");
    container.innerHTML = `
        <table>
            <thead><tr><th>Название</th><th>Предмет</th><th>Дедлайн</th><th>Статус</th><th>Результат</th></tr></thead>
            <tbody>${rows}</tbody>
        </table>`;
}

document.getElementById("add-olympiad-btn").addEventListener("click", async () => {
    const name = prompt("Название олимпиады:");
    if (!name) return;
    const subject = prompt("Предмет:");
    const deadline = prompt("Дедлайн (ГГГГ-ММ-ДД):");
    await apiFetch("/olympiads/", {
        method: "POST",
        body: JSON.stringify({ user_id: USER_ID, name, subject, deadline }),
    });
    loadOlympiads();
});
