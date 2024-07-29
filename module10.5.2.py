import multiprocessing
import datetime


class WarehouseManager:
    def __init__(self):
        self.data = {}

    def process_request(self, request, lock):
        lock.acquire() # Метод устанавливает блокировку
        try:
            product, action, quantity = request  # продукт, действие, количество
            if action == "receipt":  # пополнение
                if product in self.data:
                    self.data[product] += quantity
                else:
                    self.data[product] = quantity
            elif action == "shipment":  # отгрузка
                if product in self.data and self.data[product] >= quantity:
                    self.data[product] -= quantity
            else:
                print("нет нужного количества товара")
        finally:
            """Метод снимает блокировку. Метод может быть вызван из любого потока,
            а не только из потока, который получил блокировку."""
            lock.release()

    # Метод run класса WarehouseManager принимает список запросов requests. Создает n(n=processes) процесс(-ов)
    def run(self, requests):
        lock = multiprocessing.Lock()
        """Записываем в data результаты процессов"""
        self.data = multiprocessing.Manager().dict()

        """Создаем список процессов для каждого запроса"""
        processes = [multiprocessing.Process(target=self.process_request, args=(i, lock)) for i in requests]

        """Цикл запускает процессы"""
        for p in processes:
            p.start()

        """Цикл останавливает процессы"""
        for p in processes:
            p.join()


if __name__ == '__main__':

    # экземпляр класса WarehouseManager
    manager = WarehouseManager()

    # инициализация списка запросов
    requests = [
        ("product1", "receipt", 100),
        ("product2", "receipt", 150),
        ("product1", "shipment", 30),
        ("product3", "receipt", 200),
        ("product2", "shipment", 50),

    ]

    start = datetime.datetime.now()
    manager.run(requests)
    end = datetime.datetime.now()
    print(manager.data)
    print(end-start)