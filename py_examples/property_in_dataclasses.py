from dataclasses import dataclass


# Захотел в питоновских датаклассах использовать property, так как понадобился сеттер для поля.
# Но просто так не получится это сделать (получите ошибочку), поэтому есть небольшой обходной путь.
# У нас есть датакласс Entity с полями health и max_health.
# Для управления данным полем нам нужно вычисляемое свойство
# (например, хотим сделать так, чтобы health не падал меньше 0, или не превышал значение max_health).
# Вместо health делаем поле с названием _health, а само health делаем как property. Получается что-то вот такого:


@dataclass
class Entity:
    _health: int
    max_health: int

    @property
    def health(self) -> int:
        return self._health

    @health.setter
    def health(self, health: int) -> int:
        if health < 0:
            self._health = 0
        elif health > self.max_health:
            self._health = self.max_health
        else:
            self._health = health
