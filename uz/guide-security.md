# Xavfsizlik bo‘yicha tekshiruv ro‘yxati

Server va saytlarni himoyalash uchun panelda mavjud imkoniyatlar — bir joyda. Panel o‘rnatilgandan keyin shu ro‘yxatdan o‘ting.

## Panel va akkauntlar

- [ ] **`liveadmin` parolini almashtiring** va uni boshqa joyda ishlatmang — [Panel sozlamalari va xavfsizlik](panel-settings.md).
- [ ] **Ikki bosqichli kirishni (2FA) yoqing** va zaxira kodlarni xavfsiz joyda saqlang.
- [ ] **Tiklash emailini kiriting** — parol esdan chiqsa va muhim xabarnomalar uchun.
- [ ] **Login himoyasini sozlang:** urinishlar soni, blok muddati; o‘z IP manzilingizni oq ro‘yxatga qo‘shing.
- [ ] **fail2ban o‘rnating** (**Tizim → Ilovalar**) — SSH, FTP va pochta parol tanlash hujumlaridan himoyalanadi.
- [ ] **Panelga ishonchli sertifikat** oling yoki domen orqali kiring — [Panel manzili va SSL](panel-access.md).
- [ ] Har bir mijozga **alohida akkaunt** bering va faqat kerakli ruxsatlarni yoqing — [Foydalanuvchilar, rollar va limitlar](users.md).
- [ ] Kerak bo‘lmagan akkauntlarni o‘chirib qo‘ying yoki o‘chiring; vaqti-vaqti bilan [Amallar tarixi](api-tokens.md)ni ko‘rib chiqing.
- [ ] API tokenlarini eng kam ruxsat va qisqa muddat bilan yarating, keraksizlarini bekor qiling — [API v2 ma’lumotnomasi](api-reference.md).

## Server

- [ ] **Firewall’ni yoqing** va faqat kerakli portlarni qoldiring — [Firewall](firewall.md).
- [ ] Ishlatilmayotgan xizmatlarni to‘xtating (masalan pochta kerak bo‘lmasa) — [Tizim xizmatlari](services.md).
- [ ] Bazaga tashqi ulanishni faqat aniq IP’larga bering, `%` ishlatmang — [Ma’lumotlar bazalari](databases.md).
- [ ] SSH’ni faqat kerakli akkauntlarga yoqing.
- [ ] Panel avtomatik yangilanadi — litsenziya faol turishini kuzating — [Yangilanishlar va xabarnomalar](updates-notifications.md).

## Saytlar

- [ ] Har bir sayt uchun **SSL** va **HTTPS’ga yo‘naltirish** — [SSL sertifikatlar](ssl.md).
- [ ] Har bir saytni **alohida Linux foydalanuvchisida** yarating — bir sayt buzilsa, boshqalariga o‘tmaydi.
- [ ] Ichki va test saytlarni **IP bo‘yicha** yoki **login/parol** bilan yoping — [Sayt xavfsizligi va skanerlash](site-security.md).
- [ ] Botlar ko‘p bo‘lsa, **so‘rovlar chegarasini** yoqing — [Sayt sozlamalari](site-settings.md).
- [ ] **ClamAV** o‘rnatib, saytlarni vaqti-vaqti bilan skanerlang.
- [ ] Ishlab chiqarishdagi saytlarda PHP `display_errors` ni o‘chiq qoldiring.
- [ ] CMS, plagin va kutubxonalarni yangilab boring.

## Zaxira

- [ ] Har bir muhim sayt uchun **avtomatik zaxira** — [Zaxira nusxalar](backups.md).
- [ ] Nusxalarni **server tashqarisiga** (Google Drive yoki Dropbox) ham yuboring.
- [ ] Vaqti-vaqti bilan nusxadan **tiklashni sinab ko‘ring** — tiklab bo‘lmaydigan zaxira foydasiz.

## Buzilganda

1. Saytni vaqtincha **o‘chirib qo‘ying** yoki IP bo‘yicha yoping.
2. **Skanerlash** bilan zararli fayllarni toping va karantinga oling.
3. **Amallar tarixi** va **Loglar**ni ko‘rib, qanday kirilganini aniqlang.
4. Toza zaxira nusxadan tiklang.
5. Barcha parollarni almashtiring: panel, FTP/SSH, baza, CMS administratori, API tokenlari.
6. CMS va plaginlarni yangilang, keyin saytni yoqing.
