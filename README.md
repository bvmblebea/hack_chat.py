# hackchat.py
Web-API for [hack.chat](https://hack.chat) chatroom app
![](https://raw.githubusercontent.com/AndrewBelt/hack.chat/master/screenshot.png)

## Example
```python3
# simple welcome bot
import hackchat

def welcome_user(hcclient: hackchat.HackChatClient, message: str, user: str):
    if "hello" in message.lower():
        hcclient.send_message(f"Wassup {user}!")
        print(f"-- Greeted the user::: {user}!")
        
hcclient = hackchat.HackChatClient(nickname="WelcomeBot", channel="programming")
hcclient.messages += [welcome_user]
hcclient.on_message()
```
