# PROYEK OPTIMASI RUTE KANTOR POS GORONTALO (Kelompok 12)

## 1. Penjelasan Singkat Proyek
Proyek ini adalah aplikasi berbasis Python yang dibuat untuk membandingkan kinerja dua algoritma pencarian rute, yaitu Algoritma Dijkstra dan Algoritma Greedy, dalam mencari rute terpendek antar kelurahan di Gorontalo dengan titik pusat Kantor Pos Gorontalo. Proyek ini memvisualisasikan bagaimana Dijkstra mencari rute paling optimal secara global, sementara Greedy memilih rute terdekat pada setiap langkah (local optimum) yang kadang bisa menyebabkannya terjebak jalan buntu.

## 2. Fitur Proyek
- Komparasi Rute Tunggal (Point to Point): Membandingkan pencarian rute dan jarak antara Dijkstra dan Greedy dari 1 titik awal ke 1 titik tujuan.
- Komparasi Akumulasi Jarak (Batch Analysis): Menguji performa (batch processing) dari 1 titik awal ke 50 titik tujuan lainnya sekaligus untuk melihat perbedaan tingkat keberhasilan dan efisiensi waktu.


## 3. Penjelasan File dan Folder

* `data.py`: Berisi dataset statis dictionary Python untuk merepresentasikan nama lokasi (kelurahan) dan Adjacency List (daftar ketetanggaan) yang merepresentasikan graf peta Gorontalo.
* `main.py`: File eksekusi utama untuk menjalankan antarmuka di terminal. Menghubungkan fungsi algoritma dengan data, serta menampilkan output teks secara rapi.
* `app.py`: File server backend web menggunakan framework Flask. Bertugas memproses data rute ke format JSON dan me-render template web agar bisa divisualisasikan oleh JavaScript.
* `templates/`: Folder yang wajib ada di framework Flask untuk menyimpan file antarmuka (HTML).
  - `index.html`: Antarmuka utama web untuk form input komparasi rute dan visualisasi interaktif graf hasil perhitungan.
  - `dataset.html`: Antarmuka web yang hanya menampilkan visualisasi peta graf mentah (tanpa perhitungan rute).


### Penjelasan Detail `algoritma.py` (Langkah per baris)

File `algoritma.py` berisi dua fungsi logika inti: `dijkstra()` dan `greedy()`. Berikut adalah penjabaran mendalam setiap baris kuncinya.

---


-------------------------------------------------------------
BAGIAN 1: ALGORITMA DIJKSTRA (Pencarian Jarak Global Optimum)
-------------------------------------------------------------

**Baris 2 : `import heapq`**

Mengimpor modul Priority Queue (Antrean Prioritas) bawaan Python. Struktur data ini adalah fondasi utama Dijkstra, ia memastikan algoritma selalu mengambil dan memproses node dengan akumulasi jarak terkecil terlebih dahulu secara otomatis dan efisien.

**Baris 5 : `def dijkstra(graf, start, tujuan):`**

Mendefinisikan fungsi Dijkstra yang menerima 3 parameter: `graf` (peta/jaringan adjacency list), `start` (titik awal perjalanan), dan `tujuan` (titik akhir yang ingin dicapai).

**Baris 12 : `jarak = {node: float('infinity') for node in graf}`**

Inisialisasi Pelabelan: Memberikan label sementara sebesar tak terhingga (infinity) ke seluruh node di dalam graf sebelum proses pencarian dimulai. Ini menyatakan bahwa jarak menuju semua titik belum diketahui sama sekali.

**Baris 14 : `jarak[start] = 0`**

Titik awal diberikan label jarak 0 karena jarak dari suatu titik ke dirinya sendiri adalah nol. Ini menjadikannya node pertama yang akan diambil dari antrean prioritas.

**Baris 18 : `pq = [(0, start)]`**

Memasukkan titik awal beserta jaraknya (0) ke dalam antrean prioritas `pq` sebagai elemen pertama yang akan dievaluasi pada iterasi pertama loop.

**Baris 22 : `rute_sebelumnya = {node: None for node in graf}`**

Menyiapkan kamus memori Predecessor untuk merekam jejak rute. Dijkstra tidak menghafal seluruh jalur di depan, melainkan mencatat dari node mana setiap node dicapai dengan cara teroptimal. Data ini digunakan untuk rekonstruksi rute (backtracking) di akhir.

