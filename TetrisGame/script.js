/* DOM 節點與 Canvas Context 取用 */
const canvas = document.getElementById('tetris-canvas');
const ctx = canvas.getContext('2d');
const nextCanvas = document.getElementById('next-canvas');
const nextCtx = nextCanvas.getContext('2d');

// UI 元素
const scoreElement = document.getElementById('score-display');
const levelElement = document.getElementById('level-display');
const linesElement = document.getElementById('lines-display');
const gameOverScreen = document.getElementById('game-over-screen');
const startScreen = document.getElementById('start-screen');
const pauseScreen = document.getElementById('pause-screen');
const finalScoreElement = document.getElementById('final-score');
const startBtn = document.getElementById('start-btn');
const restartBtn = document.getElementById('restart-btn');

// --- 遊戲常數定義 ---
const COLS = 10;
const ROWS = 20;
const BLOCK_SIZE = 30; // 300 / 10 = 30
ctx.scale(BLOCK_SIZE, BLOCK_SIZE);
nextCtx.scale(BLOCK_SIZE, BLOCK_SIZE); // 這裡配置成 120 / 30 = 4x4 的預覽畫面

// 經典方塊配色對應陣列
const COLORS = [
    null,
    '#00f0f0', // 1: I (青色)
    '#0000f0', // 2: J (藍色)
    '#f0a000', // 3: L (橘色)
    '#f0f000', // 4: O (黃色)
    '#00f000', // 5: S (綠色)
    '#a000f0', // 6: T (紫色)
    '#f00000'  // 7: Z (紅色)
];

// 7 種基本方塊的矩陣定義
const SHAPES = [
    [],
    [ // 1 - I
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ],
    [ // 2 - J
        [2, 0, 0],
        [2, 2, 2],
        [0, 0, 0]
    ],
    [ // 3 - L
        [0, 0, 3],
        [3, 3, 3],
        [0, 0, 0]
    ],
    [ // 4 - O
        [4, 4],
        [4, 4]
    ],
    [ // 5 - S
        [0, 5, 5],
        [5, 5, 0],
        [0, 0, 0]
    ],
    [ // 6 - T
        [0, 6, 0],
        [6, 6, 6],
        [0, 0, 0]
    ],
    [ // 7 - Z
        [7, 7, 0],
        [0, 7, 7],
        [0, 0, 0]
    ]
];

// --- 遊戲狀態變數 ---
let board = [];
let piece = null;
let nextPiece = null;
let score = 0;
let lines = 0;
let level = 1;

let dropCounter = 0;
let dropInterval = 1000;
let lastTime = 0;
let animationId;
let gameStatus = 'START'; // START, PLAYING, PAUSED, GAMEOVER

// --- 基礎陣列與設定建立 ---
function createMatrix(w, h) {
    const matrix = [];
    while (h--) {
        matrix.push(new Array(w).fill(0));
    }
    return matrix;
}

function resetGame() {
    board = createMatrix(COLS, ROWS);
    score = 0;
    lines = 0;
    level = 1;
    updateScore();
    dropInterval = 1000;
    piece = null;
    nextPiece = getRandomPiece();
    spawnPiece();
    gameStatus = 'PLAYING';
    
    // 隱藏所有疊加層畫面
    gameOverScreen.classList.add('hidden');
    startScreen.classList.add('hidden');
    pauseScreen.classList.add('hidden');
    
    lastTime = performance.now();
    cancelAnimationFrame(animationId);
    animate(lastTime);
}

// --- 方塊邏輯 ---
function createPiece(type) {
    return {
        matrix: SHAPES[type].map(row => [...row]),
        pos: { x: 0, y: 0 },
        type: type
    };
}

function getRandomPiece() {
    // 隨機選取 1 到 7 對應形狀
    const type = Math.floor(Math.random() * 7) + 1;
    return createPiece(type);
}

function spawnPiece() {
    piece = nextPiece;
    nextPiece = getRandomPiece();
    // 將新方塊置中並放在頂部
    piece.pos.x = Math.floor(COLS / 2) - Math.floor(piece.matrix[0].length / 2);
    piece.pos.y = 0;

    // 若生成時立刻撞上，代表遊戲結束
    if (collide(board, piece)) {
        gameStatus = 'GAMEOVER';
        cancelAnimationFrame(animationId);
        showGameOver();
    }
    drawNextPiece();
}

