let addedComponents = [];
let circuitScore = 0;

function addComponent(name) {
    if(addedComponents.includes(name)) {
        alert(`${name} is already added to the board!`);
        return;
    }
    addedComponents.push(name);
    renderBoard();
}

function renderBoard() {
    let board = document.getElementById('circuitBoard');
    if(addedComponents.length === 0) {
        board.innerHTML = `<p class="board-placeholder">Click components from left panel to assemble your circuit sequence here!</p>`;
        return;
    }
    board.innerHTML = '';
    addedComponents.forEach(comp => {
        let div = document.createElement('div');
        div.className = 'added-comp';
        div.innerText = comp;
        board.appendChild(div);
    });
}

function resetBoard() {
    addedComponents = [];
    renderBoard();
    document.getElementById('bulbVisual').className = 'bulb-off';
    document.getElementById('statusText').innerText = "Circuit Incomplete";
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
        status.innerText = "✨ Circuit Complete! Bulb is Glowing!";
        status.style.color = '#34d399';
        
        let earnedCoins = 25; // Reward coins for completing the circuit
        circuitScore += earnedCoins;
        
        // Update local display immediately
        let coinsElem = document.getElementById('coinsDisplay');
        if(coinsElem) {
            coinsElem.innerText = `🪙 ${circuitScore}`;
        }

        // Send POST request to backend to update Database & Streak securely
        // fetch('/api/complete_game', {
        //     method: 'POST',
        //     headers: {
        //         'Content-Type': 'application/json'
        //     },
        //     body: JSON.stringify({ coins: earnedCoins })
        // })
        // .then(response => response.json())
        // .then(data => {
        //     if (data.status === 'success') {
        //         console.log("Database updated successfully! New Streak:", data.streak, "Total Coins:", data.coins);
        //         if(coinsElem) {
        //             coinsElem.innerText = `🪙 ${data.coins}`; // Sync with true database coin count
        //         }
        //     } else {
        //         console.warn("Failed to update database backend:", data);
        //     }
        // })
        // .catch(error => {
        //     console.error("Error communicating with backend API:", error);
        // });

        // Payload taiyar karein jo backend aur offline sync dono ke liye use hoga
        let gameResult = {
            student_id: window.currentStudentId, // Jinja2 se aane wali ID
            activity_type: "circuit_builder",     // Game ka naam
            score: 100,                           // Agar score ho toh
            points_earned: earnedCoins,           // Jeete hue coins
            streak_count: 1                       // Aapki current streak count (agar ho)
        };

        // Yahan aap apna naya offline sync function call kar sakte hain 
        // (Jo aapne offline_sync.js me banaya hai)
        if (typeof handleGameCompletion === 'function') {
            handleGameCompletion(gameResult);
        } else {
            // Fallback: Agar offline_sync.js load nahi hai toh direct fetch chalega
            fetch('/api/sync_offline_progress', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(gameResult)
            })
            .then(response => response.json())
            .then(data => {
                console.log("Progress updated:", data);
                let coinsElem = document.getElementById('coinsDisplay');
                if(coinsElem && data.coins) {
                    coinsElem.innerText = `🪙 ${data.coins}`;
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
        }

        // Show reward modal after a short delay
        setTimeout(() => {
            let modal = document.getElementById('rewardModal');
            if(modal) {
                modal.classList.remove('hidden');
            }
        }, 600);

    } else {
        bulb.className = 'bulb-off';
        status.innerText = "❌ Missing Components! Add Battery, Switch, Bulb & Wires.";
        status.style.color = '#f87171';
    }
}