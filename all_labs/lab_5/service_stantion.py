import random
import simpy

class ServiceStation:
    def __init__(self, sim_time_hours, arrival_rate, service_time, n_posts, queue_limit=None, seed=42):
        self.sim_time_hours = sim_time_hours
        self.arrival_rate = arrival_rate
        self.service_time = service_time
        self.n_posts = n_posts
        self.queue_limit = queue_limit
        self.seed = seed
        self.stats = {
            "total": 0,
            "served": 0,
            "lost": 0,
            "wait_time": [],
            "service_time": []
        }
        self.finished = False  # Флаг завершения симуляции

    def car_process(self, env, posts, service_time, queue_limit=None):
        """Процесс обслуживания автомобиля."""
        arrival_time = env.now
        # Если лимит очереди установлен и очередь уже заполнена, считаем автомобиль отказанным
        if queue_limit is not None and posts.count >= posts.capacity and len(posts.queue) >= queue_limit:
            self.stats["lost"] += 1
            return

        self.stats["served"] += 1
        with posts.request() as request:
            yield request
            wait_time = env.now - arrival_time
            self.stats["wait_time"].append(wait_time)
            yield env.timeout(random.expovariate(1.0 / service_time))
            service_duration = env.now - arrival_time - wait_time
            self.stats["service_time"].append(service_duration)

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
