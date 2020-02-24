/* globals mindspace, loggedIn, title */

mindspace.addCommand("authenticated", (playerName) => {
        document.title = `${title} | ${playerName}`
        loggedIn()
})
