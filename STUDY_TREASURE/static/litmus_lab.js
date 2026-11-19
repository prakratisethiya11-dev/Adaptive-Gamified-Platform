let currentSolution = null;
let currentType = null;
let testedCount = 0;
let score = 0;

function selectSolution(name, type) {
    currentSolution = name;
    currentType = type;
    const selInfo = document.getElementById('selectedInfo');
    if(selInfo) selInfo.innerHTML = `Current: <b style="color: #f472b6;">${name}</b>`;
    
    let liquid = document.getElementById('liquidContent');
    if(liquid) {
        liquid.style.height = '60%';
        if(type === 'acid') liquid.style.background = 'rgba(239, 68, 68, 0.5)';
        else if(type === 'base') liquid.style.background = 'rgba(59, 130, 246, 0.5)';
        else liquid.style.background = 'rgba(16, 185, 129, 0.5)';
    }

    const sRes = document.getElementById('stripResult');
    const fMsg = document.getElementById('feedbackMsg');
    if(sRes) sRes.innerText = "Solution ready! Click a Litmus Strip to test.";
    if(fMsg) fMsg.innerText = "";
}

function testStrip(stripColor) {
    if(!currentSolution) {
        alert("Please select a solution from the shelf first!");
        return;
    }
    
    let resBox = document.getElementById('stripResult');
    if(!resBox) return;

    if(currentType === 'acid') {
        if(stripColor === 'red') resBox.innerHTML = `🔴 Red Litmus remains <b>RED</b>`;
        else resBox.innerHTML = `🔴 Blue Litmus turns <b>RED</b>!`;
    } else if(currentType === 'base') {
        if(stripColor === 'red') resBox.innerHTML = `🔵 Red Litmus turns <b>BLUE</b>!`;
        else resBox.innerHTML = `🔵 Blue Litmus remains <b>BLUE</b>`;
    } else {
        if(stripColor === 'red') resBox.innerHTML = `🟢 Red Litmus remains <b>RED</b>`;
        else resBox.innerHTML = `🟢 Blue Litmus remains <b>BLUE</b>`;
    }
}

function classify(guessType) {
    if(!currentSolution) {
        alert("Please test a solution first!");
        return;
    }
    let fb = document.getElementById('feedbackMsg');
    if(!fb) return;

    if(guessType === currentType) {
        fb.style.color = '#34d399';
        fb.innerText = `✨ Correct! ${currentSolution} is a ${currentType.toUpperCase()}!`;
        score += 20;
        testedCount++;
        
        let earnedCoins = 20;

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
                const cDisp = document.getElementById('coinsDisplay');
                if(cDisp) cDisp.innerText = `🪙 ${data.coins}`;
            } else {
                console.warn("Failed to update database:", data);
            }
        })
        .catch(error => {
            console.error("Error communicating with backend API:", error);
        });

        if(testedCount >= 3) {
            const rewardModal = document.getElementById('rewardModal');
            if(rewardModal) rewardModal.classList.remove('hidden');
        }
    } else {
        fb.style.color = '#f87171';
        fb.innerText = `❌ Incorrect. Look closely at the color change!`;
    }
}