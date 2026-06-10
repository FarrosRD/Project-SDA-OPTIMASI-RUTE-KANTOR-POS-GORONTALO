# Mengimpor modul heapq bawaan Python untuk menggunakan struktur data antrean prioritas (Priority Queue)
import heapq

# Mendefinisikan fungsi dijkstra yang menerima 3 parameter: graf (peta/jaringan), start (titik awal), dan tujuan (titik akhir)
def dijkstra(graf, start, tujuan):
    """
    ALGORITMA DIJKSTRA (Global Optimum)
    Mencari rute terpendek secara global, Mempertimbangkan semua kemungkinan jalur.
    """
    # 1. Atur semua jarak awal menjadi tak terhingga (infinity), kecuali titik start (0)
    # Membuat dictionary yang memetakan setiap node di dalam graf dengan nilai awal infinity (tak terhingga)
    jarak = {node: float('infinity') for node in graf}
    # Menetapkan jarak untuk titik awal (start) ke dirinya sendiri menjadi 0 agar menjadi node pertama yang diproses
    jarak[start] = 0 
    
    # 2. Priority Queue untuk memproses simpul dengan jarak terkecil lebih dulu
    # Membuat antrean prioritas 'pq' dalam bentuk list, diisi dengan tuple pertama berisi (jarak 0, node awal)
    pq = [(0, start)]
    
    # 3. Dictionary untuk melacak jejak langkah (untuk merangkai rute di akhir)
    # Membuat dictionary untuk menyimpan node asal yang dilalui untuk mencapai suatu node, nilainya diinisialisasi 'None'
    rute_sebelumnya = {node: None for node in graf}
    
    # Memulai perulangan while yang akan terus berjalan selama priority queue (pq) masih memiliki elemen di dalamnya
    while pq:
        # Mengeluarkan (pop) node yang memiliki jarak kumulatif terkecil saat ini dari antrean prioritas
        jarak_sekarang, node_sekarang = heapq.heappop(pq)
        
        # Jika sudah sampai tujuan, pencarian dihentikan
        # Mengecek apakah node yang sedang dievaluasi adalah titik tujuan akhir
        if node_sekarang == tujuan: 
            # Jika iya, hentikan perulangan (break) karena jarak terpendek global ke tujuan sudah pasti ditemukan
            break
        
        # Abaikan jika jarak yang diproses lebih besar dari yang sudah ada
        # Memastikan tidak memproses ulang node dengan jalur yang lebih lambat dari jarak terpendek yang sudah tercatat
        if jarak_sekarang > jarak[node_sekarang]: 
            # Jika jaraknya lebih besar, langsung lewati siklus loop ini dan lanjut ke elemen pq berikutnya
            continue
            
        # 4. Evaluasi semua tetangga dari node saat ini
        # Melakukan iterasi (perulangan) pada setiap node tetangga dan nilai bobotnya (jarak) yang terhubung langsung dengan node_sekarang
        for tetangga, bobot in graf[node_sekarang].items():
            # Menghitung akumulasi jarak dari titik start menuju node tetangga melalui node_sekarang
            jarak_baru = jarak_sekarang + bobot
            
            # Jika ditemukan rute yang lebih pendek, perbarui data
            # Mengecek apakah total jarak yang baru dihitung ternyata lebih kecil (lebih cepat) daripada data jarak tetangga saat ini
            if jarak_baru < jarak[tetangga]:
                # Memperbarui data jarak terpendek menuju node tetangga tersebut dengan nilai jarak_baru
                jarak[tetangga] = jarak_baru
                # Mencatat bahwa rute terbaik untuk sampai ke node tetangga ini adalah melalui 'node_sekarang'
                rute_sebelumnya[tetangga] = node_sekarang
                # Memasukkan node tetangga beserta nilai jarak_baru-nya ke dalam antrean prioritas untuk dievaluasi pada iterasi selanjutnya
                heapq.heappush(pq, (jarak_baru, tetangga))
                
    # 5. Rekonstruksi rute dari tujuan kembali ke titik awal
    # Menginisialisasi list kosong untuk menampung rute akhir yang akan disusun mundur
    rute = []
    # Membuat variabel pointer 'node_trace' yang diawali dari titik tujuan untuk melacak jalur mundur
    node_trace = tujuan
    
    # Jika tidak ada rute yang ditemukan
    # Memeriksa jika tujuan tetap bernilai None pada 'rute_sebelumnya' dan start tidak sama dengan tujuan (artinya graf terputus)
    if rute_sebelumnya[tujuan] is None and start != tujuan:
        # Kembalikan nilai None untuk rute dan tak terhingga (infinity) untuk jarak karena rute gagal ditemukan
        return None, float('infinity')
        
    # Melakukan perulangan selama masih ada riwayat rute yang dapat dilacak mundur (belum mencapai None / batas awal)
    while node_trace is not None:
        # Menyisipkan node yang sedang dilacak ke posisi paling depan (index 0) dari list 'rute' agar urutannya dari start ke tujuan
        rute.insert(0, node_trace)
        # Mengubah 'node_trace' menjadi node sebelumnya (langkah mundur 1 titik) untuk iterasi loop berikutnya
        node_trace = rute_sebelumnya[node_trace]
        
    # Mengembalikan rute lengkap yang sudah terurut dan total jarak terpendek yang dibutuhkan untuk mencapai tujuan
    return rute, jarak[tujuan]


