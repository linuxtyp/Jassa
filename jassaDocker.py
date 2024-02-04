import random
import re
import threading, queue
from multiprocessing import Pool, cpu_count
import multiprocessing as mg
from passlib.hash import bcrypt
from getpass import getpass
import smtplib
import sys
import math
import socket
import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import re
import time
import concurrent.futures

from multiprocessing.pool import ThreadPool

#The goal would be to convert the random Bots to a neural network....









verbose = 1
cores = 6
#returnedPoints = [0 for x in range(cores)]
#returnedPoints=[]
fastplay = True #selects the card automatically if only got one choice
#Gamemodes of the diffrent Players. 0 = Bot, 1 = Local, 2 = Email, 3 = Client
players = [0,0,0,0]


imap_server=str(sys.argv[1])#your server
your_email=str(sys.argv[2])#your email

mail_refresh = 2
MailTimeout=5*60

cycle = 2*[["pl"+str(x+1),x+1] for x in range(len(players))]

def mailsetup(players,name,your_email):
	global imap,num,username,password,mail_addr
	mail_addr=["" for x in range(len(players))]
	#print(players)
	y = True
	string=""
	#print(players,name)
	mailstr=str(sys.argv[5])
	mail_addr=mailstr.strip('][').split(',')
	#mail_addr=ast.literal_eval(sys.argv[4])
	print(mail_addr)
	for x in range(len(players)):
		if players[x] == 2:
			if name[x]!="":
				string+=name[x]+" ueber email\n"
			else:
				string+="Typ ueber email\n"
			
			while y:
				try:
					#password = getpass()
					password = sys.argv[3]
					username = your_email
					imap = imaplib.IMAP4_SSL(imap_server)
					imap.login(username, password)
					y = False
				except:
					time.sleep(2)
					y = True
			#mail_addr[x]=input("Put in the receivers mail addr.\n")
			
		if players[x]==1:
			if name[x]!="":
				string+=name[x]+" spielt local\n"
			else:
				string+="Typ spielt local\n"
		if players[x]==0:
			if name[x]!="":
				string+="Bot "+name[x]+"\n"
			else:
				string+="Noname Bot\n"
	mail="""\
From: %s
Subject: Jassa
A neus Spiel mit %s Spieler isch gstartet wora.
Es spielt mit:
%s
"""%(your_email,len(players),string)

	for i in range(len(players)):
		if mail_addr[i]!="":
			mai(mail,mail_addr[i])
		if players[i]==1:
			print(mail)
			




cards = ["6","7","8","9","10","Unter","Ober","Konig","Ass"]
farben = ["Schelle","Herz","Laub","Eichel"]
deck = ["" for i in range(36)]
wertigkeit = [["Bur",20,1],["Nell",14,2],["Ass",11,3],["Konig",4,4],["Ober",3,5],["Unter",2,6],["10",10,7],["9",0,8],["8",0,9],["7",0,10],["6",0,11]]
wertigkeit_tr = [["Bur",20,1],["Nell",14,2],["Ass",11,3],["Konig",4,4],["Ober",3,5],["10",10,6],["8",0,7],["7",0,8],["6",0,9]]
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

for x in range(len(players)):
	if players[x]==3:
		global s
		s = server()
		clientsocket=s.on()



def mai(content,recepient):
	x = 0
	while x == 0:
		try:
			
			mailserver = smtplib.SMTP(imap_server,587)
			mailserver.ehlo()
			mailserver.starttls()
			mailserver.login(your_email, password)
			#print(imap_server,your_email,password,content)
			mailserver.sendmail(your_email,recepient,content)
			mailserver.quit()
			x = 1
		except:
			x = 0
			print("Mailing to %s failed. Try again in %s seconds."%(recepient,mail_refresh))
			time.sleep(mail_refresh)
	print("mail sent to: ",recepient)
