# data-kependudukan-indonesia-level-kelurahan
Data kependudukan Indonesia di level Kelurahan.

Source: https://gis.dukcapil.kemendagri.go.id/peta/

## Data
There's two format given, initially JSON is also planned to be added, but the file size exceed GitHub maximum file size. Hence why it was eventually discarded.

| Format      | Data File |
| ----------- | ----------- |
| CSV      | [data_kependudukan_kelurahan.csv](data/data_kependudukan_kelurahan.csv)       |
| Parquet   | [data_kependudukan_kelurahan.parquet](data/data_kependudukan_kelurahan.parquet)        |

The data covers population numbers, break down by gender, religion, age, and education. Here's an **example** snippets of the data, more columns are availables in the file compare to this snipped.
|   nama_prop  |   nama_kab         |   nama_kec          |   nama_kel     |   jumlah_penduduk  |   jumlah_kk  |   luas_wilayah  |   kepadatan_penduduk  |
|--------------|--------------------|---------------------|----------------|--------------------|--------------|-----------------|-----------------------|
|   ACEH       |   KAB. ACEH BARAT  |   ARONGAN LAMBALEK  |   ALUE BAGOK   |   461.0            |   164.0      |   2782.87       |   0.16565614          |
|   ACEH       |   KAB. ACEH BARAT  |   ARONGAN LAMBALEK  |   ALUE BATEE   |   235.0            |   83.0       |   2782.87       |   0.0844451           |
|   ACEH       |   KAB. ACEH BARAT  |   ARONGAN LAMBALEK  |   ALUE SUNDAK  |   275.0            |   104.0      |   2782.87       |   0.09881874          |
|   ACEH       |   KAB. ACEH BARAT  |   ARONGAN LAMBALEK  |   ARONGAN      |   319.0            |   101.0      |   2782.87       |   0.11462974          |

## Scrapping yourself
1. Clone this repository and `cd` in to it
```bash
$ git clone https://github.com/perfect-less/data-kependudukan-indonesia-level-kelurahan
$ cd data-kependudukan-indonesia-level-kelurahan
```
2. Install the Python's requirements
```bash
$ pip install -r requirements.txt
```
3. Run the script
```bash
$ python ascrapper.py
```

By the end the data should be found inside the `data` directory.
