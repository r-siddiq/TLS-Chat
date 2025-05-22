#!/usr/bin/python

"""Certificate Generation for CST311 Programming Assignment 4"""
__author__ = "Team 9"
__credits__ = [
    "Victor Gomez",
    "Rahim Siddiq",
    "Arielle Lauper"
]

import subprocess

# Generate a private key for the server
def generate_private_key():
    command = [
        "openssl", "genrsa", "-out", "server-key.pem", "2048"
    ]
    subprocess.run(command, check=True)

# Generate a certificate signing request (CSR) for the server with a challenge password
def generate_csr():
    command = [
        "openssl", "req", "-new", "-key", "server-key.pem", "-out", "server.csr",
        "-subj", "/C=US/ST=CA/L=LA/O=CST311/OU=Networking/CN=tpa4.chat.test",
        "-passin", "pass:CST311"  # Set the challenge password here
    ]
    subprocess.run(command, check=True)

# Generate the server certificate signed by your CA
def generate_certificate():
    command = [
        "openssl", "x509", "-req", "-in", "server.csr", "-CA", "/etc/ssl/demoCA/cacert.pem",
        "-CAkey", "/etc/ssl/demoCA/private/cakey.pem", "-CAcreateserial",
        "-out", "server-cert.pem", "-days", "365"
    ]
    subprocess.run(command, check=True)

# Update the /etc/hosts file to add server hostname and IP address
def update_hosts_file():
    entry = "10.0.1.2 tpa4.chat.test\n"
    try:
        with open("/etc/hosts", "a") as hosts_file:
            hosts_file.write(entry)
        print("/etc/hosts updated successfully.")
    except PermissionError:
        print("Permission denied: unable to write to /etc/hosts. Run as root.")

def main():
    # Update the hosts file with server IP and hostname
    update_hosts_file()
    
    # Generate private key
    generate_private_key()
    
    # Generate CSR
    generate_csr()
    
    # Generate the server certificate
    generate_certificate()
    
    print("Certificate generated successfully for server with IP 10.0.1.2")

if __name__ == "__main__":
    main()