import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy import stats
import json
from datetime import datetime
from typing import Dict, List, Any
import uuid

# ===== КОНФИГУРАЦИЯ =====
st.set_page_config(
    page_title="Statistical Detective 🕵️",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Кастомные стили
st.markdown("""
<style>
    .detective-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .case-card {
        border: 2px solid #e1e5e9;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: #f8f9fa;
    }
    
    .score-badge {
        background: #28a745;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ===== ГЛАВНАЯ ФУНКЦИЯ =====
def main():
    """Главная функция приложения"""
    
    # Инициализация игрового состояния
    init_game_state()
    
    # Хедер приложения
    render_header()
    
    # Боковая панель с профилем
    render_sidebar()
    
    # Основной контент
    render_main_content()
    
    # Футер
    render_footer()

# ===== ИНИЦИАЛИЗАЦИЯ =====
def init_game_state():
    """Инициализация игрового состояния"""
    if 'player_id' not in st.session_state:
        st.session_state.player_id = str(uuid.uuid4())[:8]
    
    if 'player_stats' not in st.session_state:
        st.session_state.player_stats = {
            'score': 0,
            'level': 1,
            'solved_cases': set(),
            'current_streak': 0,
            'best_streak': 0,
            'achievements': set(),
            'play_time': 0,
            'started_at': datetime.now().isoformat()
        }
    
    if 'current_case' not in st.session_state:
        st.session_state.current_case = None

# ===== ИНТЕРФЕЙС =====
def render_header():
    """Рендер заголовка"""
    st.markdown("""
    <div class="detective-header">
        <h1>🕵️ Statistical Detective</h1>
        <h3>Игра для аналитиков: Поймай ошибку раньше, чем она поймает тебя!</h3>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Боковая панель с профилем игрока"""
    with st.sidebar:
        st.header("👤 Профиль детектива")
        
        stats = st.session_state.player_stats
        
        # Основные метрики
        col1, col2 = st.columns(2)
        with col1:
            st.metric("🎯 Очки", stats['score'])
            st.metric("🔥 Серия", stats['current_streak'])
        with col2:
            st.metric("⭐ Уровень", stats['level'])
            st.metric("✅ Решено", len(stats['solved_cases']))
        
        # Прогресс до следующего уровня
        next_level_threshold = stats['level'] * 100
        current_progress = stats['score'] % 100
        progress_pct = current_progress / 100
        
        st.markdown("**Прогресс до следующего уровня:**")
        st.progress(progress_pct)
        st.caption(f"{current_progress}/100 очков")
        
        # Последние достижения
        if stats['achievements']:
            st.markdown("**🏆 Последние достижения:**")
            for achievement in list(stats['achievements'])[-3:]:
                st.success(f"🎖️ {achievement}")
        
        # Кнопка сброса (для разработки)
        if st.button("🔄 Сбросить прогресс"):
            reset_game_state()
            st.rerun()

def render_main_content():
    """Основной контент приложения"""
    
    # Навигация по режимам
    game_mode = st.selectbox(
        "🎮 Выберите режим игры:",
        [
            "🏠 Главная страница",
            "🔍 Найди ошибку в анализе",
            "🎯 Сценарии принятия решений",
            "⚠️ Поймай предвзятость",
            "🎲 Случайный кейс",
            "📊 Статистика и рейтинги"
        ]
    )
    
    # Роутинг по режимам
    if game_mode == "🏠 Главная страница":
        render_home_page()
    elif game_mode == "🔍 Найди ошибку в анализе":
        render_error_hunting_mode()
    elif game_mode == "🎯 Сценарии принятия решений":
        render_decision_scenarios_mode()
    elif game_mode == "⚠️ Поймай предвзятость":
        render_bias_hunting_mode()
    elif game_mode == "🎲 Случайный кейс":
        render_random_case_mode()
    elif game_mode == "📊 Статистика и рейтинги":
        render_stats_mode()

def render_home_page():
    """Главная страница с выбором активности"""
    st.markdown("## 🎯 Добро пожаловать, детектив!")
    
    st.markdown("""
    Ты попал в мир статистических загадок и аналитических головоломок! 
    Здесь тебя ждут реальные кейсы из маркетинговой и продуктовой аналитики.
    """)
    
    # Карточки с режимами игры
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_mode_card(
            "🔍 Охота за ошибками",
            "Найди критические ошибки в анализе данных",
            "Сложность: ⭐⭐⭐",
            "error_hunting"
        )
    
    with col2:
        render_mode_card(
            "🎯 Принятие решений",
            "Пошаговые сценарии из реальной практики",
            "Сложность: ⭐⭐⭐⭐",
            "decisions"
        )
    
    with col3:
        render_mode_card(
            "⚠️ Детектор предвзятостей",
            "Найди скрытые искажения в данных",
            "Сложность: ⭐⭐⭐⭐⭐",
            "bias_detection"
        )
    
    # Последние новости / обновления
    render_news_section()

def render_mode_card(title: str, description: str, difficulty: str, mode_key: str):
    """Рендер карточки режима игры"""
    st.markdown(f"""
    <div class="case-card">
        <h4>{title}</h4>
        <p>{description}</p>
        <p><strong>{difficulty}</strong></p>
    </div>
    """, unsafe_allow_html=True)

def render_news_section():
    """Секция новостей и обновлений"""
    st.markdown("---")
    st.markdown("## 📰 Новости детективного бюро")
    
    news_items = [
        {
            'date': '2025-05-23',
            'title': 'Добавлены новые кейсы по A/B тестированию',
            'description': 'Теперь доступны сложные сценарии с multiple testing и практической значимостью'
        },
        {
            'date': '2025-05-20',
            'title': 'Система достижений обновлена',
            'description': 'Добавлены новые бейджи для специализаций: маркетинг, продукт, веб-аналитика'
        }
    ]
    
    for news in news_items:
        with st.expander(f"📅 {news['date']} - {news['title']}"):
            st.write(news['description'])

# ===== ИГРОВЫЕ РЕЖИМЫ =====
def render_error_hunting_mode():
    """Режим охоты за ошибками"""
    st.markdown("## 🔍 Охота за ошибками в анализе")
    st.markdown("Перед тобой реальные кейсы с ошибками. Найди их все!")
    
    # Здесь будет твой код из предыдущего артефакта
    st.info("🚧 Режим в разработке. Скоро здесь появятся кейсы!")

def render_decision_scenarios_mode():
    """Режим сценариев принятия решений"""
    st.markdown("## 🎯 Сценарии принятия решений")
    st.info("🚧 Режим в разработке. Скоро здесь появятся сценарии!")

def render_bias_hunting_mode():
    """Режим охоты за предвзятостями"""
    st.markdown("## ⚠️ Детектор предвзятостей")
    st.info("🚧 Режим в разработке. Скоро здесь появится охота за bias!")

def render_random_case_mode():
    """Режим случайного кейса"""
    st.markdown("## 🎲 Случайный кейс")
    
    if st.button("🎲 Получить случайный кейс", type="primary"):
        st.info("🚧 Скоро здесь появится генератор случайных кейсов!")

def render_stats_mode():
    """Режим статистики и рейтингов"""
    st.markdown("## 📊 Статистика и рейтинги")
    
    stats = st.session_state.player_stats
    
    # Детальная статистика
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Твоя статистика")
        
        stats_data = {
            'Метрика': [
                'Общий счет',
                'Текущий уровень', 
                'Решено кейсов',
                'Текущая серия',
                'Лучшая серия',
                'Время игры (мин)'
            ],
            'Значение': [
                stats['score'],
                stats['level'],
                len(stats['solved_cases']),
                stats['current_streak'],
                stats['best_streak'],
                stats['play_time']
            ]
        }
        
        st.table(stats_data)
    
    with col2:
        st.markdown("### 🏆 Достижения")
        
        if stats['achievements']:
            for achievement in stats['achievements']:
                st.success(f"🎖️ {achievement}")
        else:
            st.info("Пока достижений нет. Начни решать кейсы!")

# ===== ИГРОВАЯ МЕХАНИКА =====
def award_points(points: int, case_id: str = None):
    """Начисление очков игроку"""
    st.session_state.player_stats['score'] += points
    
    if case_id:
        st.session_state.player_stats['solved_cases'].add(case_id)
    
    # Обновление уровня
    new_level = (st.session_state.player_stats['score'] // 100) + 1
    if new_level > st.session_state.player_stats['level']:
        st.session_state.player_stats['level'] = new_level
        st.balloons()
        st.success(f"🎉 Поздравляем! Вы достигли {new_level} уровня!")
    
    # Обновление серии
    st.session_state.player_stats['current_streak'] += 1
    st.session_state.player_stats['best_streak'] = max(
        st.session_state.player_stats['best_streak'],
        st.session_state.player_stats['current_streak']
    )
    
    # Проверка достижений
    check_achievements()

def reset_streak():
    """Сброс серии при неправильном ответе"""
    st.session_state.player_stats['current_streak'] = 0

def check_achievements():
    """Проверка и выдача достижений"""
    stats = st.session_state.player_stats
    achievements = stats['achievements']
    
    # Первые очки
    if stats['score'] >= 10 and 'Первые шаги' not in achievements:
        achievements.add('Первые шаги')
        st.success("🎖️ Достижение: 'Первые шаги' - Заработай первые очки!")
    
    # Серии
    if stats['current_streak'] >= 5 and 'Серийный детектив' not in achievements:
        achievements.add('Серийный детектив')
        st.success("🎖️ Достижение: 'Серийный детектив' - 5 правильных ответов подряд!")
    
    # Уровни
    if stats['level'] >= 3 and 'Опытный сыщик' not in achievements:
        achievements.add('Опытный сыщик')
        st.success("🎖️ Достижение: 'Опытный сыщик' - Достигни 3 уровня!")

def reset_game_state():
    """Сброс игрового состояния"""
    st.session_state.player_stats = {
        'score': 0,
        'level': 1,
        'solved_cases': set(),
        'current_streak': 0,
        'best_streak': 0,
        'achievements': set(),
        'play_time': 0,
        'started_at': datetime.now().isoformat()
    }

def render_footer():
    """Футер приложения"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 О проекте")
        st.markdown("""
        **Statistical Detective** - интерактивная игра для развития навыков 
        аналитического мышления и выявления статистических ошибок.
        """)
    
    with col2:
        st.markdown("### 🔗 Связанные проекты")
        st.markdown("""
        - [Демонстрация вероятностных законов](https://probability-laws-demo.streamlit.app/)
        - [GitHub репозиторий](https://github.com/your-username/statistics-detective)
        """)
    
    with col3:
        st.markdown("### 📈 Статистика")
        st.metric("ID сессии", st.session_state.player_id)

# ===== ЗАПУСК ПРИЛОЖЕНИЯ =====
if __name__ == "__main__":
    main()