**Baris 25 : `while pq:`**

Memulai loop utama iterasi yang akan terus berjalan selama antrean prioritas `pq` masih memiliki elemen yang belum diproses.

**Baris 27 : `jarak_sekarang, node_sekarang = heapq.heappop(pq)`**

Mengeluarkan node dengan bobot akumulasi paling ringan dari antrean. Pada titik ini, node yang baru saja di-pop telah mendapatkan Label Tetap/Permanen, jarak terpendek menuju node ini sudah pasti dan tidak akan berubah lagi.

**Baris 31–33 : `if node_sekarang == tujuan: break`**

Penghentian Dini (Early Exit). Jika node yang baru di-pop ternyata adalah titik tujuan akhir, loop langsung dihentikan. Karena sifat Priority Queue, jarak yang ditemukan pertama kali untuk titik tujuan sudah pasti merupakan jarak terpendek global.

**Baris 37–39 : `if jarak_sekarang > jarak[node_sekarang]: continue`**

Optimasi performa: mengabaikan entri lama yang sudah tidak relevan di dalam antrean. Ini terjadi karena sebuah node bisa masuk ke `pq` lebih dari sekali ketika jalur yang lebih pendek ditemukan. Jika jarak entri yang sedang diproses lebih besar dari jarak terbaik yang sudah tercatat, entri ini kedaluwarsa dan cukup dilewati.

**Baris 43 : `for tetangga, bobot in graf[node_sekarang].items():`**

Mengeksplorasi seluruh sisi jalan (tetangga) yang terhubung langsung dengan node saat ini beserta nilai bobot jaraknya masing-masing.

**Baris 45 : `jarak_baru = jarak_sekarang + bobot`**

Pembuktian Rumus: menghitung akumulasi jarak dari titik awal (start) menuju node tetangga dengan cara menjumlahkan jarak tempuh sejauh ini dengan bobot sisi menuju tetangga tersebut.

**Baris 49 : `if jarak_baru < jarak[tetangga]:`**

Proses Relaksasi: mengevaluasi apakah jalur yang baru dihitung ini lebih pendek dari jalur terbaik yang pernah ditemukan sebelumnya menuju node tetangga. Jika ya, data lama ditimpa dengan data yang lebih optimal.

**Baris 51–55 : `jarak[tetangga] = jarak_baru` ... `heapq.heappush(pq, (jarak_baru, tetangga))`**

Tiga operasi pembaruan sekaligus: (1) memperbarui rekor jarak terpendek di `jarak[tetangga]`, (2) mencatat jalur asal terbaik di `rute_sebelumnya[tetangga] = node_sekarang`, lalu (3) memasukkan tetangga ke dalam antrean prioritas dengan jarak baru untuk dievaluasi kembali pada iterasi berikutnya.

**Baris 59–74 : Blok Rekonstruksi Rute (Backtracking)**

Setelah loop selesai, rute dirangkai mundur dari titik tujuan ke titik awal menggunakan data yang tersimpan di `rute_sebelumnya`. Pointer `node_trace` dimulai dari `tujuan` dan bergerak mundur satu per satu. Setiap node disisipkan ke posisi paling depan list (`rute.insert(0, node_trace)`) agar urutan rute akhir tampil dari start ke tujuan, bukan terbalik.

**Baris 65–67 : `if rute_sebelumnya[tujuan] is None and start != tujuan: return None, float('infinity')`**

Penanganan kasus graf terputus: jika setelah loop selesai, `rute_sebelumnya[tujuan]` masih bernilai `None` dan titik awal bukan titik tujuan itu sendiri, berarti tidak ada jalur yang menghubungkan kedua titik tersebut. Fungsi mengembalikan `None` dan `infinity` sebagai sinyal kegagalan.

**Baris 77 : `return rute, jarak[tujuan]`**

Mengembalikan dua nilai: array urutan jalur optimal dari start ke tujuan, dan total bobot jarak terpendek yang dibutuhkan untuk mencapainya.

---

----------------------------------------------------------
BAGIAN 2: ALGORITMA GREEDY (Pencarian Jarak Local Optimum)
----------------------------------------------------------


