# Fayl menejeri

Fayl menejeri saytning fayllarini brauzerdan boshqarish imkonini beradi: yuklash, tahrirlash, arxivlash va boshqalar. U sayt sahifasidagi **«Fayllar»** plitkasidan ochiladi. Akkauntda **«Fayllarni boshqarish»** ruxsati bo‘lishi kerak.

![Fayl menejeri](../images/files.png)

Fayl menejeri sayt foydalanuvchisining uy papkasini ko‘rsatadi va undan tashqariga chiqmaydi. Sayt fayllari `www/<domen>` papkasida turadi. Barcha amallar sayt foydalanuvchisi nomidan bajariladi, shuning uchun fayllar egasi to‘g‘ri bo‘ladi va disk kvotasi hisobga olinadi.

## Fayl yuklash

- **«Fayl yuklash»** tugmasi yoki fayllarni oynaga **sudrab tashlash**.
- Bir faylning hajmi 2 GB gacha. Bir vaqtda bir nechta fayl yuklash mumkin.
- Bir nechta fayl yuklanganda ularning **umumiy hajmi bo‘yicha bitta progress bar** ko‘rinadi, masalan: «20 ta fayl yuklanmoqda — 7 tasi tayyor · 45%». Yuklanmagan fayllar bo‘lsa, ularni sababi bilan ko‘rish mumkin.
- Papkani yuklab bo‘lmaydi — uni arxivlab yuklang va panelda arxivdan chiqaring.

## Yangi fayl va papka

**«Yangi»** tugmasi bilan bo‘sh fayl yoki papka yaratiladi.

## Fayl ustida amallar

Faylni ikki marta bossangiz, ochiladi yoki matn muharririda tahrirlanadi. Satr oxiridagi menyu va bir nechta faylni belgilash orqali:

| Amal | Izoh |
|---|---|
| Ochish / Tahrirlash | 2 MB gacha matnli fayllar sintaksis yoritilishi bilan tahrirlanadi; kodlashni tanlash mumkin |
| Yuklab olish | Faylni kompyuterga saqlash |
| Qayta nomlash | |
| Ko‘chirish, Nusxalash | Boshqa papkaga |
| Ruxsatlarni o‘zgartirish | Masalan `644` (fayl), `755` (papka); «Ichidagilarga ham» bilan rekursiv |
| Arxivga joylash | ZIP yoki TAR.GZ arxiv yaratish |
| Arxivdan chiqarish | ZIP, TAR, GZ, RAR, 7Z va boshqalar |
| O‘chirish | Papkalar ichidagilari bilan birga o‘chadi |

Bir nechta element belgilansa, ko‘chirish, nusxalash, ruxsatlar, arxivlash va o‘chirish hammasiga birdan qo‘llanadi.

## O‘chirish haqida

- Istalgan fayl va papkani o‘chirish mumkin, yozish taqiqlangan papkalar ham ichidagilari bilan o‘chadi.
- Saytning o‘z papkasi yoki `www` o‘chirilsa, panel ularni **bo‘sh holda qayta yaratadi** — sayt ishlashda davom etadi.
- Bu papkalarni ko‘chirish yoki qayta nomlash mumkin emas, chunki sayt shu yo‘lda turadi.

## Disk statistikasi

**«Disk statistikasi»** tugmasi papka bo‘yicha joy taqsimotini ko‘rsatadi: eng katta papkalar, eng katta fayllar va kengaytmalar bo‘yicha hajm. Disk to‘lib qolganda nima joy egallayotganini topish uchun qulay.

## Xavfsizlik

Simvolik havolalar (symlink) orqali sayt foydalanuvchisi papkasidan tashqariga chiqish mumkin emas — boshqa saytlar va tizim fayllari ko‘rinmaydi.
