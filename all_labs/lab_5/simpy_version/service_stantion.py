import random
import simpy

class ServiceStation:
    def __init__(self, sim_time_hours, arrival_rate, service_time, n_posts, queue_limit=None, seed=42):
        """
        Инициализация симуляции автосервиса.

        :param sim_time_hours: Время симуляции в часах
        :param arrival_rate: Интенсивность поступления автомобилей (авто/час)
        :param service_time: Среднее время обслуживания одного автомобиля (в часах)
        :param n_posts: Количество постов обслуживания
        :param queue_limit: Максимальная длина очереди (если None, очередь бесконечна)
        :param seed: Зерно для генератора случайных чисел (для воспроизводимости)
        """
        self.sim_time_hours = sim_time_hours
        self.arrival_rate = arrival_rate
        self.service_time = service_time
        self.n_posts = n_posts
        self.queue_limit = queue_limit
        self.seed = seed
        self.stats = {
            "total": 0,  # Всего поступивших автомобилей
            "served": 0,  # Обслуженных автомобилей
            "lost": 0,  # Потерянных автомобилей (из-за переполнения очереди)
            "wait_time": [],  # Времена ожидания в очереди
            "service_time": []  # Времена обслуживания
        }
        self.finished = False

    def car_process(self, env, posts, service_time, queue_limit=None):
        """Процесс обслуживания автомобиля."""
        arrival_time = env.now
        if queue_limit is not None and posts.count >= posts.capacity and len(posts.queue) >= queue_limit:
            self.stats["lost"] += 1
            return

        with posts.request() as request:
            yield request
            wait_time = env.now - arrival_time
            self.stats["wait_time"].append(wait_time)
            service_duration = random.expovariate(1.0 / service_time)
            yield env.timeout(service_duration)
            self.stats["service_time"].append(service_duration)
            self.stats["served"] += 1

    def arrival_generator(self, env, posts, arrival_rate, service_time, queue_limit=None):
        """Генератор поступления автомобилей."""
        while True:
            yield env.timeout(random.expovariate(arrival_rate))
            self.stats["total"] += 1
            env.process(self.car_process(env, posts, service_time, queue_limit))

    def run_simulation(self):
        """Запускает симуляцию."""
        if self.seed is not None:
            random.seed(self.seed)

        env = simpy.Environment()
        posts = simpy.Resource(env, capacity=self.n_posts)
        env.process(self.arrival_generator(env, posts, self.arrival_rate, self.service_time, self.queue_limit))
        env.run(until=self.sim_time_hours)
        self.finished = True

    def get_state(self):
        """Возвращает текущее состояние симуляции, включая средние времена ожидания и обслуживания."""
        avg_wait = round(sum(self.stats["wait_time"]) / len(self.stats["wait_time"]), 4) if self.stats["wait_time"] else 0
        avg_service = round(sum(self.stats["service_time"]) / len(self.stats["service_time"]), 4) if self.stats["service_time"] else 0

        return {
            "total": self.stats["total"],
            "served": self.stats["served"],
            "lost": self.stats["lost"],
            "avg_wait_time": avg_wait,
            "avg_service_time": avg_service,
            "finished": self.finished
        }