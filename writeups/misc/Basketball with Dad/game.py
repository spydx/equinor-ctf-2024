import re
import socketserver
from random import shuffle
from time import sleep


FLAG = open("/opt/flag.txt", "r").read()


def dad_turn(state):
	v = state % 10
	missing = 10 - v
	
	numbers = []
	cv = 0
	for _ in range(3):
		n = min(missing - cv, 3)
		if n == 0:
			break
		cv += n
		numbers.append(n)
	
	shuffle(numbers)
	
	return state + cv, ''.join(str(i) for i in numbers)


def player_turn(state, inp):
	if inp and inp[-1] == '\n':
		inp = inp[:-1]
	
	if re.match("^[1-3]{1,3}$", inp):
		for c in inp:
			value = {
				"1": 1,
				"2": 2,
				"3": 3
			}.get(c, 1)
			state += value
	else:
		return -1
	
	return state


class MyTCPHandler(socketserver.BaseRequestHandler):
	def get_input(self):
		try:
			return self.request.recv(1024).decode()
		except:
			return ""
	
	def send_msg(self, msg, newline=b'\n'):
		self.request.sendall(msg.encode() + newline)
	
	# TCP Session entrypoint
	def handle(self):
		self.send_msg("Each round you get up to 3 shots, each shot is worth up to 3 points.")
		self.send_msg("First one to bring the score to 20 point wins.")
		self.send_msg("You start, and please beat my dad, he has gotten so cocky these last years.")
		
		state = 0
		while True:
			self.send_msg("\nEnter your shots as a series of numbers (max 3)\n> ", newline=b'')
			inp = self.get_input()
			state = player_turn(state, inp)
			
			if state == -1:
				self.send_msg("\nThose shots are illegal! Goodbye...")
				break
			
			self.send_msg(f"The total score is now {state}")
			
			if state == 20:
				self.send_msg(f"\nYou win! Here are my dads final words to you: {FLAG}")
				break
			
			self.send_msg(f"\nDads turn...")
			state, numbers = dad_turn(state)
			self.send_msg(f"Dads shoots...")
			sleep(1)
			self.send_msg(f"And he scores! {numbers}\n")
			self.send_msg(f"The total score is now {state}")
			
			if state == 20:
				self.send_msg("~~~~~~~~")
				self.send_msg(f"\nDad wins.")
				self.send_msg(f"\n'Hahaha, you are just as pathetic as my son'\n    - Dad")
				break


if __name__=='__main__':
	HOST, PORT = "0.0.0.0", 9999
	with socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
		server.serve_forever()
