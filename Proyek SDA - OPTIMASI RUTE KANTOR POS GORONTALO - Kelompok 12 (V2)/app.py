from flask import Flask, render_template, request
import json
import time
from data import graf_gorontalo, nama_lokasi
from algoritma import dijkstra, greedy

app = Flask(__name__)

def format_rute_html(rute, max_node=8):
    if not rute: return "Tidak ada rute"
    teks = ""
    for i, node in enumerate(rute):
        teks += str(node)
        if i < len(rute) - 1:
            if (i + 1) % max_node == 0:
                teks += " ➔<br>"
            else:
                teks += " ➔ "
    return teks

def siapkan_data_graf_gabungan(rute_dj, rute_gr, start_node=None, target_node=None, is_akumulasi=False):
    nodes = []
    edges = []
    
    edges_dj = set()
    edges_gr = set()
    trapped_node = None
    
    if is_akumulasi:
        for r in (rute_dj or []):
            for i in range(len(r)-1): edges_dj.add(tuple(sorted([r[i], r[i+1]])))
        for r in (rute_gr or []):
            for i in range(len(r)-1): edges_gr.add(tuple(sorted([r[i], r[i+1]])))
    else:
        if rute_dj:
            for i in range(len(rute_dj)-1): edges_dj.add(tuple(sorted([rute_dj[i], rute_dj[i+1]])))
        if rute_gr:
            for i in range(len(rute_gr)-1): edges_gr.add(tuple(sorted([rute_gr[i], rute_gr[i+1]])))
            if target_node and rute_gr[-1] != target_node:
                trapped_node = rute_gr[-1]

    # Render Node
    for id_node, nama in nama_lokasi.items():
        if id_node == start_node:
            color = {"background": "#3B82F6", "border": "#93C5FD"} # Biru Start yang lebih terang
            font_color, border_width = "#FFFFFF", 3
        elif target_node and id_node == target_node:
            color = {"background": "#10B981", "border": "#6EE7B7"} # Hijau Target yang lebih terang
            font_color, border_width = "#FFFFFF", 3
        elif trapped_node and id_node == trapped_node:
            color = {"background": "#EF4444", "border": "#FCA5A5"} # Merah Terang
            font_color, border_width = "#FFFFFF", 3
        else:
            color = {"background": "#475569", "border": "#94A3B8"} # Abu-abu kebiruan terang (Default Node)
            font_color, border_width = "#F8FAFC", 1 # Teks node putih 
            
        nodes.append({
            "id": id_node, "label": id_node, "title": f"{id_node} - {nama}",
            "color": color, "borderWidth": border_width,
            "font": {"color": font_color, "size": 12, "face": "Inter", "bold": True} 
        })
        
    # Render Edge
    added = set()
    for asal, tetangga in graf_gorontalo.items():
        for tujuan, bobot in tetangga.items():
            edge_id = tuple(sorted([asal, tujuan]))
            if edge_id not in added:
                added.add(edge_id)
                in_dj = edge_id in edges_dj
                in_gr = edge_id in edges_gr
                
                if in_dj and in_gr:
                    edge_color, width, dashes = "#F59E0B", 4, False # Kuning/Amber Terang (Shared/Sama)
                elif in_dj:
                    edge_color, width, dashes = "#3B82F6", 3.5, False # Biru (Dijkstra)
                elif in_gr:
                    edge_color, width, dashes = "#10B981", 3.5, [5, 5] # Hijau dashed (Greedy)
                else:
                    edge_color, width, dashes = "#64748B", 1.5, False 
                
                edges.append({
                    "from": asal, "to": tujuan,
                    "label": str(bobot) if (in_dj or in_gr) else "", 
                    "color": {"color": edge_color},
                    "width": width, "dashes": dashes,
                    "font": {"size": 12, "align": "middle", "color": "#FFFFFF", "strokeWidth": 3, "strokeColor": "#1A1C23", "bold": True}
                })
                
    return {"nodes": nodes, "edges": edges}

