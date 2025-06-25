[START]
   |
   v
Import library (requests, pandas)
   |
   v
Panggil fetch_data(api_key, origin, destination)
   |
   v
Siapkan URL + params
   |
   v
Kirim request ke HERE API
   |
   v
+--------------------------+
| Response status OK?       |
+--------------------------+
     |Yes                           |No
     v                              v
Parse JSON                    Tangkap error
     |
     v
+--------------------------+
| routes ada di response?    |
+--------------------------+
     |Yes                           |No
     v                              v
Ambil summary + instructions     Tampilkan pesan error
     |
     v
Cetak + simpan ke CSV
     |
     v
[END]