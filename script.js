// Инициализация TON Connect
const tonConnectUI = new TonConnectUI({
  manifestUrl: "https://lixaradka.github.io/TonFox/tonconnect-manifest.json",
});

// Кнопка "Connect Wallet"
document.getElementById('connect-wallet').addEventListener('click', async () => {
  try {
    await tonConnectUI.connectWallet();
    alert('Кошелек подключен!');
  } catch (error) {
    console.error('Ошибка подключения:', error);
  }
});

// Отслеживание изменений статуса кошелька
tonConnectUI.onStatusChange(wallet => {
  if (wallet) {
    const userAddress = wallet.account.address;
    console.log('Адрес кошелька:', userAddress);
    // Сохраните адрес в localStorage или отправьте на бэкенд
  } else {
    console.log('Кошелек отключен.');
  }
});