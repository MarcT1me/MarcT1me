# 🎮 Game Development

[Вернуться к главному портфолио](../README.md)

## 🔧 Игровой движок (C++/C#)

![Статус](https://img.shields.io/badge/Active_development-0.16.2-blueviolet)
![Статус](https://img.shields.io/badge/Pre_Release-0.15.5-orange)
![DirectX](https://img.shields.io/badge/DirectX-12-blue)
![DirectX](https://img.shields.io/badge/.NET-9.0-blue)
![DirectX](https://img.shields.io/badge/C++-std20-blue)

- Загрузчик ресурсов (из файловой системы)
- _Мультиоконная_ архитектура
- Кастомная _система обработки ошибок_
- Близость кода игры к движку

**Текущие возможности**:

- Рендеринг _текстурных примитивов_
- Поддержка _ввода_ (мышь/клавиатура/геймпад)

**Структура**:

```mermaid
graph LR
    QuantumEngine --- D[клиент движок]
    QuantumEngine ==> EngineCore --- E[ядро движка]
    QuantumEngine ==> MirageAPI
    MirageAPI ==> EngineCore
    MirageAPI --- B[нативный код графики]
    A[Проект игры] ==> AppLib
    AppLib ==> QuantumEngine
    AppLib --- C[Код игры]
```

**GutHub**:
[исходный код](https://github.com/MarcT1me/CSQCv2) |
[установщик](https://github.com/MarcT1me/CSQCv2/releases/tag/0.15.5)

---

## Гравитационная симуляция (Java/LibGDX)

![Статус](https://img.shields.io/badge/Release-0.12.3-green)
![Java](https://img.shields.io/badge/Java-21-orange)
![Java](https://img.shields.io/badge/LibGDX-21-red)

- Многопоточные физические расчеты большого кол-ва тел
- Динамическая визуализация траекторий
- Моделирование гравитации на основе реальных законов термодинамики

**GutHub**:
[исходный код](https://github.com/MarcT1me/GravitySimulation2-JavaEdition) |
[релиз](https://github.com/MarcT1me/GravitySimulation2-JavaEdition/releases/latest)

## Мини проекты на PyGame

![PyGame](https://img.shields.io/badge/Python-3.12.9-265176)
![PyGame](https://img.shields.io/badge/PyGame-2.6.1-AAEEBB)
