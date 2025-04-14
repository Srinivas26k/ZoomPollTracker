/**
 * Local Storage Manager for Zoom Poll Automation
 * Handles temporary storage of meeting data and polls during a session
 */
const StorageManager = {
    // Keys for storage
    KEYS: {
        CURRENT_MEETING: 'zoom_poll_automation_meeting',
        POLLS_HISTORY: 'zoom_poll_automation_polls',
        USER_SETTINGS: 'zoom_poll_automation_settings',
        POLL_STATS: 'zoom_poll_automation_stats'
    },

    /**
     * Save meeting data to local storage
     * @param {Object} meetingData - Meeting information
     */
    saveMeetingData: function(meetingData) {
        if (!meetingData) return;
        
        try {
            localStorage.setItem(this.KEYS.CURRENT_MEETING, JSON.stringify({
                data: meetingData,
                timestamp: new Date().toISOString()
            }));
            console.log('Meeting data saved to local storage');
        } catch (error) {
            console.error('Error saving meeting data to local storage:', error);
        }
    },

    /**
     * Get current meeting data from local storage
     * @returns {Object|null} Meeting data or null if not found
     */
    getMeetingData: function() {
        try {
            const data = localStorage.getItem(this.KEYS.CURRENT_MEETING);
            if (!data) return null;
            
            return JSON.parse(data).data;
        } catch (error) {
            console.error('Error getting meeting data from local storage:', error);
            return null;
        }
    },

    /**
     * Save a poll to the polls history
     * @param {Object} pollData - Poll data to save
     */
    savePoll: function(pollData) {
        if (!pollData) return;
        
        try {
            // Get existing polls
            let polls = this.getPollsHistory();
            if (!polls) polls = [];
            
            // Add the new poll with timestamp
            pollData.savedAt = new Date().toISOString();
            polls.push(pollData);
            
            // Only keep the most recent 50 polls
            if (polls.length > 50) {
                polls = polls.slice(polls.length - 50);
            }
            
            // Save back to storage
            localStorage.setItem(this.KEYS.POLLS_HISTORY, JSON.stringify(polls));
            
            // Update statistics
            this.updatePollStats(pollData);
            
            console.log('Poll saved to history');
        } catch (error) {
            console.error('Error saving poll to history:', error);
        }
    },

    /**
     * Get polls history from local storage
     * @returns {Array|null} Array of polls or null if not found
     */
    getPollsHistory: function() {
        try {
            const data = localStorage.getItem(this.KEYS.POLLS_HISTORY);
            if (!data) return [];
            
            return JSON.parse(data);
        } catch (error) {
            console.error('Error getting polls history from local storage:', error);
            return [];
        }
    },

    /**
     * Update poll statistics based on poll data
     * @param {Object} pollData - Poll data to update statistics with
     */
    updatePollStats: function(pollData) {
        try {
            let stats = this.getPollStats();
            if (!stats) {
                stats = {
                    totalPolls: 0,
                    topicCounts: {},
                    lastUpdated: null
                };
            }
            
            // Update general stats
            stats.totalPolls += 1;
            stats.lastUpdated = new Date().toISOString();
            
            // Update topic counts
            if (pollData.topic) {
                stats.topicCounts[pollData.topic] = (stats.topicCounts[pollData.topic] || 0) + 1;
            }
            
            // Save back to storage
            localStorage.setItem(this.KEYS.POLL_STATS, JSON.stringify(stats));
        } catch (error) {
            console.error('Error updating poll statistics:', error);
        }
    },

    /**
     * Get poll statistics from local storage
     * @returns {Object|null} Poll statistics or null if not found
     */
    getPollStats: function() {
        try {
            const data = localStorage.getItem(this.KEYS.POLL_STATS);
            if (!data) return null;
            
            return JSON.parse(data);
        } catch (error) {
            console.error('Error getting poll statistics from local storage:', error);
            return null;
        }
    },

    /**
     * Save user settings to local storage
     * @param {Object} settings - User settings to save
     */
    saveUserSettings: function(settings) {
        if (!settings) return;
        
        try {
            localStorage.setItem(this.KEYS.USER_SETTINGS, JSON.stringify(settings));
            console.log('User settings saved to local storage');
        } catch (error) {
            console.error('Error saving user settings to local storage:', error);
        }
    },

    /**
     * Get user settings from local storage
     * @returns {Object|null} User settings or default settings if not found
     */
    getUserSettings: function() {
        try {
            const data = localStorage.getItem(this.KEYS.USER_SETTINGS);
            if (!data) {
                // Return default settings
                return {
                    pollInterval: 900, // 15 minutes in seconds
                    darkMode: true,
                    notificationsEnabled: true,
                    autoLaunch: true
                };
            }
            
            return JSON.parse(data);
        } catch (error) {
            console.error('Error getting user settings from local storage:', error);
            return null;
        }
    },

    /**
     * Clear all stored data (for debugging or on sign out)
     */
    clearAllData: function() {
        try {
            localStorage.removeItem(this.KEYS.CURRENT_MEETING);
            localStorage.removeItem(this.KEYS.POLLS_HISTORY);
            localStorage.removeItem(this.KEYS.POLL_STATS);
            // Don't clear user settings - keep those persistent
            console.log('All temporary data cleared from local storage');
        } catch (error) {
            console.error('Error clearing data from local storage:', error);
        }
    }
};