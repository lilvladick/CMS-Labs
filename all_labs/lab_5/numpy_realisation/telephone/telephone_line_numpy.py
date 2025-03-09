import numpy as np
import threading
import time
from all_labs.lab_5.numpy_realisation.telephone.events import ArrivalEvent, DepartureEvent

class TelephoneLineNumpy:
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
        self.current_time = 0.0           # Время симуляции
        self.line_busy = False            # Состояние линии (свободна/занята)
        self.event_list = []              # Список событий
        self.stats = {'total': 0, 'served': 0, 'lost': 0}  # Статистика

        # Состояние для веб-сокета
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
            np.random.seed(self.seed)

    def generate_first_arrival(self):
        """Генерация самого первого поступления"""
        first_arrival_time = np.random.exponential(scale=1.0 / self.arrival_rate)
        self.event_list.append(ArrivalEvent(first_arrival_time))

    def next_event(self):
        """Следующее событие"""
        if not self.event_list:
            return None
        min_idx = np.argmin([event.time for event in self.event_list])
        next_event = self.event_list.pop(min_idx)
        return next_event

    def process_event(self, event):
        """Обработчик"""
        self.current_time = event.time

        if event.event_type == 'ARRIVAL':
            self.stats['total'] += 1
            if not self.line_busy:
                self.line_busy = True
                service_duration = np.random.exponential(scale=1.0 / self.service_time)
                departure_time = self.current_time + service_duration
                self.event_list.append(DepartureEvent(departure_time))
            else:
                self.stats['lost'] += 1
            next_arrival_time = self.current_time + np.random.exponential(scale=1.0 / self.arrival_rate)
            if next_arrival_time < self.sim_time:
                self.event_list.append(ArrivalEvent(next_arrival_time))

        elif event.event_type == 'DEPARTURE':
            self.line_busy = False
            self.stats['served'] += 1

    def run(self):
        """Запуск симуляции."""
        threading.Thread(target=self.update, daemon=True).start()
        self.generate_first_arrival()
        while self.event_list:
            event = self.next_event()
            if event is None or event.time > self.sim_time:
                break
            self.process_event(event)
        with self.state_lock:
            self.simulation_state["finished"] = True
        self.update_simulation_state()

    def update(self):
        """Периодически обновляет состояние симуляции для веб-сокета."""
        while not self.simulation_state["finished"]:
            self.update_simulation_state()
            time.sleep(self.update_interval)

    def update_simulation_state(self):
        """Обновление состояния симуляции."""
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
                "finished": self.current_time >= self.sim_time
            })

    def get_state(self):
        """Получение текущего состояния симуляции."""
        with self.state_lock:
            return self.simulation_state.copy()

if __name__ == "__main__":
    sim = TelephoneLineNumpy(sim_time=10000, arrival_rate=0.95, service_time=1.0, seed=42)
    sim.run()
    print(sim.get_state())