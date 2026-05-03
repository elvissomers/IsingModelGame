// Game State
let currentWidth = 2;
let currentHeight = 2;
let numCouplings = 4;
let solutionCouplings = [];
let remainingTries = 0;
let inputState = 'SPINS'; // 'SPINS' or 'COUPLINGS'
let gridCounter = 0;

// Current Active Input
let activeSpins = [];
let activeCouplings = [];

const cellSize = 60;
const margin = 40;
const gap = 80;


// Utility functions
function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId).classList.add('active');
}

function startGame(height, width) {
    currentHeight = height;
    currentWidth = width;
    
    numCouplings = height * (width - 1) + (height - 1) * width;
    solutionCouplings = Array.from({length: numCouplings}, () => Math.random() < 0.5 ? 1 : 0);
    remainingTries = 2 * numCouplings;
    inputState = 'SPINS';
    
    document.getElementById('history-panel').innerHTML = '';
    
    document.getElementById('btn-submit-spins').disabled = false;
    document.getElementById('btn-guess-couplings').disabled = false;
    document.getElementById('btn-submit-couplings').disabled = true;
    
    updateUI();
    showScreen('game-screen');
    addSpinGrid();
}

function updateUI() {
    document.getElementById('tries-left').innerText = `Tries left: ${remainingTries}`;
}

// Energy Calculation exactly matching Python `solution.py`
function getEnergy(spins, couplings) {
    let energy = 0;
    let couplingIndex = 0;

    // Horizontal couplings
    for (let r = 0; r < currentHeight; r++) {
        for (let c = 0; c < currentWidth - 1; c++) {
            if (spins[r][c] !== spins[r][c + 1]) {
                energy += couplings[couplingIndex];
            } else {
                energy += 1 - couplings[couplingIndex];
            }
            couplingIndex += 1;
        }
    }

    // Vertical couplings
    for (let r = 0; r < currentHeight - 1; r++) {
        for (let c = 0; c < currentWidth; c++) {
            if (spins[r][c] !== spins[r + 1][c]) {
                energy += couplings[couplingIndex];
            } else {
                energy += 1 - couplings[couplingIndex];
            }
            couplingIndex += 1;
        }
    }

    return energy;
}

// UI Grid Generation
function getArrowCenter(r, c) {
    let cx = margin + c * (cellSize + gap) + cellSize / 2;
    let cy = margin + r * (cellSize + gap) + cellSize / 2;
    return {cx, cy};
}

function getCouplingCenter(idx) {
    let numHoriz = currentHeight * (currentWidth - 1);
    
    if (idx < numHoriz) {
        // Horizontal
        let r = Math.floor(idx / (currentWidth - 1));
        let c = idx % (currentWidth - 1);
        let c1 = getArrowCenter(r, c);
        let c2 = getArrowCenter(r, c + 1);
        return { cx: (c1.cx + c2.cx)/2, cy: c1.cy };
    } else {
        // Vertical
        let vIdx = idx - numHoriz;
        let r = Math.floor(vIdx / currentWidth);
        let c = vIdx % currentWidth;
        let c1 = getArrowCenter(r, c);
        let c2 = getArrowCenter(r + 1, c);
        return { cx: c1.cx, cy: (c1.cy + c2.cy)/2 };
    }
}

function addSpinGrid() {
    // Lock previous grids
    document.querySelectorAll('.active-grid').forEach(el => el.classList.remove('active-grid'));

    gridCounter++;
    const rowContainer = document.createElement('div');
    rowContainer.className = 'grid-row-container';
    
    const gridDiv = document.createElement('div');
    gridDiv.className = 'grid-container active-grid';
    gridDiv.id = `grid-${gridCounter}`;
    
    const cw = 2 * margin + currentWidth * cellSize + (currentWidth - 1) * gap;
    const ch = 2 * margin + currentHeight * cellSize + (currentHeight - 1) * gap;
    gridDiv.style.width = `${cw}px`;
    gridDiv.style.height = `${ch}px`;
    
    // Initialize defaults
    activeSpins = Array.from({length: currentHeight}, () => Array(currentWidth).fill(1));
    activeCouplings = Array(numCouplings).fill(null);
    
    // Draw Couplings
    for (let i = 0; i < numCouplings; i++) {
        let center = getCouplingCenter(i);
        let comp = document.createElement('div');
        comp.className = 'coupling';
        comp.style.left = `${center.cx}px`;
        comp.style.top = `${center.cy}px`;
        comp.dataset.idx = i;
        
        comp.addEventListener('click', (e) => {
            if (inputState !== 'COUPLINGS' || !gridDiv.classList.contains('active-grid')) return;
            let val = activeCouplings[i];
            if (val === null) activeCouplings[i] = 1;
            else if (val === 1) activeCouplings[i] = 0;
            else activeCouplings[i] = null;
            
            // update DOM
            if (activeCouplings[i] === 1) {
                comp.dataset.val = "1";
                comp.innerText = "+";
            } else if (activeCouplings[i] === 0) {
                comp.dataset.val = "0";
                comp.innerText = "-";
            } else {
                delete comp.dataset.val;
                comp.innerText = "";
            }
        });
        
        gridDiv.appendChild(comp);
    }
    
    // Draw Arrows
    for (let r = 0; r < currentHeight; r++) {
        for (let c = 0; c < currentWidth; c++) {
            let center = getArrowCenter(r, c);
            let arrow = document.createElement('div');
            arrow.className = 'arrow up';
            arrow.style.left = `${center.cx}px`;
            arrow.style.top = `${center.cy}px`;
            
            arrow.addEventListener('click', () => {
                if (inputState !== 'SPINS' || !gridDiv.classList.contains('active-grid')) return;
                activeSpins[r][c] = 1 - activeSpins[r][c]; // flip
                if (activeSpins[r][c] === 1) {
                    arrow.classList.remove('down');
                    arrow.classList.add('up');
                } else {
                    arrow.classList.remove('up');
                    arrow.classList.add('down');
                }
            });
            gridDiv.appendChild(arrow);
        }
    }
    
    rowContainer.appendChild(gridDiv);
    
    const energyLabelDiv = document.createElement('div');
    energyLabelDiv.className = 'energy-label';
    energyLabelDiv.innerText = 'Energy: ?';
    energyLabelDiv.id = `energy-${gridCounter}`;
    rowContainer.appendChild(energyLabelDiv);
    
    const historyPanel = document.getElementById('history-panel');
    historyPanel.appendChild(rowContainer);
    rowContainer.scrollIntoView({ behavior: 'smooth' });
}

