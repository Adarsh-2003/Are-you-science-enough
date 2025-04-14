// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Add animation to the leaderboard rows
function animateLeaderboard() {
    const leaderboardRows = document.querySelectorAll('.table tbody tr');
    leaderboardRows.forEach((row, index) => {
        row.style.animation = `fadeIn 0.5s ease-in-out ${index * 0.1}s forwards`;
    });
}

// Add animation keyframes
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;
document.head.appendChild(style);

// Call animation when leaderboard is loaded
document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector('.table tbody tr')) {
        animateLeaderboard();
    }
}); 