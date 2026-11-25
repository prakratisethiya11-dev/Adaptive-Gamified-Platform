// Question Templates Generator
const QuestionBank = {
    templates: [
        {
            shape: 'rectangle',
            generate: () => {
                const l = Math.floor(Math.random() * 8) + 4;
                const b = Math.floor(Math.random() * 5) + 2;
                return {
                    textKey: 'gq_q_rect', textVars: { l, b },
                    shapeParams: { shape: 'rectangle', l, b },
                    correctVal: 2 * (l + b),
                    correctUnit: 'm',
                    hintKey: 'gq_hint_rect', hintVars: { l, b }
                };
            }
        },
        {
            shape: 'square',
            generate: () => {
                const s = Math.floor(Math.random() * 8) + 3;
                return {
                    textKey: 'gq_q_square', textVars: { s },
                    shapeParams: { shape: 'square', s },
                    correctVal: s * s,
                    correctUnit: 'cm²',
                    hintKey: 'gq_hint_square', hintVars: { s }
                };
            }
        },
        {
            shape: 'circle',
            generate: () => {
                const r = (Math.floor(Math.random() * 5) + 1) * 7;
                return {
                    textKey: 'gq_q_circle', textVars: { r },
                    shapeParams: { shape: 'circle', r },
                    correctVal: Math.round(2 * (22/7) * r),
                    correctUnit: 'm',
                    hintKey: 'gq_hint_circle', hintVars: { r }
                };
            }
        },
        {
            shape: 'cuboid',
            generate: () => {
                const l = Math.floor(Math.random() * 4) + 2;
                const b = Math.floor(Math.random() * 3) + 2;
                const h = Math.floor(Math.random() * 3) + 2;
                return {
                    textKey: 'gq_q_cuboid', textVars: { l, b, h },
                    shapeParams: { shape: 'cuboid', l, b, h },
                    correctVal: l * b * h,
                    correctUnit: 'cm³',
                    hintKey: 'gq_hint_cuboid', hintVars: { l, b, h }
                };
            }
        }
    ],

    getQuestions: function(count = 5) {
        const list = [];
        for(let i=0; i<count; i++) {
            const template = this.templates[Math.floor(Math.random() * this.templates.length)];
            list.push(template.generate());
        }
        return list;
    }
};

// 2D & 3D Visualizer Engine
const Visualizer = {
    threeScene: null, threeCamera: null, threeRenderer: null, threeMesh: null,

    init3D: function() {
        const container = document.getElementById('threeCanvas');
        if(!container) return;
        container.innerHTML = '';
        this.threeScene = new THREE.Scene();
        this.threeScene.background = new THREE.Color(0x090d16);

        this.threeCamera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
        this.threeCamera.position.set(8, 8, 12);

        this.threeRenderer = new THREE.WebGLRenderer({ antialias: true });
        this.threeRenderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(this.threeRenderer.domElement);

        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(10, 10, 10);
        this.threeScene.add(light);
        this.threeScene.add(new THREE.AmbientLight(0xffffff, 0.5));

        this.animate();
    },

    animate: function() {
        requestAnimationFrame(() => Visualizer.animate());
        if(Visualizer.threeMesh) Visualizer.threeMesh.rotation.y += 0.008;
        if(Visualizer.threeRenderer) Visualizer.threeRenderer.render(Visualizer.threeScene, Visualizer.threeCamera);
    },

    render: function(p) {
        const svg = document.getElementById('svgCanvas');
        const threeBox = document.getElementById('threeCanvas');

        if(p.shape === 'cuboid') {
            if(svg) svg.style.display = 'none';
            if(threeBox) threeBox.style.display = 'block';
            if(!this.threeScene) this.init3D();
            if(this.threeMesh) this.threeScene.remove(this.threeMesh);

            const geo = new THREE.BoxGeometry(p.l, p.h, p.b);
            const mat = new THREE.MeshStandardMaterial({ color: 0x6366f1, wireframe: false });
            this.threeMesh = new THREE.Mesh(geo, mat);
            this.threeScene.add(this.threeMesh);
        } else {
            if(threeBox) threeBox.style.display = 'none';
            if(svg) {
                svg.style.display = 'block';
                svg.innerHTML = '';
                
                if(p.shape === 'rectangle') {
                    svg.innerHTML = `<rect x="100" y="80" width="200" height="120" fill="rgba(99,102,241,0.3)" stroke="#6366f1" stroke-width="3"/>
                    <text x="200" y="70" fill="#fff" text-anchor="middle">L = ${p.l}m</text>
                    <text x="80" y="145" fill="#fff" text-anchor="middle">B = ${p.b}m</text>`;
                } else if(p.shape === 'square') {
                    svg.innerHTML = `<rect x="125" y="75" width="150" height="150" fill="rgba(16,185,129,0.3)" stroke="#10b981" stroke-width="3"/>
                    <text x="200" y="60" fill="#fff" text-anchor="middle">${t('gq_side')} = ${p.s}cm</text>`;
                } else if(p.shape === 'circle') {
                    svg.innerHTML = `<circle cx="200" cy="150" r="70" fill="rgba(245,158,11,0.3)" stroke="#f59e0b" stroke-width="3"/>
                    <line x1="200" y1="150" x2="270" y2="150" stroke="#fff" stroke-dasharray="4"/>
                    <text x="235" y="140" fill="#fff">r = ${p.r}m</text>`;
                }
            }
        }
    }
};

