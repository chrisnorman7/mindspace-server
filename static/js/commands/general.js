/* globals mindspace, message */

mindspace.addCommand("alert", alert)

mindspace.addCommand("title", title => document.title = title)

mindspace.addCommand("message", text => message.innerText = text)

mindspace.addCommand(
    "confirm", (
        msg, okCommand, okArgs, okKwargs, cancelCommand, cancelArgs,cancelKwargs
    ) => {
        if (confirm(msg)) {
            mindspace.sendCommand(
                {name: okCommand, args: okArgs, kwargs: okKwargs}
            )
        } else {
            mindspace.sendCommand(
            {name: cancelCommand, args: cancelArgs, kwargs: cancelKwargs}
            )
        }
    }
)