**Baris 81 : `def greedy(graf, start, tujuan):`**

Mendefinisikan fungsi heuristik Greedy yang menerima parameter yang sama dengan Dijkstra: `graf`, `start`, dan `tujuan`. Berbeda dengan Dijkstra, Greedy bekerja dengan membuat keputusan lokal terbaik di setiap langkah tanpa melihat keseluruhan gambar.

**Baris 95 : `rute = [start]`**

Menginisialisasi list rute dan langsung memasukkan titik awal sebagai titik pertama yang dilalui. Greedy merekam perjalanan secara berurutan sambil berjalan.

**Baris 97 : `jarak_total = 0`**

Mempersiapkan variabel akumulator untuk menghitung total jarak yang telah ditempuh. Nilainya akan terus bertambah setiap kali Greedy berpindah ke node berikutnya.

**Baris 99 : `node_sekarang = start`**

Menandai posisi kursor pencarian saat ini, yang diawali di titik awal. Variabel ini akan terus diperbarui setiap kali algoritma berpindah node.

**Baris 101 : `dikunjungi = {start}`**

Membuat himpunan (set) yang berisi node-node yang telah dikunjungi, diawali dengan titik awal. Ini adalah mekanisme pencegahan infinite loop, Greedy tidak boleh kembali ke node yang sudah pernah diinjak sebelumnya.

**Baris 104 : `while node_sekarang != tujuan:`**

Siklus utama yang terus berulang selama posisi kursor saat ini belum mencapai kelurahan tujuan.

**Baris 106 : `tetangga_tersedia = graf[node_sekarang]`**

Melihat seluruh persimpangan jalan yang tersedia dari posisi saat ini, mengambil dictionary berisi semua tetangga beserta bobot jaraknya dari node yang sedang ditempati.

**Baris 110–116 : `if tujuan in tetangga_tersedia:` ... `break`**

**[LANGKAH 1 — Prioritas Tertinggi]** Mengecek apakah titik tujuan terhubung langsung dengan posisi saat ini. Jika ya, Greedy langsung melompat ke tujuan tanpa perhitungan tambahan: jarak ditambahkan, tujuan dimasukkan ke rute, dan loop dihentikan.

**Baris 120–129 : `kandidat_perantara = []` ... `kandidat_perantara.append((bobot_ke_t, t))`**

**[LANGKAH 2 — Prioritas Kedua]** Jika tujuan tidak terhubung langsung, Greedy mencari tetangga yang berfungsi sebagai batu loncatan, yaitu tetangga yang belum dikunjungi dan memiliki akses langsung ke tujuan (`tujuan in graf[t]`). Semua kandidat yang memenuhi syarat dikumpulkan bersama bobot jaraknya.

**Baris 133–148 : `if kandidat_perantara:` ... `continue`**

Jika ditemukan minimal satu perantara, list `kandidat_perantara` diurutkan secara ascending lalu diambil kandidat dengan bobot terkecil (index ke-0). Node perantara terpilih dimasukkan ke rute, bobotnya diakumulasikan ke total jarak, ditandai sebagai dikunjungi, posisi diperbarui ke node tersebut, dan loop dilanjutkan dari awal dengan `continue`.

**Baris 152–162 : `jarak_terdekat = float('infinity')` ... `pilihan_terbaik = t`**

**[LANGKAH 3 — Fallback]** Jika tidak ada tetangga yang bisa menjadi perantara langsung ke tujuan, Greedy menggunakan strategi paling dasar: memilih tetangga mana pun yang belum dikunjungi dan memiliki jarak paling kecil dari posisi saat ini, tanpa mempertimbangkan apakah pilihan itu akan menguntungkan di langkah-langkah selanjutnya. Inilah inti dari sifat "local optimum" Greedy.

**Baris 166–168 : `if pilihan_terbaik is None: return rute, float('infinity'), "Gagal: Terjebak"`**

**Pembuktian Kelemahan Greedy:** Jika setelah semua tetangga diperiksa nilai `pilihan_terbaik` masih `None`, artinya semua tetangga yang ada sudah pernah dikunjungi dan tidak ada jalan baru yang bisa diambil. Karena Greedy tidak memiliki kemampuan mundur (backtracking) seperti Dijkstra, algoritma terjebak di jalan buntu dan mengembalikan status `"Gagal: Terjebak"` beserta jarak tak terhingga.

