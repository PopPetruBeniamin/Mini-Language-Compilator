# Analizor lexical complet comentat linie cu linie

import re                        # Importam modulul regex pentru a putea identifica token-urile
from typing import List, Tuple   # Pentru tipuri returnate clare

# -------------------------------------------------------------
# 1. Codificarea atomilor (tokenurilor)
# -------------------------------------------------------------
# Dicționarul asociază fiecărui tip de atom un cod numeric.
TOKEN_CODES = {
    "identificator": 0,
    "constanta": 1,
    "int": 2,
    "char": 3,
    "string": 4,
    "bool": 5,
    "const": 6,
    "for": 7,
    "while": 8,
    "do": 9,
    "if": 10,
    "else": 11,
    "cin": 12,
    "cout": 13,
    "return": 14,
    "main": 15,
    ";": 16,
    ",": 17,
    ".": 18,
    "+": 19,
    "*": 20,
    "(": 21,
    ")": 22,
    "[": 23,
    "]": 24,
    "{": 25,
    "}": 26,
    "-": 27,
    "<": 28,
    ">": 29,
    "=": 30,
    "==": 31,
    ":": 32,
    "<=": 33,
    ">=": 34,
    "!=": 35,
    "&&": 36,
    "||": 37,
}

# Construim setul de cuvinte rezervate (adica tot ce nu e identif/const)
RESERVED = {k for k in TOKEN_CODES if k not in ["identificator", "constanta"]}

# -------------------------------------------------------------
# 2. Regex pentru tokenizare
# -------------------------------------------------------------
# Detectează: spații, operatori compuși, identificatori, numere, char-uri, stringuri și orice alt caracter
TOKEN_REGEX = re.compile(
    r"\s+|==|!=|<=|>=|&&|\|\||[A-Za-z_][A-Za-z0-9_]*|[0-9]+|'[A-Za-z0-9]'|\"[A-Za-z0-9]*\"|.|\n"
)

# -------------------------------------------------------------
# 3. Funcții de recunoaștere
# -------------------------------------------------------------

def is_identifier(token: str) -> bool:
    """Verifică dacă un token este identificator valid și nu e cuvânt rezervat."""
    return re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token) is not None and token not in RESERVED


def is_int_const(token: str) -> bool:
    """Verifică dacă tokenul este un număr întreg."""
    return re.fullmatch(r"[0-9]+", token) is not None


def is_char_const(token: str) -> bool:
    """Verifică dacă tokenul este un caracter de forma 'a'."""
    return re.fullmatch(r"'[A-Za-z0-9]'", token) is not None


def is_string_const(token: str) -> bool:
    """Verifică dacă tokenul este un string de forma "abc"."""
    return re.fullmatch(r'"[A-Za-z0-9]*"', token) is not None

# -------------------------------------------------------------
# 4. Clasificarea tokenului
# -------------------------------------------------------------

def classify(token: str) -> Tuple[int, str]:
    """
    Returnează codul tokenului și valoarea lui pentru TS.
    Dacă tokenul este identificator sau constantă → returnăm și valoarea.
    Dacă este un cuvânt rezervat sau simbol → valoarea este None.
    """
    if token in RESERVED:
        return TOKEN_CODES[token], None

    if is_identifier(token):
        return TOKEN_CODES["identificator"], token

    if is_int_const(token) or is_char_const(token) or is_string_const(token):
        return TOKEN_CODES["constanta"], token

    if token in TOKEN_CODES:
        return TOKEN_CODES[token], None

    return -1, token   # Token invalid

# -------------------------------------------------------------
# 5. Analizorul lexical propriu-zis
# -------------------------------------------------------------

def lexical_analyze(source: str):
    """Primește textul sursă și returnează TS și FIP."""

    tokens = TOKEN_REGEX.findall(source)  # Extragem tokenurile brute
    tokens = [t for t in tokens if not t.isspace()]  # Eliminăm spațiile

    TS = []  # Tabela de simboluri
    FIP = [] # Forma internă a programului

    for t in tokens:
        code, value = classify(t)

        if code == -1:
            raise ValueError(f"Token nevalid: {t}")

        if value is not None:  # identificator sau constantă
            if value not in TS:
                TS.append(value)   # Adăugăm în tabel doar dacă nu există deja
            index = TS.index(value)  # Obținem poziția din TS
            FIP.append((code, index))  # Adăugăm în FIP
        else:
            FIP.append((code, -1))  # Cuvinte rezervate și simboluri nu au index

    return TS, FIP

# -------------------------------------------------------------
# 6. Funcția de analiză a unui fișier text
# -------------------------------------------------------------

def analyze_file(filename: str):
    with open(filename, "r") as f:
        content = f.read()

    TS, FIP = lexical_analyze(content)

    print("TS (Tabela de simboluri):")
    for i, s in enumerate(TS):
        print(i, s)

    print("\nFIP (Forma interna a programului):")
    for entry in FIP:
        print(entry)

# -------------------------------------------------------------
# 7. Punctul de intrare al programului
# -------------------------------------------------------------

if __name__ == "__main__":
    analyze_file("input.txt")