@app.route('/', methods=['GET', 'POST'])
def index():
    hasil = None
    if request.method == 'POST':
        start_node = request.form.get('start_node')
        target_node = request.form.get('target_node')
        jenis_perbandingan = request.form.get('jenis_perbandingan', 'tunggal')
        
        if jenis_perbandingan == 'tunggal' and start_node == target_node:
            hasil = {"error": "Titik Tujuan tidak boleh sama dengan Titik Awal!"}
        elif jenis_perbandingan == 'tunggal':
            # Pengukuran Waktu Dijkstra
            start_time = time.perf_counter()
            rute_dj, jarak_dj = dijkstra(graf_gorontalo, start_node, target_node)
            waktu_dj = (time.perf_counter() - start_time) * 1000 # ms
            
            # Pengukuran Waktu Greedy
            start_time = time.perf_counter()
            rute_gr, jarak_gr, _ = greedy(graf_gorontalo, start_node, target_node)
            waktu_gr = (time.perf_counter() - start_time) * 1000 # ms
            
            # Tentukan Status Logika Dinamis
            if jarak_gr == float('infinity'):
                status_gr = 'Gagal'
            elif abs(jarak_dj - jarak_gr) < 0.01: # Margin error kecil untuk komparasi identik
                status_gr = 'Sama'
            else:
                status_gr = 'Sub-Optimal'

            graf_gabungan = siapkan_data_graf_gabungan(rute_dj, rute_gr, start_node, target_node, is_akumulasi=False)
            
            hasil = {
                "jenis": "tunggal",
                "start": start_node, "target": target_node,
                "dj_rute": format_rute_html(rute_dj), "dj_jarak": f"{jarak_dj:.2f}", "dj_waktu": f"{waktu_dj:.4f}",
                "gr_rute": format_rute_html(rute_gr), "gr_jarak": f"{jarak_gr:.2f}" if status_gr != 'Gagal' else "Trapped",
                "gr_waktu": f"{waktu_gr:.4f}",
                "status_gr": status_gr,
                "terjebak_node": rute_gr[-1] if status_gr == 'Gagal' else None,
                "graf_json": json.dumps(graf_gabungan)
            }
        else: # Akumulasi (Batch Analysis)
            total_jarak_dj, total_jarak_gr, rute_gagal_gr = 0.0, 0.0, 0
            semua_rute_dj, semua_rute_gr = [], []
            waktu_dj_total, waktu_gr_total = 0, 0
            
            for i in range(1, 51):
                t_node = f"V{i}"
                if t_node not in nama_lokasi or t_node == start_node: continue
                
                # Dijkstra Batch
                st = time.perf_counter()
                r_dj, jarak_dj = dijkstra(graf_gorontalo, start_node, t_node)
                waktu_dj_total += (time.perf_counter() - st) * 1000
                if r_dj: 
                    total_jarak_dj += jarak_dj
                    semua_rute_dj.append(r_dj)
                
                # Greedy Batch
                st = time.perf_counter()
                r_gr, jarak_gr, _ = greedy(graf_gorontalo, start_node, t_node)
                waktu_gr_total += (time.perf_counter() - st) * 1000
                if jarak_gr != float('infinity'): total_jarak_gr += jarak_gr
                else: rute_gagal_gr += 1
                if r_gr: semua_rute_gr.append(r_gr)
            
            graf_gabungan = siapkan_data_graf_gabungan(semua_rute_dj, semua_rute_gr, start_node, None, is_akumulasi=True)
            
            hasil = {
                "jenis": "akumulasi", "start": start_node,
                "dj_jarak": f"{total_jarak_dj:.2f}", "dj_waktu": f"{waktu_dj_total:.4f}",
                "gr_jarak": f"{total_jarak_gr:.2f}", "gr_waktu": f"{waktu_gr_total:.4f}",
                "rute_gagal_gr": rute_gagal_gr,
                "cakupan_dj": "100%", "cakupan_gr": f"{round(((50 - rute_gagal_gr) / 49) * 100)}%",
                "graf_json": json.dumps(graf_gabungan)
            }

    return render_template('index.html', lokasi=nama_lokasi, hasil=hasil)

@app.route('/dataset')
def dataset():
    graf_full = siapkan_data_graf_gabungan([], [], None, None, is_akumulasi=False)
    return render_template('dataset.html', lokasi=nama_lokasi, graf_gorontalo=graf_gorontalo, graf_json=json.dumps(graf_full))

if __name__ == '__main__':
    app.run(debug=True)