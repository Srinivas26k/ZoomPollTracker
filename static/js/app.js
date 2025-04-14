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
    
    // Additional elements for real-time features
    const pollsHistoryList = document.getElementById('polls-history-list');
    const pollAnalyticsBtn = document.getElementById('poll-analytics-btn');
    const exportDataBtn = document.getElementById('export-data-btn');
    const pollStatsElement = document.getElementById('poll-stats');
    const participantsCount = document.getElementById('participants-count');
    const meetingDuration = document.getElementById('meeting-duration');
    
    // Timer variables
    let countdownInterval;
    let secondsUntilNextPoll;
    let meetingStartTime = new Date();
    let durationInterval;
    
    // Initialize from stored settings if available
    const userSettings = StorageManager.getUserSettings();
    if (userSettings && intervalInput) {
        intervalInput.value = userSettings.pollInterval;
    }
    
    // Initialize meeting data if available
    const storedMeeting = StorageManager.getMeetingData();
    if (storedMeeting) {
        console.log('Restored meeting data from local storage');
        // Update participant count if element exists
        if (participantsCount && storedMeeting.participants_count) {
            participantsCount.textContent = storedMeeting.participants_count;
        }
        
        // Initialize meeting duration timer
        if (storedMeeting.start_time) {
            const startTime = new Date(storedMeeting.start_time);
            meetingStartTime = startTime;
            startDurationTimer();
        }
    } else {
        // Save current meeting data
        const meetingIdElement = document.getElementById('meeting-id');
        if (meetingIdElement) {
            const meetingData = {
                id: meetingIdElement.getAttribute('data-meeting-id'),
                topic: document.getElementById('meeting-topic')?.textContent || 'Current Meeting',
                status: 'in_progress',
                start_time: new Date().toISOString(),
                participants_count: parseInt(participantsCount?.textContent || '0')
            };
            StorageManager.saveMeetingData(meetingData);
            startDurationTimer();
        }
    }
    
    // Initialize polls history on load
    updatePollHistory();
    
    // Setup analytics button if exists
    if (pollAnalyticsBtn) {
        pollAnalyticsBtn.addEventListener('click', showPollAnalytics);
    }
    
    // Setup export button if exists
    if (exportDataBtn) {
        exportDataBtn.addEventListener('click', exportPollData);
    }
    
    // Function to start the meeting duration timer
    function startDurationTimer() {
        if (meetingDuration) {
            updateDuration();
            durationInterval = setInterval(updateDuration, 60000); // Update every minute
        }
    }
    
    // Function to update the meeting duration display
    function updateDuration() {
        if (!meetingDuration) return;
        
        const now = new Date();
        const durationMs = now - meetingStartTime;
        const durationMinutes = Math.floor(durationMs / 60000);
        
        let durationText;
        if (durationMinutes < 60) {
            durationText = `${durationMinutes} min`;
        } else {
            const hours = Math.floor(durationMinutes / 60);
            const mins = durationMinutes % 60;
            durationText = `${hours}h ${mins}m`;
        }
        
        meetingDuration.textContent = durationText;
    }
    
    // Function to show analytics for polls
    function showPollAnalytics() {
        const stats = StorageManager.getPollStats();
        if (!stats || !pollStatsElement) return;
        
        let topicsHtml = '';
        if (stats.topicCounts) {
            // Sort topics by count (descending)
            const sortedTopics = Object.entries(stats.topicCounts)
                .sort((a, b) => b[1] - a[1]);
            
            sortedTopics.forEach(([topic, count]) => {
                const percentage = Math.round((count / stats.totalPolls) * 100);
                topicsHtml += `
                    <div class="mb-3">
                        <div class="d-flex justify-content-between mb-1">
                            <span class="fw-medium">${topic.charAt(0).toUpperCase() + topic.slice(1)}</span>
                            <span class="text-muted small">${count} polls (${percentage}%)</span>
                        </div>
                        <div class="progress" style="height: 10px;">
                            <div class="progress-bar bg-primary" role="progressbar" 
                                style="width: ${percentage}%" 
                                aria-valuenow="${percentage}" aria-valuemin="0" aria-valuemax="100"></div>
                        </div>
                    </div>
                `;
            });
        }
        
        pollStatsElement.innerHTML = `
            <div class="card shadow-sm">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h5 class="mb-0">Poll Analytics</h5>
                    <span class="badge bg-primary">${stats.totalPolls} Total Polls</span>
                </div>
                <div class="card-body">
                    <h6>Topics Distribution</h6>
                    ${topicsHtml || '<p class="text-muted">No topic data available</p>'}
                    <hr>
                    <p class="text-muted small mb-0">Data from current session only</p>
                </div>
            </div>
        `;
        
        // Show the stats with an animation
        pollStatsElement.style.display = 'block';
        pollStatsElement.classList.add('fade-in');
        
        // Add a close button
        const closeButton = document.createElement('button');
        closeButton.className = 'btn btn-sm btn-light position-absolute top-0 end-0 m-2';
        closeButton.innerHTML = '<i class="fas fa-times"></i>';
        closeButton.addEventListener('click', () => {
            pollStatsElement.classList.remove('fade-in');
            pollStatsElement.classList.add('fade-out');
            setTimeout(() => {
                pollStatsElement.style.display = 'none';
                pollStatsElement.classList.remove('fade-out');
            }, 300);
        });
        
        pollStatsElement.querySelector('.card').appendChild(closeButton);
    }
    
    // Function to export poll data as JSON
    function exportPollData() {
        const polls = StorageManager.getPollsHistory();
        if (!polls || polls.length === 0) {
            showToast('No poll data available to export', 'warning');
            return;
        }
        
        // Create export data object
        const exportData = {
            exportDate: new Date().toISOString(),
            meetingInfo: StorageManager.getMeetingData(),
            polls: polls,
            stats: StorageManager.getPollStats()
        };
        
        // Convert to JSON string
        const jsonData = JSON.stringify(exportData, null, 2);
        
        // Create a downloadable blob
        const blob = new Blob([jsonData], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        // Create a temporary link and trigger download
        const link = document.createElement('a');
        link.href = url;
        link.download = `zoom-polls-export-${new Date().toISOString().slice(0, 10)}.json`;
        document.body.appendChild(link);
        link.click();
        
        // Cleanup
        setTimeout(() => {
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        }, 100);
        
        showToast('Poll data exported successfully', 'success');
    }
    
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
                optionElement.className = 'form-check mb-3';
                optionElement.innerHTML = `
                    <input class="form-check-input" type="radio" name="pollOption" id="option${index}" value="${option}">
                    <label class="form-check-label fw-medium" for="option${index}">
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
            
            // Save poll data to local storage
            StorageManager.savePoll(data.poll);
            
            // Update poll history UI if it exists
            updatePollHistory();
        }
        
        // Update timestamp if available
        if (data.timestamp && pollTimestampElement) {
            pollTimestampElement.textContent = data.timestamp;
        }
    }
    
    // Function to update the polls history UI
    function updatePollHistory() {
        if (!pollsHistoryList) return;
        
        const polls = StorageManager.getPollsHistory();
        if (!polls || polls.length === 0) {
            pollsHistoryList.innerHTML = `
                <div class="text-center p-4 text-muted">
                    <i class="fas fa-history fa-2x mb-2"></i>
                    <p>No poll history available yet</p>
                </div>
            `;
            return;
        }
        
        // Clear existing list
        pollsHistoryList.innerHTML = '';
        
        // Add most recent 5 polls
        const recentPolls = polls.slice(-5).reverse();
        recentPolls.forEach(poll => {
            const pollItem = document.createElement('div');
            pollItem.className = 'poll-history-item p-3 border-bottom';
            
            // Format the date/time nicely
            let timeDisplay = poll.savedAt || poll.generated_at || 'Unknown time';
            if (timeDisplay !== 'Unknown time') {
                const pollDate = new Date(timeDisplay);
                timeDisplay = pollDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            }
            
            pollItem.innerHTML = `
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h6 class="mb-1 fw-bold">${poll.question}</h6>
                        <div class="small text-muted">${timeDisplay}</div>
                    </div>
                    <span class="badge bg-${poll.topic ? 'primary' : 'secondary'} text-white">
                        ${poll.topic ? poll.topic.charAt(0).toUpperCase() + poll.topic.slice(1) : 'General'}
                    </span>
                </div>
            `;
            
            // Add click event to reload this poll
            pollItem.addEventListener('click', () => {
                if (pollQuestionElement && pollOptionsElement) {
                    pollQuestionElement.textContent = poll.question;
                    pollOptionsElement.innerHTML = '';
                    
                    poll.options.forEach((option, index) => {
                        const optionElement = document.createElement('div');
                        optionElement.className = 'form-check mb-3';
                        optionElement.innerHTML = `
                            <input class="form-check-input" type="radio" name="pollOption" id="option${index}" value="${option}">
                            <label class="form-check-label fw-medium" for="option${index}">
                                ${option}
                            </label>
                        `;
                        pollOptionsElement.appendChild(optionElement);
                    });
                    
                    showToast('Historical poll loaded', 'info');
                }
            });
            
            pollsHistoryList.appendChild(pollItem);
        });
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
