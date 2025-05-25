#!/usr/bin/python3

import argparse
import os
import pickle

STATE_FILE = os.environ["XDG_STATE_HOME"] + "/package-mon"
GREEN = "\x1b[32m"
RESET = "\x1b[00m"

def preproces_includes(lines, dirname):
    for (i, line) in enumerate(lines):
        if line.startswith("@include"):
            filename = line.split()[1]
            new_lines = open(os.path.join(dirname, filename), "r").readlines()
            lines = lines[:i] + new_lines + lines[i+1:]
    return lines


def get_packages(file="config.conf"):
    abs_path = os.path.abspath(file)
    dirname =os.path.dirname(abs_path)
    lines = open(file, "r").readlines()
    lines = preproces_includes(lines, dirname)
    packages = []
    for line in lines:
        if line.strip() != "" and not line.strip().startswith("#"):
            packages.append(line.strip())

    return packages

def main():
    parser = argparse.ArgumentParser(description="Declarative package management made easy.")
    parser.add_argument("filename", help="The name of the file to process")
    args = parser.parse_args()

    packages = get_packages(args.filename)

    to_remove = []

    # Detect package manager
    if os.path.exists("/usr/bin/pacman"):
        pkg_mgr = "arch"
    elif os.path.exists("/usr/bin/apt-get"):
        pkg_mgr = "ubuntu"
    elif os.path.exists("/usr/bin/dnf"):
        pkg_mgr = "fedora"
    elif os.path.exists("/usr/bin/yum"):
        pkg_mgr = "rhel"
    elif os.path.exists("/usr/bin/zypper"):
        pkg_mgr = "suse"
    elif os.path.exists("/sbin/apk") or os.path.exists("/usr/bin/apk"):
        pkg_mgr = "alpine"
    else:
        print("Unsupported system: supported package managers are pacman, apt, dnf, yum, zypper, apk.")
        return

    # If state file exists - append to_remove by comparing file and packages var
    try:
        state_pkgs = pickle.loads(open(STATE_FILE, "rb").read())
        for pkg in state_pkgs:
            if pkg not in packages:
                to_remove.append(pkg)
    except:
        pass

    # Uninstall removed packages
    if len(to_remove) != 0:
        if pkg_mgr == "arch":
            cmd = f"sudo pacman -R {' '.join(to_remove)}"
        elif pkg_mgr == "ubuntu":
            cmd = f"sudo apt-get remove -y {' '.join(to_remove)}"
        elif pkg_mgr == "fedora":
            cmd = f"sudo dnf remove -y {' '.join(to_remove)}"
        elif pkg_mgr == "rhel":
            cmd = f"sudo yum remove -y {' '.join(to_remove)}"
        elif pkg_mgr == "suse":
            cmd = f"sudo zypper rm -y {' '.join(to_remove)}"
        elif pkg_mgr == "alpine":
            cmd = f"sudo apk del {' '.join(to_remove)}"
        print(f"{GREEN}[+] Running: {cmd}{RESET}")
        os.system(cmd)

    # Sync packages
    if len(packages) != 0:
        if pkg_mgr == "arch":
            cmd = f"sudo pacman -S --needed {' '.join(packages)}"
        elif pkg_mgr == "ubuntu":
            cmd = f"sudo apt-get install -y {' '.join(packages)}"
        elif pkg_mgr == "fedora":
            cmd = f"sudo dnf install -y {' '.join(packages)}"
        elif pkg_mgr == "rhel":
            cmd = f"sudo yum install -y {' '.join(packages)}"
        elif pkg_mgr == "suse":
            cmd = f"sudo zypper in -y {' '.join(packages)}"
        elif pkg_mgr == "alpine":
            cmd = f"sudo apk add {' '.join(packages)}"
        print(f"{GREEN}[+] Running: {cmd}{RESET}")
        os.system(cmd)

    # Save packages to state file (state/package-mon) - pickle
    open(STATE_FILE, "wb").write(pickle.dumps(packages))

    print(f"{GREEN}[+] Sync complete{RESET}")


if __name__=="__main__":
    main()
