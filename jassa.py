import numpy as np
import random
import re
import threading
from multiprocessing import Pool, cpu_count
import multiprocessing as mg
#import tensorflow as tf
from passlib.hash import bcrypt
from getpass import getpass
import smtplib
import sys
import matplotlib
import nnfs
from nnfs.datasets import spiral_data
nnfs.init()
np.random.seed(0)
import math
import socket


#The goal would be to convert the random Bots to a neural network....

"""
def spiral_data(points, classes):
    X = np.zeros((points*classes, 2))
    y = np.zeros(points*classes, dtype='uint8')
    for class_number in range(classes):
        ix = range(points*class_number, points*(class_number+1))
        r = np.linspace(0.0, 1, points)  # radius
        t = np.linspace(class_number*4, (class_number+1)*4, points) + np.random.randn(points)*0.2
        X[ix] = np.c_[r*np.sin(t*2.5), r*np.cos(t*2.5)]
        y[ix] = class_number
    return X, y
import matplotlib.pyplot as plt
X,y=spiral_data(100,3)
"""

#Part 4:
class Layer_Dense:
	def __init__(self,n_inputs,n_neurons):
		self.weights = 0.1*np.random.randn(n_inputs,n_neurons)
		self.biases = np.zeros((1, n_neurons))
	def forward(self,inputs):
		self.output = np.dot(inputs,self.weights) + self.biases
class Activation_ReLU:
	def forward(self,inputs):
		self.output = np.maximum(0,inputs)
class Activation_Softmax:
	def forward(self,inputs):
		exp_values = np.exp(inputs - np.max(inputs,axis=1,keepdims=True)) # - max... for anitoverflow
		probabilities = exp_values / np.sum(exp_values,axis=1, keepdims=True)
		self.output = probabilities
class Loss:
	def calculate(self,output,y):
		sample_losses = self.forward(output,y)
		data_loss = np.mean(sample_losses)
		return data_loss
class Loss_CategoricalCrossentropy(Loss):
	def forward(self,y_pred,y_true):
		samples=len(y_pred)
		y_pred_clipped=np.clip(y_pred,1e-7,1-1e-7)
		if len(y_true.shape) == 1:
			correct_cofidences = y_pred_clipped[range(samples),y_true]
		elif len(y_true.shape) == 2:
			correct_cofidences = np.sum(y_pred_clipped*y_true, axis=1)
		negative_log_likelihoods = -np.log(correct_cofidences)
		return negative_log_likelihoods
#X,y = spiral_data(samples= 100,classes=3)
#dense1 = Layer_Dense(2,3)
#activation1 = Activation_ReLU()
#dense2 = Layer_Dense(3,3)
#activation2 = Activation_Softmax()
#dense1.forward(X)
#activation1.forward(dense1.output)
#
#dense2.forward(activation1.output)
#activation2.forward(dense2.output)
#print(activation2.output[:5])
#
#loss_function = Loss_CategoricalCrossentropy()
#loss = loss_function.calculate(activation2.output, y)
#print("Loss:" , loss)


"""
print(bcrypt.setting_kwds)
# ('salt', 'rounds', 'ident', 'truncate_error')
print(bcrypt.default_rounds)
# 12

hasher = bcrypt.using(rounds=13)  # Make it slower

password = getpass()
hashed_password = hasher.hash(password)
print(hashed_password)
# $2b$13$H9.qdcodBFCYOWDVMrjx/uT.fbKzYloMYD7Hj2ItDmEOnX5lw.BX.

# Alg Rounds  Salt (22 char)            Hash (31 char)

print(hasher.verify(password, hashed_password))
# True
"""

#port = 465  # For SSL
#password = input("Type your password and press enter: ")
#
## Create a secure SSL context
#context = ssl.create_default_context()
#
#with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#    server.login("mn05mayrhofer@gmail.com", password)







verbose = 1
cores = 6
global p1m,p2m,p3m,email1,email2,email3,password
#Gamemodes of the diffrent Players. 0 = Bot, 1 = Local, 2 = Email, 3 = Client
p1m=0
p2m=0
p3m=0
if p1m == 2 or p2m == 2 or p3m == 2:
	password = getpass()
#Put in the email addr of the players
email1=""
email2=""
email3=""



