"""Download the GSE10072 series matrix into data/."""
import os
import urllib.request

URL = ("https://ftp.ncbi.nlm.nih.gov/geo/series/GSE10nnn/GSE10072/"
       "matrix/GSE10072_series_matrix.txt.gz")
OUT = os.path.join(os.path.dirname(__file__), "..", "data",
                   "GSE10072_series_matrix.txt.gz")

os.makedirs(os.path.dirname(OUT), exist_ok=True)
if os.path.exists(OUT):
    print("already downloaded:", OUT)
else:
    urllib.request.urlretrieve(URL, OUT)
    print("saved to", OUT)