// Game Core Logic & Timer/Reward System
const Game = {
    score: 0, coins: 0, questions: [], currentIndex: 0,
    secondsElapsed: 0, timerInterval: null,

    init: function() {
        document.querySelectorAll('.zone-card').forEach(card => {
            card.addEventListener('click', () => Game.startQuest());
        });
        const subBtn = document.getElementById('submitBtn');
        const hintBtn = document.getElementById('hintBtn');
        const nextBtn = document.getElementById('nextBtn');
        const mapBtn = document.getElementById('backToMapBtn');
        const finishBtn = document.getElementById('finishQuestBtn');

        if(subBtn) subBtn.onclick = () => Game.checkAnswer();
        if(hintBtn) hintBtn.onclick = () => Game.showHint();
        if(nextBtn) nextBtn.onclick = () => Game.nextQuestion();
        if(mapBtn) mapBtn.onclick = () => Game.showScreen('zoneMapScreen');
        if(finishBtn) finishBtn.onclick = () => Game.showScreen('zoneMapScreen');

        // Re-draw the shape labels when the language is changed in the middle of a question
        document.addEventListener('languagechange', () => {
            const q = Game.questions[Game.currentIndex];
            const quest = document.getElementById('questScreen');
            if(q && quest && quest.classList.contains('active')) Visualizer.render(q.shapeParams);
        });
    },

    showScreen: function(id) {
        document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
        const target = document.getElementById(id);
        if(target) target.classList.add('active');
    },

    startQuest: function() {
        this.questions = QuestionBank.getQuestions(5);
        this.currentIndex = 0;
        this.score = 0;
        this.secondsElapsed = 0;
        
        clearInterval(this.timerInterval);
        this.timerInterval = setInterval(() => {
            Game.secondsElapsed++;
            const tVal = document.getElementById('timerVal');
            if(tVal) tVal.innerText = Game.secondsElapsed;
        }, 1000);

        this.showScreen('questScreen');
        this.loadQuestion();
    },

    loadQuestion: function() {
        const q = this.questions[this.currentIndex];
        const qProg = document.getElementById('qProgress');
        const pFill = document.getElementById('progressFill');
        const cScore = document.getElementById('currentScore');
        const qText = document.getElementById('questionText');
        const fb = document.getElementById('feedbackBox');
        const nBtn = document.getElementById('nextBtn');
        const sBtn = document.getElementById('submitBtn');
        const uAns = document.getElementById('userAnswer');

        if(qProg) i18n.set(qProg, 'gq_question_of', { i: this.currentIndex + 1, total: this.questions.length });
        if(pFill) pFill.style.width = `${((this.currentIndex)/this.questions.length)*100}%`;
        if(cScore) cScore.innerText = this.score;
        if(qText) i18n.set(qText, q.textKey, q.textVars);

        if(fb) fb.classList.add('hidden');
        if(nBtn) nBtn.classList.add('hidden');
        if(sBtn) sBtn.classList.remove('hidden');
        if(uAns) uAns.value = '';

        Visualizer.render(q.shapeParams);
    },

    checkAnswer: function() {
        const q = this.questions[this.currentIndex];
        const uAnsElem = document.getElementById('userAnswer');
        const uUnitElem = document.getElementById('userUnit');
        if(!uAnsElem || !uUnitElem) return;

        const val = parseFloat(uAnsElem.value);
        const unit = uUnitElem.value;

        const fb = document.getElementById('feedbackBox');
        if(!fb) return;
        fb.classList.remove('hidden');

        if(Math.abs(val - q.correctVal) < 0.5 && unit === q.correctUnit) {
            this.score += 100;
            fb.className = 'feedback-box correct';
            i18n.set(fb, 'gq_correct');
            const sBtn = document.getElementById('submitBtn');
            const nBtn = document.getElementById('nextBtn');
            if(sBtn) sBtn.classList.add('hidden');
            if(nBtn) nBtn.classList.remove('hidden');
        } else {
            fb.className = 'feedback-box incorrect';
            i18n.set(fb, 'gq_incorrect');
        }
    },

    showHint: function() {
        const q = this.questions[this.currentIndex];
        const fb = document.getElementById('feedbackBox');
        if(!fb) return;
        fb.classList.remove('hidden');
        fb.className = 'feedback-box';
        i18n.set(fb, q.hintKey, q.hintVars);
    },

    nextQuestion: function() {
        this.currentIndex++;
        if(this.currentIndex < this.questions.length) {
            this.loadQuestion();
        } else {
            clearInterval(this.timerInterval);
            this.finishQuest();
        }
    },

    finishQuest: function() {
        this.showScreen('resultsScreen');
        const rScore = document.getElementById('resScore');
        const rTime = document.getElementById('resTime');
        if(rScore) rScore.innerText = this.score;
        if(rTime) rTime.innerText = `${this.secondsElapsed}s`;

        // Time & Score Based Reward System
        let stars = "⭐⭐⭐";
        let badge = "gq_badge_gold";
        let coinsEarned = 50;

        if (this.secondsElapsed > 45 || this.score < 400) {
            stars = "⭐⭐";
            badge = "gq_badge_silver";
            coinsEarned = 30;
        } else if (this.secondsElapsed > 90) {
            stars = "⭐";
            badge = "gq_badge_bronze";
            coinsEarned = 15;
        }

        const sRow = document.getElementById('starsRow');
        const rCoins = document.getElementById('resCoins');
        const rBadge = document.getElementById('resBadge');
        const cDisp = document.getElementById('coinsDisplay');
        const bDisp = document.getElementById('badgeDisplay');

        if(sRow) sRow.innerText = stars;
        if(rCoins) rCoins.innerText = `+${coinsEarned}`;
        if(rBadge) i18n.set(rBadge, badge);
        if(bDisp) bDisp.textContent = '🏷️ ' + t(badge);

        // Securely sync coins and streak with the backend database
        fetch('/api/complete_game', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ coins: coinsEarned })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log("Database updated successfully! New Streak:", data.streak, "Total Coins:", data.coins);
                if(cDisp) cDisp.innerText = `🪙 ${data.coins}`;
            } else {
                console.warn("Failed to update database:", data);
            }
        })
        .catch(error => {
            console.error("Error communicating with backend API:", error);
        });
    }
};

window.addEventListener('DOMContentLoaded', () => Game.init());