function submitSpins() {
    if (remainingTries <= 0) {
        alert("You have zero tries left! You lost!");
        return;
    }
    
    remainingTries--;
    let energy = getEnergy(activeSpins, solutionCouplings);
    
    let label = document.getElementById(`energy-${gridCounter}`);
    label.innerText = `Energy: ${energy}`;
    
    updateUI();
    
    if (remainingTries > 0) {
        addSpinGrid();
    } else {
        alert("You have zero tries left for spins! Let's guess couplings.");
        startCouplingsMode();
    }
}

function startCouplingsMode() {
    inputState = 'COUPLINGS';
    
    document.getElementById('btn-submit-spins').disabled = true;
    document.getElementById('btn-guess-couplings').disabled = true;
    document.getElementById('btn-submit-couplings').disabled = false;
    
    let label = document.getElementById(`energy-${gridCounter}`);
    if (label) {
        label.innerText = "Guessing...";
        label.style.color = "var(--color-coupling-pos)";
    }
    
    let activeGrid = document.querySelector('.active-grid');
    if (activeGrid) {
        activeGrid.classList.add('mode-couplings');
    }
}

function submitCouplings() {
    if (activeCouplings.includes(null)) {
        alert("Please assign (+ or -) to all bonds by clicking the grey blocks!");
        return;
    }
    
    let correct = activeCouplings.every((val, index) => val === solutionCouplings[index]);
    
    document.getElementById('btn-submit-couplings').disabled = true;
    let activeGrid = document.querySelector('.active-grid');
    if(activeGrid) activeGrid.classList.remove('active-grid');
    
    if (correct) {
        startFireworks();
        setTimeout(() => alert("Congratulations, you successfully mapped the couplings!"), 500);
    } else {
        showSolutionModal();
    }
}

function renderSolutionGrid(containerId) {
    const container = document.getElementById(containerId);
    container.innerHTML = '';
    
    const cw = 2 * margin + currentWidth * cellSize + (currentWidth - 1) * gap;
    const ch = 2 * margin + currentHeight * cellSize + (currentHeight - 1) * gap;
    container.style.width = `${cw}px`;
    container.style.height = `${ch}px`;
    container.style.margin = "0 auto";
    
    // Draw solution couplings
    for (let i = 0; i < numCouplings; i++) {
        let center = getCouplingCenter(i);
        let comp = document.createElement('div');
        comp.className = 'coupling';
        comp.style.left = `${center.cx}px`;
        comp.style.top = `${center.cy}px`;
        
        let val = solutionCouplings[i];
        if (val === 1) {
            comp.dataset.val = "1";
            comp.innerText = "+";
        } else {
            comp.dataset.val = "0";
            comp.innerText = "-";
        }
        container.appendChild(comp);
    }
}

function showSolutionModal() {
    renderSolutionGrid('modal-grid-container');
    const modal = document.getElementById('solution-modal');
    modal.classList.add('show');
}

function closeModal() {
    document.getElementById('solution-modal').classList.remove('show');
    showScreen('start-menu');
}

// --- Fireworks Animation ---
const canvas = document.getElementById('fireworks-canvas');
const ctx = canvas.getContext('2d');
let particles = [];
let animFrame;

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
window.addEventListener('resize', resizeCanvas);
resizeCanvas();

function startFireworks() {
    for (let i = 0; i < 6; i++) {
        setTimeout(() => {
            let x = canvas.width * 0.2 + Math.random() * canvas.width * 0.6;
            let y = canvas.height * 0.2 + Math.random() * canvas.height * 0.6;
            createExplosion(x, y);
        }, i * 400);
    }
    if (!animFrame) animLoop();
    
    setTimeout(() => {
        cancelAnimationFrame(animFrame);
        animFrame = null;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles = [];
        showScreen('start-menu'); // return to menu
    }, 4000);
}

function createExplosion(x, y) {
    const colors = ['#F1C40F', '#E74C3C', '#9B59B6', '#3498DB', '#2ECC71', '#FFFFFF'];
    for(let i=0; i<40; i++) {
        particles.push({
            x: x, y: y,
            vx: (Math.random() - 0.5) * 15,
            vy: (Math.random() - 0.5) * 15,
            size: Math.random() * 5 + 3,
            color: colors[Math.floor(Math.random() * colors.length)],
            life: 100
        });
    }
}

function animLoop() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for(let i=particles.length-1; i>=0; i--) {
        let p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.2; // gravity
        p.life -= 1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
        ctx.fillStyle = p.color;
        ctx.fill();
        if(p.life <= 0) particles.splice(i, 1);
    }
    animFrame = requestAnimationFrame(animLoop);
}
