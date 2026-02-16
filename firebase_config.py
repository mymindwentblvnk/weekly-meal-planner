"""Firebase configuration for the meal planner app.

This file reads Firebase credentials from environment variables.
DO NOT commit actual credentials to git.
"""

import os

# Firebase configuration - Read from environment variables
FIREBASE_CONFIG = {
    'apiKey': os.environ.get('FIREBASE_API_KEY', 'AIzaSyCk59CMEVd1c1jhj9FJUghUf6qUr8bdVt0'),
    'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN', 'weekly-meal-planner-12eec.firebaseapp.com'),
    'projectId': os.environ.get('FIREBASE_PROJECT_ID', 'weekly-meal-planner-12eec'),
    'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET', 'weekly-meal-planner-12eec.firebasestorage.app'),
    'messagingSenderId': os.environ.get('FIREBASE_MESSAGING_SENDER_ID', '800656898079'),
    'appId': os.environ.get('FIREBASE_APP_ID', '1:800656898079:web:aadf75b4bd50aedbe0fd2a'),
    'measurementId': os.environ.get('FIREBASE_MEASUREMENT_ID', 'G-5GHSNVM91G')
}


def get_firebase_config_js() -> str:
    """Generate JavaScript code for Firebase configuration.

    Returns:
        JavaScript code string that initializes Firebase
    """
    return f"""
// Firebase configuration
const firebaseConfig = {{
    apiKey: "{FIREBASE_CONFIG['apiKey']}",
    authDomain: "{FIREBASE_CONFIG['authDomain']}",
    projectId: "{FIREBASE_CONFIG['projectId']}",
    storageBucket: "{FIREBASE_CONFIG['storageBucket']}",
    messagingSenderId: "{FIREBASE_CONFIG['messagingSenderId']}",
    appId: "{FIREBASE_CONFIG['appId']}"
}};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Initialize services
const auth = firebase.auth();
const db = firebase.firestore();

// Enable offline persistence
db.enablePersistence()
    .catch((err) => {{
        if (err.code == 'failed-precondition') {{
            console.warn('Persistence failed: Multiple tabs open');
        }} else if (err.code == 'unimplemented') {{
            console.warn('Persistence not available in this browser');
        }}
    }});

// Configure Google Auth Provider
const googleProvider = new firebase.auth.GoogleAuthProvider();
"""


def get_firebase_imports() -> str:
    """Generate Firebase SDK import script tags.

    Returns:
        HTML script tags for Firebase SDKs
    """
    return """
    <!-- Firebase SDKs -->
    <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-auth-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-firestore-compat.js"></script>
"""