def read_mail(messages,N,imap):
	for i in range(messages, messages-N, -1):
	    # fetch the email message by ID
	    res, msg = imap.fetch(str(i), "(RFC822)")
	    for response in msg:
	        if isinstance(response, tuple):
	            # parse a bytes email into a message object
	            msg = email.message_from_bytes(response[1])
	            # decode the email subject
	            subject, encoding = decode_header(msg["Subject"])[0]
	            if isinstance(subject, bytes):
	                # if it's a bytes, decode to str
	                subject = subject.decode(encoding)
	            # decode email sender
	            From, encoding = decode_header(msg.get("From"))[0]
	            if isinstance(From, bytes):
	                From = From.decode(encoding)
	            #print("Subject:", subject)
	            #print("From:", From)
	            # if the email message is multipart
	            if msg.is_multipart():
	                # iterate over email parts
	                for part in msg.walk():
	                    # extract content type of email
	                    content_type = part.get_content_type()
	                    content_disposition = str(part.get("Content-Disposition"))
	                    try:
	                        # get the email body
	                        body = part.get_payload(decode=True).decode()
	                    except:
	                        pass
	                    if content_type == "text/plain" and "attachment" not in content_disposition:
	                        # print text/plain emails and skip attachments
	                        #print("\n",body)
	                        return body
	            else:
	                # extract content type of email
	                content_type = msg.get_content_type()
	                # get the email body
	                body = msg.get_payload(decode=True).decode()
	                if content_type == "text/plain":
	                    # print only text email parts
	                    #print(body,"else")
	                    return body
	                return body
	            #print("="*100)
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
	random.shuffle(deck)
	return deck
def cyclePlayers(cycle,playernum):
	#print(cycle)
	for x in range(playernum):
		if x + playernum +1 >= playernum*2:
			cycle[x]=cycle[playernum]
		else:
			cycle[x]=cycle[x+playernum+1]
	for x in range(playernum):
		cycle[x+playernum]=cycle[x]
	#print(cycle)
	return cycle
#class player(players):
#	def init(self):
#		return [["" for i in range(int(36/len(players)))],0]
def init_game(players):
	p =["p"+str(i+1) for i in range(len(players))]
	#print(p)
	for i in range(len(players)):
		p[i] = [["" for i in range(int(36/len(players)))],0]
	#print(p)
	tabel=[["","",""]for i in range(len(players))]
	cycle = 2*[["pl"+str(x+1),x+1] for x in range(len(players))]
	return tabel,p,cycle
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



def give_cards(verbose,deck,p,players,cycle):
	i=0
	res = re.findall(r'\w+', deck[-1])


	def find_trumpf(deck,p):
		if len(players)%2 == 0:
		
			if players[0] == 0:
				trumpf=p[0][0][random.randint(0,len(p[0][0])-1)][1]
			if players[0] == 1:
				print(p[0][0])
				x = True
				while x:
					try:
						trumpf = input("\n Des sind dine Karta. Seg Trumpf a: Schelle 0, Herz 1, Laub 2, Eichel 3: ")
						trumpf = farben[int(trumpf)]
						x=False
					except:
						x = True
			if players[0] == 2:
				num = random.randint(1,90000)
				intuitive=intu(p[0][0],"")
				meil = """\
From: %s
Subject: Trumpf
ID%s
Dine Karta: %s
Seg Trumpf a: Schelle 0, Herz 1, Laub 2, Eichel 3
Schrib di numma fo dinam Trumpf zruck.
"""%(your_email,num,intuitive)
				print(meil)
				mai(meil,mail_addr[0])
				trumpf = farben[int(waiting(num))]
			if players[0] == 3:
				trumpf=p[len(players)-1][0][random.randint(0,len(p[0][0]))][1]
				
		elif len(players)%3 == 0:
			trumpf=p[len(players)-1][0][int(36/len(players))-1][1]
			if verbose == 1:
				print(p[len(players)-1][0][int(36/len(players))-1],"hot ",cycle[len(players)-1][0])
		else:
			trumpf=deck[35].split()[0::1][1]

			#print(Gschloapft: trumpf)
		return trumpf
	def bur_nell(p,trumpf):	
		for x in range(len(players)):
			for y in range(int(36/len(players))):
				if p[x][0][y] == ["Unter",trumpf]:
					p[x][0][y] = ["Bur", trumpf]
				if p[x][0][y] == ["9",trumpf]:
					p[x][0][y] = ["Nell", trumpf]
		return p

	for x in range(len(players)):
			for y in range(int(36/len(players))):
				p[x][0][y]=deck[y+x*int(36/len(players))]
	
	for x in range(len(players)):
		p[x][0]=[item.split()[0::1] for item in p[x][0]]
	trumpf=find_trumpf(deck,p)

	p=bur_nell(p,trumpf)
	#print(p,trumpf)
	if verbose == 1:
		print("\n",trumpf,"\n")

	return trumpf,p
