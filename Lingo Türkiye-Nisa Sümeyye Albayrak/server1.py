import socket

class Server:
    def __init__(self, word, attempts):
        self.target_word = word.upper()
        self.max_attempts = attempts
        self.attempts_left = self.max_attempts
        self.guessed_letters = [False] * len(self.target_word)
        self.guess_count = 0

    def process_guess(self, guess):
        guess = guess.upper()
        if len(guess) != len(self.target_word):
            return "Girilen kelimenin uzunluğu hedef kelimenin uzunluğuyla aynı olmalı."

        self.guess_count += 1

        for i in range(len(self.target_word)):
            if self.target_word[i] == guess[i]:
                self.guessed_letters[i] = True

        partial_word = ""
        for i in range(len(self.target_word)):
            if self.guessed_letters[i]:
                partial_word += self.target_word[i]
            elif guess[i] in self.target_word:
                partial_word += guess[i].lower()
            else:
                partial_word += "_"

        if partial_word == self.target_word:
            return f"Tebrikler! Kelimeyi doğru tahmin ettiniz: {self.target_word}"

        if guess != self.target_word:
            self.attempts_left -= 1
            if self.attempts_left == 0:
                return f"Üzgünüz! Hakkınız kalmadı. Doğru kelime: {self.target_word}"
            return f"Yanlış tahmin. Kalan hakkınız: {self.attempts_left}. Tahmininiz: {partial_word}"

def main():
    host = "127.0.0.1"  # Sunucu IP adresi
    port = 4337  # Sunucu port numarası

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print("Sunucu dinlemede...")

    client_socket, client_address = server_socket.accept()
    print(f"Gelen bağlantı: {client_address[0]}:{client_address[1]}")

    target_word = "KALP"
    max_attempts = 5

    server = Server(target_word, max_attempts)

    # İlk tahminin K harfi ile başlamasını sağlamak için istemciye bir mesaj gönder
    client_socket.send("K".encode())

    while True:
        guess = client_socket.recv(1024).decode().strip()
        print("Alınan tahmin:", guess)

        result = server.process_guess(guess)
        client_socket.send(result.encode())

        if result.startswith("Tebrikler") or result.startswith("Üzgünüz"):
            break

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
