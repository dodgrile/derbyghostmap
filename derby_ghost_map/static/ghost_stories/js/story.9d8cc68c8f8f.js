document.addEventListener('DOMContentLoaded', function() {
    initAudioPlayer();
    setupAmbientSounds();
});

// Initialize audio narration player
function initAudioPlayer() {
    const toggleButton = document.getElementById('toggle-narration');
    const audioPlayer = document.getElementById('audio-player');
    
    if (toggleButton && audioPlayer) {
        toggleButton.addEventListener('click', function() {
            audioPlayer.classList.toggle('hidden');
            
            // If revealing the player
            if (!audioPlayer.classList.contains('hidden')) {
                // Auto-play the narration
                const audio = audioPlayer.querySelector('audio');
                if (audio) {
                    audio.play().catch(error => {
                        // Auto-play may be blocked by browser
                        console.log('Auto-play prevented by browser', error);
                    });
                }
                
                // Update button text
                toggleButton.innerHTML = '<i class="fas fa-times"></i> Hide narration';
            } else {
                // Update button text
                toggleButton.innerHTML = '<i class="fas fa-headphones"></i> Listen to the story';
                
                // Pause audio
                const audio = audioPlayer.querySelector('audio');
                if (audio && !audio.paused) {
                    audio.pause();
                }
            }
        });
        
        // Add volume fade-in effect for smoother experience
        const narrationAudio = audioPlayer.querySelector('audio');
        if (narrationAudio) {
            narrationAudio.addEventListener('play', function() {
                this.volume = 0;
                
                let fadeIn = setInterval(() => {
                    if (this.volume < 0.9) {
                        this.volume += 0.1;
                    } else {
                        this.volume = 1;
                        clearInterval(fadeIn);
                    }
                }, 100);
            });
        }
    }
}

// Handle ambient background sounds
function setupAmbientSounds() {
    const ambientToggle = document.getElementById('ambient-toggle');
    
    if (ambientToggle) {
        // Create ambient sound
        const ambientSound = new Audio('/static/ghost_stories/audio/ambient-background.mp3');
        ambientSound.loop = true;
        ambientSound.volume = 0.15;
        
        // Check user preference from localStorage
        const ambientEnabled = localStorage.getItem('ambient-sound-enabled') !== 'false';
        ambientToggle.checked = ambientEnabled;
        
        // Set up toggle functionality
        ambientToggle.addEventListener('change', function() {
            if (this.checked) {
                ambientSound.play().catch(error => {
                    console.log('Ambient sound autoplay prevented', error);
                });
                localStorage.setItem('ambient-sound-enabled', 'true');
            } else {
                ambientSound.pause();
                localStorage.setItem('ambient-sound-enabled', 'false');
            }
        });
        
        // Only play if enabled (after user interaction)
        document.addEventListener('click', function initAmbient() {
            if (ambientEnabled) {
                ambientSound.play().catch(error => {
                    console.log('Ambient sound autoplay prevented', error);
                });
            }
            // Remove this listener after first click
            document.removeEventListener('click', initAmbient);
        }, { once: true });
    }
}