#!/usr/bin/python3

import argparse
import os
import pickle

STATE_FILE = os.environ["XDG_STATE_HOME"] + "/package-mon"
GREEN = "\x1b[32m"
RESET = "\x1b[00m"

def preproces_includes(lines):
    for (i, line) in enumerate(lines):
        if line.startswith("@include"):
            filename = line.split()[1]
            new_lines = open(filename, "r").readlines()
            lines = lines[:i] + new_lines + lines[i+1:]
    return lines


def get_packages(file="config.conf"):
    lines = open(file, "r").readlines()
    lines = preproces_includes(lines)
    packages = []
    for line in lines:
        if line.strip() != "" and not line.strip().startswith("#"):
            packages.append(line.strip())

    return packages

def main():
    parser = argparse.ArgumentParser(description="Declarative arch package management")
    parser.add_argument("filename", help="The name of the file to process")
    args = parser.parse_args()

    packages = get_packages(args.filename)

    to_remove = []

    # If state file exists - append to_remove by comparing file and packages var
    try:
        state_pkgs = pickle.loads(open(STATE_FILE, "rb").read())
        for pkg in state_pkgs:
            if pkg not in packages:
                to_remove.append(pkg)
    except:
        pass

    # Uninstall removed packages
    # If file didn't exist (initial launch) arr will be empty so nothing to remove
    if len(to_remove) != 0:
        cmd = f"sudo pacman -R {' '.join(to_remove)}"
        print(f"{GREEN}[+] Running: {cmd}{RESET}")
        os.system(cmd)

    # Sync packages
    if len(packages) != 0:
        cmd = f"sudo pacman -S --needed {' '.join(packages)}"
        print(f"{GREEN}[+] Running: {cmd}{RESET}")
        os.system(cmd)

    # Save packages to state file (state/package-mon) - pickle
    open(STATE_FILE, "wb").write(pickle.dumps(packages))

    print(f"{GREEN}[+] Sync complete{RESET}")


if __name__=="__main__":
    main()
