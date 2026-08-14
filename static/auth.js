import { initializeApp } from "https://www.gstatic.com/firebasejs/12.1.0/firebase-app.js";
import {
    getAuth,
    createUserWithEmailAndPassword,
    signInWithEmailAndPassword,
    signOut,
    onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/12.1.0/firebase-auth.js";


// =====================================================
// Firebase configuration
// =====================================================

  const firebaseConfig = {
    apiKey: "AIzaSyBJMVqqm1feGVjrwIOOD8jL_2m-tpjt2SU",
    authDomain: "cloudcart-e-commerce.firebaseapp.com",
    projectId: "cloudcart-e-commerce",
    storageBucket: "cloudcart-e-commerce.firebasestorage.app",
    messagingSenderId: "718678922900",
    appId: "1:718678922900:web:1ac04fd4e740b89d4e4681"
  };


// =====================================================
// Initialize Firebase
// =====================================================

const firebaseApp = initializeApp(firebaseConfig);
const auth = getAuth(firebaseApp);


// =====================================================
// Registration
// =====================================================

window.registerUser = async function () {

    const email = document.getElementById("register-email").value.trim();
    const password = document.getElementById("register-password").value;
    const confirmPassword =
        document.getElementById("register-confirm-password").value;

    const message = document.getElementById("auth-message");

    if (!email || !password || !confirmPassword) {
        message.textContent = "Please fill in all fields.";
        return;
    }

    if (password !== confirmPassword) {
        message.textContent = "Passwords do not match.";
        return;
    }

    try {

        await createUserWithEmailAndPassword(
            auth,
            email,
            password
        );

        message.textContent = "Account created successfully.";

        setTimeout(() => {
            window.location.href = "/";
        }, 1000);

    } catch (error) {

        console.error(error);

        message.textContent = getFriendlyAuthError(error);

    }
};


// =====================================================
// Login
// =====================================================

window.loginUser = async function () {

    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;

    const message = document.getElementById("auth-message");

    if (!email || !password) {
        message.textContent = "Please enter email and password.";
        return;
    }

    try {

        // Step 1: Authenticate with Firebase
        const result = await signInWithEmailAndPassword(
            auth,
            email,
            password
        );

        // Step 2: Get the authenticated Firebase user
        const user = result.user;

        // Step 3: Get Firebase ID token
        const idToken = await user.getIdToken();

        console.log("Firebase login successful.");
        console.log("User:", user.email);

        // Step 4: Send ID token to Flask backend
        const response = await fetch("/api/auth/verify", {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${idToken}`
            }
        });

        // Step 5: Read Flask response
        const data = await response.json();

        console.log("Backend authentication response:", data);

        // Step 6: Verify backend authentication
        if (!response.ok || !data.authenticated) {
            throw new Error(
                "Backend authentication verification failed."
            );
        }

        message.textContent = "Login successful.";

        // Step 7: Redirect to CloudCart homepage
        setTimeout(() => {
            window.location.href = "/";
        }, 500);

    } catch (error) {

        console.error("Authentication error:", error);

        message.textContent = getFriendlyAuthError(error);

    }
};


// =====================================================
// Logout
// =====================================================

window.logoutUser = async function () {

    try {

        await signOut(auth);

        window.location.href = "/";

    } catch (error) {

        console.error("Logout error:", error);

    }
};


// =====================================================
// Authentication state
// =====================================================

onAuthStateChanged(auth, (user) => {

    const loggedOutLinks =
        document.querySelectorAll(".logged-out");

    const loggedInLinks =
        document.querySelectorAll(".logged-in");

    const userEmail =
        document.querySelectorAll(".user-email");

    if (user) {

        loggedOutLinks.forEach(element => {
            element.style.display = "none";
        });

        loggedInLinks.forEach(element => {
            element.style.display = "inline";
        });

        userEmail.forEach(element => {
            element.textContent = user.email;
        });

        console.log("Logged in:", user.email);

    } else {

        loggedOutLinks.forEach(element => {
            element.style.display = "inline";
        });

        loggedInLinks.forEach(element => {
            element.style.display = "none";
        });

        console.log("User is not logged in.");

    }

});


// =====================================================
// Friendly Firebase errors
// =====================================================

function getFriendlyAuthError(error) {

    switch (error.code) {

        case "auth/email-already-in-use":
            return "An account already exists with this email.";

        case "auth/invalid-email":
            return "Please enter a valid email address.";

        case "auth/weak-password":
            return "Password is too weak.";

        case "auth/invalid-credential":
            return "Invalid email or password.";

        case "auth/user-not-found":
            return "No account found with this email.";

        case "auth/wrong-password":
            return "Incorrect password.";

        default:
            return "Authentication failed. Please try again.";
    }
}

// =====================================================
// Checkout authentication
// =====================================================

const checkoutForm = document.getElementById("checkout-form");

if (checkoutForm) {

    checkoutForm.addEventListener("submit", async (event) => {

        event.preventDefault();

        const message =
            document.getElementById("checkout-message");

        const user = auth.currentUser;

        // Check Firebase login
        if (!user) {

            message.textContent =
                "Please login before placing an order.";

            setTimeout(() => {
                window.location.href = "/login";
            }, 1000);

            return;
        }

        try {

            // Get Firebase ID token
            const idToken = await user.getIdToken();

            // Collect checkout form data
            const formData = new FormData(checkoutForm);

            // Send request to Flask
            const response = await fetch("/checkout", {

                method: "POST",

                headers: {
                    "Authorization": `Bearer ${idToken}`
                },

                body: formData
            });

            // Handle authentication failure
            if (response.status === 401) {

                message.textContent =
                    "Your login session is invalid. Please login again.";

                setTimeout(() => {
                    window.location.href = "/login";
                }, 1000);

                return;
            }

            // Get returned HTML
            const html = await response.text();

            // Replace current page with checkout result
            document.open();
            document.write(html);
            document.close();

        } catch (error) {

            console.error(
                "Checkout authentication error:",
                error
            );

            message.textContent =
                "Unable to place order. Please try again.";
        }

    });

}

// =====================================================
// My Orders authentication
// =====================================================

const myOrdersLink =
    document.getElementById("my-orders-link");

if (myOrdersLink) {

    myOrdersLink.addEventListener("click", async (event) => {

        event.preventDefault();

        const user = auth.currentUser;

        if (!user) {

            window.location.href = "/login";
            return;

        }

        try {

            // Get Firebase ID token
            const idToken = await user.getIdToken();

            // Request My Orders page with authentication
            const response = await fetch("/my-orders", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${idToken}`
                }
            });

            if (response.status === 401) {

                window.location.href = "/login";
                return;

            }

            if (!response.ok) {

                throw new Error(
                    "Unable to load orders."
                );

            }

            // Get rendered HTML
            const html = await response.text();

            // Display My Orders page
            document.open();
            document.write(html);
            document.close();

        } catch (error) {

            console.error(
                "My Orders error:",
                error
            );

            alert(
                "Unable to load your orders. Please try again."
            );

        }

    });

}

