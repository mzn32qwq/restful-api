import subprocess

# Start the server
server_process = subprocess.Popen(["python3", "server.py"])

# Start the URL shortener
subprocess.run(["python3", "URL_short.py"])
