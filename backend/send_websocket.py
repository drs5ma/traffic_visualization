from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import json
import threading
from Queue import Queue #threadsafe
import sys
from thread import start_new_thread
import time
q = Queue()

lookup = {}
host = '192.241.169.138'

def f():
    global q
    global lookup
    while True:
        try:

            line = sys.stdin.readline()
            if not line:
                continue
            line = line.strip()

            dstip,dstport,dstloc,srcip,srcport,srcloc = line.rstrip().split(' ')        

            #if srcloc not in lookup:
            #    q.put(json.dumps([srcloc]))
            #    lookup[srcloc] = srcip
            #if dstloc not in lookup:
            #    q.put(json.dumps([dstloc]))
            #    lookup[dstloc] = dstip
            if (srcloc,dstloc) not in lookup:
                q.put((srcip,srcport,srcloc,dstip,dstport,dstloc))
                lookup[(srcloc,dstloc)] = (srcip,dstip)

        except ValueError:
            continue
start_new_thread(f, ())


def h(q,lu):
    l = q.qsize()
    
    print 'unloading queue of size '+str(l)
    
    for i in range(l):
        f =q.get()
        print 'entry: '+str(f)
    lu = {}


print q.qsize()

duration  = 24*60.0 #seconds
granularity = 0.5 #seconds
steps = int(duration/granularity)




class SimpleEcho(WebSocket):
    def handleMessage(self):
        pass
            
    def handleConnected(self):
        print self.address, 'connected'
        start_new_thread(self.worker,())

    def handleClose(self):
        print self.address, 'closed'

    def worker(self):
        global lookup
        for i in range(steps+1):
            while not q.empty():
                srcip,srcport,srcloc,dstip,dstport,dstloc = q.get()
                
                self.sendMessage(str(json.dumps([{'ip':srcip,'loc':srcloc},{'ip':dstip,'loc':dstloc}])))
                port = dstport if srcip!=host else srcport
                print 'port ',port,' srcloc',srcloc,'dstloc',dstloc
            lookup = {}
            print 'emptied q',q.qsize()
            time.sleep(granularity)
        return 0
        

        
server = SimpleWebSocketServer('', 80, SimpleEcho)
server.serveforever()