def inde(liste,str):
	for a in range(len(liste)):
		if liste[a][0] == str:
			return a
def stich(tabel,trumpf,players,cycle):
	cases=0
	which = 0
	max = 100,0
	#print(tabel)
	for x in range(len(players)):
		if tabel[x][1] == trumpf:
			if inde(wertigkeit,tabel[x][0]) < max[0] :
				max = inde(wertigkeit,tabel[x][0]),x
		else:
			if inde(wertigkeit,tabel[x][0]) + 19 < max[0] and tabel[0][1] == tabel[x][1]:
				max = inde(wertigkeit,tabel[x][0]) + 19,x
	which = max[1]
	#print(which,tabel,players,cycle)
	cycleIndex=100
	for i in range(len(cycle)):
		if cycle[i][0] == tabel[which][2]:
			cycleIndex=i
	if which < 11:
		#print(tabel[which][2],int(tabel[which][2][2]))
		#return cycle[cycle.index([tabel[which][2],int(tabel[which][2][2])])][1]-1####error
		#return cycle[cycle.index([tabel[which][2],])]
		return cycle.index([tabel[which][2],cycle[cycleIndex][1]])
	else:
		#return cycle[cycle.index([tabel[which][2],int(str(tabel[which][2][2])+str(tabel[which][2][3]))])][1]-1	
		return cycle.index([tabel[which][2],cycle[cycleIndex][1]])

def count(tabel,players):
	points = 0
	for q in range(len(players)):
		points += wertigkeit[inde(wertigkeit,tabel[q][0])][1]
	return points
def turn(round,tabel,verbose,trumpf,p,players,cycle):
	
	if round == 0:
		tabel=[["","",""]for i in range(len(players))]
		global table_last
		table_last = tabel
		tabel,p=pl(0,tabel,p,trumpf,round,players,cycle)
		if verbose == 1:
			print("Table: ",tabel,"\n")


		if round == int(36/len(players))-1:
			max=stich(tabel,trumpf,players,cycle)
			p[max][1] += 5
			p[max][1] += count(tabel,players)

	else: 
		table_last=tabel
		max=stich(tabel,trumpf,players,cycle)
		p[max][1] += count(tabel,players)
		tabel = tabel=[["","",""]for i in range(len(players))]
		tabel,p=pl(max,tabel,p,trumpf,round,players,cycle)
		
		
		if verbose == 1:
			print("Table: ",tabel,"\n")
		if round == int(36/len(players))-1:
			max=stich(tabel,trumpf,players,cycle)
			p[max][1] += 5
			p[max][1] += count(tabel,players)
	return tabel,p
def allowed(order,p,tabel,trumpf):
	#print(p)
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