# Mendefinisikan fungsi greedy yang menerima parameter graf, start (titik awal), dan tujuan (titik akhir)
def greedy(graf, start, tujuan):
    """
    ALGORITMA GREEDY (Local Optimum)
    Menyelesaikan masalah secara langkah demi langkah dengan 
    memilih opsi terbaik yang tersedia saat itu juga

    Logika Sesuai Referensi:
    1. Jika tujuan terhubung langsung, pilih tujuan.
    2. Jika tidak, cari tetangga yang terhubung ke tujuan, lalu pilih
       tetangga dengan jarak terdekat dari posisi SAAT INI (tanpa dijumlahkan).
    3. Jika tidak ada, baru pilih tetangga terdekat secara umum.

    """
    # Menginisialisasi list rute dan langsung memasukkan titik awal (start) sebagai rute yang pertama kali dilalui
    rute = [start]
    # Menginisialisasi variabel untuk menghitung akumulasi total jarak yang telah ditempuh dengan nilai 0
    jarak_total = 0
    # Menandai posisi kita saat ini berada, yang diawali pada titik start
    node_sekarang = start
    # Membuat set 'dikunjungi' berisi node yang telah didatangi (dimulai dari start) agar tidak berputar-putar di node yang sama (looping)
    dikunjungi = {start} 
    
    # Memulai perulangan while yang akan terus berjalan selama posisi node_sekarang belum mencapai titik tujuan
    while node_sekarang != tujuan:
        # Mengambil dictionary berisi semua node tetangga yang terhubung dengan node_sekarang beserta bobot jaraknya
        tetangga_tersedia = graf[node_sekarang]
        
        # LANGKAH 1: Pilih langsung jika tujuan terhubung langsung dengan posisi SAAT INI
        # Memeriksa apakah node tujuan ada di dalam daftar tetangga dari node yang sedang kita tempati
        if tujuan in tetangga_tersedia:
            # Jika ada, tambahkan jarak dari node saat ini ke tujuan ke dalam jarak_total
            jarak_total += tetangga_tersedia[tujuan]
            # Masukkan node tujuan ke dalam daftar rute akhir
            rute.append(tujuan)
            # Hentikan pencarian (break loop) karena kita sudah langsung sampai di tujuan
            break

        # LANGKAH 2: Cari tetangga yang memiliki akses langsung ke tujuan
        # Menginisialisasi list kosong untuk menyimpan tetangga yang bisa menjadi batu loncatan perantara langsung menuju tujuan
        kandidat_perantara = []
        # Melakukan iterasi (perulangan) pada seluruh tetangga (t) dan jaraknya (bobot_ke_t) dari node saat ini
        for t, bobot_ke_t in tetangga_tersedia.items():
            # Memeriksa apakah node tetangga (t) belum pernah dikunjungi sebelumnya
            if t not in dikunjungi:
                # Memeriksa lebih dalam, apakah node tetangga (t) ini memiliki jalur yang langsung mengarah ke tujuan
                if tujuan in graf[t]:
                    # Simpan hanya jarak menuju tetangga 
                    # Jika memenuhi syarat, tambahkan tuple (bobot jarak menuju tetangga, nama tetangga) ke dalam list kandidat
                    kandidat_perantara.append((bobot_ke_t, t))
        
        # Jika ada perantara, pilih yang terdekat dari posisi SAAT INI
        # Mengecek apakah list kandidat_perantara memiliki isi (minimal ada satu perantara yang valid)
        if kandidat_perantara:
            # Mengurutkan kandidat_perantara secara ascending berdasarkan elemen pertama tuple (bobot terpendek berada di indeks awal)
            kandidat_perantara.sort() 
            # Mengekstrak bobot jarak dan nama node dari kandidat terbaik (index ke-0) yang posisinya paling dekat
            bobot_terpilih, node_terpilih = kandidat_perantara[0]
            
            # Menambahkan node perantara yang berhasil terpilih ke dalam list rute
            rute.append(node_terpilih)
            # Menambahkan nilai bobotnya ke dalam kalkulasi total jarak tempuh sementara
            jarak_total += bobot_terpilih
            # Menandai bahwa node perantara ini sekarang telah dikunjungi agar tidak diulangi lagi nanti
            dikunjungi.add(node_terpilih)
            # Memperbarui posisi kita (node_sekarang) ke node perantara yang baru saja dipilih
            node_sekarang = node_terpilih
            # Menggunakan perintah 'continue' untuk melewati sisa baris kode di bawah ini dan langsung kembali ke awal loop while
            continue
        
        # LANGKAH 3: Jika tidak ada jalan perantara ke tujuan, pilih tetangga terdekat biasa
        # Menginisialisasi nilai variabel jarak_terdekat dengan tak terhingga (infinity) sebagai acuan pembanding awal
        jarak_terdekat = float('infinity')
        # Menyiapkan variabel untuk menampung nama tetangga dengan jarak terdekat, dengan nilai awal None
        pilihan_terbaik = None
        # Kembali melakukan iterasi membedah setiap tetangga (t) dan jaraknya (bobot_ke_t)
        for t, bobot_ke_t in tetangga_tersedia.items():
            # Mencari tetangga yang belum dikunjungi DAN jaraknya lebih kecil (lebih dekat) dari jarak_terdekat yang tercatat sejauh ini
            if t not in dikunjungi and bobot_ke_t < jarak_terdekat:
                # Jika ditemukan yang lebih kecil, perbarui rekor nilai jarak_terdekat dengan bobot tetangga ini
                jarak_terdekat = bobot_ke_t
                # Jadikan tetangga ini sebagai kandidat tunggal pilihan_terbaik
                pilihan_terbaik = t
        
        # semua tetangga buntu
        # Setelah semua tetangga diiterasi, mengecek apakah nilai pilihan_terbaik masih None (artinya semua jalan buntu/sudah dikunjungi)
        if pilihan_terbaik is None:
            # Jika buntu, hentikan algoritma dan kembalikan rute terakhir, jarak tak terhingga, dan pesan error gagal karena terjebak
            return rute, float('infinity'), "Gagal: Terjebak"
            
        # Menambahkan tetangga terbaik (terdekat biasa) ke dalam daftar rute
        rute.append(pilihan_terbaik)
        # Mengakumulasikan bobot jarak dari node sebelumnya ke pilihan_terbaik ke dalam total jarak tempuh
        jarak_total += jarak_terdekat
        # Menandai pilihan_terbaik ini ke dalam himpunan (set) node yang telah resmi dikunjungi
        dikunjungi.add(pilihan_terbaik)
        # Memperbarui posisi node saat ini agar berpindah ke posisi pilihan_terbaik untuk pencarian pada iterasi loop berikutnya
        node_sekarang = pilihan_terbaik
        
    # Jika loop while berhasil terselesaikan secara alami (posisi sudah di tujuan), kembalikan rute komplit, total jarak, dan status berhasil
    return rute, jarak_total, "Berhasil"