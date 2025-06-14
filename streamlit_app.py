import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Настройка стиля seaborn
sns.set_style('whitegrid')

st.title("Дашборд продаж")

# Загрузим данные из CSV (замени путь на свой)
@st.cache_data
def load_data():
    url = "shopping_trends.csv"  # или загрузи локальный файл через st.file_uploader
    df = pd.read_csv(url)
    return df

df = load_data()


# Очистка данных: убираем пробелы и приводим к одному регистру
df['Gender'] = df['Gender'].astype(str).str.strip().str.capitalize()

# Теперь замена на русский
df['Gender'] = df['Gender'].replace({
    'Female': 'Женщины',
    'Male': 'Мужчины'
})


# Переводим значения столбцов на русский
df['Category'] = df['Category'].replace({
    'Clothing': 'Одежда',
    'Electronics': 'Электроника',
    'Groceries': 'Продукты',
    'Cosmetics': 'Косметика',
    'Home': 'Дом',
    'Other': 'Другое',
    'Footwear': 'Обувь',
    'Accessories': 'Аксессуары',
    'Outerwear': 'Верхняя одежда',
})
df['Gender'] = df['Gender'].replace({
    'Female': 'Женщины',
    'Male': 'Мужчины'
})
df['Season'] = df['Season'].replace({
    'Spring': 'Весна',
    'Summer': 'Лето',
    'Fall': 'Осень',
    'Winter': 'Зима'
})
df['Frequency of Purchases'] = df['Frequency of Purchases'].replace({
    'Everyday': 'Ежедневно',
    'Weekly': 'Еженедельно',
    'Monthly': 'Ежемесячно',
    'Rarely': 'Редко',
    'Every 3 Months': 'Каждые 3 месяца',
    'Bi-Weekly': 'Дважды в неделю',
    'Quarterly': 'Квартально',
    'Fortnightly': 'Каждые 2 недели',
    'Annually': 'Ежегодно'})
if 'Payment Method' in df.columns:
    df['Payment Method'] = df['Payment Method'].replace({
        'Credit Card': 'Карта',
        'Cash': 'Наличные',
        'Online': 'Онлайн',
        'Mobile Payment': 'Мобильный платеж',
        'Bank Transfer': 'Банковский перевод',
        'Gift Card': 'Подарочная карта',
        'PayPal': 'PayPal',
        'Cryptocurrency': 'Криптовалюта',
        'Other': 'Другое',
        'Debit Card': 'Дебетовая карта',
        'Venmo': 'Перевод на карту',
    })

# Колонки для двух колонок
col1, col2 = st.columns(2)


# График 1: Средняя сумма покупки по категориям
with col2:
    st.subheader("Средняя сумма покупки по категориям")
    avg_purchase = df.groupby('Category')['Purchase Amount (USD)'].mean().sort_values()
    fig, ax = plt.subplots()
    avg_purchase.plot(kind='barh', color='coral', ax=ax)
    ax.set_xlabel("Средняя сумма покупки (USD)")
    ax.set_ylabel("Категория")
    st.pyplot(fig)

# График 2: Пол покупателей
with col1:
    st.subheader("Распределение по полу")
    gender_counts = df['Gender'].value_counts()
    fig, ax = plt.subplots()
    gender_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#ff9999'], ax=ax)
    ax.set_ylabel('')
    st.pyplot(fig)

# График 3: Количество покупок по сезонам
with col2:
    st.subheader("Количество покупок по сезонам")
    season_counts = df['Season'].value_counts()
    fig, ax = plt.subplots()
    sns.barplot(x=season_counts.index, y=season_counts.values, palette='viridis', ax=ax)
    ax.set_xlabel("Сезон")
    ax.set_ylabel("Количество покупок")
    st.pyplot(fig)


# График 4: Частота покупок
with col2:
    st.subheader("Частота покупок")
    freq_counts = df['Frequency of Purchases'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(6,4))
    sns.barplot(x=freq_counts.index, y=freq_counts.values, palette='magma', ax=ax)
    ax.set_xlabel("Частота покупок")
    ax.set_ylabel("Количество")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# График 5: Возрастная структура покупателей
with col1:
    st.subheader("Возрастная структура покупателей")
    fig, ax = plt.subplots()
    sns.histplot(df['Age'], bins=10, kde=True, color='skyblue', ax=ax)
    ax.set_xlabel("Возраст")
    ax.set_ylabel("Количество покупателей")
    st.pyplot(fig)

# График 6: Распределение по способу оплаты
with col1:
    st.subheader("Распределение по способу оплаты")
    if 'Payment Method' in df.columns:
        payment_counts = df['Payment Method'].value_counts()
        fig, ax = plt.subplots()
        payment_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, ax=ax, cmap='Pastel1')
        ax.set_ylabel('')
        st.pyplot(fig)
    else:
        st.info("Нет данных о способе оплаты.")