// --- 碰撞與基礎操作 ---
function collide(board, p) {
    const m = p.matrix;
    const o = p.pos;
    for (let y = 0; y < m.length; ++y) {
        for (let x = 0; x < m[y].length; ++x) {
            // 檢查方塊實體是否與版面邊界或已存在的方塊重疊
            if (m[y][x] !== 0 &&
               (board[y + o.y] && board[y + o.y][x + o.x]) !== 0) {
                return true;
            }
        }
    }
    return false;
}

function merge(board, p) {
    p.matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                board[y + p.pos.y][x + p.pos.x] = value;
            }
        });
    });
}

function rotatePiece(matrix, dir) {
    // 矩陣轉置
    for (let y = 0; y < matrix.length; ++y) {
        for (let x = 0; x < y; ++x) {
            [matrix[x][y], matrix[y][x]] = [matrix[y][x], matrix[x][y]];
        }
    }
    // 翻轉列實現方向旋轉
    if (dir > 0) {
        matrix.forEach(row => row.reverse());
    } else {
        matrix.reverse();
    }
}

function attemptRotate(dir) {
    const pos = piece.pos.x;
    let offset = 1;
    rotatePiece(piece.matrix, dir);
    // 初階踢牆系統 (Wall Kick)
    while (collide(board, piece)) {
        piece.pos.x += offset;
        offset = -(offset + (offset > 0 ? 1 : -1));
        if (offset > piece.matrix[0].length) {
            rotatePiece(piece.matrix, -dir); // 解除旋轉
            piece.pos.x = pos; // 復原位移
            return;
        }
    }
}

function dropPiece() {
    piece.pos.y++;
    if (collide(board, piece)) {
        piece.pos.y--; // 卡住時退回一格
        merge(board, piece);
        sweep();
        spawnPiece();
    }
    dropCounter = 0; // 重置掉落計時
}

function movePiece(dir) {
    piece.pos.x += dir;
    if (collide(board, piece)) {
        piece.pos.x -= dir;
    }
}

function hardDrop() {
    // 直接推到最底
    while (!collide(board, piece)) {
        piece.pos.y++;
    }
    piece.pos.y--;
    merge(board, piece);
    sweep();
    spawnPiece();
    dropCounter = 0;
}

// 取得幽靈預覽方塊的最低著陸點 Y 軸座標
function getGhostPos() {
    const ghost = {
        matrix: piece.matrix,
        pos: { x: piece.pos.x, y: piece.pos.y }
    };
    while (!collide(board, ghost)) {
        ghost.pos.y++;
    }
    ghost.pos.y--;
    return ghost.pos;
}

// --- 清除行數與結算計分 ---
function sweep() {
    let linesCleared = 0;
    outer: for (let y = ROWS - 1; y >= 0; --y) {
        // 尋找符合整條填滿的狀態
        for (let x = 0; x < COLS; ++x) {
            if (board[y][x] === 0) {
                continue outer;
            }
        }
        // 將該行切下補上全白 0 重返頂端
        const row = board.splice(y, 1)[0].fill(0);
        board.unshift(row);
        ++y; // 維持索引繼續測驗同階的狀態
        linesCleared++;
    }

    if (linesCleared > 0) {
        // 經典計分公式
        const lineScores = [0, 40, 100, 300, 1200];
        score += lineScores[linesCleared] * level;
        lines += linesCleared;
        
        // 每 10 行提升一等級
        level = Math.floor(lines / 10) + 1;
        // 等級越高，掉落間隔就越短（最低限制 100毫秒）
        dropInterval = Math.max(100, 1000 - (level - 1) * 100);
        
        updateScore();
    }
}

function updateScore() {
    scoreElement.innerText = score;
    levelElement.innerText = level;
    linesElement.innerText = lines;
}