// =====================================================
// Individual Order Details authentication
// =====================================================

window.loadOrderDetails = async function (event, url) {

    // Prevent normal browser navigation
    event.preventDefault();

    try {

        // Get currently authenticated Firebase user
        const user = auth.currentUser;

        if (!user) {

            console.warn(
                "No authenticated Firebase user found."
            );

            window.location.href = "/login";
            return false;
        }

        console.log(
            "Loading order for:",
            user.email
        );

        // Get Firebase ID token
        const idToken = await user.getIdToken(true);

        console.log(
            "Firebase ID token obtained."
        );

        // Request order details with authentication
        const response = await fetch(
            url,
            {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${idToken}`
                }
            }
        );

        console.log(
            "Order details response:",
            response.status
        );

        if (response.status === 401) {

            alert(
                "Your login session has expired. Please login again."
            );

            window.location.href = "/login";

            return false;
        }

        if (response.status === 404) {

            alert("Order not found.");

            return false;
        }

        if (!response.ok) {

            throw new Error(
                `Order request failed: ${response.status}`
            );

        }

        // Get returned HTML
        const html = await response.text();

        // Display Order Details page
        document.open();
        document.write(html);
        document.close();

    } catch (error) {

        console.error(
            "Order details error:",
            error
        );

        alert(
            "Unable to load order details. Please try again."
        );

    }

    return false;
};

