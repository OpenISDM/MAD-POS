import subprocess

# child = subprocess.Popen(["./ngrok","-log=stdout",\
# 	"-subdomain=testingqwer","-authtoken","W_0D4KY5as11SvSupBMT","80"],stdout= subprocess.PIPE)

# child = subprocess.Popen(["ping","-c","5","www.google.com"],stdout= subprocess.PIPE)

# child = subprocess.Popen(["./ngrok -log=stdout 80&"],shell=True)
child = subprocess.Popen(["nohup","./ngrok","-log=stdout",\
	"-subdomain=testing546asdfasdf","-authtoken","W_0D4KY5as11SvSupBMT","80"])

print("codsdfsd")
