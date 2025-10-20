import socket

try:
    print(socket.gethostbyname("nspd.gov.ru"))
    print("✅ DNS работает, домен разрешается.")
except Exception as e:
    print("❌ Ошибка DNS:", e)
