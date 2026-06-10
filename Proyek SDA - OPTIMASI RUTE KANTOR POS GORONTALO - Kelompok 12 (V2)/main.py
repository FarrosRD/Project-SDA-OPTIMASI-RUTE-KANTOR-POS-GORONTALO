from data import graf_gorontalo, nama_lokasi
from algoritma import dijkstra, greedy

def format_rute(rute, max_per_line=3):
    """
    Fungsi untuk mencetak tampilan rute di terminal.
    """
    if not rute: 
        return "Tidak ada rute ditemukan."
    
    lines = []
    current_line = []
    
    for i, node in enumerate(rute):
        # Mengambil nama asli lokasi dari dictionary 'nama_lokasi' berdasarkan ID (node)
        teks_node = f"{node} ({nama_lokasi[node]})"
        current_line.append(teks_node)
        
        # Mengecek apakah jumlah node di baris ini sudah mencapai batas (max_per_line) 
        # atau jika ini adalah elemen terakhir dalam list rute
        if len(current_line) == max_per_line or i == len(rute) - 1:
            if not lines:
                # Untuk baris pertama, gabungkan string langsung
                lines.append(" → ".join(current_line))
            else:
                # Untuk baris kedua dan seterusnya, beri spasi indentasi agar sejajar
                lines.append("  → " + " → ".join(current_line))
            
            # Reset array current_line untuk mulai menampung node untuk baris baru berikutnya
            current_line = []
            
    # Menggabungkan semua baris yang tersimpan dengan karakter Enter/Newline (\n)
    return "\n".join(lines)


def fitur_rute_tunggal():
    """
    Fungsi untuk menjalankan skenario komparasi dari 1 Titik Awal ke 1 Titik Tujuan.
    """
    print("\n" + "="*50)
    print(" FITUR 1: PERBANDINGAN RUTE TUNGGAL ")
    print("="*50)
    print("\nPetunjuk: Masukkan id node (Misal: V0, V1, ... V50)")
    
    # 1. PROSES VALIDASI INPUT 
    # Meminta input titik awal secara berulang sampai user memasukkan ID yang terdaftar di graf
    while True:
        start_node = input("Masukkan Titik Awal (Start Node) : ").strip().upper()
        if start_node in nama_lokasi:
            break
        print("Input tidak valid! Pastikan ID Node benar (Misal: V0).")
        
    # Meminta input titik tujuan secara berulang dengan syarat tambahan: tidak boleh sama dengan titik awal
    while True:
        target_node = input("Masukkan Titik Tujuan (Target Node): ").strip().upper()
        if target_node in nama_lokasi:
            if target_node != start_node:
                break
            else:
                print("Titik tujuan tidak boleh sama dengan titik awal.")
        else:
            print("Input tidak valid! Pastikan ID Node benar (Misal: V1).")

    # 2. EKSEKUSI ALGORITMA
    # Menjalankan Dijkstra dan menangkap hasil rute serta jaraknya
    rute_dj, jarak_dj = dijkstra(graf_gorontalo, start_node, target_node)
    print("\n" + "─"*40)
    print("> DIJKSTRA (Global Optimum)")
    print("Jalur:")
    print(format_rute(rute_dj))
    print(f"\n>> Total Jarak : {jarak_dj:.2f} Km")
    print("─"*40)

    # Menjalankan Greedy dan menangkap hasil rute, jarak, serta status keberhasilannya
    rute_gr, jarak_gr, status_gr = greedy(graf_gorontalo, start_node, target_node)
    print("\n> GREEDY (Local Optimum)")
    print(f"Status : {status_gr}")
    print("Jalur:")
    print(format_rute(rute_gr))
    
    # Jika jarak tidak bernilai 'infinity' (artinya rute ketemu), cetak angkanya
    if jarak_gr != float('infinity'):
        print(f"\n>> Total Jarak : {jarak_gr:.2f} Km")
    else:
        print("\n>> Total Jarak : Tidak terhingga (Jalan Buntu)")
    print("─"*40)

    # 3. ANALISIS & KESIMPULAN
    # Membandingkan jarak hasil kedua algoritma untuk mencetak kesimpulan mana yang lebih baik
    print("\nKESIMPULAN:")
    if jarak_gr != float('infinity'):
        if jarak_dj < jarak_gr:
            print(f"Algoritma Dijkstra ({jarak_dj:.2f} Km) lebih optimal karena menghasilkan rute yang lebih pendek dibandingkan algoritma Greedy ({jarak_gr:.2f} Km).")
        elif jarak_dj == jarak_gr:
            print(f"Kedua algoritma menghasilkan rute dengan panjang yang sama ({jarak_dj:.2f} Km).")
        else:
            print(f"Algoritma Greedy ({jarak_gr:.2f} Km) lebih optimal dari Dijkstra ({jarak_dj:.2f} Km).")
    else:
        print("Algoritma Dijkstra jauh lebih baik karena algoritma Greedy terjebak di local optimum dan tidak menemukan jalan mencapai tujuan.")
    print("\nKetik ENTER untuk kembali ke Menu Utama...")
    input()


