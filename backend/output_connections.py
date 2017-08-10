
import sys
import json
import requests
import subprocess as sub

ip_to_loc = {}
ip_to_route = {}

db = open('db.txt','r+')
for lines in db:
    ip,loc = lines.rstrip().split(' ')
    ip_to_loc[ip] = loc
db.close()
#print 'using db: ',ip_to_loc
db = open('db.txt','a')
def get_loc(ip):
    r = requests.get("http://freegeoip.net/json/"+ip)
    try:
        try:
            js= str(json.loads(r.content)['latitude'])+","+str(json.loads(r.content)['longitude'])
            loc = str(js)
            db.write(ip+' '+loc+'\n')
            return loc
        except KeyError:
            pass#print r
            #print r.content
            #print json.loads(r.content)
            return '0.0,0.0'
    except ValueError:
        if r.status_code == 404:
            print ip, "no location found for that ip"
        return "none"


def get_route(ip):
    a = []
    p = sub.Popen(('./iplookup', google), stdout=sub.PIPE)
    for row in iter(p.stdout.readline, b''):
        a.append(row.rstrip())
    return a

def get_locs(route):
    loc_route = []
    for ip in route:
        if ip not in ip_to_loc:
            loc_route.append(get_loc(ip))
        else:
            loc_route.append(ip_to_loc[ip])
    return loc_route




#route = [my_ip, ip, .. , ip]

my_ip = '192.241.169.138'
google = '172.217.3.46'

#print get_route(google)

#w = open('w.txt','w+')


p = sub.Popen(('sudo', 'tcpdump', '-l', '-n'), stdout=sub.PIPE)
#p = sub.Popen(('sudo', 'tcpdump', '-l', '-n', 'not port 22'), stdout=sub.PIPE)
for row in iter(p.stdout.readline, b''):
    #src_ip,src_port = row.rstrip().split(' ')[2].rsplit(':',1)
    #dst_ip,dst_port = row.rstrip().split(' ')[4].rsplit(':',1)
    #print src_ip, ' > ', dst_ip

    try:
        # 05:03:10.316525 IP 192.241.169.138 > 75.102.136.100: ICMP echo reply, id 57281, seq 1, length 64
        if 'IP' not in row.rstrip() or 'IP6' in row.rstrip():
            continue
        arrow = row.rstrip().split('IP ')[1].split(':')[0]
        
        
        src_ip =  arrow.split(' > ')[0]
        if src_ip.count('.')==4:
            src_ip,src_port = src_ip.rsplit('.',1)
        else:
            src_port = None
            
        dst_ip = arrow.split(' > ')[1]
        if dst_ip.count('.')==4:
            dst_ip,dst_port =  dst_ip.rsplit('.',1)
        else:
            dst_port = None

            
        if src_ip not in ip_to_loc:
            pass
            srcloc = get_loc(src_ip)
            #route = get_route(src_ip)
            #route = get_locs(route)
            #w.write(json.dumps([loc])+'\n')
            #print(json.dumps([loc])+'\n')
            #print src_ip+" "+loc
            #for r in route:
            #    w.write(json.dumps([r])+'\n')
            #w.flush()

            ip_to_loc[src_ip] = srcloc
            #ip_to_route[src_ip] = route
        else:
            #print row
            pass
            #for r in ip_to_route[src_ip]:
            #    w.write(json.dumps([r])+'\n')   
            #w.write(json.dumps([ip_to_loc[src_ip]])+'\n')
            #print src_ip+" "+ip_to_loc[src_ip]
            srcloc = ip_to_loc[src_ip]
            #print(json.dumps([ip_to_loc[src_ip]])+'\n')
            #w.flush()
            
        if dst_ip not in ip_to_loc:

            dstloc = get_loc(dst_ip)
            #route = get_route(dst_ip)
            #route = get_locs(route)
            #for r in route:
            #    w.write(json.dumps([r])+'\n')
            #print(json.dumps([loc])+'\n')
            #print dst_ip+" "+loc
            
            #w.write(json.dumps([loc])+'\n')
            
            #w.flush()

            ip_to_loc[dst_ip] = dstloc
            #ip_to_route[dst_ip] = route
        else:
            #print row#for r in ip_to_route[dst_ip]:
            #    w.write(json.dumps([r])+'\n')
            #w.write(json.dumps([ip_to_loc[dst_ip]])+'\n')
            #print(json.dumps([ip_to_loc[dst_ip]])+'\n')
            #print dst_ip+" "+ip_to_loc[dst_ip]
            dstloc = ip_to_loc[dst_ip]
            #w.flush()
        try:
            print dst_ip+" "+str(dst_port)+" "+dstloc+" "+src_ip+" "+str(src_port)+" "+srcloc
        except TypeError:
            print 'TYPE EROR'
            print row
        #print row
        sys.stdout.flush()
    except ValueError:
        pass#print 'valueerror' #row.rstrip().split(' ')[2], row.rstrip().split(' ')[4][:-1]
        #print row
    
                
#w.close()