// --- 圖形介面繪製 ---
function drawMatrix(matrix, offset, context, isGhost = false) {
    matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value !== 0) {
                // 如果是預覽落點的幽靈方塊，使用半透明
                context.fillStyle = isGhost ? `rgba(255,255,255,0.15)` : COLORS[value];
                context.fillRect(x + offset.x, y + offset.y, 1, 1);
                
                // 為有色彩的方塊加上經典方塊立體浮雕感
                if (!isGhost) {
                    context.fillStyle = 'rgba(255,255,255,0.3)';
                    context.fillRect(x + offset.x, y + offset.y, 1, 0.1); // 上高光
                    context.fillRect(x + offset.x, y + offset.y, 0.1, 1); // 左高光
                    
                    context.fillStyle = 'rgba(0,0,0,0.3)';
                    context.fillRect(x + offset.x, y + offset.y + 0.9, 1, 0.1); // 下陰影
                    context.fillRect(x + offset.x + 0.9, y + offset.y, 0.1, 1); // 右陰影
                }
            }
        });
    });
}

function drawNextPiece() {
    nextCtx.clearRect(0, 0, nextCanvas.width, nextCanvas.height);
    if (!nextPiece) return;
    
    // 將預設放置於 4x4 畫面正中央
    const offset = {
        x: (4 - nextPiece.matrix[0].length) / 2,
        y: (4 - nextPiece.matrix.length) / 2
    };
    drawMatrix(nextPiece.matrix, offset, nextCtx);
}

function draw() {
    // 徹底刷新畫布
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // 繪製場上已固定的方塊陣列
    drawMatrix(board, { x: 0, y: 0 }, ctx);

    if (piece && gameStatus === 'PLAYING') {
        // 先繪製在最底下的幽靈方塊預覽
        const ghostPos = getGhostPos();
        drawMatrix(piece.matrix, ghostPos, ctx, true);
        
        // 再繪製當前活躍掉落的方塊實體
        drawMatrix(piece.matrix, piece.pos, ctx);
    }
}

// --- 核心遊戲流程循環 ---
function animate(time = 0) {
    if (gameStatus !== 'PLAYING') return;

    const deltaTime = time - lastTime;
    lastTime = time;

    dropCounter += deltaTime;
    if (dropCounter > dropInterval) {
        dropPiece();
    }

    draw();
    animationId = requestAnimationFrame(animate);
}

// --- 遊戲介面控制 ---
function showGameOver() {
    finalScoreElement.innerText = score;
    gameOverScreen.classList.remove('hidden');
    draw(); // 更新視覺把最後定格畫出
}

function togglePause() {
    if (gameStatus === 'PLAYING') {
        gameStatus = 'PAUSED';
        pauseScreen.classList.remove('hidden');
        draw();
    } else if (gameStatus === 'PAUSED') {
        gameStatus = 'PLAYING';
        pauseScreen.classList.add('hidden');
        lastTime = performance.now();
        animate(lastTime);
    }
}

// 接收鍵盤快捷設定
document.addEventListener('keydown', event => {
    // 阻止方向鍵與空白鍵讓網頁自帶滑動
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(event.key)) {
        event.preventDefault();
    }
    
    // 如果不是遊玩狀態只監聽恢復按鍵
    if (gameStatus !== 'PLAYING' && event.key !== 'p' && event.key !== 'P' && event.key !== 'Escape') {
        return;
    }

    switch (event.key) {
        case 'ArrowLeft':
            movePiece(-1);
            break;
        case 'ArrowRight':
            movePiece(1);
            break;
        case 'ArrowDown':
            dropPiece();
            break;
        case 'ArrowUp':
        case ' ': // 空白硬下落
            hardDrop();
            break;
        case 'z':
        case 'Z':
            attemptRotate(-1); // 逆時針
            break;
        case 'x':
        case 'X':
            attemptRotate(1); // 順時針
            break;
        case 'p':
        case 'P':
        case 'Escape':
            if (gameStatus === 'PLAYING' || gameStatus === 'PAUSED') {
                togglePause();
            }
            break;
    }
    
    if (gameStatus === 'PLAYING') {
        draw(); // 即時視覺反饋
    }
});

// 按鈕註冊
startBtn.addEventListener('click', resetGame);
restartBtn.addEventListener('click', resetGame);

// 一開始先進入準備畫面，繪製初始無畫面狀態的背景
draw();