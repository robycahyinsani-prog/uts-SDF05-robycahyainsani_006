# UTS Software Development Fundamentals

**Nama:** Roby Cahya Insani  
**NIM:** 25120300006

## C1 — Refactoring

### a. Masalah Kualitas Kode

Kode legacy:

```python
def p(x, y, f):
    t = x * y
    if f:
        t = t * 0.9
    return t * 1.11
```

Masalah yang ditemukan:

1. **Nama tidak deskriptif** — `p`, `x`, `y`, `f`, `t` tidak menjelaskan maksudnya.
2. **Magic numbers** — `0.9` dan `1.11` tidak diberi nama konstanta, sehingga sulit dipahami dan diubah.
3. **Flag boolean `f` tidak jelas** — artinya hanya bisa dipahami dengan membaca isi fungsi.
4. **Tanggung jawab bercampur** — satu fungsi menghitung subtotal, diskon, dan pajak sekaligus.
5. **Tidak ada dokumentasi/type hint** — menyulitkan orang lain memahami kode.

### b. Versi Refactored

Kode lengkap tersedia di `code/pricing.py`. Berikut kutipannya:

```python
"""Modul untuk menghitung total harga order."""

# Konstanta bernama (menghilangkan magic numbers)
MEMBER_DISCOUNT_RATE = 0.10   # diskon 10% untuk member
TAX_RATE = 0.11               # pajak 11%


def calculate_subtotal(price: float, quantity: int) -> float:
    """Menghitung subtotal sebelum diskon dan pajak."""
    return price * quantity


def apply_member_discount(subtotal: float, is_member: bool) -> float:
    """Menerapkan diskon member jika pembeli adalah member."""
    if is_member:
        return subtotal * (1 - MEMBER_DISCOUNT_RATE)
    return subtotal


def apply_tax(amount: float) -> float:
    """Menerapkan pajak pada amount."""
    return amount * (1 + TAX_RATE)


def calculate_order_total(price: float, quantity: int, is_member: bool) -> float:
    """Menghitung total order setelah diskon dan pajak."""
    subtotal = calculate_subtotal(price, quantity)
    discounted = apply_member_discount(subtotal, is_member)
    return apply_tax(discounted)
```

Perubahan yang dilakukan:

- Nama fungsi dan variabel dibuat deskriptif.
- Magic numbers diganti konstanta bernama (`MEMBER_DISCOUNT_RATE`, `TAX_RATE`).
- Tanggung jawab dipisah menjadi fungsi-fungsi kecil (separation of responsibilities).
- Ditambahkan type hint dan docstring.

### c. Mengapa Behavior Tetap Sama

Refactored version mempertahankan perilaku karena urutan operasi dan nilai konstanta identik dengan versi lama:

- `0.9` setara dengan `1 - MEMBER_DISCOUNT_RATE` = `1 - 0.10`.
- `1.11` setara dengan `1 + TAX_RATE` = `1 + 0.11`.

**Contoh:** `price = 100`, `quantity = 2`, `is_member = True`

- **Versi lama:**
  - `t = 100 * 2 = 200`
  - `f = True → t = 200 * 0.9 = 180`
  - `return 180 * 1.11 = 199.8`
- **Versi baru:**
  - `subtotal = 100 * 2 = 200`
  - `discounted = 200 * (1 - 0.10) = 180`
  - `total = 180 * (1 + 0.11) = 199.8`

Hasil sama: **199.8**.

### d. Test

Test lengkap tersedia di `code/test_pricing.py`. Berikut kutipannya:

```python
import pytest
from pricing import calculate_order_total


def test_calculate_order_total_member():
    """Member mendapat diskon 10% lalu pajak 11%."""
    assert calculate_order_total(100, 2, True) == pytest.approx(199.8)


def test_calculate_order_total_non_member():
    """Non-member tidak dapat diskon, tetap kena pajak 11%."""
    assert calculate_order_total(100, 2, False) == pytest.approx(222.0)
```

Test yang dipilih:

