# Recon: nmap port scan + gobuster directory enumeration. Run from inside scripts/.
import os
import subprocess
from datetime import datetime

TARGET = "vulnbank.org"


def scan(cmd, out_file):
    print(f"[recon] $ {' '.join(cmd)}")
    with open(out_file, "w") as f, subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as proc:
        for line in proc.stdout:
            print(line, end="")
            f.write(line)


if __name__ == "__main__":
    os.makedirs("artifacts", exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # each run gets its own file, nothing gets overwritten
    scan(["nmap", "-sV", TARGET], f"artifacts/nmap_output_{stamp}.txt")  # no -p: let nmap find open ports itself
    print()
    scan(["gobuster", "dir", "-u", f"https://{TARGET}", "-w", "wordlist.txt"], f"artifacts/gobuster_output_{stamp}.txt")
