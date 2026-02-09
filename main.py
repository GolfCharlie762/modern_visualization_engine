"""
Modern Visualization Engine (MVE) - основа нового движка для визуализации
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple, Callable
from enum import Enum
import warnings

# Для GPU-ускорения (опционально)
try:
    import cupy as cp
    GPU_AVAILABLE = True
except ImportError:
    cp = np
    GPU_AVAILABLE = False

try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False


class Backend(Enum):
    """Доступные бэкенды для рендеринга"""
    CPU = "cpu"
    GPU = "gpu"
    WEBGL = "webgl"  # Для веб-приложений
    VULKAN = "vulkan"  # Для высокой производительности


class Theme(Enum):
    """Предустановленные темы"""
    DARK = "dark"
    LIGHT = "light"
    SOLARIZED = "solarized"
    MATRIX = "matrix"


@dataclass
class Color:
    """Класс для работы с цветами"""
    r: float  # 0-255
    g: float
    b: float
    a: float = 255.0
    
    def to_tuple(self) -> Tuple[float, float, float, float]:
        return (self.r, self.g, self.b, self.a)
    
    def to_normalized(self) -> Tuple[float, float, float, float]:
        return (self.r/255.0, self.g/255.0, self.b/255.0, self.a/255.0)
    
    @classmethod
    def from_hex(cls, hex_color: str, alpha: float = 255.0):
        """Создание цвета из HEX строки"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return cls(r, g, b, alpha)
    
    @classmethod
    def from_name(cls, name: str, alpha: float = 255.0):
        """Создание цвета по имени"""
        colors = {
            'red': (255, 0, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'yellow': (255, 255, 0),
            'cyan': (0, 255, 255),
            'magenta': (255, 0, 255),
        }
        if name in colors:
            r, g, b = colors[name]
            return cls(r, g, b, alpha)
        return cls(0, 0, 0, alpha)


@dataclass
class Canvas:
    """Холст для рисования"""
    width: int
    height: int
    dpi: int = 96
    background: Color = field(default_factory=lambda: Color(255, 255, 255))
    backend: Backend = Backend.CPU
    
    def __post_init__(self):
        self._init_buffer()
    
    def _init_buffer(self):
        """Инициализация буфера для рисования"""
        if self.backend == Backend.GPU and GPU_AVAILABLE:
            # Используем GPU буфер
            self.buffer = cp.zeros((self.height, self.width, 4), dtype=cp.float32)
        else:
            # CPU буфер (numpy array)
            self.buffer = np.zeros((self.height, self.width, 4), dtype=np.float32)
        
        # Заполняем фон
        bg_norm = self.background.to_normalized()
        self.buffer[:, :] = bg_norm
    
    def clear(self, color: Optional[Color] = None):
        """Очистка холста"""
        if color is None:
            color = self.background
        bg_norm = color.to_normalized()
        
        if self.backend == Backend.GPU and GPU_AVAILABLE:
            self.buffer[:] = cp.array(bg_norm, dtype=cp.float32)
        else:
            self.buffer[:] = np.array(bg_norm, dtype=np.float32)
    
    def get_image(self) -> np.ndarray:
        """Получение изображения как numpy array"""
        if self.backend == Backend.GPU and GPU_AVAILABLE:
            return cp.asnumpy(self.buffer)
        return self.buffer
    
    def save(self, filename: str, quality: int = 95):
        """Сохранение изображения"""
        img_data = self.get_image()
        
        if PILLOW_AVAILABLE:
            # Конвертируем в uint8 и создаем изображение
            img_uint8 = (img_data * 255).astype(np.uint8)
            img = Image.fromarray(img_uint8, 'RGBA')
            
            if filename.lower().endswith('.png'):
                img.save(filename, 'PNG')
            else:
                # Для JPEG конвертируем в RGB
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                img.save(filename, quality=quality)
        else:
            # Сохраняем как raw numpy array
            np.save(filename.replace('.png', '.npy').replace('.jpg', '.npy'), img_data)
            warnings.warn("Pillow не установлен, используется сохранение в numpy формате")


class Renderer:
    """Базовый класс рендерера"""
    
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.xp = cp if (canvas.backend == Backend.GPU and GPU_AVAILABLE) else np
    
    def draw_line(self, x1: float, y1: float, x2: float, y2: float, 
                  color: Color, width: float = 1.0):
        """Рисование линии (базовая реализация)"""
        # TODO: Реализовать алгоритм Брезенхема для GPU/CPU
        pass
    
    def draw_circle(self, center_x: float, center_y: float, radius: float,
                    color: Color, fill: bool = True, stroke_width: float = 1.0):
        """Рисование окружности"""
        # TODO: Реализовать эффективный алгоритм
        pass
    
    def draw_rectangle(self, x: float, y: float, width: float, height: float,
                       color: Color, fill: bool = True, stroke_width: float = 1.0):
        """Рисование прямоугольника"""
        buffer = self.canvas.buffer
        h, w, _ = buffer.shape
        
        # Конвертируем координаты в целочисленные индексы
        x_start = max(0, int(x))
        y_start = max(0, int(y))
        x_end = min(w, int(x + width))
        y_end = min(h, int(y + height))
        
        if x_start < x_end and y_start < y_end:
            color_norm = self.xp.array(color.to_normalized(), dtype=self.xp.float32)
            
            if fill:
                buffer[y_start:y_end, x_start:x_end] = color_norm
            else:
                # Только обводка
                buffer[y_start, x_start:x_end] = color_norm
                buffer[y_end-1, x_start:x_end] = color_norm
                buffer[y_start:y_end, x_start] = color_norm
                buffer[y_start:y_end, x_end-1] = color_norm


class Plot:
    """Базовый класс для графиков"""
    
    def __init__(self, width: int = 800, height: int = 600, 
                 backend: Backend = Backend.CPU, theme: Theme = Theme.LIGHT):
        self.canvas = Canvas(width, height, backend=backend)
        self.renderer = Renderer(self.canvas)
        self.theme = theme
        self._apply_theme()
        
    def _apply_theme(self):
        """Применение выбранной темы"""
        themes = {
            Theme.DARK: {
                'background': Color(30, 30, 35),
                'grid': Color(60, 60, 65),
                'text': Color(220, 220, 220),
            },
            Theme.LIGHT: {
                'background': Color(255, 255, 255),
                'grid': Color(240, 240, 240),
                'text': Color(0, 0, 0),
            },
            Theme.SOLARIZED: {
                'background': Color(0, 43, 54),
                'grid': Color(7, 54, 66),
                'text': Color(131, 148, 150),
            }
        }
        
        self.colors = themes.get(self.theme, themes[Theme.LIGHT])
        self.canvas.background = self.colors['background']
        self.canvas.clear()
    
    def scatter(self, x: np.ndarray, y: np.ndarray, 
                color: Color = Color.from_name('blue'), 
                size: float = 5.0, alpha: float = 1.0):
        """Точечный график"""
        # Нормализуем данные к размерам холста
        x_norm = self._normalize_x(x)
        y_norm = self._normalize_y(y)
        
        # TODO: Реализовать эффективное рисование точек на GPU
        
        return self
    
    def line(self, x: np.ndarray, y: np.ndarray,
             color: Color = Color.from_name('red'),
             width: float = 2.0):
        """Линейный график"""
        # TODO: Реализовать
        return self
    
    def bar(self, x: np.ndarray, heights: np.ndarray,
            color: Color = Color.from_name('green'),
            width: float = 0.8):
        """Столбчатая диаграмма"""
        # TODO: Реализовать
        return self
    
    def _normalize_x(self, x: np.ndarray) -> np.ndarray:
        """Нормализация X координат"""
        if len(x) == 0:
            return np.array([])
        x_min, x_max = x.min(), x.max()
        if x_max == x_min:
            return np.zeros_like(x)
        return (x - x_min) / (x_max - x_min) * (self.canvas.width - 1)
    
    def _normalize_y(self, y: np.ndarray) -> np.ndarray:
        """Нормализация Y координат"""
        if len(y) == 0:
            return np.array([])
        y_min, y_max = y.min(), y.max()
        if y_max == y_min:
            return np.zeros_like(y)
        return (1 - (y - y_min) / (y_max - y_min)) * (self.canvas.height - 1)
    
    def show(self):
        """Показ графика (заглушка для развития)"""
        print("Plot created with dimensions:", self.canvas.width, "x", self.canvas.height)
        print("Backend:", self.canvas.backend.value)
        print("Theme:", self.theme.value)
        
        if PILLOW_AVAILABLE:
            img_data = self.canvas.get_image()
            img_uint8 = (img_data * 255).astype(np.uint8)
            img = Image.fromarray(img_uint8, 'RGBA')
            img.show()
        else:
            warnings.warn("Pillow не установлен для отображения изображений")
    
    def save(self, filename: str):
        """Сохранение графика"""
        self.canvas.save(filename)


class Figure:
    """Класс для сложных композиций графиков"""
    
    def __init__(self, rows: int = 1, cols: int = 1, 
                 width: int = 1200, height: int = 800,
                 backend: Backend = Backend.CPU):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.backend = backend
        
        self.plots = []
        self.layout = None  # TODO: Реализовать систему компоновки
    
    def add_subplot(self, row: int, col: int, plot: Plot):
        """Добавление подграфика"""
        # TODO: Реализовать
        pass
    
    def render(self):
        """Рендеринг всей фигуры"""
        # TODO: Реализовать композицию
        pass


# Утилитарные функции для быстрого создания графиков
def quick_plot(x: np.ndarray, y: np.ndarray, 
               plot_type: str = 'line', **kwargs) -> Plot:
    """Быстрое создание графика"""
    plot = Plot(**kwargs.get('plot_kwargs', {}))
    
    if plot_type == 'line':
        plot.line(x, y, **kwargs)
    elif plot_type == 'scatter':
        plot.scatter(x, y, **kwargs)
    elif plot_type == 'bar':
        plot.bar(x, y, **kwargs)
    
    return plot


def multi_plot(data: List[Tuple[np.ndarray, np.ndarray]], 
               plot_types: List[str], **kwargs) -> Figure:
    """Создание нескольких графиков"""
    fig = Figure(len(data), 1, **kwargs.get('figure_kwargs', {}))
    
    for i, ((x, y), plot_type) in enumerate(zip(data, plot_types)):
        plot = quick_plot(x, y, plot_type, **kwargs)
        fig.add_subplot(i + 1, 1, plot)
    
    return fig


# Пример использования
if __name__ == "__main__":
    # Создаем тестовые данные
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    # Пример 1: Простой график
    print("Создание простого графика...")
    plot = Plot(theme=Theme.DARK, backend=Backend.CPU)
    plot.scatter(x, y, color=Color.from_hex('#FF6B6B'), size=3.0)
    plot.line(x, y, color=Color.from_name('cyan'), width=1.5)
    
    # Рисуем прямоугольник для демонстрации
    plot.renderer.draw_rectangle(50, 50, 100, 100, 
                                 Color.from_hex('#4ECDC4', alpha=200), 
                                 fill=True)
    
    plot.save("output.png")
    
    # Пример 2: Проверка GPU бэкенда
    if GPU_AVAILABLE:
        print("\nПроверка GPU бэкенда...")
        plot_gpu = Plot(backend=Backend.GPU)
        plot_gpu.scatter(x, y * 2)
        plot_gpu.save("output_gpu.png")
    
    print("\nОсновные возможности движка:")
    print("1. Поддержка CPU/GPU рендеринга")
    print("2. Современная система цветов")
    print("3. Темы оформления")
    print("4. Модульная архитектура")
    print("5. Подготовка для WebGL/Vulkan")