**Baris 171–177 : `rute.append(pilihan_terbaik)` ... `node_sekarang = pilihan_terbaik`**

Mengeksekusi perpindahan posisi: node terpilih ditambahkan ke rute, bobotnya diakumulasikan ke `jarak_total`, node ditandai sebagai dikunjungi, dan posisi `node_sekarang` diperbarui untuk iterasi berikutnya.

**Baris 180 : `return rute, jarak_total, "Berhasil"`**

Mengembalikan tiga nilai setelah loop berhasil diselesaikan secara alami: array rute lengkap yang dilalui, total akumulasi jarak, dan string status `"Berhasil"`. Perhatikan bahwa Greedy mengembalikan 3 nilai, sedangkan Dijkstra hanya 2, karena Greedy perlu menyertakan status keberhasilan yang bisa berupa `"Berhasil"` atau `"Gagal: Terjebak"`.

## 4. Cara Menjalankan Program

### A. Persyaratan (Prerequisites)
1. Pastikan Python sudah terinstall di komputermu (versi 3.x).
2. Untuk menjalankan versi Web HTML, kamu membutuhkan framework Flask. Buka terminal/command prompt dan ketik:
   `pip install flask`

### B. Menjalankan Tampilan Terminal (CLI)
1. Buka Terminal atau Command Prompt.
2. Arahkan direktori (`cd`) ke dalam folder proyek ini.
3. Ketik dan jalankan perintah: `python main.py`
4. Program akan menampilkan menu interaktif. Ketik angka `1` atau `2` untuk memilih fitur yang diinginkan.
5. Masukkan ID Node awal dan tujuan sesuai petunjuk di layar (contoh: V0, V1, dst).

### C. Menjalankan Tampilan Web (HTML)
1. Buka Terminal atau Command Prompt.
2. Arahkan direktori (`cd`) ke dalam folder proyek ini.
3. Ketik dan jalankan perintah: `python app.py`
4. Di terminal akan muncul tulisan indikator seperti `* Running on http://127.0.0.1:5000`.
5. Jangan tutup terminal tersebut. Buka Web Browser (Chrome, Firefox, Safari, dll).
6. Ketikkan alamat `http://127.0.0.1:5000` di address bar browser lalu tekan Enter.
7. Aplikasi web antarmuka HTML akan tampil. Kamu dapat memilih titik awal dan titik tujuan di panel sebelah kiri lalu menekan tombol "Compare Route" untuk melihat visualisasi perbandingan algoritma di peta.


## 5. Referensi Program

Program ini dikembangkan berdasarkan penelitian berikut:

Lakutu, N. F., Katili, M. R., Mahmud, S. L., & Yahya, N. I. (2023). *Algoritma Dijkstra dan Algoritma Greedy Untuk Optimasi Rute Pengiriman Barang Pada Kantor Pos Gorontalo*. EULER: Jurnal Ilmiah Matematika, Sains dan Teknologi, 11(1), 55–65. https://doi.org/10.34312/euler.v11i1.18244

### Ringkasan Referensi

Penelitian ini membandingkan Algoritma Dijkstra dan Algoritma Greedy dalam menentukan rute pengiriman barang pada Kantor Pos Gorontalo menggunakan model graf berbobot yang terdiri dari 50 simpul (kelurahan).

Hasil penelitian menunjukkan bahwa:

- Algoritma Dijkstra menghasilkan total jarak tempuh **304,90 km**.
- Algoritma Greedy menghasilkan total jarak tempuh **441,60 km**.
- Algoritma Dijkstra memberikan solusi yang lebih optimal karena mengevaluasi seluruh alternatif lintasan sebelum menentukan jalur terbaik.
- Algoritma Greedy lebih cepat dalam pengambilan keputusan lokal, tetapi tidak selalu menghasilkan solusi optimal secara global.

Implementasi pada proyek ini menggunakan dataset lokasi dan konsep graf yang diadaptasi dari penelitian tersebut untuk keperluan pembelajaran, simulasi, dan analisis perbandingan algoritma pencarian rute.
