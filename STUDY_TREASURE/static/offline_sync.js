/**
 * Study Treasure - Offline Score, Points & Streak Sync Manager
 * Yeh script offline hone par game/quiz ke data ko localStorage me save karti hai
 * aur internet wapas aane par automatic database me sync kar deti hai.
 */

const OFFLINE_STORAGE_KEY = 'study_treasure_pending_sync';

/**
 * Main function to call when a game or quiz is completed
 * @param {Object} payload - Data containing student_id, score, points, streak, etc.
 */
function handleGameCompletion(payload) {
    // Add a timestamp to track when it was played offline
    const dataWithTimestamp = {
        ...payload,
        timestamp: new Date().toISOString()
    };

    if (navigator.onLine) {
        // Agar internet available hai, toh direct backend par bhejo
        syncDataToServer(dataWithTimestamp);
    } else {
        // Agar offline hai, toh localStorage me queue kar lo
        saveDataLocally(dataWithTimestamp);
        console.warn("Device is offline. Score, points & streak saved locally.");
        
        // Optional: User ke liye UI alert ya notification show kar sakte hain
        if (typeof showOfflineToast === 'function') {
            showOfflineToast("Aap offline hain! Aapka progress local device par secure hai.");
        }
    }
}

/**
 * Sends the data payload to the Flask backend API
 * @param {Object} data 
 */
function syncDataToServer(data) {
    fetch('/api/sync_offline_progress', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Server sync failed');
        }
        return response.json();
    })
    .then(result => {
        console.log("Progress successfully synced with database:", result);
    })
    .catch(error => {
        console.error("Network error during sync, saving locally as fallback:", error);
        saveDataLocally(data);
    });
}

/**
 * Saves pending data into browser's localStorage
 * @param {Object} data 
 */
function saveDataLocally(data) {
    let pendingQueue = JSON.parse(localStorage.getItem(OFFLINE_STORAGE_KEY)) || [];
    pendingQueue.push(data);
    localStorage.setItem(OFFLINE_STORAGE_KEY, JSON.stringify(pendingQueue));
}

/**
 * Event Listener: Automatically triggers when internet connection is restored
 */
window.addEventListener('online', () => {
    console.log("Internet connection restored! Syncing pending offline progress...");
    let pendingQueue = JSON.parse(localStorage.getItem(OFFLINE_STORAGE_KEY)) || [];

    if (pendingQueue.length > 0) {
        // Process all stored offline records one by one
        Promise.all(pendingQueue.map(item => {
            return fetch('/api/sync_offline_progress', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(item)
            }).then(res => res.json());
        }))
        .then(() => {
            console.log("All offline scores, points & streaks successfully synced!");
            // Clear local storage queue after successful sync
            localStorage.removeItem(OFFLINE_STORAGE_KEY);
            
            if (typeof showSyncSuccessToast === 'function') {
                showSyncSuccessToast("Aapka offline progress database ke sath sync ho gaya hai!");
            }
        })
        .catch(err => {
            console.error("Error occurred while syncing batch data:", err);
        });
    }
});