cards = ["6","7","8","9","10","Unter","Ober","Konig","Ass"]
farben = ["Schelle","Eichel","Herz", "Laub"]
deck = ["" for i in range(36)]
wertigkeit = [["Bur",20,1],["Nell",14,2],["Ass",11,3],["Konig",4,4],["Ober",3,5],["Unter",2,6],["10",10,7],["9",0,8],["8",0,9],["7",0,10],["6",0,11]]
class server:
	
	def on(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((socket.gethostname(),1234))
		s.listen(2)
		print("Server started")
		while True:
			clientsocket,address = s.accept()
			print(f"Connection from {address} has been established!")
			return clientsocket

	def msg(self,message,clientsocket,):
		clientsocket.send(bytes(str(message),"utf-8"))
	def stop(self,clientsocket):
		clientsocket.close()
	def receive(self,clientsocket):
		re = clientsocket.recv(1024)
		deco=int(re.decode("utf-8"))
		return deco


if p1m == 3 or p2m == 3 or p3m == 3:
	global s
	s = server()
	clientsocket=s.on()

	
	
def mai(content,recepient):
	mailserver = smtplib.SMTP('mtmayr.com',587)
	mailserver.ehlo()
	mailserver.starttls()
	mailserver.login('manuel@mtmayr.com', password)
	mailserver.sendmail('manuel@mtmayr.com',recepient,content)
	mailserver.quit()
	print("mail sent to: ",recepient)
def initialize_deck():
	i=0
	for x in range(len(farben)):
		for y in range(len(cards)):
			deck[i]=cards[y] + " " + farben[x]
			i += 1
	return deck
def show_deck():
	for x in range(36):
		print(deck[x])
def shuffle(deck):
	np.random.seed(random.randint(1,100000000))
	np.random.shuffle(deck)
	return deck


def init_game():
	p1=[["" for i in range(12)],0]
	p2=[["" for i in range(12)],0]
	p3=[["" for i in range(12)],0]
	tabel = [["","",""],["","",""],["","",""]]
	return tabel,p1,p2,p3
def abheben():
	i=random.randint(0,36)
	f_half=["" for i in range(i)]
	s_half=["" for i in range(36-i)]
	for x in range(i):
		f_half[x]=deck[x]
	for x in range(36-i):
		s_half[x]=deck[x+i]
	for x in range(36):
		if x < 36-i:
			deck[x]=s_half[x]
		else:
			deck[x]=f_half[x-(36-i)]



def give_cards(verbose,deck,p1,p2,p3):
	i=0
	res = re.findall(r'\w+', deck[-1])
	trumpf=res[1]
	if verbose == 1:
		print("\n",trumpf,"\n")
	cycle = ["p1","p2","p3"]
	def bsundrig(v,deck):
		farb = re.findall(r'\w+', deck[v])
		if farb == ["Unter",trumpf]:
			deck[x] = "Bur" + " " + trumpf
		if farb == ["9",trumpf]:
			deck[x] = "Nell"+ " " + trumpf
	for x in range(36):
		if i == 3:
			i = 0
		if i == 2:
			bsundrig(x,deck)
			p1[0][p1[1]]=deck[x]
			p1[1] += 1
			i=3
		if i == 1:
			bsundrig(x,deck)
			p2[0][p2[1]]=deck[x]
			p2[1] += 1
			i = 2
		if i == 0:
			bsundrig(x,deck)
			p3[0][p3[1]]=deck[x]
			p3[1] += 1
			i = 1
	
	p1[1] = 0
	p2[1] = 0
	p3[1] = 0

	p1[0]=[item.split()[0::1] for item in p1[0]]
	p2[0]=[item.split()[0::1] for item in p2[0]]
	p3[0]=[item.split()[0::1] for item in p3[0]]
	return trumpf,p1,p2,p3
def inde(liste,str):
	a=0
	for x in range(len(liste)):
		if liste[x][0] == str:
			return x
def turn(round,tabel,p1,p2,p3,verbose,trumpf):
	
	if round == 0:
		tabel = [["","",""],["","",""],["","",""]]
		global table_last
		table_last=tabel
		tabel,p1=pl1(0,tabel,p1,trumpf)
		tabel,p2=pl2(1,tabel,p2,trumpf)
		tabel,p3=pl3(2,tabel,p3,trumpf)
		if verbose == 1:
			print("Table: ",tabel,"\n")

	else: 
		def stich(tabel):
			max = [21,0]
			for y in range(3):
				for z in range(len(wertigkeit)):
					if wertigkeit[z][0] == tabel[y][0]:
						if (wertigkeit[z][2] < max[0] and tabel[0][1] == tabel[y][1]):
							max = wertigkeit[z][2],y
			if tabel[0][1] != trumpf and (tabel[1][1] == trumpf or tabel[2][1] == trumpf):
				if tabel[2][1] != trumpf:	
					max = inde(wertigkeit,tabel[max[1]][0]),1
				if tabel[1][1] != trumpf:
					max = inde(wertigkeit,tabel[max[1]][0]),2
				if tabel[2][1] == trumpf and tabel[1][1] == trumpf:
					if inde(wertigkeit,tabel[1][0]) < inde(wertigkeit,tabel[2][0]):
						max = inde(wertigkeit,tabel[1][0]),1
					else:
						max = inde(wertigkeit,tabel[2][0]),2
			return max

		def count(tabel):
			points = 0
			for q in range(3):
				points += wertigkeit[inde(wertigkeit,tabel[q][0])][1]
			return points
		max=stich(tabel)
		table_last=tabel
		if tabel[max[1]][2] == "pl1":
			p1[1] += count(tabel)
			tabel = [["","",""],["","",""],["","",""]]
			tabel,p1=pl1(0,tabel,p1,trumpf)
			tabel,p2=pl2(1,tabel,p2,trumpf)
			tabel,p3=pl3(2,tabel,p3,trumpf)
			if verbose == 1:
				print("Table: ",tabel,"\n")
			if round == 11:
				max=stich(tabel)
				p1[1] += count(tabel)
				p1[1] += 5
		elif tabel[max[1]][2] == "pl2":
			p2[1] += count(tabel)
			tabel = [["","",""],["","",""],["","",""]]
			tabel,p2=pl2(0,tabel,p2,trumpf)
			tabel,p3=pl3(1,tabel,p3,trumpf)
			tabel,p1=pl1(2,tabel,p1,trumpf)
			if verbose == 1:
				print("Table: ",tabel,"\n")
			if round == 11:
				p2[1] += 5
				p2[1] += count(tabel)
		else:
			p3[1] += count(tabel)
			tabel = [["","",""],["","",""],["","",""]]
			tabel,p3=pl3(0,tabel,p3,trumpf)
			tabel,p1=pl1(1,tabel,p1,trumpf)
			tabel,p2=pl2(2,tabel,p2,trumpf)
			if verbose == 1:
				print("Table: ",tabel,"\n")
			if round == 11:
				p3[1] += 5
				p3[1] += count(tabel)
	return tabel,p1,p2,p3
def allowed(order,p,tabel,trumpf):
	alw=[]
	if tabel[0][0] == "":
		alw=p[0].copy()
	else:
		for i in range(len(p[0])):
			if p[0][i][1] == tabel[0][1]:
				alw.append(p[0][i])

	if len(alw) == 0:
		alw=p[0]
	elif len(alw) != 0 and tabel[0][1] != trumpf and tabel[0][0] != "":
		for j in range(len(p[0])):
			if p[0][j][1] == trumpf:
				alw.append(p[0][j])
	if len(alw) == 1 and alw[0][0] == "Bur" and len(p[0]) != 1:
		alw=[]
		alw=p[0].copy()
	ab = []
	if tabel[0][1] != trumpf and tabel[1][1] == trumpf:
		length = len(alw)
		x=0
		
		while(x < length):
			if wertigkeit[inde(wertigkeit,alw[x][0])][2] > wertigkeit[inde(wertigkeit,tabel[1][0])][2] and alw[x][1] == trumpf:
				ab.append(x)
			x += 1
	err = alw.copy()
	for y in range(len(ab)):
		del err[ab[len(ab)-y-1]]
	if len(err) == 0:
		err=p[0].copy()
	return err



def plx(alw,tabel,p,order,name,x,recepient,trumpf):

	
	def intu(alw):
		intuitive=[["","",""] for i in range(len(alw))]
		for y in range(len(alw)):
			intuitive[y][0]=(alw[y][0])
			intuitive[y][1]=alw[y][1]
			intuitive[y][2]=str(y)
		return intuitive
	if x == 1:
		intuitive=intu(alw)
		print(tabel,"\n",intuitive)
		card = int(input("Pick a card: "))

	elif x == 0:
		card=random.randint(0,len(alw)-1)

	elif x == 2:
		intuitive=intu(alw)
		global table_last



		meil = """\
From: manuel@mtmayr.com
Subject: Karten
Trumpf-> %s
Last Played -> %s
What lays on the table: %s
Your available Cards: %s
Tell the sender the index of you card of choice
"""%(trumpf,table_last,tabel,intuitive)
		mai(meil,recepient)
		table_last=[]
		card = int(input("Pick a card: "))



	elif x == 3:
		intuitive=intu(alw)
		message="""
Trumpf: %s 
Last Played : %s
What lays on the table: %s
Your available Cards: %s
Write the index of your card:
"""%(trumpf,table_last,tabel,intuitive)
		s.msg(message,clientsocket)
		print("Message sent!\n")
		card = s.receive(clientsocket)




	tabel[order][0]=alw[card][0]
	tabel[order][1]=alw[card][1]
	tabel[order][2]=name
	del p[0][p[0].index(alw[card])]
	return tabel,p



def pl1(order,tabel,p1,trumpf):
	alw=allowed(order,p1,tabel,trumpf)
	tabel,p1 = plx(alw,tabel,p1,order,"pl1",p1m,email1,trumpf)
	return tabel,p1
def pl2(order,tabel,p2,trumpf):
	alw=allowed(order,p2,tabel,trumpf)
	tabel,p2 = plx(alw,tabel,p2,order,"pl2",p2m,email2,trumpf)
	return tabel,p2
def pl3(order,tabel,p3,trumpf):
	alw=allowed(order,p3,tabel,trumpf)
	tabel,p3 = plx(alw,tabel,p3,order,"pl3",p3m,email3,trumpf)
	return tabel,p3
def game_same_cards(verbose):
	tabel,p1,p2,p3=init_game()
	trumpf,p1,p2,p3=give_cards(verbose,deck,p1,p2,p3)
	for x in range(12):
		tabel,p1,p2,p3=turn(x,tabel,p1,p2,p3,verbose,trumpf)
	return p1,p2,p3	

def game(verbose):
	tabel,p1,p2,p3=init_game()
	deck=initialize_deck()
	deck=shuffle(deck)
	trumpf,p1,p2,p3=give_cards(verbose,deck,p1,p2,p3)
	for x in range(12):
		tabel,p1,p2,p3=turn(x,tabel,p1,p2,p3,verbose,trumpf)
	return p1,p2,p3	
	winner(p1[1],p2[1],p3[1],p1m,p2m,p3m)
def games(repetitions,verbose):
	deck=initialize_deck()
	deck=shuffle(deck)
	global p1_all,p2_all,p3_all
	for ahh in range(repetitions):
		p1,p2,p3=game_same_cards(verbose)
		p1_all += p1[1]
		p2_all += p2[1]
		p3_all += p3[1]
	winner(p1_all,p2_all,p3_all,p1m,p2m,p3m)
def perfect_cards(reps):
	def check(p,trumpf):
		tr=0
		bns = []
		mit = 0
		wertigkeit_tr = [["Bur",20,1],["Nell",14,2],["Ass",11,3],["Konig",4,4],["Ober",3,5],["10",10,6],["8",0,7],["7",0,8],["6",0,9]]
		for x in range(len(p[0])):
			
			if p[0][x][1] == trumpf:
				wert=wertigkeit_tr[inde(wertigkeit_tr,p[0][x][0])][2]
				bns.append(wert)
				tr += 1
				
		bns.sort()
		for y in range(tr):
			if bns[y] == y+1:
				mit += 1
		return tr, mit

	max = [0,0]
	quantity = 0
	for x in range(reps):
		tabel,p1,p2,p3=init_game2()
		deck=initialize_deck()
		deck=shuffle(deck)
		trumpf,p1,p2,p3=give_cards2(verbose,deck,p1,p2,p3)
		#print(p1)
		cp = [check(p1,trumpf),check(p2,trumpf),check(p3,trumpf)]
		for u in range(3):
			if cp[u][1] > max[0]:
				max[0] = cp[u][1]
				max[1] = cp[u][0]
			if cp[u][0] > quantity:
				quantity = cp[u][0]
	print("Die besten ", max[0],"Trümpfe und ",max[1]," Trümpfe insgesammt\nDie meisten Trümpfe: ",quantity)
class myFred(threading.Thread):
	def __init__(self,iD,name):
		threading.Thread.__init__(self)
		self.iD = iD
		self.name=name
	def run(self):
		print("Starte",self.iD)
		games(self.iD)
		print("Beende",self.iD)
def perfect_cards_threaded(reps,cores):

	threads = []
	for i in range(cores):
	  threads.append(mg.Process(target=perfect_cards, args=(int(reps/6),)))
	for t in threads:
	  t.start()
	#for t in threads:
	#  t.join()
def threaded(rounds):
	global p1_all,p2_all,p3_all
	threads = []
	for i in range(cores):
		threads.append(mg.Process(target=games, args=(int(rounds/6),verbose)))
	for t in threads:
	  	t.start()
	for t in threads:
		t.join()
def winner(p1p,p2p,p3p,p1m,p2m,p3m):
	print("pl1: ",p1p)
	print("pl2: ",p2p)
	print("pl3: ",p3p)
	meil = """\
From: manuel@mtmayr.com
Subject: Ergebnisse
Player 1: %s
Player 2: %s
Player 3: %s
"""%(p1p,p2p,p3p)
	message = """\
The Results:
Player 1: %s
Player 2: %s
Player 3: %s
"""%(p1p,p2p,p3p)
	if p1m == 2:
		mai(meil,email1)
	if p2m == 2:
		mai(meil,email2)
	if p3m == 2:
		mai(meil,email3)
	if p1m == 3 or p2m == 3 or p3m == 3:
		s.msg(message,clientsocket)
		s.stop(clientsocket)
p1_all=0
p2_all=0
p3_all=0

#games(1,verbose)
#threaded(6000)
game(verbose)
#perfect_cards_threaded(10000,cores) 

