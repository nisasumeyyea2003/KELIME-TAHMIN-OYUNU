import socket

def main():
    host = "127.0.0.1"  # Sunucu IP adresi
    port = 4337  # Sunucu port numarası

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        print("Sunucuya bağlandı.")

        # Sunucudan başlangıçta tahminin ilk harfini al
        initial_guess = client_socket.recv(1024).decode()
        print("Sunucunun ilk tahmini:", initial_guess)

        # Tahminin ilk harfi K olduğundan emin ol
        if initial_guess != "K":
            print("Hata: Sunucunun ilk tahmini K değil.")
            return

        while True:
            guess = input("Kelimeyi girin: ")
            client_socket.send(guess.encode())

            result = client_socket.recv(1024).decode().strip()
            print("Sunucudan gelen sonuç:", result)

            if result.startswith("Tebrikler") or result.startswith("Üzgünüz"):
                break

if __name__ == "__main__":
    main()
