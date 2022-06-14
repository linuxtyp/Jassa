import random
import re
import threading
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
#The goal would be to convert the random Bots to a neural network....









verbose = 1
cores = 6
#Gamemodes of the diffrent Players. 0 = Bot, 1 = Local, 2 = Email, 3 = Client
players = [0,0,0,0]
#Put in the email addr of the players
mail_addr = ["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""]

imap_server=""#your server
your_email=""#your email
mail_refresh = 4

cycle = 2*[["pl"+str(x+1),x+1] for x in range(len(players))]
for x in range(len(players)):
	if players[x] == 2:
		global imap,num
		y = True
		while y:
			try:
				password = getpass()
				username = your_email
				imap = imaplib.IMAP4_SSL(imap_server)
				imap.login(username, password)
				y = False
			except:
				time.sleep(2)
				y = True



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
			mailserver.sendmail(your_email,recepient,content)
			mailserver.quit()
			x = 1
		except:
			x = 0
			print("Mailing to %s failed. Try again in 10 seconds."% recepient)
			time.sleep(10)
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

class player():
	def init(self):
		return [["" for i in range(int(36/len(players)))],0]
def init_game():
	p =["p"+str(i+1) for i in range(len(players))]
	#print(p)
	for i in range(len(players)):
		p[i] = [["" for i in range(int(36/len(players)))],0]
	#print(p)
	tabel=[["","",""]for i in range(len(players))]
	return tabel,p
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



def give_cards(verbose,deck,p):
	i=0
	res = re.findall(r'\w+', deck[-1])


	def find_trumpf(deck,p):
		if len(players)%2 == 0:
		
			if players[0] == 0:
				trumpf=p[0][0][random.randint(0,len(p[0][0])-1)][1]
			if players[0] == 1:
				print(p[0][0])
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
				mai(meil,mail_addr[0])
				trumpf = farben[int(waiting(num))]
			if players[0] == 3:
				trumpf=p[len(players)-1][0][random.randint(0,len(p[0][0]))][1]
				
		elif len(players)%3 == 0:
			trumpf=p[len(players)-1][0][int(36/len(players))-1][1]
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
def stich(tabel,trumpf):
	cases=0
	which = 0
	max = 100,0
	for x in range(len(players)):
		if tabel[x][1] == trumpf:
			if inde(wertigkeit,tabel[x][0]) < max[0] :
				max = inde(wertigkeit,tabel[x][0]),x
		else:
			if inde(wertigkeit,tabel[x][0]) + 19 < max[0] and tabel[0][1] == tabel[x][1]:
				max = inde(wertigkeit,tabel[x][0]) + 19,x
	which = max[1]
	if which < 11:
		return cycle[cycle.index([tabel[which][2],int(tabel[which][2][2])])][1]-1
	else:
		return cycle[cycle.index([tabel[which][2],int(str(tabel[which][2][2])+str(tabel[which][2][3]))])][1]-1	

def count(tabel):
	points = 0
	for q in range(len(players)):
		points += wertigkeit[inde(wertigkeit,tabel[q][0])][1]
	return points
def turn(round,tabel,verbose,trumpf,p):
	
	if round == 0:
		tabel=[["","",""]for i in range(len(players))]
		global table_last
		table_last = tabel
		tabel,p=pl(0,tabel,p,trumpf)
		if verbose == 1:
			print("Table: ",tabel,"\n")


		if round == int(36/len(players))-1:
			max=stich(tabel,trumpf)
			p[max][1] += 5
			p[max][1] += count(tabel)

	else: 
		table_last=tabel
		max=stich(tabel,trumpf)
		p[max][1] += count(tabel)
		tabel = tabel=[["","",""]for i in range(len(players))]
		tabel,p=pl(max,tabel,p,trumpf)
		
		
		if verbose == 1:
			print("Table: ",tabel,"\n")
		if round == int(36/len(players))-1:
			max=stich(tabel,trumpf)
			p[max][1] += 5
			p[max][1] += count(tabel)
	return tabel,p
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
def plx(tabel,p,order,name,x,recepient,trumpf):
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
		num = random.randint(1,90000)



		meil = """\
From: %s
Subject: Karten
ID%s
Trumpf-> %s
Last Played -> %s
What lays on the table: %s
Your available Cards: %s
Please write back only the index of your card back soon.
"""%(your_email,num,trumpf,table_last,tabel,intuitive)
		mai(meil,recepient)
		table_last=[]
		idm = 0
		print("waiting")
		while int(idm) != int(num):

			status, messages = imap.select("INBOX")
			messages = int(messages[0])
			N=1
			body=read_mail(messages,N,imap)
			try:
				sys.stdout.write(".")
				sys.stdout.flush()
				match = re.search('ID(\d+)',body)
				idm = match.group(1)
				card = body[0]
				card=int(card)
				try:
					if int(body[1])%1==0:
						card = body[0]+body[1]
					#print(body[0]+body[1],body[0],body[1])
				except:
					pass
				if card == "<":
					match = re.search('class=MsoNormal>(\d+)',body)
					card = match.group(1)
					card=int(card)
			except:
				sys.stdout.write("X")
				sys.stdout.flush()
			time.sleep(mail_refresh)
		num = random.randint(1,90000)
		print("\n")
		
	elif x == 3:
		intuitive=intu(alw,trumpf)
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
	while int(idm) != int(num):
		status, messages = imap.select("INBOX")
		messages = int(messages[0])
		N=1
		body=read_mail(messages,N,imap)
		try:
			sys.stdout.write(".")
			sys.stdout.flush()
			match = re.search('ID(\d+)',body)
			idm = match.group(1)
			card = body[0]
			try:
				if int(body[1])%1==0:
					card = body[0]+body[1]
			except:
				pass
			if card == "<":
				match = re.search('class=MsoNormal>(\d+)',body)
				card = match.group(1)
		except:
			sys.stdout.write("X")
			sys.stdout.flush()
		time.sleep(mail_refresh)
	return card
def pl(order,tabel,p,trumpf):
	for x in range(len(players)):
		tabel,p[cycle[x+order][1]-1] = plx(tabel,p[cycle[x+order][1]-1],cycle[x][1]-1,cycle[x+order][0],players[cycle[x+order][1]-1],mail_addr[cycle[x+order][1]-1],trumpf)
	return tabel,p

def game_same_cards(verbose):
	tabel,p=init_game()
	trumpf,p=give_cards(verbose,deck,p)
	for x in range(len(p[0][0])):
		tabel,p=turn(x,tabel,verbose,trumpf,p)
	return p

def game(verbose):
	tabel,p=init_game()
	deck = initialize_deck()
	deck=shuffle(deck)
	trumpf,p=give_cards(verbose,deck,p)
	for x in range(len(p[0][0])):
		tabel,p=turn(x,tabel,verbose,trumpf,p)

	winner(p)
def games(repetitions,verbose):
	deck=initialize_deck()
	deck=shuffle(deck)
	for ahh in range(repetitions):
		p=game_same_cards(verbose)

	winner(p)
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
		trumpf,p1,p2,p3=give_cards(verbose,deck,p1,p2,p3)
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
def winner(p):
	meil = """\
From: %s
Subject: Ergebnisse
"""%(your_email)
	for x in range(len(players)):
		print("pl",x+1," :",p[x][1])
		meil=meil + str("pl"+str(x+1)+"-> "+str(p[x][1])+"\n")
	#print(meil)
	for x in range(len(players)):
		if players[x] == 2:
			mai(meil,mail_addr[x])
		if players[x]==3:
			s.msg(meil,clientsocket)
			s.stop(clientsocket)



#perfect_cards_threaded(10000,cores) 
#games(1,verbose)
#threaded(6000)
game(verbose)
