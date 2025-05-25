<h1 align="center">📦 declpm - Declarative Package Management Made Easy 🚀</h1>

---

## ✨ Quick Start

1. **Install Requirements**  
   Make sure you have Python 3 available and the required package manager (Arch, Ubuntu, Fedora, RHEL, SUSE, Alpine).

2. **Prepare Your Package List**  
   Create a `config.conf` file (or any text file) with a list of packages you want installed, one per line.  
   Example:
   ```
   vim
   git
   curl
   ```

   You can split your package lists into multiple files and include them:
   ```
   # config.conf
   @include devtools.conf
   htop
   ```
   ```
   # devtools.conf
   gcc
   gdb
   ```

3. **Run declpm**  
   ```bash
   python3 declpm.py config.conf
   ```

   - The script detects your system's package manager and installs/removes packages to match your config.
   - Supported managers: `pacman` (Arch), `apt-get` (Ubuntu), `dnf` (Fedora), `yum` (RHEL), `zypper` (SUSE), `apk` (Alpine).

4. **State Tracking**  
   - declpm keeps track of installed packages in your `$XDG_STATE_HOME/package-mon` file.
   - On each run, it will remove packages not present in your config, keeping your system declarative!

---

## 🤔 What is declpm?

`declpm` is a simple, declarative tool for managing packages across major Linux distributions.  
Just list your desired packages, run the tool, and declpm will **sync** your system—installing missing packages and removing any not in your list!

- **Cross-distro:** Works with popular Linux package managers.
- **Declarative:** Your system matches your package list—no more drift!
- **Simple:** One file, one command, done.

---

## 🛠 Usage

```bash
python3 declpm.py <your-list.conf>
```
- `<your-list.conf>`: A plain text file listing packages to be present on your system.

#### Example
```bash
python3 declpm.py config.conf
```

---

## ⚡ Features

- Installs missing packages, removes extras
- Supports @include for modular configs
- Cross-distro support
- Tracks state for accurate removals

---

## 📄 License

MIT License – see [LICENSE](LICENSE) for details.

---

<h3 align="center">Made with ❤️ by Ernest1338</h3>
