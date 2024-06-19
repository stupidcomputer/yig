import fitz

from .HSYIG import HSYIG
from .HSMUN import HSMUN

if __name__ == "__main__":
    d = fitz.open("MUNB2023.pdf")
    res = HSMUN(d)
    print(res.output)
