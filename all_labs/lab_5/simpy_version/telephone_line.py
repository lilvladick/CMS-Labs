import simpy
import random
import threading
import time

class TelephoneLine:
    def __init__(self, sim_time=10000, arrival_rate=0.95, service_time=1.0, seed=42, update_interval=0.1):
        """
        Инициализация симуляции.
        :param sim_time: время симуляции (в минутах)
        :param arrival_rate: интенсивность вызовов (вызов/мин)
        :param service_time: среднее время обслуживания (мин)
        :param seed: значение seed для random (опционально)
        :param update_interval: интервал обновления состояния (в секундах)
        """
        self.sim_time = sim_time
        self.arrival_rate = arrival_rate
        self.service_time = service_time
        self.seed = seed
        self.update_interval = update_interval

        self.env = simpy.Environment()
        self.line = simpy.Resource(self.env, capacity=1)
        self.stats = {'total': 0, 'served': 0, 'lost': 0}

        self.simulation_state = {
            "total": 0,
            "served": 0,
            "lost": 0,
            "finished": False,
            "p_served": 0.0,
            "p_lost": 0.0,
            "ratio": None
        }
        self.state_lock = threading.Lock()

        if self.seed is not None:
            random.seed(self.seed)
            
    def update(self):
        """Периодически обновляет состояние симуляции для веб-сокета."""
        while not self.simulation_state["finished"]:
            self.update_simulation_state()
            time.sleep(self.update_interval)


    def update_simulation_state(self):
        with self.state_lock:
            total = self.stats["total"]
            served = self.stats["served"]
            lost = self.stats["lost"]

            self.simulation_state.update({
                "total": total,
                "served": served,
                "lost": lost,
                "p_served": served / total if total > 0 else 0,
                "p_lost": lost / total if total > 0 else 0,
                "ratio": served / lost if lost > 0 else None,
                "finished": self.env.now >= self.sim_time
            })

    def call_process(self, env):
        """
        Процесс обработки звонка.
        Если линия свободна, вызов обслуживается, иначе – отклоняется.
        """
        if self.line.count < self.line.capacity:
            with self.line.request() as req:
                yield req
                self.stats['served'] += 1
                yield env.timeout(random.expovariate(1.0 / self.service_time))
        else:
            self.stats['lost'] += 1

    def arrival_generator(self, env):
        """Генерация входящих вызовов по экспоненциальному закону interarrival."""
        while True:
            yield env.timeout(random.expovariate(self.arrival_rate))
            self.stats['total'] += 1
            env.process(self.call_process(env))

    def run(self):
        threading.Thread(target=self.update, daemon=True).start()
        self.env.process(self.arrival_generator(self.env))
        self.env.run(until=self.sim_time)
        self.update_simulation_state()


    def get_state(self):
        with self.state_lock:
            return self.simulation_state.copy()
