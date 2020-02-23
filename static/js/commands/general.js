/* globals mindspace, message */

mindspace.addCommand("alert", alert)

mindspace.addCommand("title", title => document.title = title)

mindspace.addCommand("message", text => message.innerText = text)
