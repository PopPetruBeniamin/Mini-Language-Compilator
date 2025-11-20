import re
from typing import Tuple, Optional, List, Any

# ---------------------------
# 1. Atoms codification (tokens)
# ---------------------------
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

# ---------------------------
# 2. Regex tokens
# ---------------------------
TOKEN_REGEX = re.compile(
    r"\s+|==|!=|<=|>=|&&|\|\||[A-Za-z_][A-Za-z0-9_]*|[0-9]+|'[A-Za-z0-9]'|\"[A-Za-z0-9]*\"|.|\n"
)

# ---------------------------
# 3. Recognition functions
# ---------------------------
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

def classify(token: str) -> Tuple[int, Optional[str]]:
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
    return -1, token

# ---------------------------
# BST para ST
# ---------------------------
class STNode:
    def __init__(self, key: str):
        self.key = key
        self.left: Optional['STNode'] = None
        self.right: Optional['STNode'] = None

class SymbolTableBST:
    def __init__(self):
        self.root: Optional[STNode] = None

    def insert(self, key: str) -> STNode:
        """Insert the key, if doesn't exist it returns the node of the key."""
        if self.root is None:
            self.root = STNode(key)
            return self.root

        cur = self.root
        while True:
            if key == cur.key:
                return cur  # already exits
            elif key < cur.key:
                if cur.left is None:
                    cur.left = STNode(key)
                    return cur.left
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = STNode(key)
                    return cur.right
                cur = cur.right

    def find(self, key: str) -> Optional[STNode]:
        cur = self.root
        while cur:
            if key == cur.key:
                return cur
            elif key < cur.key:
                cur = cur.left
            else:
                cur = cur.right
        return None

    def inorder_list(self) -> List[str]:
        """Keys in lexicographic order."""
        out: List[str] = []
        def inorder(n: Optional[STNode]):
            if n is None: return
            inorder(n.left)
            out.append(n.key)
            inorder(n.right)
        inorder(self.root)
        return out

    def inorder_nodes(self) -> List[STNode]:
        """Listing the nodes in lexicographic order (useful for mapping nodes->index)."""
        out: List[STNode] = []
        def inorder(n: Optional[STNode]):
            if n is None: return
            inorder(n.left)
            out.append(n)
            inorder(n.right)
        inorder(self.root)
        return out

# ---------------------------
#  5. Lexical analyze
# ---------------------------
def lexical_analyze(source: str):
    tokens = TOKEN_REGEX.findall(source)
    tokens = [t for t in tokens if not t.isspace()]

    st = SymbolTableBST()
    # internal PIF: saving identifiers/consts (code, node)
    # for reserved tokens we save (code, None)
    pif_nodes: List[Tuple[int, Optional[STNode]]] = []

    for t in tokens:
        code, value = classify(t)
        if code == -1:
            raise ValueError(f"Invalid token: {t}")

        if value is not None:  # identifier o constant
            # insert or search node
            node = st.find(value)
            if node is None:
                node = st.insert(value)
            pif_nodes.append((code, node))
        else:
            pif_nodes.append((code, None))

    return st, pif_nodes

# ---------------------------
# 6. The text file analysis function
# ---------------------------
def pif_nodes_to_numeric(pif_nodes: List[Tuple[int, Optional[STNode]]], st: SymbolTableBST) -> List[Tuple[int, int]]:
    """
    Convert the PIF that contains references to nodes into a PIF (code, index)
    where index is the current lexicographic position of the node in the ST.
    Reserved tokens will have an index of -1.
    """
    # Building the mapping node -> index trough inorder
    nodes_inorder = st.inorder_nodes()
    node_to_index = {node: idx for idx, node in enumerate(nodes_inorder)}
    numeric_pif: List[Tuple[int, int]] = []
    for code, node in pif_nodes:
        if node is None:
            numeric_pif.append((code, -1))
        else:
            numeric_pif.append((code, node_to_index[node]))
    return numeric_pif

# ---------------------------
#  7. The text file analysis function
# ---------------------------
def analyze_file(filename: str):
    with open(filename, "r") as f:
        content = f.read()
    st, pif_nodes = lexical_analyze(content)

    print("ST (symbol table):")
    inorder_keys = st.inorder_list()
    for i, key in enumerate(inorder_keys):
        print(i, key)

    numeric_pif = pif_nodes_to_numeric(pif_nodes, st)
    print("\nPIF (Program Internal Form):")
    for entry in numeric_pif:
        print(entry)

# ---------------------------
# 8. Main
# ---------------------------
if __name__ == "__main__":
    analyze_file("input.txt")