def gen_X(trumpf,tabel,order,alw):
	order_ohe=[-1,-1,-1]
	order_ohe[order]=1
	
	def cards_to_int(cards):
		deckset = [-1 for i in range(36)]
		for x in range(len(cards)):
			if cards[x][1] == "Schelle":
				if cards[x][1] == trumpf:
					deckset[(wertigkeit_tr[inde(wertigkeit_tr,cards[x][0])][2])-1]=1
				else:
					deckset[(wertigkeit[inde(wertigkeit,cards[x][0])][2])-3]=1
			if cards[x][1] == "Herz":
				if cards[x][1] == trumpf:
					deckset[(wertigkeit_tr[inde(wertigkeit_tr,cards[x][0])][2])+8]=1
				else:
					deckset[(wertigkeit[inde(wertigkeit,cards[x][0])][2])+6]=1
			if cards[x][1] == "Laub":
				if cards[x][1] == trumpf:
					deckset[(wertigkeit_tr[inde(wertigkeit_tr,cards[x][0])][2])+17]=1
				else:
					deckset[(wertigkeit[inde(wertigkeit,cards[x][0])][2])+15]=1
			if cards[x][1] == "Eichel":
				if cards[x][1] == trumpf:
					deckset[(wertigkeit_tr[inde(wertigkeit_tr,cards[x][0])][2])+26]=1
				else:
					deckset[(wertigkeit[inde(wertigkeit,cards[x][0])][2])+24]=1
		return deckset
	#print(alw)
	deckset = cards_to_int(alw)

	X=[order,deckset]
def intu(alw,trumpf):
	sort = [["","",""] for i in range(36)]
	for x in range(len(alw)):
		if alw[x][1] == "Schelle":
			if alw[x][1] == trumpf:
				sort[(wertigkeit_tr[inde(wertigkeit_tr,alw[x][0])][2])-1]=[alw[x][0],alw[x][1],""]
			else:
				sort[(wertigkeit[inde(wertigkeit,alw[x][0])][2])-3]=[alw[x][0],alw[x][1],""]
		if alw[x][1] == "Herz":
			if alw[x][1] == trumpf:
				sort[(wertigkeit_tr[inde(wertigkeit_tr,alw[x][0])][2])+8]=[alw[x][0],alw[x][1],""]
			else:
				sort[(wertigkeit[inde(wertigkeit,alw[x][0])][2])+6]=[alw[x][0],alw[x][1],""]
		if alw[x][1] == "Laub":
			if alw[x][1] == trumpf:
				sort[(wertigkeit_tr[inde(wertigkeit_tr,alw[x][0])][2])+17]=[alw[x][0],alw[x][1],""]
			else:
				sort[(wertigkeit[inde(wertigkeit,alw[x][0])][2])+15]=[alw[x][0],alw[x][1],""]
		if alw[x][1] == "Eichel":
			if alw[x][1] == trumpf:
				sort[(wertigkeit_tr[inde(wertigkeit_tr,alw[x][0])][2])+26]=[alw[x][0],alw[x][1],""]
			else:
				sort[(wertigkeit[inde(wertigkeit,alw[x][0])][2])+24]=[alw[x][0],alw[x][1],""]
	for x in range(36):
		if sort[35-x][1] == "":
			del sort[35-x]
	for y in range(len(alw)):
		sort[y][2]=str(y)
	return sort
def plx(tabel,p,order,name,x,recepient,trumpf,runde):#name specification
	alw=allowed(order,p,tabel,trumpf)


	intuitive=intu(alw,trumpf)
	if x == 1:
		intuitive=intu(alw,trumpf)
		print(tabel,"\n",intuitive)
		card = int(input("Pick a card: "))

	elif x == 0:
		#gen_X(trumpf,tabel,order,alw)
		card=random.randint(0,len(alw)-1)

	elif x == 2:
		intuitive=intu(alw,trumpf)
		global table_last #table_last donly works sometimes
		if len(alw) > 1 or fastplay == False:
			num = random.randint(1,90000)

			meil = """\
From: %s
Subject: Karten Player %s
ID%s
Runde %s
Trumpf-> %s
Zletzt gspielt -> %s
Was ligt -> %s
Dine moeglichen Karta -> %s
Schrib da Index fo dina Karta zruck. Des isch die Zahl nebs da Karta
"""%(your_email,name,num,runde,trumpf,table_last,tabel,intuitive)
			#print(meil)
			mai(meil,recepient)
			card=waiting(num)
			num = random.randint(1,90000)
			print("\n")
		elif len(alw) == 1 and fastplay == True:
			card=0
			if verbose == 1:
				print("Player %s scipped because he had only one choice."%name)
			msg="""\
From: %s
Subject: Karten Player %s
Du bisch usglo wora weil du nur oa karta spiela hosch kuenna.
Runde %s
Trumpf: %s
Last Played: %s
What lays on the table: %s
Your Cards: %s
"""%(your_email,name,runde,trumpf,table_last,tabel,intuitive)
			mai(msg,recepient)
	elif x == 3:
		intuitive=intu(alw,trumpf)
		message="""
Trumpf: %s 
Zletscht Gspielt : %s
Was ligt: %s
Dine möglichen karta: %s
Schrib da inde fo dina Karta zruck:
"""%(trumpf,table_last,tabel,intuitive)
		s.msg(message,clientsocket)
		print("Message sent!\n")
		card = s.receive(clientsocket)


	if type(card) is str or card > len(alw)-1:
		card=random.randint(0,len(alw)-1)
		if verbose == 1:
			print("Invalid number. Chosing %s"%str(card))
	if x != 0:
		tabel[order][0]=intuitive[card][0]
		tabel[order][1]=intuitive[card][1]
		tabel[order][2]=name
		del p[0][p[0].index([intuitive[card][0],intuitive[card][1]])]
		return tabel,p
	else:
		tabel[order][0]=alw[card][0]
		tabel[order][1]=alw[card][1]
		tabel[order][2]=name
		del p[0][p[0].index([alw[card][0],alw[card][1]])]
		return tabel,p		

