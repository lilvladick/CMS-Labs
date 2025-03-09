import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

import unittest
import simpy
from all_labs.lab_5.simpy_version.telephone_line import TelephoneLine


class TestTelephoneLine(unittest.TestCase):

    def setUp(self):
        """Создаем объект для тестирования перед каждым тестом."""
        self.sim_time = 10  # время симуляции (минуты)
        self.arrival_rate = 0.95  # интенсивность вызовов
        self.service_time = 1.0  # среднее время обслуживания
        self.seed = 42  # seed для random
        self.update_interval = 0.1  # интервал обновления состояния

        self.telephone_line = TelephoneLine(sim_time=self.sim_time,
                                            arrival_rate=self.arrival_rate,
                                            service_time=self.service_time,
                                            seed=self.seed,
                                            update_interval=self.update_interval)

    def test_initial_state(self):
        """Проверяем начальное состояние симуляции."""
        self.assertEqual(self.telephone_line.simulation_state['total'], 0)
        self.assertEqual(self.telephone_line.simulation_state['served'], 0)
        self.assertEqual(self.telephone_line.simulation_state['lost'], 0)
        self.assertFalse(self.telephone_line.simulation_state['finished'])


    def test_call_process_lost(self):
        """Проверяем, что звонки отклоняются, если линия занята."""
        env = simpy.Environment()
        line = self.telephone_line.line
        env.process(self.telephone_line.call_process(env))
        env.run(until=env.now + 1)
        env.process(self.telephone_line.call_process(env))
        env.run(until=env.now + 1)

        self.assertEqual(self.telephone_line.stats['lost'], 1)

    def test_simulation_state_update(self):
        """Проверяем обновление состояния симуляции."""
        self.telephone_line.stats = {'total': 10, 'served': 7, 'lost': 3}

        self.telephone_line.update_simulation_state()

        self.assertEqual(self.telephone_line.simulation_state['total'], 10)
        self.assertEqual(self.telephone_line.simulation_state['served'], 7)
        self.assertEqual(self.telephone_line.simulation_state['lost'], 3)
        self.assertEqual(self.telephone_line.simulation_state['p_served'], 0.7)
        self.assertEqual(self.telephone_line.simulation_state['p_lost'], 0.3)
        self.assertEqual(round(self.telephone_line.simulation_state['ratio'], 4), 2.3333)

    def test_simulation_finish(self):
        """Проверяем завершение симуляции."""
        self.telephone_line.sim_time = 1
        self.telephone_line.env = simpy.Environment()

        self.telephone_line.run()

        self.assertTrue(self.telephone_line.simulation_state['finished'])

    def test_get_state(self):
        """Проверяем метод получения состояния симуляции."""
        self.telephone_line.stats = {'total': 10, 'served': 5, 'lost': 5}
        self.telephone_line.update_simulation_state()

        state = self.telephone_line.get_state()
        self.assertEqual(state['total'], 10)
        self.assertEqual(state['served'], 5)
        self.assertEqual(state['lost'], 5)

if __name__ == '__main__':
    unittest.main()