- **Input:** `price = 100`, `quantity = 2`, `is_member = True`
- **Expected output:** `199.8`
- **Alasan:** memverifikasi bahwa diskon member (10%) dan pajak (11%) diterapkan dengan benar dan berurutan.

---

## C2 — Git

### a. Sequence Command

```bash
git checkout -b feat/member-discount
# edit pricing.py
git add pricing.py
git commit -m "feat: add member discount validation"
git checkout main
```

Penjelasan:

- `git checkout -b` membuat branch baru **dan** langsung pindah ke sana.
- `git add` memasukkan perubahan ke staging area.
- `git commit` menyimpan perubahan ke history branch.
- `git checkout main` kembali ke branch utama.

### b. Merge dan Dua Kemungkinan Hasil

```bash
git merge feat/member-discount
```

Dua kemungkinan hasil:

1. **Fast-forward** — terjadi jika `main` tidak memiliki commit baru sejak branch dibuat. Git hanya memindahkan pointer `main` ke commit branch. Tidak ada merge commit.
2. **Conflict** — terjadi jika `main` dan branch mengubah baris yang sama secara berbeda. Git berhenti dan meminta resolusi manual.

### c. Git Status Saat Conflict dan Tiga Langkah Resolusi

Saat conflict, `git status` menampilkan:

```
Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   pricing.py
```

Artinya file `pricing.py` diubah di kedua branch dan belum di-resolve.

Tiga langkah resolusi:

1. **Edit file** — buka file, selesaikan marker `<<<<<<<`, `=======`, `>>>>>>>`, hapus marker, pilih/gabungkan kode yang benar.
2. **`git add <file>`** — tandai file sudah resolved.
3. **`git commit`** — buat commit resolusi.

### d. Cancel Merge

```bash
git merge --abort
```

Efek: membatalkan proses merge yang sedang berjalan dan mengembalikan working tree serta index ke kondisi sebelum merge dimulai. Perubahan yang belum di-commit akan hilang.

---

## C3 — Modularization

### a. Module Breakdown

| Modul | Tanggung Jawab |
|-------|----------------|
| `reader.py` | Membaca `orders.csv` dan mengembalikan list of orders. |
| `pricing.py` | Menghitung subtotal, diskon member, dan pajak. |
| `report_writer.py` | Menulis hasil perhitungan ke `report.txt`. |
| `summary_printer.py` | Mencetak ringkasan (jumlah order, grand total) ke layar. |
| `app.py` | Orkestrasi: memanggil reader → pricing → writer → printer. |

### b. Dependency Direction

```
app.py
  ├── reader.py
  ├── pricing.py
  ├── report_writer.py
  └── summary_printer.py
```

Dependency mengarah dari `app.py` (orkestrator) ke modul-modul spesifik. Modul inti seperti `pricing.py` tidak bergantung pada I/O, sehingga bisa dites terpisah dan tidak terpengaruh perubahan format file. Ini menurunkan coupling dan memudahkan pengujian.

### c. Modul yang Bisa Dites Tanpa File System

- `pricing.py` — hanya menerima angka dan mengembalikan angka.
- `summary_printer.py` — bisa dites dengan capture output (mock `print`).

Ini penting karena test menjadi **cepat**, **deterministik**, dan **tidak bergantung pada environment** (tidak perlu file `orders.csv` atau `report.txt`). Mudah dijalankan di CI/CD.

### d. Dua Risiko Jika Separation Tanpa Testing

1. **Regression tidak terdeteksi** — perilaku bisa berubah tanpa disadari saat memindahkan kode antar modul.
2. **Interface antar modul kacau** — parameter/return tidak cocok, baru ketahuan saat runtime.

---

## Section D — Code Review Case Study

### D1 — Analisis Pull Request

Kode yang di-review:

```python
def calculate_average(scores):
    return sum(scores) / len(scores)
    d = scores
    total = 0
    for i in range(len(d)):
        total = total + d[i]
    return total / len(d) + 1
```

