# hack_chat.py
Web-API for [hack.chat](https://hack.chat) minimal, distraction-free chat application
![](https://raw.githubusercontent.com/AndrewBelt/hack.chat/master/screenshot.png)

## Example
```python3
import hack_chat

def welcome_user(hack_chat: hack_chat.HackChat, message: str, user: str):
    if "hello" in message.lower():
        hack_chat.send_message(f"Wassup {user}!")
        print(f"-- Greeted the user::: {user}!")
        
hack_chat = hackchat.HackChat(nickname="WelcomeBot", channel="programming")
hack_chat.messages += [welcome_user]
hack_chat.on_message()
```