def waiting(num):
	idm = 0
	print("Waiting")
	counter = 0
	while int(idm) != int(num):
		N=1
		try:
			status, messages = imap.select("INBOX")
			messages = int(messages[0])
			body=read_mail(messages,N,imap)
			match = re.search('ID(\d+)',body)
			idm = match.group(1)
			card = body[0]
			card=int(card)
			try:
				if int(body[1])%1==0:
					card = body[0]+body[1]
					card=int(card)
			except:
				pass
			if card == "<":
				match = re.search('class=MsoNormal>(\d+)',body)
				card = match.group(1)
				card(int(card))
			#sys.stdout.write(".")
			#sys.stdout.flush()
		except:
			pass
			#sys.stdout.write("X")
			#sys.stdout.flush()

		time.sleep(mail_refresh)
		
		if counter*mail_refresh>MailTimeout:
			print("\nTimeout\n")
			return 0
		counter +=1
	print(card)
	return card
def pl(order,tabel,p,trumpf,runde,players,cycle):
	for x in range(len(players)):
		tabel,p[cycle[x+order][1]-1] = plx(tabel,p[cycle[x+order][1]-1],cycle[x][1]-1,cycle[x+order][0],players[cycle[x+order][1]-1],mail_addr[cycle[x+order][1]-1],trumpf,runde)
	return tabel,p

def game_same_cards(verbose):
	tabel,p,cycle=init_game(players)
	trumpf,p=give_cards(verbose,deck,p,players,cycle)
	for x in range(len(p[0][0])):
		tabel,p=turn(x,tabel,verbose,trumpf,p,players,cycle)
	return p

def game(verbose,playernum,players,name):
	tabel,p,cycle=init_game(players)
	deck = initialize_deck()
	deck=shuffle(deck)
	cycle = 2*[["pl"+str(x+1),x+1] for x in range(len(players))]
	for x in range(len(players)):
		if name[x]!="":
			cycle[x][0] = name[x]
	#print(cycle)
	#print(players,cycle)
	#cyclePlayers(cycle,playernum):
	trumpf,p=give_cards(verbose,deck,p,players,cycle)
	for x in range(len(p[0][0])):
		tabel,p=turn(x,tabel,verbose,trumpf,p,players,cycle)
	#print(p,players)
	winner(p,players,name)
	#for x in range(len(players)):
	#	if players[x] != 0:
	#		winner(p,players,name)
			
	result = ""
	if verbose == 1:
		#for x in range(playernum):
		#	if x != playernum-1:
		#		result += str(x+1)+" Player: "+str(p[x][1])+", "
		#	else:
		#		result += str(x+1)+" Player: "+str(p[x][1])+"\n"
		#print(result)
		pass
	return p
