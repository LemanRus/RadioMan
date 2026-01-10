# RadioMan

Приложение для радиолюбителей, помогающее в создании собственных электронных устройств. Включает справочники по маркировке компонентов, различные калькуляторы и полезную информацию для каждого радиолюбителя.

## Возможности

### 📋 Маркировки компонентов

Приложение содержит подробные справочники по маркировке электронных компонентов:

- **Резисторы:**
  - Маркировка выводных (TH) резисторов с цветовыми кольцами
  - Маркировка SMD резисторов (включая стандарт EIA-96)
  
- **Конденсаторы:**
  - Маркировка выводных (TH) конденсаторов
  - Маркировка SMD конденсаторов

### 🧮 Калькуляторы

Набор полезных калькуляторов для электронных расчётов:

- **Конвертер единиц** — преобразование единиц измерения:
  - Длины (мил, дюйм, см, мм)
  - Площади (мил², дюйм², см², мм², круг. мил)
  - Ёмкости (пФ, нФ, мкФ)
  - Мощности (Ватт, эрг/с)

- **Расчёт резистора для LED** — подбор ограничивающего резистора для светодиода

- **Расчёт индуктивности:**
  - Расчёт индуктивности по параметрам катушки
  - Расчёт размеров катушки по заданной индуктивности

- **Параллельное соединение резисторов** — расчёт эквивалентного сопротивления

- **Последовательное соединение конденсаторов** — расчёт эквивалентной ёмкости

- **Делитель напряжения:**
  - Расчёт выходного напряжения
  - Расчёт сопротивлений для заданного напряжения

- **LM317 регулятор напряжения:**
  - Расчёт выходного напряжения
  - Расчёт выходного тока

### 📚 Справочник

Обширная база знаний для радиолюбителей:

- **Теория** — теоретические основы электроники
- **Схемы** — типовые схемы и их описания
- **Распиновка** — распиновка популярных компонентов
- **Соединения** — схемы соединений компонентов
- **Микросхемы и аналоги:**
  - Обширная база данных отечественных микросхем
  - Поиск зарубежных аналогов
  - Организовано по сериям с изображениями
- **Лайфхаки** — полезные советы и трюки

### ❓ Помощь

- **Как использовать** — инструкция по использованию приложения
- **О приложении** — информация о версии и разработчике

## Технические особенности

- **Платформа:** Android (сборка через Buildozer)
- **Фреймворк:** Kivy/KivyMD
- **Архитектура:** Модульная структура кода
- **Данные:** Хранение справочных данных в JSON файлах с кэшированием
- **Производительность:** Оптимизированная загрузка данных с асинхронной генерацией UI элементов
- **UX:** Плавные анимации переходов, индикаторы загрузки, адаптивный интерфейс

## Требования

- Python 3.10+ (для разработки)
- Buildozer (для сборки Android APK)
- Android SDK и NDK (устанавливаются автоматически через Buildozer)

## Установка и сборка

### Для разработки

1. Клонируйте репозиторий:
```bash
git clone https://github.com/LemanRus/RadioMan.git
cd RadioMan
```

2. Создайте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Запустите приложение:
```bash
python main.py
```

### Сборка для Android

1. Установите Buildozer (если ещё не установлен):
```bash
pip install buildozer
```

