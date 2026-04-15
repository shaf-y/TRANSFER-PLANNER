document.getElementById('generateBtn').addEventListener('click', async () => {
    const btn = document.getElementById('generateBtn');
    const container = document.getElementById('planContainer');
    
    // Add loading state
    btn.innerHTML = `<span class="btn-text">Calculating Optimization...</span>`;
    btn.style.opacity = '0.8';
    btn.disabled = true;

    try {
        const response = await fetch('/api/plan');
        const data = await response.json();
        
        // Clear previous and show container
        container.innerHTML = '';
        container.classList.remove('hidden');

        // Build UI
        data.plan.forEach((quarter, index) => {
            const delay = index * 0.15; // Staggered animation
            
            // Calculate absolute max difficulty safely (assuming roughly 40 is extreme)
            const maxDiff = 40; 
            const diffPercentage = Math.min((quarter.difficulty_score / maxDiff) * 100, 100);
            
            // Heatmap color logic
            let heatmapColor = 'var(--heatmap-low)';
            let diffLabel = 'Manageable';
            if (quarter.difficulty_score > 25) {
                heatmapColor = 'var(--heatmap-med)';
                diffLabel = 'Intense';
            }
            if (quarter.difficulty_score >= 32) {
                heatmapColor = 'var(--heatmap-high)';
                diffLabel = 'Extreme / Weeder Focus';
            }

            const isWarning = quarter.total_units > quarter.max_units;

            const card = document.createElement('div');
            card.className = 'quarter-card';
            card.style.animationDelay = `${delay}s`;
            
            card.innerHTML = `
                <div class="quarter-header">
                    <h2 class="term-title">${quarter.term}</h2>
                    <div class="unit-counter ${isWarning ? 'warn' : ''}">
                        ${quarter.total_units} / ${quarter.max_units} Units
                    </div>
                </div>
                
                <ul class="course-list">
                    ${quarter.courses.map(course => `
                        <li class="course-item">
                            <span class="course-id">${course.id}</span>
                            <div class="course-name">${course.name}</div>
                            <div class="course-meta">
                                <span>${course.units} Units</span>
                                <span>Diff: ${course.difficulty}/10</span>
                            </div>
                        </li>
                    `).join('')}
                </ul>
                
                <div class="heatmap-container">
                    <div class="heatmap-label">
                        <span>Difficulty Heatmap</span>
                        <span style="color: ${heatmapColor}">${diffLabel}</span>
                    </div>
                    <div class="heatmap-bar">
                        <div class="heatmap-fill" style="width: 0%; background: ${heatmapColor}; box-shadow: 0 0 10px ${heatmapColor}"></div>
                    </div>
                </div>
            `;
            
            container.appendChild(card);
            
            // Trigger animation for heatmap fill shortly after DOM insertion
            setTimeout(() => {
                const fill = card.querySelector('.heatmap-fill');
                if (fill) fill.style.width = `${diffPercentage}%`;
            }, 50 + (index * 150));
        });
        
    } catch (error) {
        console.error('Error fetching plan:', error);
        container.innerHTML = `<p style="color: red; text-align: center; width: 100%;">Failed to load the optimal plan. Ensure backend is running.</p>`;
        container.classList.remove('hidden');
    } finally {
        btn.innerHTML = `<span class="btn-text">Regenerate Plan</span><span class="btn-glow"></span>`;
        btn.style.opacity = '1';
        btn.disabled = false;
    }
});
