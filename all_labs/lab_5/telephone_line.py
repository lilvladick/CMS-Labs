import simpy
import random
import time
import threading

class TelephoneLine:
    def init(self, sim_time, arrival_rate, service_time, seed=None, update_interval=0.1):
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
    
    def update_simulation_state(self):
        with self.state_lock:
            self.simulation_state["total"] = self.stats["total"]
            self.simulation_state["served"] = self.stats["served"]
            self.simulation_state["lost"] = self.stats["lost"]
            p_served = self.stats["served"] / self.stats["total"] if self.stats["total"] > 0 else 0
            p_lost = self.stats["lost"] / self.stats["total"] if self.stats["total"] > 0 else 0
            ratio = self.stats["served"] / self.stats["lost"] if self.stats["lost"] > 0 else None
            self.simulation_state["p_served"] = p_served
            self.simulation_state["p_lost"] = p_lost
            self.simulation_state["ratio"] = ratio
            self.simulation_state["finished"] = (self.env.now >= self.sim_time)
    
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
        """
        Генерация входящих вызовов по экспоненциальному закону interarrival.
        """
        call_id = 0
        while True:
            yield env.timeout(random.expovariate(self.arrival_rate))
            call_id += 1
            self.stats['total'] += 1
            env.process(self.call_process(env))
    
    def run(self):
        """
        Запускает симуляцию пошагово с обновлением состояния.
        """
        self.env.process(self.arrival_generator(self.env))
        while self.env.now < self.sim_time:
            self.env.step()
            self.update_simulation_state()
            time.sleep(self.update_interval)
        self.update_simulation_state()
    
    def get_state(self):
        with self.state_lock:
            return self.simulation_state.copy()