def games(repetitions,verbose,playernum):
	deck=initialize_deck()
	deck=shuffle(deck)
	for ahh in range(repetitions):
		p=game_same_cards(verbose)
	for x in range(playernum):
		returnedPoints[x] += p[x][1]
def perfect_cards(reps):
	def check(p,trumpf):
		tr=0
		bns = []
		mit = 0
		
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
		tabel,p1,p2,p3=init_game()
		deck=initialize_deck()
		deck=shuffle(deck)
		trumpf,p1,p2,p3=give_cards(verbose,deck,p1,p2,p3,players,cycle)
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
def gamesDiffrentCards(repetitions,verbose,playernum,save):
	#global returnedPoints
	#returnedPoints = [0 for x in range(playernum)]
	#returnedPoints.append([])
	combined = [0 for x in range(playernum)]
	deck=initialize_deck()
	deck=shuffle(deck)
	for ahh in range(repetitions):
		p=game(verbose,playernum)
		for x in range(playernum):
			combined[x] += p[x][1]
			#q.put(p[x][1])
			#returnedPoints[index]="hello"
			#returnedPoints[len(returnedPoints-1)] += p[x][1]
	#print(combined)
	x = 0
	while x == 0:
		try:

			with open("points.txt", 'a') as f:
				f.write(str(combined)+"|")
			x=1
		except:
			x=0
	return combined
def threaded(rounds,playernum):
	global p1_all,p2_all,p3_all
	#global returnedPoints
	pool = ThreadPool(processes=cores)
	returnedPoints = [None]*cores
	threads = []
	#q = queue.Queue()
	#for x in range(cores):
	#	returnedPoints = pool.apply_async(gamesDiffrentCards, (int(rounds/6),verbose,playernum,returnedPoints,0))
	for i in range(cores):
		threads.append(mg.Process(target=gamesDiffrentCards, args=(int(rounds/6),verbose,playernum,1)))
	for t in threads:
	  	t.start()
	for t in threads:
		t.join()
	with open("points.txt", 'r') as f:
		data=f.read()
	with open("points.txt", 'w') as f:
		points=f.write("")

	
	#print(data)
	data_into_list = data.split("|")
	#print(data_into_list,"\n")

	real=[]
	data_into_list.remove("")
	for x in range(len(data_into_list)):
		#data_into_list[x]=list(data_into_list[x])
		real.append(data_into_list[x].strip('][').split(', '))
	for y in range(len(real)):
		for x in range(len(real[0])):
			try:
				real[y][x]=int(real[y][x])
			except:
				pass
	#print(real)
	combinedP=[0 for x in range(len(real[0]))]
	#print(combinedP)
	for i in range(len(real)):
		for j in range(len(real[i])):
			combinedP[j]+=real[i][j]
	#print(combinedP)
	#with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
	#	for x in range(cores):
	#		future = executor.submit(gamesDiffrentCards,int(rounds/6),verbose,playernum)
	#		return_value = future.result()
	#	print(return_value)
	#print(future.result())
	#executor = ThreadPoolExecutor(max_workers=3)
	#executor.submit(gamesDiffrentCards,int(rounds/6),verbose,playernum)
	#executor.submit(gamesDiffrentCards,int(rounds/6),verbose,playernum)
	#executor.submit(gamesDiffrentCards,int(rounds/6),verbose,playernum)
	#print(t.join(returnedPoints))
	#print(returnedPoints.get())
	#return returnedPoints.get()
	return combinedP
def winner(p,players,name):
	meil = """\
From: %s
Subject: Ergebnisse
"""%(your_email)
	for x in range(len(players)):
		#print("pl",x," :",p[x][1])
		#print(player)
		#print(meil)
		if name[x]!="":
			meil=meil + str(name[x]+"-> "+str(p[x][1])+"\n")
		else:
			meil=meil + str("pl"+str(x+1)+"-> "+str(p[x][1])+"\n")
	print(meil)
	#print(meil)
	for x in range(len(players)):
		if players[x] == 2:
			mai(meil,mail_addr[x])
		if players[x]==3:
			s.msg(meil,clientsocket)
			s.stop(clientsocket)
