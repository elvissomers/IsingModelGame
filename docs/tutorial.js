
const tutorialData = [
    {
        "text": "Welcome to the Ising Model Game!\n\nIn this game, you will be exploring a grid of spins. Every \"spin\" can point either \"up\" or \"down\".\n\nClick on the arrows below to toggle them!",
        "grids": [
            {
                "width": 2,
                "height": 1,
                "mode": "SPINS",
                "spins": [
                    [
                        1,
                        0
                    ]
                ],
                "couplings": [
                    null
                ],
                "label": "Click arrows to toggle"
            }
        ]
    },
    {
        "text": "Between the spins, there are \"couplings\".\n\nA coupling can be \"negative\" or \"positive\".",
        "grids": [
            {
                "width": 2,
                "height": 1,
                "mode": "LOCKED",
                "spins": [
                    [
                        1,
                        1
                    ]
                ],
                "couplings": [
                    0
                ],
                "label": "Negative Coupling"
            },
            {
                "width": 2,
                "height": 1,
                "mode": "LOCKED",
                "spins": [
                    [
                        1,
                        1
                    ]
                ],
                "couplings": [
                    1
                ],
                "label": "Positive Coupling"
            }
        ]
    },
    {
        "text": "Every configuration has a certain amount of energy. The energy is given by the couplings.\n\nIf the coupling is negative, the energy will be 0 when the two arrows point in different directions.\n\nBut the energy will be 1 when the two arrows point in the same direction.",
        "grids": [
            {
                "width": 2,
                "height": 1,
                "mode": "LOCKED",
                "spins": [
                    [
                        1,
                        0
                    ]
                ],
                "couplings": [
                    0
                ],
                "label": "Energy = 0"
            },
            {
                "width": 2,
                "height": 1,
                "mode": "LOCKED",
                "spins": [
                    [
                        1,
                        1
                    ]
                ],
                "couplings": [
                    0
                ],
                "label": "Energy = 1"
            }
        ]
    },
    {
        "text": "If the coupling is positive, the situation is reversed!\n\nThe energy will be 0 when the arrows point in the same direction.\nBut it will be 1 when they point in different directions!",
        "grids": [
            {
                "width": 2,
                "height": 1,
                "mode": "LOCKED",
                "spins": [
                    [
                        1,
                        1
                    ]
                ],
                "couplings": [
                    1
                ],
                "label": "Energy = 0"
            },
            {
                "width": 2,
                "height": 1,
                "mode": "LOCKED",
                "spins": [
                    [
                        1,
                        0
                    ]
                ],
                "couplings": [
                    1
                ],
                "label": "Energy = 1"
            }
        ]
    },
    {
        "text": "Using this information, try to see what energy you get for a specific configuration!\n\nUsing multiple configurations, you can figure out whether the couplings are positive or negative.\n\nBut be careful! You only get one guess.",
        "grids": []
    }
];

const cellSize = 60;
const margin = 40;
const gap = 30;

function getArrowCenter(r, c) {
    let cx = margin + c * (cellSize + gap) + cellSize / 2;
    let cy = margin + r * (cellSize + gap) + cellSize / 2;
    return {cx, cy};
}

function getCouplingCenter(idx, width, height) {
    let numHoriz = height * (width - 1);
    
    if (idx < numHoriz) {
        let r = Math.floor(idx / (width - 1));
        let c = idx % (width - 1);
        let c1 = getArrowCenter(r, c);
        let c2 = getArrowCenter(r, c + 1);
        return { cx: (c1.cx + c2.cx)/2, cy: c1.cy };
    } else {
        let vIdx = idx - numHoriz;
        let r = Math.floor(vIdx / width);
        let c = vIdx % width;
        let c1 = getArrowCenter(r, c);
        let c2 = getArrowCenter(r + 1, c);
        return { cx: c1.cx, cy: (c1.cy + c2.cy)/2 };
    }
}

function renderGrid(gridData, container) {
    const width = gridData.width;
    const height = gridData.height;
    const mode = gridData.mode;
    let spins = JSON.parse(JSON.stringify(gridData.spins));
    let couplings = JSON.parse(JSON.stringify(gridData.couplings));
    
    const wrapper = document.createElement('div');
    wrapper.style.display = 'flex';
    wrapper.style.flexDirection = 'column';
    wrapper.style.alignItems = 'center';
    
    const gridDiv = document.createElement('div');
    gridDiv.className = 'grid-container active-grid mode-couplings'; 
    gridDiv.style.position = 'relative';
    gridDiv.style.backgroundColor = 'var(--color-grid-bg)';
    gridDiv.style.borderRadius = '10px';
    
    // We remove .mode-couplings if it's SPINS mode so couplings aren't clickable looking, but we might want them grey anyway.
    
    const cw = 2 * margin + width * cellSize + (width - 1) * gap;
    const ch = 2 * margin + height * cellSize + (height - 1) * gap;
    gridDiv.style.width = `${cw}px`;
    gridDiv.style.height = `${ch}px`;
    
    const numCouplings = height * (width - 1) + (height - 1) * width;
    
    const drawGrid = () => {
        gridDiv.innerHTML = '';
        
        for (let i = 0; i < numCouplings; i++) {
            let center = getCouplingCenter(i, width, height);
            let comp = document.createElement('div');
            comp.className = 'coupling';
            comp.style.left = `${center.cx}px`;
            comp.style.top = `${center.cy}px`;
            
            let val = couplings[i];
            if (val === 1) {
                comp.dataset.val = "1";
                comp.innerText = "+";
            } else if (val === 0) {
                comp.dataset.val = "0";
                comp.innerText = "-";
            }
            
            comp.addEventListener('click', (e) => {
                if (mode !== 'COUPLINGS') return;
                if (couplings[i] === null) couplings[i] = 1;
                else if (couplings[i] === 1) couplings[i] = 0;
                else couplings[i] = null;
                drawGrid();
            });
            
            gridDiv.appendChild(comp);
        }
        
        for (let r = 0; r < height; r++) {
            for (let c = 0; c < width; c++) {
                let center = getArrowCenter(r, c);
                let arrow = document.createElement('div');
                arrow.className = 'arrow ' + (spins[r][c] === 1 ? 'up' : 'down');
                arrow.style.left = `${center.cx}px`;
                arrow.style.top = `${center.cy}px`;
                
                arrow.addEventListener('click', () => {
                    if (mode !== 'SPINS') return;
                    spins[r][c] = 1 - spins[r][c];
                    drawGrid();
                });
                
                gridDiv.appendChild(arrow);
            }
        }
    };
    
    drawGrid();
    wrapper.appendChild(gridDiv);
    
    if (gridData.label) {
        const labelDiv = document.createElement('div');
        labelDiv.style.marginTop = '15px';
        labelDiv.style.color = 'var(--text-color)';
        labelDiv.style.fontWeight = 'bold';
        labelDiv.style.fontSize = '1.2rem';
        labelDiv.innerText = gridData.label;
        wrapper.appendChild(labelDiv);
    }
    
    container.appendChild(wrapper);
}

function initTutorialPage(pageIndex) {
    const pageData = tutorialData[pageIndex];
    const container = document.getElementById('grids-container');
    container.innerHTML = '';
    
    if (pageData.grids && pageData.grids.length > 0) {
        pageData.grids.forEach(gridData => {
            renderGrid(gridData, container);
        });
    }
}
