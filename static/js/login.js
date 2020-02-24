/* globals mindspace, socketURL, loginForm, loginButton, username, password, keyboard */

let submitting = false
const oldLoginValue = loginButton.value

loginForm.onsubmit = e => {
    e.preventDefault()
    if (submitting) {
            return // Don't let them login twice.
    }
    submitting = true
    loginButton.value = "Connecting..."
    loginButton.disabled = true
    mindspace.connect(socketURL)
    mindspace.socket.onopen = () => {
            mindspace.sendCommand(
                {
                    name: "login",
                    args: [username.value, password.value]
                }
            )
    }
    mindspace.socket.onclose = () => {
        submitting = false
        loginForm.hidden = false
        keyboard.hidden = true
        loginButton.disabled = false
        loginButton.value = oldLoginValue
    }
    mindspace.socket.onerror = () => {
            mindspace.socket.onclose()
            alert("There was an error with the websocket. Please try again.")
    }
}

function loggedIn() {
    username.value = ""
    password.value = ""
    loginForm.hidden = true
    keyboard.hidden = false
    loginButton.disabled = false
    loginButton.value = oldLoginValue
    keyboard.focus()
}

this.loggedIn = loggedIn
