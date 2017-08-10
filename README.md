# traffic_visualization

usage:

1. on machine to monitor traffic:
```bash
$> cd backend
$> touch db.txt
$> python output_connections.py | python send_websocket.py
```

2. on machine producing visualization:
```bash
$> cd frontend
$> python -m SimpleHTTPServer 80
```

3. navigate to http://localhost on visualization machine



other info:
makes requests to ipinfo.io
caches ip -> lat,lon info in db.txt
firewall might cause problems