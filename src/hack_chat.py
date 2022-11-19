import websocket
from json import dumps
from json import loads
from time import sleep
from threading import Thread

class HackChat:
	def __init__(
			self,
			nickname: str,
			password: str = None,
			channel: str = "programming") -> None:
		self.nickname = nickname
		self.password = password
		self.channel = channel
		self.on_join = []
		self.on_leave = []
		self.messages = []
		self.statistics = []
		self.online_users = []
		self.ws = websocket.create_connection("wss://hack.chat/chat-ws")
		self.send_packet(
			{
				"cmd": "join",
				"channel": self.channel,
				"nick": self.format_nickname(self.nickname, self.password)
			}
		)
		Thread(target=self.ping_thread).start()

	def send_packet(self, packet: dict) -> None:
		self.ws.send(dumps(packet))

	def format_nickname(
			self,
			nickname: str,
			password: str = None) -> str:
		if password:
			self.nickname = f"{nickname}#{password}"
		return nickname

	def send_message(self, message: str) -> None:
		self.send_packet({"cmd": "chat", "text": message})

	def send_message_to(
			self,
			nickname: str,
			message: str) -> None:
		self.send_packet(
			{"cmd": "whisper", "nick": nickname, "text": message}
		)

	def change_nickname(self, nickname: str) -> None:
		self.nickname = nickname
		self.send_packet({"cmd": "changenick", "nick": nickname})

	def move_from_channel(self, channel: str) -> None:
		self.channel = channel
		self.send_packet({"cmd": "move", "channel": channel})

	def invite_user(seld, nickname: str) -> None:
		self.send_packet({"cmd": "invite", "nick": nickname})

	def get_statistics(self) -> None:
		self.send_packet({"cmd": "stats"})

	def ban_user(self, nickname: str) -> None:
		"""
		REQUIRES:
			password - of admin or moderator
		"""
		self.send_packet({"cmd": "ban", "nick": nickname})

	def unban_user(self, user_ip: str) -> None:
		"""
		REQUIRES:
			password - of admin or moderator
		"""
		self.send_packet({"cmd": "unban", "ip": user_ip})


	def kick_user(self, nickname: str) -> None:
		"""
		REQUIRES:
			password - of admin or moderator
		"""
		self.send_packet({"cmd": "kick", "nick": nickname})

	def add_moderator(self, nickname: str) -> None:
		"""
		REQUIRES:
			password - of admin or moderator
		"""
		self.send_packet({"cmd": "addmod", "nick": nickname})

	def save_config(self) -> None:
		self.send_packet({"cmd": "saveconfig"})

	def listen(self) -> None:
		Thread(target=self.on_message).start()

	def on_message(self) -> None:
		while True:
			response = loads(self.ws.recv())
			if response["cmd"] == "chat":
				for handler in list(self.messages):
					handler(
						self,
						response["text"],
						response["nick"])
			if response["cmd"] == "onlineAdd":
				self.online_users.append(response["nick"])
				for handler in list(self.on_join):
					handler(self, response["nick"])
			if response["cmd"] == "onlineRemove":
				self.online_users.remove(response["nick"])
				for handler in list(self.on_leave):
					handler(self, response["nick"])
			if response["cmd"] == "onlineSet":
				for nickname in response["nicks"]:
					self.online_users.append(nickname)
			if response["cmd"] == "info" and response.get("type") == "whisper":
				for handler in list(self.on_whisper):
					handler(
						self,
						response["text"],
						response["from"],
						response)
			if response["cmd"] == "info" and " IPs " in response["text"]:
				for handler in list(self.statistics):
					handler(self, response["text"])

	def ping_thread(self) -> None:
		while self.ws.connected:
			self.send_packet({"cmd": "ping"})
			sleep(60)