def steigerSim(goal,playernum,wisa,out,reps,startingP,verbose):
	stats = [0,0]

	for x in range(reps):
		pl=[0 for x in range(playernum)]
		register = [ 0 for x in range(playernum)]
		cycle = 2*[["pl"+str(x+1),x+1] for x in range(playernum)]
		if startingP == 514:
			gegnerP=0
		else:
			gegnerP=(157-(startingP/2))*2
		team = [startingP+wisa,gegnerP]
		while (team[0] < goal) and (team[1] < 1000):
			tabel,p,cycle=init_game(pl)
			deck = initialize_deck()
			deck=shuffle(deck)
			trumpf,p=give_cards(verbose,deck,p,pl,cycle)
			#print(p)
			for x in range(len(p[0][0])):
				tabel,p=turn(x,tabel,verbose,trumpf,p,pl,cycle)
			#combinedP=threaded(reps,playernum)
			if team[0] != 0 or team[1] != 0:
				cycle=cyclePlayers(cycle,playernum)
			#if out == 1:
				#print(cycle)
			rng = random.randint(0,3)
			haus = 1
			if rng == 0:
				haus = 2
			for i in range(playernum):
				if i%2 == 0:
					#team[1]+=combinedP[i]*haus
					team[1]+=p[i][1]*haus
				else:
					#team[0]+=combinedP[i]*haus
					team[0] += p[i][1]*haus
		#if out == 1:
		#print(team)
		if team[0] > goal and team[1] > 1000:
			if team[0]-goal > team[1] - 1000:
				stats[0] += 1
			else:
				stats[1] += 1
		elif team[0] > goal:
			stats[0] += 1
		else:
			stats[1] += 1
	percent = int((stats[0]/reps)*100)
	if out == 1:
		print(stats[0]," steiger wins	",stats[1]," gegner wins")
		print("\n",percent,"% Gewinnchance als Steiger mit ",playernum," Spieler uf ",goal,"\n")
		

	x = 0
	while x == 0:
		try:
			with open("points.txt", 'a') as f:
				f.write(str(percent)+"|")
			x=1
		except:
			x=0
	return percent

def myround(x, toleranz,goal):
    if x >= goal-toleranz and x <= goal+toleranz:
    	x=goal
    return x
def steigerSimThreaded(istarting,pl,wisa,out,reps,startingP):
	pool = ThreadPool(processes=cores)
	returnedPoints = [None]*cores
	threads = []
	for i in range(cores):
		threads.append(mg.Process(target=steigerSim, args=(istarting,pl,wisa,0,int(reps/6),startingP,0)))
	for t in threads:
	  	t.start()
	for t in threads:
		t.join()
	with open("points.txt", 'r') as f:
		data=f.read()
	with open("points.txt", 'w') as f:
		points=f.write("")

	
	#print(data)
	data_into_list = data.split("|")
	#print(data_into_list,"\n")

	real=[]
	data_into_list.remove("")
	#for x in range(len(data_into_list)):
		#data_into_list[x]=list(data_into_list[x])
		#real.append(data_into_list.split(', '))
	for x in range(len(data_into_list)):
		try:
			data_into_list[x]=int(data_into_list[x])
			#print(data_into_list[x])
		except:
			pass
	#print(data_into_list)
	combinedP=0
	#print(combinedP)
	for j in range(len(data_into_list)):
		combinedP+=data_into_list[j]
	combinedP=combinedP/cores
	#print(combinedP,"%")
	print("\n",combinedP,"% Gewinnchance als Steiger mit ",pl," Spieler uf ",istarting,"\n")
	return combinedP
