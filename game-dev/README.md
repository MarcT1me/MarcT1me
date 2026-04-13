# 🎮 Game Development

[Вернуться к главному портфолио](../README.md)

## 🔧 StellarEngine (C++/C#)
![Статус](https://img.shields.io/badge/Active_development-0.5.0-blueviolet)
![DotNET](https://img.shields.io/badge/.NET-9.0-512BD4?logo=dotnet&logoColor=white)
![Cpp](https://img.shields.io/badge/C++-std20-00599C?logo=cplusplus&logoColor=white)

Основной репозиторий 3D движка над которым ведётся вся работа (остальные R&D скрыты)

- Гипермодульная архитектура
- Полная изоляция модулей друг от друга
- Кастомные системы обработки ошибок и многопоточности
- Масштабируимость и переиспользуемость модулей
- .NET SDK wrapper
- Окончательное определение Core Concept и Project Vision

**GutHub**:
[исходный код](https://github.com/QuantumDevTeam/StellarEngine)

## 🔧 Игровой движок (C++/C#)

![Статус](https://img.shields.io/badge/droped-0.23.0-red)
![Статус](https://img.shields.io/badge/Pre_Release-0.15.5-orange)
![DirectX](https://img.shields.io/badge/DirectX-12-blue)
![DotNET](https://img.shields.io/badge/.NET-9.0-512BD4?logo=dotnet&logoColor=white)
![Cpp](https://img.shields.io/badge/C++-std20-00599C?logo=cplusplus&logoColor=white)

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

## 💫 Гравитационная симуляция (Java/LibGDX)

![Статус](https://img.shields.io/badge/Release-0.12.3-green)
![Java](https://img.shields.io/badge/Java-21-ED8B00?logo=coffeescript&logoColor=white)
![LibGDX](https://img.shields.io/badge/LibGDX-0.13.1-red?logo=coffeescript&logoColor=white)

- Многопоточные физические расчеты большого кол-ва тел
- Динамическая визуализация траекторий
- Моделирование гравитации на основе реальных законов термодинамики

**GutHub**:
[исходный код](https://github.com/MarcT1me/GravitySimulation2-JavaEdition) |
[релиз](https://github.com/MarcT1me/GravitySimulation2-JavaEdition/releases/latest)

## Мини проекты на PyGame

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![PyGame](https://img.shields.io/badge/PyGame-2.6.1-AAEEBB?logo=python&logoColor=white)

### 🔫 ShooterGame

Простейшая игра - шутер

GitHub: [исходный код](https://github.com/MarcT1me/ShooterGameV2)

### 🏓 Pong game

Простая Pong game

```requirements
# requirements.txt
pygame
pyglm
```

#### управление

`W/S` - левая ракетка
`Up/Down` - правая ракетка

### ⭐ SpaceStars

Симуляция 3д через движение звёзд "в камеру"

```requirements
# requirements.txt
pygame
```

#### управление

J - "прыжок" (смена конфигурации симуляции с 1 на 2)

#### конфиги

`settings.json` - настройки окна, размеры, FPS и Alpha, влияющую на длину шлейфа от звезды\
`params.json` - настройка симуляции, размеры звёзд, таблицы выбора цветов, количество звёзд и их зоны спавна
