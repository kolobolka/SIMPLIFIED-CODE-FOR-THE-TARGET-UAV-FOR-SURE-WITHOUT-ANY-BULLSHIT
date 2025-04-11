import time
import random
import logging

logging.basicConfig(
    format="[%(asctime)s][%(levelname)s] %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("target_uav.log"), logging.StreamHandler()]
)

class TargetUAV:
    """
    БПЛА-мишень с реалистичным поведением боевого аппарата
    """
    def __init__(self):
        self.altitude = 0
        self.speed = 0
        self.health = 100
        self.status = "На земле"
        self.mission_complete = False
        self.evasion_cooldown = 0
        logging.info("Инициализация боевой мишени завершена") 
        
    def arm(self):
        """Подготовка к боевому заданию"""
        try:
            self._pre_flight_checks()
            self.status = "Готов к взлету"
            logging.info("Предстартовые проверки пройдены")
        except Exception as e:
            self.status = f"Авария: {str(e)}"
            logging.error(f"Отказ системы: {str(e)}")
            raise

    def takeoff(self):
        """Взлет с набором боевой высоты"""
        if self.status != "Готов к взлету":
            raise RuntimeError("Невозможно выполнить взлет")
            
        target_altitude = random.randint(300, 500)  
        logging.info(f"Начало боевого взлета до {target_altitude} м")
        
        while self.altitude < target_altitude:
            self.altitude += 50
            self.speed = random.randint(120, 180)  
            time.sleep(0.5)
            self._random_evasion()  
            
        self.status = "В боевом режиме"
        logging.warning("Боевой режим активирован")

    def execute_mission(self):
        """Выполнение боевого задания с имитацией атак"""
        start_time = time.time()
        while time.time() - start_time < 120:  
            self._combat_maneuvers()
            self._check_damage()
            time.sleep(1)
            if self.health <= 0:
                break
        self.mission_complete = True
        self.return_to_base()

    def take_damage(self, hit_power):
        """Обработка попаданий [[8]][[3]]"""
        if random.random() < 0.3:  
            logging.warning("Попадание ПРЕДОТВРАЩЕНО системой защиты")
            return
            
        self.health = max(0, self.health - hit_power)
        logging.error(f"Попадание! Осталось здоровья: {self.health}%")
        
        if self.health < 30:
            self.status = "Поврежден"
            logging.critical("Критические повреждения! Переход в режим уклонения")

    def return_to_base(self):
        """Аварийная посадка при повреждениях [[9]]"""
        logging.info("Начало аварийной посадки")
        while self.altitude > 0:
            self.altitude = max(0, self.altitude - 50)
            self.speed = 60  
            time.sleep(0.5)
            logging.info(f"Посадка: {self.altitude} м")
        self.status = "На земле" if self.health > 0 else "Уничтожен"
        logging.info(f"Статус после посадки: {self.status}")

    def _combat_maneuvers(self):
        """Боевые маневры с имитацией атак"""
        if time.time() < self.evasion_cooldown:
            return
            
        maneuver = random.choices(
            ["Пикирование", "Боевой разворот", "Противозенитный зигзаг"],
            weights=[0.4, 0.3, 0.3],  
            k=1
        )[0]
        
        self.speed = random.randint(150, 200)
        self.altitude += random.randint(-50, 50)
        self.altitude = max(50, min(self.altitude, 500)) 
        self.evasion_cooldown = time.time() + 2  
        
        logging.warning(f"Боевой маневр: {maneuver} (скорость={self.speed} км/ч)")

    def _check_damage(self):
        """Система самодиагностики [[3]]"""
        if self.health < 50 and random.random() < 0.2:
            self.speed = max(80, self.speed - 30)
            logging.error("Повреждение двигателя! Снижение скорости")

    def _pre_flight_checks(self):
        logging.info("Проверка систем...")
        time.sleep(1)
        if random.random() < 0.1:
            raise RuntimeError("Ошибка системы наведения")

if __name__ == "__main__":
    target = TargetUAV()
    
    try:
        target.arm()
        target.takeoff()
        
        attack_thread = threading.Thread(target=lambda: [
            time.sleep(random.uniform(5, 15)) or 
            target.take_damage(random.randint(10, 30)) 
            for _ in range(5)
        ])
        attack_thread.start()
        
        target.execute_mission()
        
    except Exception as e:
        logging.error(f"КРИТИЧЕСКОЕ ПОВРЕЖДЕНИЕ: {str(e)}")
        target.return_to_base()
