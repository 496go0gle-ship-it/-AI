document.addEventListener('DOMContentLoaded', () => {
    // State
    const state = {
        student_id: 'student_' + Math.random().toString(36).substring(2, 9), // 仮のID生成
        history: []
    };

    // Elements
    const difficultyInput = document.getElementById('difficulty');
    const difficultyVal = document.getElementById('difficulty-val');
    const historyForm = document.getElementById('history-form');
    const historyList = document.getElementById('history-list');
    const historyCount = document.getElementById('history-count');
    const generateBtn = document.getElementById('generate-btn');
    const resultContent = document.getElementById('result-content');
    const resultTemplate = document.getElementById('result-template');
    
    // API_KEY
    const API_KEY = "my-secret-key-123";

    // Event Listeners
    difficultyInput.addEventListener('input', (e) => {
        difficultyVal.textContent = e.target.value;
    });

    historyForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const genre = document.getElementById('genre').value;
        const difficulty = parseFloat(document.getElementById('difficulty').value);
        const isCorrect = document.querySelector('input[name="is_correct"]:checked').value === 'true';
        const timeSpent = parseInt(document.getElementById('time_spent').value, 10);

        if (!genre) return alert('ジャンルを選択してください');

        const newHistoryItem = {
            genre: genre,
            difficulty: difficulty,
            is_correct: isCorrect,
            time_spent_seconds: timeSpent
        };

        state.history.push(newHistoryItem);
        renderHistory();
        updateGenerateButton();
        
        // Reset form partially
        document.getElementById('genre').value = '';
    });

    generateBtn.addEventListener('click', async () => {
        if (state.history.length === 0) return;

        // UI Loading state
        generateBtn.disabled = true;
        generateBtn.querySelector('.btn-text').textContent = 'AIが問題を生成中...';
        generateBtn.querySelector('.loader').classList.remove('hidden');
        
        resultContent.innerHTML = `
            <div class="waiting-state">
                <div class="pulse-ring"></div>
                <p>Gemini AIがZPDを分析し、最適な問題を生成しています...</p>
            </div>
        `;

        try {
            const response = await fetch('/api/v1/tutor/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': API_KEY
                },
                body: JSON.stringify({
                    student_id: state.student_id,
                    history: state.history
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            renderResult(data);
        } catch (error) {
            console.error("Error generating question:", error);
            resultContent.innerHTML = `
                <div class="info-block" style="border-left: 4px solid var(--danger)">
                    <h4>❌ エラーが発生しました</h4>
                    <p>API通信に失敗しました。サーバーが起動しているか、APIキーが正しいか確認してください。</p>
                    <p style="font-size: 0.8rem; margin-top: 10px; color: var(--text-muted)">${error.message}</p>
                </div>
            `;
        } finally {
            // Restore button
            generateBtn.disabled = false;
            generateBtn.querySelector('.btn-text').textContent = '🚀 AIに問題を出してもらう';
            generateBtn.querySelector('.loader').classList.add('hidden');
        }
    });

    // Functions
    function renderHistory() {
        if (state.history.length === 0) {
            historyList.innerHTML = '<li class="empty-state">履歴がありません</li>';
            historyCount.textContent = '0';
            return;
        }

        historyList.innerHTML = '';
        state.history.forEach((item, index) => {
            const li = document.createElement('li');
            li.className = 'history-item';
            
            const statusIcon = item.is_correct ? '✅' : '❌';
            
            li.innerHTML = `
                <div class="history-item-details">
                    <span class="h-genre">${item.genre}</span>
                    <span class="h-meta">難易度: ${item.difficulty.toFixed(1)} | 時間: ${item.time_spent_seconds}秒</span>
                </div>
                <div class="h-status">${statusIcon}</div>
            `;
            
            // 最新の要素が一番上に来るようにする
            historyList.prepend(li);
        });
        
        historyCount.textContent = state.history.length;
    }

    function updateGenerateButton() {
        generateBtn.disabled = state.history.length === 0;
    }

    function renderResult(data) {
        resultContent.innerHTML = '';
        
        // Clone template
        const clone = resultTemplate.content.cloneNode(true);
        
        // Fill data
        clone.querySelector('.target-genre-text').textContent = data.target_genre;
        clone.querySelector('.rationale-text').textContent = data.rationale;
        clone.querySelector('.question-text').textContent = data.recommended_question;
        clone.querySelector('.advice-text').textContent = data.learning_advice;
        clone.querySelector('.explanation-text').textContent = data.explanation;
        
        resultContent.appendChild(clone);
    }
});
