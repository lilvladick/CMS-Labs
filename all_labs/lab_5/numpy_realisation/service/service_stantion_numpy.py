import numpy as np

class ServiceStationNumPy:
    def __init__(self, sim_time_hours, arrival_rate, service_time, n_posts, queue_limit=None, seed=42):
        self.sim_time_hours = sim_time_hours  # Время симуляции в часах
        self.arrival_rate = arrival_rate      # Интенсивность прибытия (авто/час)
        self.service_time = service_time      # Среднее время обслуживания (часы)
        self.n_posts = n_posts                # Количество постов обслуживания
        self.queue_limit = queue_limit        # Максимальная длина очереди
        self.seed = seed                      # Зерно для воспроизводимости
        self.current_time = 0.0               # Текущее время
        self.event_list = []                  # Отсортированный список событий
        self.queue = []                       # Очередь клиентов
        self.posts = [None] * n_posts         # Состояние постов обслуживания(None - свободен)
        self.rng = np.random.default_rng(seed) # Генератор случайных чисел
        self.stats = {"total": 0, "served": 0, "lost": 0, "wait_time": [], "service_time": []}

    def generate_arrival(self):
        """Генерирует событие прибытия."""
        time_to_next = self.rng.exponential(1.0 / self.arrival_rate)
        arrival_time = self.current_time + time_to_next
        if arrival_time < self.sim_time_hours:
            self.event_list.append((arrival_time, 'ARRIVAL'))
            self.event_list.sort()

    def generate_departure(self, post_index):
        """Генерирует событие завершения обслуживания."""
        service_duration = self.rng.exponential(self.service_time)
        departure_time = self.current_time + service_duration
        self.event_list.append((departure_time, 'DEPARTURE', post_index))
        self.event_list.sort()
        return service_duration

    def process_arrival(self):
        """Обрабатывает прибытие клиента."""
        self.stats["total"] += 1
        if any(post is None for post in self.posts):
            for i in range(self.n_posts):
                if self.posts[i] is None:
                    self.posts[i] = self.current_time
                    service_duration = self.generate_departure(i)
                    self.stats["service_time"].append(service_duration)
                    self.stats["served"] += 1
                    break
        else:
            if self.queue_limit is None or len(self.queue) < self.queue_limit:
                self.queue.append(self.current_time)
            else:
                self.stats["lost"] += 1

    def process_departure(self, post_index):
        """Обрабатывает завершение обслуживания."""
        if self.queue:
            arrival_time = self.queue.pop(0)
            wait_time = self.current_time - arrival_time
            self.stats["wait_time"].append(wait_time)
            service_duration = self.generate_departure(post_index)
            self.stats["service_time"].append(service_duration)
            self.stats["served"] += 1
        else:
            self.posts[post_index] = None

    def run_simulation(self):
        """Запускает симуляцию."""
        self.generate_arrival()
        while self.event_list:
            event = self.event_list.pop(0)
            self.current_time = event[0]
            if self.current_time > self.sim_time_hours:
                break
            if event[1] == 'ARRIVAL':
                self.process_arrival()
                self.generate_arrival()
            elif event[1] == 'DEPARTURE':
                self.process_departure(event[2])

    def get_state(self):
        """Возвращает статистику симуляции."""
        avg_wait = np.mean(self.stats["wait_time"]) if self.stats["wait_time"] else 0
        avg_service = np.mean(self.stats["service_time"]) if self.stats["service_time"] else 0
        return {
            "total": self.stats["total"],
            "served": self.stats["served"],
            "lost": self.stats["lost"],
            "avg_wait_time": round(avg_wait, 4),
            "avg_service_time": round(avg_service, 4)
        }
if __name__ == "__main__":
    station = ServiceStationNumPy(sim_time_hours=8, arrival_rate=10, service_time=0.5, n_posts=2, queue_limit=5)
    station.run_simulation()
    print(station.get_state())