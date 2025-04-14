document.addEventListener('DOMContentLoaded', function() {
    // Connect to Socket.IO
    const socket = io();
    
    // DOM elements
    const transcriptElement = document.getElementById('transcript');
    const pollQuestionElement = document.getElementById('poll-question');
    const pollOptionsElement = document.getElementById('poll-options');
    const pollTimestampElement = document.getElementById('poll-timestamp');
    const nextPollTimeElement = document.getElementById('next-poll-time');
    const generatePollBtn = document.getElementById('generate-poll-btn');
    const intervalInput = document.getElementById('interval-input');
    const updateIntervalBtn = document.getElementById('update-interval-btn');
    const countdownElement = document.getElementById('countdown');
    const pollContainer = document.getElementById('poll-container');
    
    // Timer variables
    let countdownInterval;
    let secondsUntilNextPoll;
    
    // Initialize countdown if we have time data
    if (nextPollTimeElement) {
        secondsUntilNextPoll = parseInt(nextPollTimeElement.getAttribute('data-seconds') || '0');
        startCountdown();
    }
    
    // Listen for poll updates from server
    socket.on('poll_update', function(data) {
        updatePoll(data);
        resetCountdown(data.poll_interval || parseInt(nextPollTimeElement.getAttribute('data-interval') || '900'));
    });
    
    // Manual poll generation
    if (generatePollBtn) {
        generatePollBtn.addEventListener('click', function() {
            fetch('/api/generate-poll', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Poll update will be handled by socket event
                    showToast('Poll generated successfully!', 'success');
                }
            })
            .catch(error => {
                console.error('Error generating poll:', error);
                showToast('Failed to generate poll', 'danger');
            });
        });
    }
    
    // Update interval
    if (updateIntervalBtn && intervalInput) {
        updateIntervalBtn.addEventListener('click', function() {
            const newInterval = parseInt(intervalInput.value);
            if (isNaN(newInterval) || newInterval < 1) {
                showToast('Please enter a valid interval (minimum 1 second)', 'warning');
                return;
            }
            
            fetch('/api/update-interval', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ interval: newInterval })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showToast(data.message, 'success');
                    resetCountdown(newInterval);
                    // Update the data attribute for future reference
                    if (nextPollTimeElement) {
                        nextPollTimeElement.setAttribute('data-interval', newInterval.toString());
                    }
                } else {
                    showToast(data.message, 'danger');
                }
            })
            .catch(error => {
                console.error('Error updating interval:', error);
                showToast('Failed to update interval', 'danger');
            });
        });
    }
    
    // Function to update the poll display
    function updatePoll(data) {
        // Update transcript if available
        if (data.transcript && transcriptElement) {
            transcriptElement.textContent = data.transcript;
        }
        
        // Update poll question and options
        if (data.poll && pollQuestionElement && pollOptionsElement) {
            pollQuestionElement.textContent = data.poll.question;
            
            // Clear existing options
            pollOptionsElement.innerHTML = '';
            
            // Add new options
            data.poll.options.forEach((option, index) => {
                const optionElement = document.createElement('div');
                optionElement.className = 'form-check';
                optionElement.innerHTML = `
                    <input class="form-check-input" type="radio" name="pollOption" id="option${index}" value="${option}">
                    <label class="form-check-label" for="option${index}">
                        ${option}
                    </label>
                `;
                pollOptionsElement.appendChild(optionElement);
            });
            
            // Add poll animation
            pollContainer.classList.add('poll-highlight');
            setTimeout(() => {
                pollContainer.classList.remove('poll-highlight');
            }, 2000);
        }
        
        // Update timestamp if available
        if (data.timestamp && pollTimestampElement) {
            pollTimestampElement.textContent = data.timestamp;
        }
    }
    
    // Start countdown timer
    function startCountdown() {
        // Clear any existing interval
        if (countdownInterval) {
            clearInterval(countdownInterval);
        }
        
        // Update countdown immediately
        updateCountdown();
        
        // Update countdown every second
        countdownInterval = setInterval(updateCountdown, 1000);
    }
    
    // Update the countdown display
    function updateCountdown() {
        if (secondsUntilNextPoll <= 0) {
            // Poll should be generated soon, wait for server update
            countdownElement.textContent = 'Generating poll...';
            return;
        }
        
        // Calculate minutes and seconds
        const minutes = Math.floor(secondsUntilNextPoll / 60);
        const seconds = secondsUntilNextPoll % 60;
        
        // Format the countdown
        countdownElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        
        // Decrease the countdown
        secondsUntilNextPoll--;
    }
    
    // Reset countdown with new interval
    function resetCountdown(interval) {
        secondsUntilNextPoll = interval;
        startCountdown();
    }
    
    // Toast notification function
    function showToast(message, type = 'info') {
        // Create toast container if it doesn't exist
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'position-fixed bottom-0 end-0 p-3';
            document.body.appendChild(toastContainer);
        }
        
        // Create toast element
        const toastId = `toast-${Date.now()}`;
        const toast = document.createElement('div');
        toast.className = `toast show bg-${type} text-white`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        toast.id = toastId;
        
        toast.innerHTML = `
            <div class="toast-header bg-${type} text-white">
                <strong class="me-auto">Notification</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;
        
        // Add to container
        toastContainer.appendChild(toast);
        
        // Auto-hide after 3 seconds
        setTimeout(() => {
            const toastElement = document.getElementById(toastId);
            if (toastElement) {
                toastElement.remove();
            }
        }, 3000);
        
        // Add click listener to close button
        const closeButton = toast.querySelector('.btn-close');
        if (closeButton) {
            closeButton.addEventListener('click', function() {
                toast.remove();
            });
        }
    }
});
