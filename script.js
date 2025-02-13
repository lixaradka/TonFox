const state = {
    level: 1,
    xp: 0,
    balance: 0,
    miningProgress: 0,
    hunger: 100,
    isMining: false,
    upgrades: {
        miningSpeed: 1,
        hungerRate: 1,
        autoFeed: false
    },
    nextLevelXP: 100
}

// Магазин улучшений
const shopItems = [
    {
        id: 'mining_speed',
        name: 'Ускорение майнинга',
        price: 50,
        effect: () => state.upgrades.miningSpeed *= 1.5
    },
    {
        id: 'hunger_boost',
        name: 'Снижение голода',
        price: 75,
        effect: () => state.upgrades.hungerRate *= 0.7
    },
    {
        id: 'auto_feeder',
        name: 'Автокорм',
        price: 200,
        effect: () => state.upgrades.autoFeed = true
    }
]

// Инициализация звуков (реальные звуки нужно добавить)
const sounds = {
    coin: new Audio('https://assets.mixkit.co/active_storage/sfx/2408/2408-preview.mp3'),
    levelUp: new Audio('https://assets.mixkit.co/active_storage/sfx/2689/2689-preview.mp3'),
    warning: new Audio('https://assets.mixkit.co/active_storage/sfx/2595/2595-preview.mp3')
}

// Расширенные методы
function showNotification(text, type = 'info') {
    const notification = document.createElement('div')
    notification.className = `notification ${type}`
    notification.textContent = text
    document.getElementById('notifications').appendChild(notification)
    
    setTimeout(() => {
        notification.remove()
    }, 3000)
}

function createCoinEffect(x, y) {
    const coin = document.createElement('div')
    coin.className = 'coin-effect'
    coin.innerHTML = '🪙'
    coin.style.left = `${x}px`
    coin.style.top = `${y}px`
    document.body.appendChild(coin)
    
    setTimeout(() => coin.remove(), 1000)
}

function checkLevelUp() {
    if (state.xp >= state.nextLevelXP) {
        state.level++
        state.xp = 0
        state.nextLevelXP *= 1.5
        sounds.levelUp.play()
        showNotification(`Уровень повышен! Текущий уровень: ${state.level}`, 'success')
        updateUI()
    }
}

function buyUpgrade(itemId) {
    const item = shopItems.find(i => i.id === itemId)
    if (state.balance >= item.price) {
        state.balance -= item.price
        item.effect()
        showNotification(`${item.name} куплено!`, 'success')
        sounds.coin.play()
        updateUI()
    } else {
        showNotification('Недостаточно средств!', 'error')
        sounds.warning.play()
    }
}

// Модифицированная логика майнинга
function startMining() {
    if (state.hunger <= 0 || state.isMining) return
    
    state.isMining = true
    elements.mineButton.innerHTML = `
        <i class="fas fa-stop-circle"></i>
        Стоп
    `
    
    state.intervalId = setInterval(() => {
        state.miningProgress += 0.1 * state.upgrades.miningSpeed
        state.hunger -= 0.05 * state.upgrades.hungerRate
        state.xp += 0.01
        
        if (state.miningProgress >= 100) {
            const earned = 0.1 * state.level
            state.balance += earned
            state.miningProgress = 0
            createCoinEffect(elements.petImage.offsetLeft + 90, elements.petImage.offsetTop + 90)
            sounds.coin.play()
        }
        
        if (state.hunger <= 20) {
            elements.hungerProgress.classList.add('critical-hunger')
            if (state.hunger <= 0) {
                state.hunger = 0
                stopMining()
                showNotification('Питомец голоден! Накормите его!', 'error')
                sounds.warning.play()
            }
        } else {
            elements.hungerProgress.classList.remove('critical-hunger')
        }
        
        checkLevelUp()
        updateUI()
    }, 10)
}

// Добавляем обработчик для магазина
document.querySelector('.nav-item[href="#shop"]').addEventListener('click', () => {
    const shopContent = shopItems.map(item => `
        <div class="shop-item">
            <h3>${item.name}</h3>
            <p>Цена: ${item.price} 🪙</p>
            <button onclick="buyUpgrade('${item.id}')">Купить</button>
        </div>
    `).join('')
    
    // Реализуйте отображение магазина в модальном окне
    // или отдельной странице
})

// Инициализация
// Добавьте недостающие элементы в elements
updateUI()