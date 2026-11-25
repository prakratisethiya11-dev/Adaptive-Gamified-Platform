let addedComponents = [];
let circuitScore = 0;

function addComponent(name) {
    if(addedComponents.includes(name)) {
        alert(t('cb_already_added', { name: '@cb_name_' + name.toLowerCase() }));
        return;
    }
    addedComponents.push(name);
    renderBoard();
}

function renderBoard() {
    let board = document.getElementById('circuitBoard');
    if(addedComponents.length === 0) {
        board.innerHTML = '<p class="board-placeholder" data-i18n="cb_placeholder"></p>';
        i18n.apply(board);
        return;
    }
    board.innerHTML = '';
    addedComponents.forEach(comp => {
        let div = document.createElement('div');
        div.className = 'added-comp';
        i18n.set(div, 'cb_name_' + comp.toLowerCase());
        board.appendChild(div);
    });
}

function resetBoard() {
    addedComponents = [];
    renderBoard();
    document.getElementById('bulbVisual').className = 'bulb-off';
    i18n.set(document.getElementById('statusText'), 'cb_incomplete');
    document.getElementById('statusText').style.color = '#f87171';
}

function testCircuit() {
    let hasBattery = addedComponents.includes('Battery');
    let hasSwitch = addedComponents.includes('Switch');
    let hasBulb = addedComponents.includes('Bulb');
    let hasWire = addedComponents.includes('Wire');

    let bulb = document.getElementById('bulbVisual');
    let status = document.getElementById('statusText');

    if(hasBattery && hasSwitch && hasBulb && hasWire) {
        bulb.className = 'bulb-on';
        i18n.set(status, 'cb_complete');
        status.style.color = '#34d399';
        
        let earnedCoins = 25; // Reward coins for completing the circuit
        circuitScore += earnedCoins;
        
        // Update local display immediately
        let coinsElem = document.getElementById('coinsDisplay');
        if(coinsElem) {
            coinsElem.innerText = `🪙 ${circuitScore}`;
        }

        // Send POST request to backend to update Database & Streak securely
        fetch('/api/complete_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ coins: earnedCoins })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log("Database updated successfully! New Streak:", data.streak, "Total Coins:", data.coins);
                if(coinsElem) {
                    coinsElem.innerText = `🪙 ${data.coins}`; // Sync with true database coin count
                }
            } else {
                console.warn("Failed to update database backend:", data);
            }
        })
        .catch(error => {
            console.error("Error communicating with backend API:", error);
        });

        // Show reward modal after a short delay
        setTimeout(() => {
            let modal = document.getElementById('rewardModal');
            if(modal) {
                modal.classList.remove('hidden');
            }
        }, 600);

    } else {
        bulb.className = 'bulb-off';
        i18n.set(status, 'cb_missing');
        status.style.color = '#f87171';
    }
}