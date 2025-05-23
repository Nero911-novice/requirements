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
import time
import random

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
    
    # Получаем кейсы для поиска ошибок
    error_cases = get_analysis_error_cases()
    
    # Выбор сложности
    difficulty = st.selectbox("Уровень сложности:", ["Новичок", "Аналитик", "Эксперт"])
    
    # Фильтруем кейсы по сложности
    available_cases = [case for case in error_cases if case['difficulty'] == difficulty]
    
    if not available_cases:
        st.warning("Все кейсы этого уровня решены! Попробуй другой уровень.")
        return
    
    # Выбираем случайный нерешенный кейс
    unsolved_cases = [case for case in available_cases if case['id'] not in st.session_state.player_stats['solved_cases']]
    if not unsolved_cases:
        unsolved_cases = available_cases  # Показываем все, если все решены
    
    # Выбор конкретного кейса
    case_titles = [case['title'] for case in unsolved_cases]
    if case_titles:
        selected_title = st.selectbox("Выберите кейс:", case_titles)
        current_case = next(case for case in unsolved_cases if case['title'] == selected_title)
        
        # Отображаем кейс
        display_analysis_case(current_case)

def render_decision_scenarios_mode():
    """Режим сценариев принятия решений"""
    st.markdown("## 🎯 Сценарии принятия решений")
    st.markdown("Пошаговые кейсы из реальной маркетинговой аналитики. Каждое решение влияет на исход!")
    
    scenarios = get_decision_scenarios()
    
    scenario_choice = st.selectbox("Выберите сценарий:", [s['title'] for s in scenarios])
    selected_scenario = next(s for s in scenarios if s['title'] == scenario_choice)
    
    play_scenario(selected_scenario)

def render_bias_hunting_mode():
    """Режим охоты за предвзятостями"""
    st.markdown("## ⚠️ Детектор предвзятостей")
    st.markdown("Найди скрытые искажения и предвзятости в данных!")
    
    bias_cases = get_bias_cases()
    
    bias_choice = st.selectbox("Выберите кейс:", [case['title'] for case in bias_cases])
    selected_case = next(case for case in bias_cases if case['title'] == bias_choice)
    
    display_bias_case(selected_case)

