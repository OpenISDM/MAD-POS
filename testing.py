import subprocess

url='subscriberadd'

subprocess.call(["./ngrok","-authtoken", \
	"W_0D4KY5as11SvSupBMT", "-subdomain=" + url, str(80)])