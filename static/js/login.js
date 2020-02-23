/* globals mindspace, socketURL, loginForm, loginButton, username, password */

loginForm.onsubmit = e => {
    e.preventDefault()
    let oldLoginValue = loginButton.value
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
            username.value = ""
            username.password = ""
            loginForm.hidden = true
            loginButton.disabled = false
            loginButton.value = oldLoginValue
    }
    mindspace.socket.onclose = () => {
        loginForm.hidden = false
    }
}
