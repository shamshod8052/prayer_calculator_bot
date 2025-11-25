# 🕌 Namoz Vaqti Bot

> Bu bot namoz qazolaringizni doimiy hisoblab borishda ko'maklashadi. Viloyatlar bo'yicha namoz vaqtlarini ko'rsatadi. Qazolar sonini qo'lda o'zgartirish ham mumkin. Har kunlik qaysi namozlarni o'qidi yoki yo'q — barchasi maxsus tugmali so'rovnoma orqali bazaga kiritiladi.
> Bot: @tafsoft_namoz_bot

---

## 📖 Description

**Namoz Vaqti Bot** — musulmonlar uchun qulay yordamchi bo‘lib, foydalanuvchilarga quyidagilarni taqdim etadi:

- Viloyatlar bo‘yicha aniq **namoz vaqtlarini ko‘rsatish**
- O‘qilmagan namozlarni **qazo hisobida yuritish**
- Qazolar sonini **qo‘lda o‘zgartirish**
- Har kuni avtomatik yuboriladigan **interaktiv tugmali so‘rovnoma** orqali o‘qilgan/o‘qilmagan namozlarni bazaga yozish

Loyiha **Django** va **Aiogram 3** yordamida yaratilgan bo‘lib, ma’lumotlar bazasi orqali statistikani ham saqlaydi.

---
<img width="600" alt="image" src="https://github.com/user-attachments/assets/9af9e013-5f4c-49de-a30d-3f0348a9dcfb" />
<img width="600" alt="image" src="https://github.com/user-attachments/assets/e33ee40c-b27f-42c4-b6c2-c1a51e6ab884" />
<img width="600" alt="image" src="https://github.com/user-attachments/assets/2a08302f-6508-4344-a4b2-fd6845ddb344" />
<img width="600" alt="image" src="https://github.com/user-attachments/assets/8442f9bc-6613-444f-a8ef-60e34a4c57f7" />





## 📦 Tech Stack

- **Python 3.11.6**
- **Django 4.2.20**
- **aiogram 3.20.0**
- **PostgreSQL**
- **Redis**
- **django-ckeditor 6.7.2**
- **django-jazzmin 3.0.0**
- **psycopg2-binary 2.9.10**
- **requests 2.32.4**
- **pytz 2024.1**
- **environs 14.1.1**

---

## 🧩 Features

- 🕒 Viloyatlar bo‘yicha **aniq namoz vaqtlarini chiqarish**
- 🕌 Har kunlik namozlar uchun **interaktiv tugmali so‘rovnoma**
- 📊 O‘qilgan/o‘qilmagan namozlarni **bazaga yozish**
- ➕ Qazolar sonini **qo‘lda o‘zgartirish**
- 🔄 Qazo namozlarini **avtomatik hisoblab borish**
- 🧮 Foydalanuvchi uchun umumiy **qazo statistikasini chiqarish**

---

## ⚙️ Installation

1. **Ushbu repositoryni klonlab oling:**
   ```bash
   git clone https://github.com/username/namoz-vaqti-bot.git
   cd namoz-vaqti-bot
   ```
2.
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```
4. Kerakli kutubxonalarni o'rnating.
   ```bash
   pip install -r requirements.txt
   ```
6. Django migratsiyalarini bajaring:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
7. Django serverni ishga tushiring:
   ```bash
   python manage.py runserver
   ```
9. Botni ishga tushiring:
    ```bash
   python manage.py runbot
   ```

🧑‍💻 Author

Shamshod Ramazonov
Python Backend Developer

📜 License

This project is licensed under the MIT License.
