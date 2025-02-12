document.getElementById('connectWallet').addEventListener('click', async () => {
    if (window.Telegram && Telegram.WebApp) {
        try {
            Telegram.WebApp.ready();
            Telegram.WebApp.expand();

            const invoice = {
                title: "Пополнение баланса",
                description: "Пополните ваш баланс на 10 TON",
                currency: "TON",
                prices: [
                    { label: "10 TON", amount: "1000000000" }
                ],
                payload: JSON.stringify({ userId: 12345 })
            };

            Telegram.WebApp.openInvoice(invoice, (status) => {
                if (status === 'paid') {
                    alert("Оплата прошла успешно!");
                } else {
                    alert("Оплата отменена.");
                }
            });
        } catch (error) {
            console.error("Ошибка при подключении кошелька:", error);
        }
    } else {
        alert("Telegram WebApp не доступен. Откройте приложение через Telegram.");
    }
    document.getElementById('connectWallet').addEventListener('click', function() {
        alert("Кнопка нажата!");
    });
});