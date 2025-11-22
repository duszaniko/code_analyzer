### Install
# pip install --upgrade streamlit
# pip install --upgrade pyflakes
# pip install --upgrade asttokens
# pip install --upgrade pyflakes

# Install ollama from: https://ollama.com/download/windows
# run a package: ollama run llama3 (pulls if not yet downloaded)

# run code with command: streamlit run code_analyzer.py

from pyflakes.api import check
from pyflakes.reporter import Reporter
from io import StringIO
from io import BytesIO
from ollama import chat


import streamlit as st
import ast
import asttokens
import requests
import json
import keyword
import tokenize
import re




# -------------------------------# AST Metadata Collector# -------------------------------
class MetadataVisitor(ast.NodeVisitor):
    def __init__(self, asttokens_ref):
        self.atok = asttokens_ref
        self.variables = []
        self.functions = []
        self.classes = []
        self.imports = []

    def _pos(self, node):
        start, end = self.atok.get_text_range(node)
        return {"start": start, "end": end, "line": node.lineno, "col": node.col_offset}

    def visit_Name(self, node):
        kind = "load" if isinstance(node.ctx, ast.Load) else "assign"
        if kind == "assign":
            kind = "assign"
        pos = self._pos(node)
        self.variables.append({"name": node.id, "kind": kind, **pos})
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        pos = self._pos(node)
        self.functions.append({"name": node.name, **pos})
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        pos = self._pos(node)
        self.classes.append({"name": node.name, **pos})
        self.generic_visit(node)
    def visit_import(self, node):
        for alias in node.names:
            pos = self._pos(node)
            self.imports.append({"name": alias.asname or alias.name, **pos})

    def visit_importFrom(self, node):
        for alias in node.names:
            pos = self._pos(node)
            self.imports.append({"name": alias.asname or alias.name, **pos})

# -------------------------------# Keywords detection# -------------------------------
def extract_keywords_positions(code: str):
    """Return list of dicts: {name, start, end, line, col} for keywords."""
    keywords_positions = []
    tokens = tokenize.tokenize(BytesIO(code.encode('utf-8')).readline)
    for tok in tokens:
        tok_type = tok.type
        tok_string = tok.string
        if tok_type == tokenize.NAME and keyword.iskeyword(tok_string):
            keywords_positions.append({
                "name": tok_string,
                "start": tok.start[1] + sum(len(l) + 1 for l in code.splitlines()[:tok.start[0]-1]),
                "end": None, # we'll fill in later
                "line": tok.start[0],
                "col": tok.start[1]
            })
            # end position in absolute char offsets
            keywords_positions[-1]["end"] = keywords_positions[-1]["start"] + len(tok_string)
    return keywords_positions

# -------------------------------# PyFlakes parser# -------------------------------
def parse_pyflakes(output: str, code: str):
    diagnostics = []
    for line in output.splitlines():
        if ":" not in line:
            continue
        parts = line.split(":")
        if len(parts) < 3:
            continue
        _, line_no, message = parts[0], parts[1], ":".join(parts[2:])
        line_no = int(line_no.strip())
        msg = message.strip()

        var_name = None
        if "undefined name" in msg:
            import re
            m = re.search(r"'([^']+)'", msg)
            if m:
                var_name = m.group(1)

        col = None
        start = None
        end = None
        if var_name:
            lines = code.splitlines()
            if 1 <= line_no <= len(lines):
                line_text = lines[line_no - 1]
                col = line_text.find(var_name)
                if col != -1:
                    char_count_before = sum(len(l) + 1 for l in lines[:line_no - 1])
                    start = char_count_before + col
                    end = start + len(var_name)

        diagnostics.append({
            "message": msg,
            "line": line_no,
            "col": col,
            "start": start,
            "end": end
        })
    return diagnostics

# -------------------------------# Combined analyzer# -------------------------------
def analyze(code: str):
    # 1) AST metadata
    atok = asttokens.ASTTokens(code, parse=True)
    visitor = MetadataVisitor(atok)
    visitor.visit(atok.tree)
    # 2) Keywords metadata
    keywords_positions = extract_keywords_positions(code)
    # 3) PyFlakes diagnostics
    stdout = StringIO()
    stderr = StringIO()
    reporter = Reporter(stdout, stderr)
    check(code, filename="<input>", reporter=reporter)
    pyflakes_raw = stdout.getvalue().strip()
    pyflakes_structured = parse_pyflakes(pyflakes_raw, code)
    return {
                "symbols": {            
                    "variables": visitor.variables,
                    "functions": visitor.functions,
                    "classes": visitor.classes,
                     "imports": visitor.imports,"keywords": keywords_positions
                     },
                "pyflakes_raw": pyflakes_raw,
                "pyflakes": pyflakes_structured
                }

def ollama_explain(code: str, static_info: str, model: str = "llama3") -> str:
    prompt = f"""
    You are a Python code analysis assistant.
    Static analysis information:
    {static_info}
    Explain clearly what the following Python code does.
    Focus on high-level behavior and key operations.
    {code}
    """
    with st.expander("Prompt sent to ML"):
        st.write(prompt)
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }    )
    return response.json()["response"]


st.set_page_config(page_title="Code Analyzer", layout='wide')
st.title("Code Analyzer")

default_code_string = """
import math
x = 10
for i in range(5):
    if x > i:
        print("hi")
    else:
        y = i
"""


code_string = st.text_area("Copy code here!", value=default_code_string, height=250)
button_pressed = st.button("Analyze code")

if button_pressed:
    st.code(code_string, language="python")
    static_info = json.dumps(analyze(code_string), indent=2)
    with st.expander(label="Extracted structure"):
        st.json(static_info)
    
    with st.spinner(text="Code analytics in progress..."):
        explanation = ollama_explain(code_string, static_info)
        with st.expander("Answer from ML"):
            st.text(explanation)    