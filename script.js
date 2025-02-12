const tonConnectUI = new TonConnectUI({
    manifestUrl: "https://ваш-сайт/tonconnect-manifest.json",
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
  
  // Пример отправки TON
  async function sendTon(toAddress, amount) {
    const transaction = {
      messages: [
        {
          address: toAddress,
          amount: String(amount * 1e9), // TON в наноТОН
        },
      ],
      validUntil: Math.floor(Date.now() / 1000) + 300, // 5 минут
    };
  
    try {
      await tonConnectUI.sendTransaction(transaction);
      alert('Транзакция отправлена!');
    } catch (error) {
      console.error('Ошибка отправки:', error);
    }
  }