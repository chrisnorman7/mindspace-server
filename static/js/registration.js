const createForm = document.querySelector("#createForm")
const username = document.querySelector("#username")
const name = document.querySelector("#name")
const password = document.querySelector("#password")
const confirmPassword = document.querySelector("#confirm")

createForm.onsubmit = e => {
    if (!username.value) {
        alert("Your username cannot be blank.")
        username.focus()
    } else if (!name.value) {
        alert("Your character name must not be blank.")
        name.focus()
    } else if (!password.value) {
        alert("You must provide a password.")
        password.focus()
    } else if (password.value != confirmPassword.value) {
        alert("Your passwords do not match.")
        confirmPassword.focus()
    } else {
        return
    }
    e.preventDefault()
}
