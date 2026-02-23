import subprocess, os, time

def kill_port(port):
    try:
        output = subprocess.check_output(f'netstat -ano | findstr :{port}', shell=True).decode()
        for line in output.splitlines():
            parts = line.split()
            if len(parts) > 4:
                pid = parts[-1]
                print(f"Killing PID {pid} on port {port}")
                subprocess.run(f'taskkill /F /PID {pid}', shell=True)
    except:
        pass

print("Cleaning port 8000...")
kill_port(8000)
time.sleep(2)

log_path = 'final_debug.log'
with open(log_path, 'w', encoding='utf-8') as f:
    f.write("Starting server process...\n")
    f.flush()
    
    # Use sys.executable to ensure we use the same python
    import sys
    cmd = [sys.executable, '-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000']
    
    proc = subprocess.Popen(cmd, stdout=f, stderr=f, cwd=os.getcwd())
    f.write(f"Launched uvicorn with PID {proc.pid}\n")
    f.flush()
    
    print("Waiting for server to start...")
    time.sleep(15) # Give it plenty of time
    
    f.write("Probing health endpoint...\n")
    f.flush()
    
    try:
        import urllib.request
        with urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=10) as response:
            status = response.getcode()
            body = response.read().decode()
            f.write(f"Health check SUCCESS: status={status}, body={body}\n")
    except Exception as e:
        f.write(f"Health check FAILED: {str(e)}\n")
    
    f.write("\nChecking if process is still alive...\n")
    if proc.poll() is None:
        f.write("Uvicorn process is still running.\n")
    else:
        f.write(f"Uvicorn process EXITED with code {proc.returncode}\n")
        # Try to read the end of the log in case of crash
        f.flush()

print("Diagnostic complete. Check final_debug.log")
