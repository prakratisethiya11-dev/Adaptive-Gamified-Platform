let currentSolution = null;   // key such as 'lemon', 'soap', 'vinegar', 'tap', 'baking'
let currentType = null;       // 'acid' | 'base' | 'neutral'
let testedCount = 0;
let score = 0;

function selectSolution(key, type) {
    currentSolution = key;
    currentType = type;
    const selInfo = document.getElementById('selectedInfo');
    if(selInfo) i18n.set(selInfo, 'll_current', { name: '@sol_' + key }, true);

    let liquid = document.getElementById('liquidContent');
    if(liquid) {
        liquid.style.height = '60%';
        if(type === 'acid') liquid.style.background = 'rgba(239, 68, 68, 0.5)';
        else if(type === 'base') liquid.style.background = 'rgba(59, 130, 246, 0.5)';
        else liquid.style.background = 'rgba(16, 185, 129, 0.5)';
    }

    const sRes = document.getElementById('stripResult');
    const fMsg = document.getElementById('feedbackMsg');
    if(sRes) i18n.set(sRes, 'll_ready');
    if(fMsg) i18n.set(fMsg, null);
}

function testStrip(stripColor) {
    if(!currentSolution) {
        alert(t('ll_select_first'));
        return;
    }

    let resBox = document.getElementById('stripResult');
    if(!resBox) return;

    // keys: ll_acid_red, ll_acid_blue, ll_base_red, ll_base_blue, ll_neutral_red, ll_neutral_blue
    i18n.set(resBox, 'll_' + currentType + '_' + stripColor, null, true);
}

function classify(guessType) {
    if(!currentSolution) {
        alert(t('ll_test_first'));
        return;
    }
    let fb = document.getElementById('feedbackMsg');
    if(!fb) return;

    if(guessType === currentType) {
        fb.style.color = '#34d399';
        i18n.set(fb, 'll_correct', { name: '@sol_' + currentSolution, type: '@type_' + currentType });
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
        i18n.set(fb, 'll_incorrect');
    }
}