Deskripsi PR: *"small improvement to the average function"*
Test baru: **tidak ada**

---

### a. Masalah dan Klasifikasi

#### Masalah 1: Dead Code (Unreachable Code) — **BLOCKING ISSUE**

- **Apa:** Baris 3–7 tidak akan pernah dieksekusi karena baris 2 sudah `return`.
- **Kenapa blocking:** Kode yang dimaksud PR ini ("improvement") tidak berfungsi sama sekali. Fungsi hanya menjalankan baris 2.
- **Dampak:** Perubahan sia-sia, membingungkan reviewer, dan bisa menimbulkan bug tersembunyi.

#### Masalah 2: Perubahan Behavior yang Tidak Dijelaskan — **BLOCKING ISSUE**

- **Apa:** Ada `+ 1` di baris 7 yang mengubah hasil average (kalau sampai dieksekusi).
- **Kenapa blocking:** Mengubah perilaku fungsi tanpa alasan tertulis dan tanpa test. Average + 1 salah secara matematis.
- **Dampak:** Kalau kode ini sampai jalan, semua perhitungan average jadi salah.

#### Masalah 3: Tidak Ada Test Baru — **BLOCKING ISSUE**

- **Apa:** PR "small improvement" tapi tidak menyertakan test.
- **Kenapa blocking:** Tidak ada bukti bahwa perubahan benar dan tidak merusak fitur lain.
- **Dampak:** Regresi tidak terdeteksi.

#### Masalah 4: Duplikasi Logika — **SUGGESTION**

- **Apa:** Ada dua cara menghitung average: `sum(scores) / len(scores)` (baris 2) dan loop manual (baris 4–6).
- **Kenapa suggestion:** Bukan bug langsung, tapi bikin kode tidak konsisten dan membingungkan.
- **Dampak:** Maintenance jadi sulit.

#### Masalah 5: Variabel `d` Tidak Perlu — **NIT**

- **Apa:** `d = scores` hanya membuat alias tanpa manfaat.
- **Kenapa nit:** Kosmetik, tidak mempengaruhi behavior.
- **Dampak:** Sedikit mengganggu readability.

#### Masalah 6: Deskripsi PR Tidak Informatif — **SUGGESTION**

- **Apa:** Deskripsi hanya "small improvement to the average function".
- **Kenapa suggestion:** Reviewer tidak tahu kenapa perubahan ini dibuat, apa yang berubah, dan dampaknya.
- **Dampak:** Review jadi lambat, diskusi jadi panjang.

#### Masalah 7: Nama `i` di Loop — **NIT**

- **Apa:** `for i in range(len(d))` pakai index manual.
- **Kenapa nit:** Di Python, lebih baik `for score in d:` atau `sum(d)`.
- **Dampak:** Gaya penulisan kurang Pythonic.

---

### b. Tiga Review Comment (Problem, Impact, Proposed Improvement)

#### Comment 1

- **Problem:** Ada dead code setelah `return` pertama (baris 3–7 tidak akan pernah dieksekusi).
- **Impact:** Perubahan pada baris 7 (`+ 1`) tidak akan pernah berjalan, sehingga PR ini tidak melakukan apa pun. Kode tersebut sia-sia dan membingungkan.
- **Proposed Improvement:** Hapus baris 3–7, atau pindahkan logika yang dimaksud sebelum `return` pertama.

#### Comment 2

- **Problem:** Ada `+ 1` pada return kedua yang mengubah hasil average tanpa penjelasan.
- **Impact:** Jika sampai dieksekusi, hasil average menjadi salah (selalu +1 dari nilai seharusnya). Ini bug logika.
- **Proposed Improvement:** Hapus `+ 1`, atau jelaskan alasan perubahan dan tambahkan test yang membuktikan.

#### Comment 3

- **Problem:** PR tidak menyertakan test baru.
- **Impact:** Tidak ada bukti bahwa perubahan benar, dan tidak ada jaring pengaman terhadap regresi.
- **Proposed Improvement:** Tambahkan test untuk `calculate_average` dengan input normal, list kosong, dan nilai negatif.

