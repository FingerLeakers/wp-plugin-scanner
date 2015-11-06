import urllib2
import threading
import sys

dirs 		= []
plugins		= []
class brouteforce(threading.Thread):
	def __init__(self,url,file):
		threading.Thread.__init__(self)
		self.url 	= url
		self.file	= file
	def run(self):
		checkdir(self.url,self.file)

def checkdir(url,file):
	global dirs
	site 	= url
	while True:
		try:
			dir	= file.readline().replace('\n','')
			if(dir == ''):
				break
		except:
			break
		

		addr 	= url + '/wp-content/plugins/' + dir + '/'
		request	= urllib2.Request(addr)
		request.add_header('User-agent','Mozila 5.10')
		while True:
			try:
				request = urllib2.urlopen(request,timeout=60)
			
				if(request.code == 200):
					print "[+] "+addr
					if(len(dir.split('.')) == 1):
						dirs.append(dir)
				break

					
			except urllib2.URLError, e:
				try:
					if(e.code == 200):
						print "[+] "+addr
						if(len(dir.split('.')) == 1):
							dirs.append(dir)
					break
				except:
					pass


def find_between( s, first, last ,pointer):
    try:
        start = s.index(first, pointer) + len( first )
        end = s.index(last, start)
        return (s[start:end],end)
    except ValueError:
        return ("",0)
def update():
	global plugins
	plugin 	= ''
	pointer = 0
	for i in range(1,10):
		while True:
			url 	= 'http://wordpress.org/plugins/browse/popular/page/'+str(i)+'/'
			request	= urllib2.Request(url)
			request.add_header('User-agent','Mozila 5.10')
			try:
				request = urllib2.urlopen(request,timeout=60)
				html 	= request.read()
				while True:
					(plugin,pointer) = find_between(html,'<h4><a href="https://wordpress.org/plugins/','/">',pointer)
					if(plugin == ""):
						break
					else:
						
						print "[+] "+plugin
						plugins.append(plugin)
				break
			except KeyboardInterrupt:
				sys.exit(0)

	file 	= open('plugin.txt','r')
	txt 	= file.read()
	file.close()
	file 	= open('plugin.txt','a')
	for i in plugins:
		if(txt.find(i) == -1):
			file.write(i+'\n')
	file.close()
	print "[+] "+str(len(plugins))+" New Plugins add to database"
def printm():
	print '''
######################################################################
###                 WORDPRESS PLUGIN SCANNER                       ###
###              PYTHON FOR PENETRATION TESTERS                    ###
######################################################################
	
	Options:
	[+] 1) Plugins Scanner
	[+] 2) Update Plugin List
	'''
def main():

	printm()
	option	= raw_input('>>> Enter Option Number: ')
	
	if(str(option) == '1'):
		url 		= raw_input('>>> Enter Site URL: ')
		threadnum	= raw_input('>>> Enter Thread Number: ')
		file 	= open('wp\\plugin.txt','r')
		threads = []
		
		for i in range(int(threadnum)):
			thread 		= brouteforce(url,file)
			thread.start()
			threads.append(thread)
		for i in threads:
			i.join()
		file.close()
	elif(str(option) == '2'):
		update()

main()
