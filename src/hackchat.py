import websocket
from time import sleep
from threading import Thread
from json import dumps, loads


class HackChatClient:
    def __init__(
            self,
            nickname: str,
            password: str = None,
            channel: str = "programming"):
        self.nickname = nickname
        self.password = password
        self.channel = channel
        self.on_join = []
        self.on_leave = []
        self.messages = []
        self.statistics = []
        self.online_users = []
        self.ws = websocket.create_connection("wss://hack.chat/chat-ws")
        self.send_packet({"cmd": "join",
                          "channel": self.channel,
                          "nick": self.format_nickname(self.nickname,
                                                       self.password)})
        Thread(target=self.ping_thread).start()

    # send packet
    def send_packet(self, packet: dict):
        self.ws.send(dumps(packet))

    def format_nickname(self, nickname: str, password: str = None):
        if password:
            self.nickname = f"{nickname}#{password}"
        return nickname

    # send message in chat
    def send_message(self, message: str):
        self.send_packet({"cmd": "chat", "text": message})

    # send message to user
    def send_message_to(self, nickname: str, message: str):
        self.send_packet({"cmd": "whisper", "nick": nickname, "text": message})

    # change current nickname to new
    def change_nickname(self, nickname: str):
        self.nickname = nickname
        self.send_packet({"cmd": "changenick", "nick": nickname})

    # moves from current channel to other channel
    def move_from_channel(self, channel: str):
        self.channel = channel
        self.send_packet({"cmd": "move", "channel": channel})

    # invites user to a randomly generated channel
    def invite_user(seld, nickname: str):
        self.send_packet({"cmd": "invite", "nick": nickname})

    # get statistics
    def get_statistics(self):
        self.send_packet({"cmd": "stats"})

    # Ban <nickname> from hack.chat for 24 hours you need moderator or admin
    # <password>
    def ban_user(self, nickname: str):
        self.send_packet({"cmd": "ban", "nick": nickname})

    # Unban <nickname> you need moder or admin <password>
    def unban_user(self, user_ip: str):
        self.send_packet({"cmd": "unban", "ip": user_ip})

    # kick user to another channel for this you need moderator <password>
    def kick_user(self, nickname: str):
        self.send_packet({"cmd": "kick", "nick": nickname})

    # Makes the user a moderator for this you need admin <password>
    def add_moderator(self, nickname: str):
        self.send_packet({"cmd": "addmod", "nick": nickname})

    # Saves hack.chat current config. Only for admins
    def save_config(self):
        self.send_packet({"cmd": "saveconfig"})

    # listen
    def listen(self):
        Thread(target=self.on_message).start()

    # on_message
    def on_message(self):
        while True:
            response = loads(self.ws.recv())
            if response["cmd"] == "chat":
                for handler in list(self.messages):
                    handler(self, response["text"], response["nick"])
            elif response["cmd"] == "onlineAdd":
                self.online_users.append(response["nick"])
                for handler in list(self.on_join):
                    handler(self, response["nick"])
            elif response["cmd"] == "onlineRemove":
                self.online_users.remove(response["nick"])
                for handler in list(self.on_leave):
                    handler(self, response["nick"])
            elif response["cmd"] == "onlineSet":
                for nickname in response["nicks"]:
                    self.online_users.append(nickname)
            elif response["cmd"] == "info" and response.get("type") == "whisper":
                for handler in list(self.on_whisper):
                    handler(self, response["text"], response["from"], response)
            elif response["cmd"] == "info" and " IPs " in response["text"]:
                for handler in list(self.statistics):
                    handler(self, response["text"])

    # ping to retain websocket connection
    def ping_thread(self):
        while self.ws.connected:
            self.send_packet({"cmd": "ping"})
            sleep(60)
