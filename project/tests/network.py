import socket

def run_network_checks():
    results = []
    try:
        host = socket.gethostname()
        results.append({"name": "Hostname", "status": bool(host), "detail": host})
    except Exception as e:
        results.append({"name": "Hostname", "status": False, "detail": str(e)})
    return results