def breakEven(players,percent,wisa,starting,reps,startingP):
	chances = 0
	toleranz = 3
	while myround(chances,toleranz,percent) != percent:

		#threadChances = [0 for x in range(cores)]
		#results=[]
		#for j in range(players):
			#pool = ThreadPool(processes=cores)
			#threadChances = [None]*cores
			#result = pool.apply_async(steigerSim, (starting,players,40,0,reps))
			#chances += threadChances.get()
			#results.append(result)
			#print(chances)
		#[result.wait() for result in results]
		#for x in range(cores):
		#	print(results[x])
		#print(threadChances)
		#for x in range(cores):
		#chances += threadChances[x]
		#chances = chances/cores
		#print(chances)
		#chances = steigerSim(starting,players,wisa,1,reps,startingP)
		chances = int(steigerSimThreaded(starting,players,wisa,0,reps,startingP))
		print("\n",chances,"% Gewinnchance als Steiger mit ",players," Spieler uf ",starting,"\n")
		if chances == myround(percent,toleranz,percent):
			pass
		elif chances > myround(percent,toleranz,percent):
			starting += 5
		elif chances < myround(percent,toleranz,percent):
			starting -= 5
	print(starting)
def default(text,defa):
	inp = input(text)
	if inp=="":
		return defa
	else:
		try:
			return int(inp)
		except:
			return defa
def names(text,defa):
	inp = input(text)
	#print(defa)
	if inp=="":
		return defa[0],defa[1]
	else:
		try:
			return int(inp.split(" ")[0]),inp.split(" ")[1]
		except:
			try:
				return int(inp),""
			except:
				return defa[0],defa[1]
def menu(your_email):
	global imap,num,username,password,mail_addr
	mail_addr=["" for x in range(36)]
	inp = -1
	players = [0 for x in range(3)]
	while inp != "0":
		inp = input("0: Exit\n1: Settings\n2: Gewinnchance für steiger berechnen\n3: Steigernde punkte für a spezifische gewinnchance berechnen\n4: Einzelnes Spiel simuliera ")
		if inp == "1":
			sett=1
			while sett != 0:
				sett = input("1: Enable Email: ")
				if sett == 1:
					mailsetup(players)
					mail_refresh = 4
		if inp == "2":
			pl = default("Wie vile spieler? ",3)
			starting = default("Uf wie viel punkte söllan die chancen berechnet wöra? ",1000)
			wisa = default("Wie viel punkte wöran in da ersta runde gwisa? ",40)
			reps = default("Wie viel steiger? (umse mehr umso sicherer des ergebnis) ",1000)
			startingP = default("Punkte ida 1. Runde(default match 514 P) ",514)
			print("Spieler %s, Wis: %s, reps: %s, Punkte: %s, Punkte ida ersta Runde: %s"%(pl,wisa,reps,starting,startingP))
			
			steigerSimThreaded(starting,pl,wisa,1,reps,startingP)
		if inp == "3":
			pl = default("Wie vile spieler? ",3)
			ziel = default("Was für a gewinnchance? ",50)
			starting = default("Startpunkt der Berechnung? ",1000)
			wisa = default("Wie viel punkte wöran in da ersta runde gwisa? ",40)
			reps = default("Wie viel steiger pro wiederholung? (umse mehr umso sicherer der ergebnis) ",200)
			startingP = default("Punkte ida 1. Runde(default match 514 P) ",514)
			print("Spieler %s,Gewinnchance: %s Wis: %s, reps: %s, Start: %s, Punkte ida ersta Runde: %s"%(pl,ziel,wisa,reps,starting,startingP))
			
			breakEven(pl,ziel,wisa,starting,reps,startingP)

		if inp == "4":
			pl = default("Wie vile spieler? ",3)
			name=[0 for x in range(pl)]
			players=[0 for x in range(pl)]
			for x in range(pl):
				players[x],name[x]=names("Playermode: 0:Bot 1:Local 2: Email 3: Client ",[0,""])
			mailsetup(players,name,your_email)
			#print(name)
			#print(players)
			game(1,len(players),players,name)
#menu(your_email)

pla = int(sys.argv[4])
print(sys.argv[4])
name=[0 for x in range(pla)]
players=[0 for x in range(pla)]
for x in range(pla):
	#players[x],name[x]=names("Playermode: 0:Bot 1:Local 2: Email 3: Client ",[0,""])
	players[x]=2
	name[x]="Typ "+ str(x)
mailsetup(players,name,your_email)
#print(name)
#print(players)
game(1,len(players),players,name)
