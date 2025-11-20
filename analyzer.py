import re                        # importing regex module to identify the tokens
from typing import Tuple, Optional, List  # For clear returned types

# -------------------------------------------------------------
# 1. Atoms codification (tokens)
# -------------------------------------------------------------
# Dictionary that associate atoms with a numeric code
TOKEN_CODES = {
    "identifier": 0,
    "constant": 1,
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

# Building the reserved words set (identifier/const are excluded)
RESERVED = {k for k in TOKEN_CODES if k not in ["identifier", "constant"]}

# -------------------------------------------------------------
# 2. Regex for tokens
# -------------------------------------------------------------
# Detects: space, operators, identifiers, numbers, chars, strings and other characters
TOKEN_REGEX = re.compile(
    r"\s+|==|!=|<=|>=|&&|\|\||[A-Za-z_][A-Za-z0-9_]*|[0-9]+|'[A-Za-z0-9]'|\"[A-Za-z0-9]*\"|.|\n"
)

# -------------------------------------------------------------
# 3. Recognition functions
# -------------------------------------------------------------

def is_identifier(token: str) -> bool:
    """Verifies if a token is a valid identifier and is not a reserved word."""
    return re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token) is not None and token not in RESERVED

def is_int_const(token: str) -> bool:
    """Verifies if a token is an integer."""
    return re.fullmatch(r"[0-9]+", token) is not None

def is_char_const(token: str) -> bool:
    """Verifies if a token is a character following the form 'a'."""
    return re.fullmatch(r"'[A-Za-z0-9]'", token) is not None

def is_string_const(token: str) -> bool:
    """Verifies if a token is a string following the form "abc"."""
    return re.fullmatch(r'"[A-Za-z0-9]*"', token) is not None

# -------------------------------------------------------------
# 4. Tokens classification
# -------------------------------------------------------------

def classify(token: str) -> Tuple[int, str]:
    """
    Returns the token code and its code for ST (Symbol Table).
    If token is an identifier or a constant -> returns its value too
    If token is a reserved world or a symbol -> its value is None
    """
    if token in RESERVED:
        return TOKEN_CODES[token], None

    if is_identifier(token):
        return TOKEN_CODES["identifier"], token

    if is_int_const(token) or is_char_const(token) or is_string_const(token):
        return TOKEN_CODES["constant"], token

    if token in TOKEN_CODES:
        return TOKEN_CODES[token], None

    return -1, token   # Invalid toker

# -------------------------------------------------------------
# 5. BST implementation for ST (lexicographically ordered)
# -------------------------------------------------------------
class STNode:
    def __init__(self, key: str):
        self.key = key
        self.left: Optional['STNode'] = None
        self.right: Optional['STNode'] = None
        # opcional: id único de inserción si quieres índices estables
        # self.insert_id = None

class SymbolTableBST:
    def __init__(self):
        self.root: Optional[STNode] = None

    def insert(self, key: str) -> STNode:
        """Insert key if not present. Return the node containing key."""
        if self.root is None:
            self.root = STNode(key)
            return self.root

        cur = self.root
        while True:
            if key == cur.key:
                return cur  # ya existe
            elif key < cur.key:
                if cur.left is None:
                    cur.left = STNode(key)
                    return cur.left
                cur = cur.left
            else:  # key > cur.key
                if cur.right is None:
                    cur.right = STNode(key)
                    return cur.right
                cur = cur.right

    def find(self, key: str) -> Optional[STNode]:
        cur = self.root
        while cur is not None:
            if key == cur.key:
                return cur
            elif key < cur.key:
                cur = cur.left
            else:
                cur = cur.right
        return None

    def inorder_list(self) -> List[str]:
        """Return list of keys in lexicographic order (inorder traversal)."""
        result: List[str] = []
        def inorder(node: Optional[STNode]):
            if not node:
                return
            inorder(node.left)
            result.append(node.key)
            inorder(node.right)
        inorder(self.root)
        return result

    def __contains__(self, key: str) -> bool:
        return self.find(key) is not None

# -------------------------------------------------------------
# 6. Lexical analyzer
# -------------------------------------------------------------
def lexical_analyze(source: str):
    """The function receives the source code in text format and returns ST and PIF (Program Internal Form)."""

    tokens = TOKEN_REGEX.findall(source)  # Extracting tokens
    tokens = [t for t in tokens if not t.isspace()]  # Deleting spaces

    st = SymbolTableBST()  # Sybol table
    PIF = [] # Program Internal Form

    for t in tokens:
        code, value = classify(t)

        if code == -1:
            raise ValueError(f"Invalid token: {t}")

        if value is not None:  # identifier or constant
            if value not in st:
                st.insert(value)
                # obtener la lista inorder y la posición (índice) lexicográfica
            inorder_keys = st.inorder_list()
            index = inorder_keys.index(value)  # índice lexicográfico actual
            PIF.append((code, index))
        else:
            PIF.append((code, -1))  # Reserved words and symbols have no index

    return st, PIF

# -------------------------------------------------------------
# 7. The text file analysis function
# -------------------------------------------------------------

def analyze_file(filename: str):
    with open(filename, "r") as f:
        content = f.read()

    st, PIF = lexical_analyze(content)

    print("ST (Symbol table) - lexicographic order:")
    inorder_keys = st.inorder_list()
    for i, s in enumerate(inorder_keys):
        print(i, s)

    print("\nPIF (Program Internal Form):")
    for entry in PIF:
        print(entry)

# -------------------------------------------------------------
# 8. Main
# -------------------------------------------------------------

if __name__ == "__main__":
    analyze_file("input.txt")