2. Убедитесь, что установлены необходимые системные зависимости (для Linux/WSL):
```bash
sudo apt install -y build-essential git unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

3. Соберите APK:
```bash
buildozer android debug
```

4. Готовый APK будет находиться в папке `bin/`

**Примечание:** Для сборки рекомендуется использовать Python 3.10 или 3.11, так как Python 3.12+ может иметь проблемы совместимости с некоторыми зависимостями Buildozer.

## Структура проекта

```
RadioMan/
├── data/                    # JSON файлы с данными
│   ├── chips_analogs.json
│   ├── resistor_markings.json
│   ├── smd_resistor_markings.json
│   └── capacitor_markings.json
├── kv/                      # Kivy UI файлы
│   ├── calculation_screens/
│   ├── handbook_screens/
│   ├── help_screens/
│   ├── markings_screens/
│   └── toplevel_screens/
├── media/                   # Изображения и ресурсы
├── screens/                 # Модули экранов приложения
│   ├── calculations/       # Калькуляторы
│   ├── handbook/           # Справочник
│   ├── help/               # Помощь
│   ├── markings/           # Маркировки
│   ├── managers.py
│   └── widgets.py
├── data_loader.py           # Загрузчик данных с кэшированием
├── main.py                  # Точка входа приложения
├── buildozer.spec          # Конфигурация Buildozer
└── requirements.txt        # Python зависимости
```

## Версия

Текущая версия: **0.8**

## Лицензия

См. файл [LICENSE](LICENSE)

## Автор

Разработано для сообщества радиолюбителей.

GitHub: [LemanRus/RadioMan](https://github.com/LemanRus/RadioMan)

---

# RadioMan

An application for electronics enthusiasts, helping in creating custom electronic devices. Includes component marking guides, various calculators, and useful information for every radio amateur.

## Features

### 📋 Component Markings

The application contains detailed guides for marking electronic components:

- **Resistors:**
  - Through-hole (TH) resistor marking with color bands
  - SMD resistor marking (including EIA-96 standard)
  
- **Capacitors:**
  - Through-hole (TH) capacitor marking
  - SMD capacitor marking

### 🧮 Calculators

A set of useful calculators for electronic calculations:

- **Unit Converter** — conversion of measurement units:
  - Length (mil, inch, cm, mm)
  - Area (mil², inch², cm², mm², circular mil)
  - Capacitance (pF, nF, µF)
  - Power (Watt, erg/s)

- **LED Resistor Calculation** — selection of current-limiting resistor for LED

- **Inductance Calculation:**
  - Calculate inductance from coil parameters
  - Calculate coil dimensions for given inductance

- **Parallel Resistor Connection** — equivalent resistance calculation

- **Series Capacitor Connection** — equivalent capacitance calculation

- **Voltage Divider:**
  - Output voltage calculation
  - Resistance calculation for given voltage

- **LM317 Voltage Regulator:**
  - Output voltage calculation
  - Output current calculation

### 📚 Handbook

Extensive knowledge base for electronics enthusiasts:

- **Theory** — theoretical foundations of electronics
- **Schematics** — typical circuits and their descriptions
- **Pinout** — pinouts of popular components
- **Connections** — component connection diagrams
- **Chips and Analogs:**
  - Extensive database of domestic (CIS) integrated circuits
  - Search for foreign analogs
  - Organized by series with images
- **Lifehacks** — useful tips and tricks

### ❓ Help

- **How to Use** — application usage instructions
- **About** — version and developer information

## Technical Features

- **Platform:** Android (build via Buildozer)
- **Framework:** Kivy/KivyMD
- **Architecture:** Modular code structure
- **Data:** Storage of reference data in JSON files with caching
- **Performance:** Optimized data loading with asynchronous UI element generation
- **UX:** Smooth transition animations, loading indicators, adaptive interface

## Requirements

- Python 3.10+ (for development)
- Buildozer (for Android APK build)
- Android SDK and NDK (installed automatically via Buildozer)

## Installation and Build

### For Development

1. Clone the repository:
```bash
git clone https://github.com/LemanRus/RadioMan.git
cd RadioMan
```

2. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

### Android Build

1. Install Buildozer (if not already installed):
```bash
pip install buildozer
```

2. Make sure necessary system dependencies are installed (for Linux/WSL):
```bash
sudo apt install -y build-essential git unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

3. Build APK:
```bash
buildozer android debug
```

4. The ready APK will be in the `bin/` folder

**Note:** For building, it is recommended to use Python 3.10 or 3.11, as Python 3.12+ may have compatibility issues with some Buildozer dependencies.

## Project Structure

```
RadioMan/
├── data/                    # JSON data files
│   ├── chips_analogs.json
│   ├── resistor_markings.json
│   ├── smd_resistor_markings.json
│   └── capacitor_markings.json
├── kv/                      # Kivy UI files
│   ├── calculation_screens/
│   ├── handbook_screens/
│   ├── help_screens/
│   ├── markings_screens/
│   └── toplevel_screens/
├── media/                   # Images and resources
├── screens/                 # Application screen modules
│   ├── calculations/       # Calculators
│   ├── handbook/           # Handbook
│   ├── help/               # Help
│   ├── markings/           # Markings
│   ├── managers.py
│   └── widgets.py
├── data_loader.py           # Data loader with caching
├── main.py                  # Application entry point
├── buildozer.spec          # Buildozer configuration
└── requirements.txt        # Python dependencies
```

## Version

Current version: **0.8**

## License

See [LICENSE](LICENSE) file

## Author

Developed for the electronics enthusiasts community.

GitHub: [LemanRus/RadioMan](https://github.com/LemanRus/RadioMan)

## Screenshots

![](screenshots/2023-10-12%2022-37-53.JPG)

![](screenshots/2023-10-12%2022-37-58.JPG)

![](screenshots/2023-10-12%2022-39-49.JPG)

![](screenshots/2023-10-12%2022-42-07.JPG)