def fitur_akumulasi_jarak():
    """
    Fungsi untuk menjalankan skenario (batch analysis): 
    1 Titik Awal ke SEMUA titik lainnya (50 node) untuk melihat tren jarak jangka panjang.
    """
    print("\n" + "="*50)
    print(" FITUR 2: KOMPARASI AKUMULASI JARAK (1 KE SEMUA) ")
    print("="*50)
    
    # Validasi input node awal sama seperti pada fitur pertama
    while True:
        start_node = input("Masukkan Node Awal (Start Node): ").strip().upper()
        if start_node in nama_lokasi:
            break
        print("Input tidak valid! Pastikan ID Node benar (Misal: V0 atau V1).")
        
    print(f"\nMengeksekusi iterasi rute dari {start_node} ({nama_lokasi[start_node]}) ke seluruh 50 kelurahan...\n")
    
    # Variabel penampung total jarak dari seluruh perhitungan
    total_jarak_dj = 0
    total_jarak_gr = 0
    rute_gagal_gr = 0 # Variabel untuk menghitung berapa kali Greedy gagal/buntu

    # Melakukan perulangan otomatis (iterasi) menciptakan target dari V1 sampai V50
    for i in range(1, 51):
        target_node = f"V{i}"
        
        # Mengeksekusi abaikan (continue) jika target_node tidak valid atau sama dengan titik awal
        if target_node not in nama_lokasi or target_node == start_node:
            continue
        
        # Hitung Dijkstra: kita hanya mengambil nilai jaraknya (indeks ke-1), rutenya tidak dicetak
        _, jarak_dj = dijkstra(graf_gorontalo, start_node, target_node)
        total_jarak_dj += jarak_dj # Tambahkan jarak ke total keseluruhan Dijkstra
        
        # Hitung Greedy
        _, jarak_gr, _ = greedy(graf_gorontalo, start_node, target_node)
        
        # Jika Greedy berhasil menemukan jalan, tambahkan ke total jarak Greedy
        if jarak_gr != float('infinity'):
            total_jarak_gr += jarak_gr
        else:
            # Jika Greedy gagal menemukan tujuan (infinity), tambahkan counter kegagalan
            rute_gagal_gr += 1
            
    # OUTPUT HASIL AKUMULASI
    print("─"*40)
    print("HASIL PERHITUNGAN AKUMULASI:")
    print(f"• Total Jarak Kumulatif Dijkstra : {total_jarak_dj:.2f} Km")
    print(f"• Total Jarak Kumulatif Greedy   : {total_jarak_gr:.2f} Km")
    if rute_gagal_gr > 0:
        print(f"  (*Greedy terjebak buntu di {rute_gagal_gr} rute dan diabaikan dari total)")
    print("─"*40)
        
    # KESIMPULAN  
    print("\nKESIMPULAN PEMBUKTIAN:")
    if total_jarak_dj < total_jarak_gr:
        print(f"Pembuktian BERHASIL! Algoritma Dijkstra terbukti jauh lebih optimal.")
        print(f"Jarak akumulasi Greedy membengkak akibat perilaku algoritma yang")
        print(f"sering terjebak mencari jarak terdekat jangka pendek (Local Optimum).")
    elif total_jarak_dj == total_jarak_gr:
        print("Hasil pembuktian sama kuat. Kedua algoritma menghasilkan jarak kumulatif yang sama.")
    else:
        print("Pada titik awal ini, Algoritma Greedy menghasilkan rute akumulasi yang lebih pendek.")
        
    print("\nKetik ENTER untuk kembali ke Menu Utama...")
    input()


def main():
    """
    Fungsi Utama (Entry Point) yang akan menahan program agar terus berjalan (Loop)
    menampilkan menu sampai pengguna memilih untuk keluar (exit).
    """
    while True:
        # Menampilkan header menu
        print("\n" * 2) 
        print("======================================================")
        print("    PROGRAM OPTIMASI RUTE KANTOR POS GORONTALO        ")
        print("    Struktur Data dan Algoritma - Kelompok 12         ")
        print("======================================================")
        print("Pilih Menu Komparasi Program:")
        print("1. Komparasi Rute Tunggal (Satu Titik Tujuan Spesifik)")
        print("2. Komparasi Akumulasi Jarak (Pembuktian 50 Node)")
        print("3. Keluar")
        
        # Menerima pilihan user
        pilihan = input("\nMasukkan pilihan menu (1/2/3): ").strip()
        
        # Mengeksekusi fungsi sesuai pilihan yang diberikan
        if pilihan == '1':
            fitur_rute_tunggal()
        elif pilihan == '2':
            fitur_akumulasi_jarak()
        elif pilihan == '3':
            print("\nTerima kasih telah menggunakan program ini.\n")
            break # Menghentikan infinite loop, program selesai
        else:
            print("\n[!] Pilihan tidak valid, silakan ketik 1, 2, atau 3.")
            print("Ketik ENTER untuk mengulang...")
            input()

# Blok ini memastikan main() hanya dijalankan jika file ini dieksekusi langsung
if __name__ == "__main__":
    main()