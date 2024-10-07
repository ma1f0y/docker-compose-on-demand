const crypto = require('crypto');

// Function to calculate SHA-256 hash of a given input
function sha256(data) {
    return crypto.createHash('sha256').update(data).digest('hex');
}

// Function to solve the PoW (find the nonce)
function solvePoW(challenge, difficulty) {
    let nonce = 0;
    const target = '0'.repeat(difficulty);  // Create a string of zeros for the required difficulty

    while (true) {
        const hash = sha256(challenge + nonce);
        if (hash.startsWith(target)) {
            console.log(`PoW Solved! Nonce: ${nonce}, Hash: ${hash}`);
            return nonce;
        }
        nonce++;
    }
}

// Example usage:
// Example challenge received from the server
// get the challenge from user input 
const challenge = "D3HzAege2VT1mbAi"
const difficulty = 4;           // Example difficulty (leading zeros)
const nonce = solvePoW(challenge, difficulty);

console.log(`Solved nonce: ${nonce}`);