---

### c. Behavior Change untuk `scores = [2, 4, 6]`

#### Versi Lama (sebelum PR)

```python
def calculate_average(scores):
    return sum(scores) / len(scores)
```

Input `[2, 4, 6]`:

- `sum([2, 4, 6]) = 12`
- `len([2, 4, 6]) = 3`
- `12 / 3 = 4.0`

**Output: 4.0**

#### Versi PR (versi baru)

```python
def calculate_average(scores):
    return sum(scores) / len(scores)   # ← return pertama
    d = scores
    total = 0
    for i in range(len(d)):
        total = total + d[i]
    return total / len(d) + 1          # ← tidak pernah dieksekusi
```

Input `[2, 4, 6]`:

- Baris pertama: `sum([2, 4, 6]) / len([2, 4, 6]) = 12 / 3 = 4.0` → langsung return.
- Baris setelahnya tidak dieksekusi.

**Output: 4.0**

#### Kesimpulan

Output sama (4.0), tapi ini bukan karena PR benar, melainkan karena **dead code**. PR ini tidak mengubah behavior apa pun. Kalau `+ 1` dimaksudkan untuk mengubah hasil, PR ini gagal mewujudkannya.

Kalau dead code dihapus dan `+ 1` benar-benar dieksekusi:

- Input `[2, 4, 6]` → `12 / 3 + 1 = 4.0 + 1 = 5.0`
- **Output: 5.0** (salah secara matematis).

---

### d. Satu Test yang Harus Diminta

```python
import pytest

def test_calculate_average_empty_list():
    with pytest.raises(ZeroDivisionError):
        calculate_average([])
```

**Kenapa penting:**

- Memastikan perilaku saat list kosong: `sum([]) / len([]) = 0 / 0` → `ZeroDivisionError`.
- Test ini memaksa author memutuskan apakah mau raise error yang jelas, return 0, atau None.
- Tanpa test ini, edge case seperti ini mudah terlewat dan bisa menyebabkan crash di production.

**Test tambahan yang baik diminta:**

```python
def test_calculate_average_normal():
    assert calculate_average([2, 4, 6]) == 4.0

def test_calculate_average_single_element():
    assert calculate_average([5]) == 5.0

def test_calculate_average_negative():
    assert calculate_average([-2, 2]) == 0.0
```

---

### e. Behavior untuk Empty List

#### Versi Lama

```python
def calculate_average(scores):
    return sum(scores) / len(scores)
```

Input `[]`:

- `sum([]) = 0`
- `len([]) = 0`
- `0 / 0` → **`ZeroDivisionError`**

#### Versi PR

```python
def calculate_average(scores):
    return sum(scores) / len(scores)   # ← langsung dieksekusi
    # baris lain tidak tercapai
```

Input `[]`:

- Baris pertama: `sum([]) / len([]) = 0 / 0` → **`ZeroDivisionError`**
- Baris setelahnya tidak dieksekusi.

**Kedua versi sama-sama error** untuk input kosong.

#### Cara Menangani yang Benar

**Opsi 1: Raise exception yang jelas**

```python
def calculate_average(scores):
    if not scores:
        raise ValueError("scores must not be empty")
    return sum(scores) / len(scores)
```

Kapan dipakai: kalau average dari list kosong memang tidak terdefinisi (paling umum di produksi).

**Opsi 2: Return 0**

```python
def calculate_average(scores):
    if not scores:
        return 0.0
    return sum(scores) / len(scores)
```

Kapan dipakai: kalau domain menganggap average dari list kosong = 0.

**Opsi 3: Return None**

```python
def calculate_average(scores):
    if not scores:
        return None
    return sum(scores) / len(scores)
```

Kapan dipakai: kalau pemanggil harus secara eksplisit menangani kasus kosong.

Yang penting: pilih satu, dokumentasikan, dan tambahkan test untuk memverifikasinya.