# Subnet Addressing and TLS-Enabled Group Chat

This project combines network configuration using Mininet with the development of a TLS-enabled group chat system.

---

## ⚙️ Components

- **Custom Mininet Topology:** Subnetted, multi-router network setup using `legacy_network.py`.
- **TLS-Enabled Chat Service:** A multi-client server built from the TCP chat service in Assignment 3.
- **Certificate Generation:** OpenSSL-driven, auto-signed server certificate using `certificate_generation.py`.

---

## 🖥️ System Requirements

This project is intended to run inside an **Oracle VirtualBox VM** with a **Ubuntu-based Linux OS**.

### Recommended VM Configuration:

- **OS:** Ubuntu 20.04+
- **Memory:** 2 GB+
- **Disk:** 10 GB+
- **Root Access:** Required

### Software Dependencies

Install the following inside your VM:

```bash
sudo apt-get update
sudo apt-get install mininet xterm openssl python3-pip
```

---

## 🛠️ Setup Instructions

### 1. Generate TLS Certificates

Run this before launching Mininet:

```bash
sudo -E python3 certificate_generation.py
```

- **Common name:** `tpa4.chat.test`  
- **Passphrase:** `CST311`  
- This updates `/etc/hosts` and creates `server-key.pem` and `server-cert.pem`.

---

### 2. Launch the Network

Start the Mininet topology and open chat terminals:

```bash
sudo -E python3 legacy_network.py
```

This script will:

- Configure all hosts and routers
- Assign IP addresses and static routes
- Auto-launch:
  - `tpa4_chat_server.py` on `h4`
  - `tpa4_chat_client.py` on `h1`, `h2`, and `h3` via `xterm`

---

### 3. Verify Network Connectivity

In the Mininet CLI, run:

```bash
pingall
```

✅ All hosts should successfully reach each other.

---

### 4. Chat Application Behavior

- **Server:** Runs on `h4` (`10.0.1.2`) and listens on port `12000`
- **Clients:** Run on `h1`, `h2`, and `h3`, each in its own terminal
- **Communication:** Encrypted using TLS with a self-signed certificate
- **Termination:** Typing `bye` closes the client session

---

## 📚 References

- [Mininet](https://github.com/mininet/mininet)
- [Python TLS Socket Programming](https://docs.python.org/3/library/ssl.html)
- [OpenSSL Manual](https://www.openssl.org/docs/)