def render_random_case_mode():
    """Режим случайного кейса"""
    st.markdown("## 🎲 Случайный кейс")
    st.markdown("Получи случайный кейс для тренировки навыков!")
    
    if st.button("🎲 Получить случайный кейс", type="primary"):
        # Собираем все кейсы
        all_cases = []
        all_cases.extend(get_analysis_error_cases())
        all_cases.extend([{'type': 'scenario', **s} for s in get_decision_scenarios()])
        all_cases.extend([{'type': 'bias', **b} for b in get_bias_cases()])
        
        if all_cases:
            import random
            random_case = random.choice(all_cases)
            
            st.success(f"🎯 Случайный кейс: **{random_case['title']}**")
            
            if random_case.get('type') == 'scenario':
                st.markdown("**Тип**: Сценарий принятия решений")
                play_scenario(random_case)
            elif random_case.get('type') == 'bias':
                st.markdown("**Тип**: Детектор предвзятостей")
                display_bias_case(random_case)
            else:
                st.markdown("**Тип**: Поиск ошибки в анализе")
                display_analysis_case(random_case)

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
        - [GitHub репозиторий](https://github.com/Nero911-novice/statistics-detective)
        """)
    
    with col3:
        st.markdown("### 📈 Статистика")
        st.metric("ID сессии", st.session_state.player_id)

# ===== КЕЙСЫ И ДАННЫЕ =====

def get_analysis_error_cases() -> List[Dict]:
    """База кейсов с ошибками в анализе"""
    return [
        {
            'id': 'marketing_conversion_1',
            'difficulty': 'Новичок',
            'title': 'Анализ конверсии email-кампании',
            'description': """
            **Ситуация**: Маркетолог анализирует эффективность email-кампании.
            
            **Данные**:
            - Отправлено писем: 10,000
            - Открыто писем: 2,500 (25%)
            - Переходы на сайт: 250 (10% от открывших)
            - Покупки: 25 (10% от перешедших)
            
            **Вывод маркетолога**: "Конверсия кампании составляет 10%"
            """,
            'chart_data': {
                'emails_sent': 10000,
                'opened': 2500,
                'clicked': 250,
                'purchased': 25
            },
            'options': [
                "Конверсия должна считаться от общего числа отправленных писем (0.25%)",
                "Ошибка в расчете процента открытия",
                "Нужно учесть bounce rate",
                "Анализ корректен, ошибки нет"
            ],
            'correct': 0,
            'explanation': """
            **Правильный ответ**: Конверсия должна считаться от общего числа отправленных писем.
            
            **Объяснение**: Маркетолог считал конверсию от числа перешедших (25/250 = 10%), 
            но истинная конверсия кампании = покупки/отправленные письма = 25/10,000 = 0.25%.
            
            **Урок**: Всегда четко определяй базу для расчета конверсии!
            """,
            'points': 10
        },
        {
            'id': 'ab_test_significance',
            'difficulty': 'Аналитик', 
            'title': 'Ложная значимость A/B теста',
            'description': """
            **Ситуация**: Анализируешь A/B тест новой посадочной страницы.
            
            **Результаты**:
            - Группа A (контроль): 1,000 визитов, 50 конверсий (5.0%)
            - Группа B (тест): 1,000 визитов, 65 конверсий (6.5%)
            - p-value = 0.048 (< 0.05)
            
            **Вывод**: "Тест статистически значим! Внедряем версию B!"
            """,
            'chart_data': None,
            'options': [
                "Нужно проверить мощность теста",
                "Размер выборки слишком мал для надежных выводов", 
                "Не учтена практическая значимость (effect size)",
                "Все перечисленное выше"
            ],
            'correct': 3,
            'explanation': """
            **Правильный ответ**: Все перечисленное выше.
            
            **Проблемы**:
            1. **Мощность теста**: При таких размерах выборки мощность ~60% (нужно >80%)
            2. **Малая выборка**: 1000 визитов недостаточно для конверсии ~5%
            3. **Effect size**: Разница 1.5% может быть не значима практически
            
            **Урок**: Статистическая значимость ≠ практическая значимость!
            """,
            'points': 15
        },
        {
            'id': 'simpsons_paradox',
            'difficulty': 'Эксперт',
            'title': 'Парадокс Симпсона в маркетинге',
            'description': """
            **Ситуация**: Сравниваешь эффективность двух рекламных каналов.
            
            **Общие результаты**:
            - Канал A: 1000 показов, 100 кликов (10% CTR)
            - Канал B: 1000 показов, 80 кликов (8% CTR)
            
            **По устройствам**:
            Desktop: A = 200/300 (66.7%), B = 50/100 (50%)
            Mobile: A = 100/700 (14.3%), B = 30/900 (3.3%)
            
            **Вопрос**: Какой канал лучше?
            """,
            'chart_data': {
                'total': {'A': 0.10, 'B': 0.08},
                'desktop': {'A': 0.667, 'B': 0.50},
                'mobile': {'A': 0.143, 'B': 0.033}
            },
            'options': [
                "Канал A лучше - общий CTR выше",
                "Канал B лучше - эффективнее на всех устройствах",
                "Парадокс Симпсона: A лучше в каждой группе, но B лучше в целом",
                "Недостаточно данных для выводов"
            ],
            'correct': 2,
            'explanation': """
            **Правильный ответ**: Парадокс Симпсона.
            
            **Объяснение**: 
            - Канал A лучше на КАЖДОМ типе устройства
            - Но общий CTR канала A ниже из-за разного распределения трафика
            - A получает больше сложного mobile-трафика (70% vs 90%)
            
            **Урок**: Всегда анализируй данные в разрезе сегментов!
            """,
            'points': 25
        },
        {
            'id': 'correlation_causation',
            'difficulty': 'Аналитик',
            'title': 'Корреляция vs Причинность',
            'description': """
            **Ситуация**: Аналитик нашел сильную корреляцию между расходами на рекламу и продажами.
            
            **Данные за 12 месяцев**:
            - Корреляция между ad spend и revenue: r = 0.89
            - При увеличении рекламы на $1000, revenue растет на $3500
            
            **Вывод**: "Каждый доллар рекламы приносит $3.50 дохода. Увеличиваем бюджет в 2 раза!"
            """,
            'chart_data': None,
            'options': [
                "Корреляция не означает причинность - нужны дополнительные тесты",
                "ROI 3.5:1 отличный, можно увеличивать бюджет",
                "Нужно учесть seasonality и другие факторы",
                "А и С правильные"
            ],
            'correct': 3,
            'explanation': """
            **Правильный ответ**: А и С правильные.
            
            **Проблемы**:
            1. **Корреляция ≠ Причинность**: Возможно, продажи растут из-за сезонности
            2. **Omitted variable bias**: Не учтены конкуренты, экономика, тренды
            3. **Reverse causality**: Возможно, при росте продаж увеличивают рекламу
            
            **Правильно**: A/B тест с контрольной группой без увеличения рекламы
            """,
            'points': 20
        },
        {
            'id': 'cherry_picking',
            'difficulty': 'Новичок', 
            'title': 'Селективная подача данных',
            'description': """
            **Ситуация**: Менеджер продукта представляет результаты нового feature.
            
            **Презентация**:
            "Наш новый feature показал отличные результаты:
            - Engagement вырос на 15% (с 20% до 23%)
            - Time on page увеличилось на 30 секунд
            - Положительные отзывы составили 78%"
            
            **Скрытая информация**:
            - Retention упал с 45% до 38%
            - Conversion rate снизился с 3.2% до 2.8%
            - Тестировали только на power users
            """,
            'chart_data': None,
            'options': [
                "Результаты отличные, feature успешен",
                "Cherry-picking: показаны только положительные метрики",
                "Нужно больше времени для оценки",
                "Тест проведен некорректно"
            ],
            'correct': 1,
            'explanation': """
            **Правильный ответ**: Cherry-picking данных.
            
            **Проблема**: Показаны только метрики, которые улучшились, а критические 
            бизнес-метрики (retention, conversion) скрыты.
            
            **Урок**: Всегда требуй полную картину метрик, особенно северные звезды!
            """,
            'points': 10
        }
    ]

def get_decision_scenarios() -> List[Dict]:
    """База сценариев принятия решений"""
    return [
        {
            'title': 'Кризис снижения конверсии',
            'id': 'conversion_crisis',
            'description': """
            **Ситуация**: Конверсия интернет-магазина упала с 3% до 2% за последний месяц.
            Руководство требует срочного анализа и плана действий.
            """,
            'steps': [
                {
                    'text': "С чего начнешь анализ?",
                    'options': [
                        "Сразу проверю технические изменения на сайте",
                        "Проанализирую данные в разрезе сегментов",
                        "Запущу A/B тест новой страницы",
                        "Изучу конкурентов"
                    ],
                    'correct': 1,
                    'feedback': {
                        0: "Хорошая мысль, но сначала нужно понять масштаб проблемы через данные.",
                        1: "Отлично! Сегментный анализ покажет, где именно проблема.",
                        2: "Преждевременно - сначала нужно найти причину текущего падения.",
                        3: "Полезно, но вторично. Сначала разберись с собственными данными."
                    }
                },
                {
                    'text': "Сегментный анализ показал: мобильная конверсия упала с 2.5% до 1.2%, десктопная стабильна (4.2%). Следующий шаг?",
                    'options': [
                        "Проверю изменения в мобильной версии сайта",
                        "Изучу источники трафика на мобильных",
                        "Проанализирую техническую производительность мобильной версии",
                        "Все вышеперечисленное"
                    ],
                    'correct': 3,
                    'feedback': {
                        0: "Правильно, но этого недостаточно для полной картины.",
                        1: "Важный аспект, но не единственный.",
                        2: "Критически важно, но нужен комплексный подход.",
                        3: "Превосходно! Комплексный анализ даст полную картину."
                    }
                },
                {
                    'text': "Анализ показал: новый мобильный checkout увеличил количество шагов с 3 до 5. Скорость загрузки выросла с 2с до 4с. Что делаешь?",
                    'options': [
                        "Откатываю изменения немедленно",
                        "Запускаю A/B тест старой vs новой версии",
                        "Оптимизирую новую версию (скорость + UX)",
                        "Собираю фокус-группу для качественного исследования"
                    ],
                    'correct': 2,
                    'feedback': {
                        0: "Быстро, но не оптимально - теряешь потенциальные улучшения новой версии.",
                        1: "Хорошо, но ты уже знаешь проблемы - лучше их сначала исправить.",
                        2: "Отлично! Фиксишь известные проблемы, сохраняя потенциал новой версии.",
                        3: "Полезно, но слишком медленно для кризисной ситуации."
                    }
                }
            ]
        },
        {
            'title': 'Аномальный рост метрики',
            'id': 'metric_anomaly', 
            'description': """
            **Ситуация**: Вчера DAU вырос на 40% без видимых причин. 
            Менеджмент в восторге, но тебе что-то кажется подозрительным.
            """,
            'steps': [
                {
                    'text': "Твоя первая реакция на аномальный рост?",
                    'options': [
                        "Поздравлю команду с отличным результатом",
                        "Проверю данные на наличие ошибок и дубликатов",
                        "Проанализирую источники трафика",
                        "Проверю, не было ли технических изменений"
                    ],
                    'correct': 1,
                    'feedback': {
                        0: "Слишком рано радоваться - аномалии часто означают ошибки в данных.",
                        1: "Правильно! Первым делом - валидация данных.",
                        2: "Важно, но сначала убедись, что данные корректны.",
                        3: "Хорошая мысль, но начни с проверки качества данных."
                    }
                },
                {
                    'text': "Обнаружил: система аналитики считала одного пользователя как нескольких из-за бага. Как поступишь?",
                    'options': [
                        "Исправлю данные задним числом и никому не скажу",
                        "Сообщу команде об ошибке и исправлю метрики",
                        "Оставлю как есть - рост уже анонсировали",
                        "Создам новую метрику вместо исправления старой"
                    ],
                    'correct': 1,
                    'feedback': {
                        0: "Непрозрачно и может привести к неправильным решениям в будущем.",
                        1: "Правильно! Честность в данных критически важна.",
                        2: "Плохо - команда будет принимать решения на основе ложных данных.",
                        3: "Избыточно сложно и создает путаницу."
                    }
                }
            ]
        }
    ]

def get_bias_cases() -> List[Dict]:
    """База кейсов с предвзятостями"""
    return [
        {
            'title': 'Предвзятость выжившего в A/B тесте',
            'id': 'survivorship_bias',
            'description': """
            **Кейс**: Тестируем новую форму подписки на email.
            
            **Результаты через 2 недели**:
            - Версия A: 1000 показов, 100 подписок (10%)
            - Версия B: 1000 показов, 150 подписок (15%)
            
            **Вывод**: "Версия B лучше на 50%! Внедряем!"
            """,
            'bias_type': 'survivorship',
            'chart_data': {
                'shown': [1000, 1000],
                'subscribed': [100, 150],
                'active_after_month': [85, 90]
            },
            'questions': [
                "Какую предвзятость ты видишь в этом анализе?",
                "Что еще нужно проверить?"
            ],
            'hints': [
                "Подумай о долгосрочной перспективе...",
                "Что происходит с подписчиками через месяц?"
            ],
            'revelation': """
            **Скрытая информация**: Через месяц активных остались:
            - Версия A: 85 из 100 (85% retention)
            - Версия B: 90 из 150 (60% retention)
            
            **Вывод**: Версия B привлекает больше подписчиков, но они менее качественные!
            """
        },
        {
            'title': 'Систематическая ошибка отбора',
            'id': 'selection_bias',
            'description': """
            **Исследование**: Эффективность нового email-дизайна.
            
            **Методология**: Отправили новый дизайн подписчикам, которые открывали 
            письма в последние 30 дней.
            
            **Результат**: Open rate увеличился с 25% до 35%!
            """,
            'bias_type': 'selection',
            'questions': [
                "В чем проблема этого исследования?",
                "Как это влияет на выводы?"
            ],
            'hints': [
                "Подумай о выборке...",
                "Кого включили в тест?"
            ],
            'revelation': """
            **Проблема**: Тестировали только на активных пользователях!
            Это как тестировать новый самолет только на пилотах-асах.
            
            **Правильно**: Случайная выборка из всей базы подписчиков.
            """
        },
        {
            'title': 'Предвзятость подтверждения',
            'id': 'confirmation_bias',
            'description': """
            **Ситуация**: Продуктовая команда запустила новый feature. 
            После двух недель A/B теста:
            
            **Метрики**:
            - Engagement: +12% ✅
            - Session duration: +8% ✅  
            - Revenue per user: -3% ❌
            - User retention: -5% ❌
            
            **Вывод команды**: "Feature успешен! Engagement растет!"
            """,
            'bias_type': 'confirmation',
            'questions': [
                "Какая предвзятость проявляется в выводах?",
                "Как правильно интерпретировать результаты?"
            ],
            'hints': [
                "Команда видит только то, что хочет видеть...",
                "Какие метрики важнее для бизнеса?"
            ],
            'revelation': """
            **Предвзятость подтверждения**: Команда фокусируется только на положительных 
            метриках, игнорируя критичные для бизнеса (revenue, retention).
            
            **Правильно**: Смотреть на полную картину метрик и их приоритеты.
            """
        }
    ]

def display_analysis_case(case: Dict):
    """Отображение кейса для анализа"""
    st.markdown(f"### {case['title']}")
    st.markdown(case['description'])
    
    # Визуализация данных, если есть
    if case.get('chart_data'):
        create_case_visualization(case)
    
    # Варианты ответов
    st.markdown("### 🤔 Что не так с этим анализом?")
    
    answer = st.radio("Выбери правильный ответ:", case['options'], key=f"case_{case['id']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Проверить ответ", key=f"check_{case['id']}"):
            check_analysis_answer(case, answer)
    
    with col2:
        if st.button("💡 Подсказка", key=f"hint_{case['id']}"):
            give_hint(case)

def create_case_visualization(case: Dict):
    """Создание визуализации для кейса"""
    case_id = case['id']
    
    if case_id == 'marketing_conversion_1':
        # Воронка конверсии
        fig, ax = plt.subplots(figsize=(10, 6))
        
        stages = ['Отправлено', 'Открыто', 'Перешли', 'Купили']
        values = [10000, 2500, 250, 25]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        bars = ax.bar(stages, values, color=colors, alpha=0.7)
        
        # Добавляем проценты
        for i, (bar, value) in enumerate(zip(bars, values)):
            if i > 0:
                pct = (value / values[i-1]) * 100
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100,
                       f'{pct:.1f}%', ha='center', va='bottom', fontweight='bold')
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
                   f'{value:,}', ha='center', va='center', color='white', fontweight='bold')
        
        ax.set_title("Воронка email-кампании", fontsize=14)
        ax.set_ylabel("Количество")
        
        fig.tight_layout()
        st.pyplot(fig)
        
    elif case_id == 'simpsons_paradox':
        # Демонстрация парадокса Симпсона
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Общие результаты
        channels = ['Канал A', 'Канал B']
        ctr_total = [10, 8]
        ax1.bar(channels, ctr_total, color=['blue', 'red'], alpha=0.7)
        ax1.set_title("Общий CTR (%)")
        ax1.set_ylabel("CTR (%)")
        
        # По устройствам
        devices = ['Desktop', 'Mobile']
        ctr_a = [66.7, 14.3]
        ctr_b = [50.0, 3.3]
        
        x = np.arange(len(devices))
        width = 0.35
        
        ax2.bar(x - width/2, ctr_a, width, label='Канал A', color='blue', alpha=0.7)
        ax2.bar(x + width/2, ctr_b, width, label='Канал B', color='red', alpha=0.7)
        
        ax2.set_title("CTR по устройствам (%)")
        ax2.set_ylabel("CTR (%)")
        ax2.set_xticks(x)
        ax2.set_xticklabels(devices)
        ax2.legend()
        
        fig.tight_layout()
        st.pyplot(fig)

def check_analysis_answer(case: Dict, user_answer: str):
    """Проверка ответа пользователя"""
    correct_index = case['correct']
    user_index = case['options'].index(user_answer)
    
    if user_index == correct_index:
        st.success("🎉 Правильно! Отличная работа, детектив!")
        st.markdown(case['explanation'])
        
        # Начисляем очки
        award_points(case['points'], case['id'])
        
        st.balloons()
        
    else:
        st.error("❌ Неправильно. Попробуй еще раз!")
        reset_streak()
        
        # Показываем частичную подсказку
        st.info("💡 Подсказка: Внимательно посмотри на определения и базы для расчета.")

def give_hint(case: Dict):
    """Система подсказок"""
    hints = {
        'marketing_conversion_1': "🔍 Подсказка: Обрати внимание на то, от какого числа считается процент. Что такое 'конверсия кампании'?",
        'ab_test_significance': "🔍 Подсказка: p-value < 0.05 не гарантирует практической значимости. Какие еще метрики важны?",
        'simpsons_paradox': "🔍 Подсказка: Посмотри на результаты отдельно по каждому устройству. Что происходит внутри групп vs в целом?",
        'correlation_causation': "🔍 Подсказка: Корреляция не равна причинности. Какие факторы могли повлиять?",
        'cherry_picking': "🔍 Подсказка: Какие важные метрики могли быть скрыты?"
    }
    
    hint = hints.get(case['id'], "🔍 Общая подсказка: Всегда проверяй определения, базы расчета и скрытые переменные!")
    st.info(hint)

def play_scenario(scenario: Dict):
    """Проигрывание сценария"""
    st.markdown(f"### {scenario['title']}")
    st.markdown(scenario['description'])
    
    # Инициализация состояния сценария
    scenario_key = f"scenario_{scenario['id']}"
    if scenario_key not in st.session_state:
        st.session_state[scenario_key] = {'step': 0, 'score': 0, 'choices': []}
    
    current_step = st.session_state[scenario_key]['step']
    
    if current_step < len(scenario['steps']):
        step = scenario['steps'][current_step]
        
        st.markdown(f"#### Шаг {current_step + 1}")
        st.markdown(step['text'])
        
        choice = st.radio("Твое решение:", step['options'], key=f"{scenario_key}_step_{current_step}")
        
        if st.button("Принять решение", key=f"{scenario_key}_decide_{current_step}"):
            user_choice_index = step['options'].index(choice)
            st.session_state[scenario_key]['choices'].append(user_choice_index)
            
            # Показываем обратную связь
            feedback = step['feedback'][user_choice_index]
            
            if user_choice_index == step['correct']:
                st.success(f"✅ {feedback}")
                st.session_state[scenario_key]['score'] += 10
                award_points(10)
            else:
                st.warning(f"🤔 {feedback}")
                reset_streak()
            
            # Переходим к следующему шагу
            st.session_state[scenario_key]['step'] += 1
            
            time.sleep(2)
            st.rerun()
    
    else:
        # Сценарий завершен
        total_score = st.session_state[scenario_key]['score']
        max_score = len(scenario['steps']) * 10
        
        st.success(f"🎉 Сценарий завершен! Ваш результат: {total_score}/{max_score}")
        
        if total_score == max_score:
            st.markdown("👑 Превосходная работа! Ты принял все оптимальные решения.")
        elif total_score >= max_score * 0.7:
            st.markdown("👍 Хорошая работа! Большинство решений были правильными.")
        else:
            st.markdown("📚 Есть что улучшить. Попробуй еще раз!")
        
        if st.button("Начать заново", key=f"{scenario_key}_restart"):
            del st.session_state[scenario_key]
            st.rerun()

def display_bias_case(case: Dict):
    """Отображение кейса с предвзятостью"""
    st.markdown(f"### {case['title']}")
    st.markdown(case['description'])
    
    # Создаем график с "обманчивыми" данными
    if 'chart_data' in case:
        create_bias_visualization(case, reveal_bias=False)
    
    # Вопросы для размышления
    for i, question in enumerate(case['questions']):
        st.markdown(f"**🤔 {question}**")
        user_input = st.text_area(f"Твои мысли:", key=f"bias_input_{case['id']}_{i}", height=100)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💡 Подсказка", key=f"bias_hint_{case['id']}"):
            for hint in case['hints']:
                st.info(hint)
    
    with col2:
        if st.button("🎭 Раскрыть предвзятость", key=f"bias_reveal_{case['id']}"):
            st.error("⚠️ **ПРЕДВЗЯТОСТЬ ОБНАРУЖЕНА!**")
            st.markdown(case['revelation'])
            
            # Показываем "честный" график
            if 'chart_data' in case:
                create_bias_visualization(case, reveal_bias=True)
    
    with col3:
        if st.button("✅ Понял!", key=f"bias_understood_{case['id']}"):
            award_points(20, case['id'])
            st.success("Отлично! +20 очков детектива!")

def create_bias_visualization(case: Dict, reveal_bias: bool = False):
    """Создание визуализации для демонстрации предвзятости"""
    if case['id'] == 'survivorship_bias':
        fig, ax = plt.subplots(figsize=(10, 6))
        
        versions = ['Версия A', 'Версия B']
        subscriptions = case['chart_data']['subscribed']
        
        bars = ax.bar(versions, subscriptions, color=['blue', 'orange'], alpha=0.7)
        
        # Добавляем проценты
        for bar, sub, shown in zip(bars, subscriptions, case['chart_data']['shown']):
            pct = (sub / shown) * 100
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                   f'{pct:.0f}%', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title("Результаты A/B теста подписок" + 
                    (" (ПОЛНАЯ КАРТИНА)" if reveal_bias else ""), fontsize=14)
        ax.set_ylabel("Количество подписок")
        
        if reveal_bias:
            # Показываем retention
            ax2 = ax.twinx()
            retention = [active/sub * 100 for active, sub in 
                        zip(case['chart_data']['active_after_month'], subscriptions)]
            
            line = ax2.plot(versions, retention, 'ro-', linewidth=3, markersize=10, 
                           label='Retention через месяц (%)')
            ax2.set_ylabel("Retention (%)", color='red')
            ax2.tick_params(axis='y', labelcolor='red')
            
            # Добавляем аннотации retention
            for i, (version, ret) in enumerate(zip(versions, retention)):
                ax2.annotate(f'{ret:.0f}%', xy=(i, ret), xytext=(10, 10),
                           textcoords='offset points', color='red', fontweight='bold')
            
            ax2.legend(loc='upper right')
        
        fig.tight_layout()
        st.pyplot(fig)

# ===== ЗАПУСК ПРИЛОЖЕНИЯ =====
if __name__ == "__main__":
    main()
