import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from collections import defaultdict
import secrets

ARQUIVO = "numeros_existentes.txt"
TAMANHOS_VALIDOS = {6, 7}

# ===================== CORE =====================

def parse_linha(linha):
    partes = linha.strip().split("-")
    if len(partes) not in TAMANHOS_VALIDOS:
        return None, "Inválido"

    try:
        nums = [int(p) for p in partes]
    except ValueError:
        return None, "Inválido"

    if len(set(nums)) != len(nums):
        return None, "Inválido"

    if any(n < 1 or n > 60 for n in nums):
        return None, "Inválido"

    return (len(nums), tuple(sorted(nums))), "OK"


def carregar_jogos():
    if not Path(ARQUIVO).exists():
        return []

    jogos = []
    with open(ARQUIVO) as f:
        for linha in f:
            if linha.strip():
                jogo, status = parse_linha(linha)
                jogos.append((linha.strip(), jogo, status))
    return jogos


def detectar_duplicados(jogos):
    contador = defaultdict(int)
    for _, jogo, status in jogos:
        if jogo and status == "OK":
            contador[jogo] += 1
    return {j for j, qtd in contador.items() if qtd > 1}


def gerar_jogos_6(qtd, jogos_existentes):
    existentes_6 = {
        jogo for _, jogo, status in jogos_existentes
        if jogo and status == "OK" and jogo[0] == 6
    }

    novos = set()
    rng = secrets.SystemRandom()

    while len(novos) < qtd:
        nums = tuple(sorted(rng.sample(range(1, 61), 6)))
        jogo = (6, nums)

        if jogo not in existentes_6 and jogo not in novos:
            novos.add(jogo)

    return sorted(novos)


def salvar_existentes(jogos):
    with open(ARQUIVO, "w") as f:
        for _, jogo, status in jogos:
            if jogo:
                _, nums = jogo
                f.write("-".join(f"{n:02d}" for n in nums) + "\n")


# ===================== GUI =====================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mega-Sena • Gerenciador")
        self.geometry("1150x700")

        self.jogos_novos = []

        self._criar_resumo()
        self._criar_tabelas()
        self._criar_controles()

        self.refresh()

    # ---------- UI ----------

    def _criar_resumo(self):
        self.resumo = ttk.Frame(self)
        self.resumo.pack(fill="x", padx=10, pady=6)

        self.lbls = {}
        for k in ["Total", "OK", "Duplicados", "Inválidos", "6 números", "7 números"]:
            lbl = ttk.Label(self.resumo)
            lbl.pack(side="left", padx=14)
            self.lbls[k] = lbl

    def _criar_tabelas(self):
        paned = ttk.PanedWindow(self, orient="vertical")
        paned.pack(fill="both", expand=True, padx=10)

        self.frame_exist = ttk.Labelframe(paned, text="📂 Números Existentes")
        paned.add(self.frame_exist, weight=2)
        self.tree_exist = self._treeview(self.frame_exist)

        self.frame_novos = ttk.Labelframe(paned, text="🎲 Números Novos (pré-visualização)")
        paned.add(self.frame_novos, weight=1)
        self.tree_novos = self._treeview(self.frame_novos)

    def _treeview(self, parent):
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True)

        tree = ttk.Treeview(container, columns=("numeros", "status"), show="headings")
        tree.heading("numeros", text="Números")
        tree.heading("status", text="Status")
        tree.column("numeros", width=900)
        tree.column("status", width=120, anchor="center")

        tree.tag_configure("odd", background="#f5f5f5")
        tree.tag_configure("even", background="#ffffff")

        vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(container, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        return tree

    def _criar_controles(self):
        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=10, pady=8)

        ttk.Label(frame, text="Qtd jogos novos (6):").pack(side="left")
        self.qtd_var = tk.IntVar(value=10)
        ttk.Entry(frame, width=6, textvariable=self.qtd_var).pack(side="left", padx=6)

        ttk.Button(frame, text="Gerar novos", command=self.gerar_novos).pack(side="left", padx=6)
        ttk.Button(frame, text="Salvar novos", command=self.salvar_novos).pack(side="left", padx=6)
        ttk.Button(frame, text="🔄 Refresh", command=self.refresh).pack(side="left", padx=6)

    # ---------- LÓGICA ----------

    def refresh(self):
        jogos = carregar_jogos()
        duplicados = detectar_duplicados(jogos)

        self.tree_exist.delete(*self.tree_exist.get_children())

        total = ok = dup = inv = c6 = c7 = 0
        linhas = []

        for linha, jogo, status in jogos:
            if jogo:
                tamanho, nums = jogo
                numeros = "-".join(f"{n:02d}" for n in nums)
                c6 += tamanho == 6
                c7 += tamanho == 7
            else:
                numeros = linha

            if jogo and jogo in duplicados:
                status = "Duplicado"
                dup += 1
                prio = 2
            elif status == "OK":
                ok += 1
                prio = 3
            else:
                inv += 1
                prio = 1

            linhas.append((prio, numeros, status))

        linhas.sort(key=lambda x: x[0])

        for i, (_, numeros, status) in enumerate(linhas):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree_exist.insert("", "end", values=(numeros, status), tags=(tag,))

        total = len(jogos)
        self.lbls["Total"].config(text=f"🔢 Total: {total}")
        self.lbls["OK"].config(text=f"✅ OK: {ok}")
        self.lbls["Duplicados"].config(text=f"⚠️ Duplicados: {dup}")
        self.lbls["Inválidos"].config(text=f"❌ Inválidos: {inv}")
        self.lbls["6 números"].config(text=f"🎯 6 números: {c6}")
        self.lbls["7 números"].config(text=f"🎯 7 números: {c7}")

        self.jogos_existentes = jogos

    def gerar_novos(self):
        self.tree_novos.delete(*self.tree_novos.get_children())
        self.jogos_novos.clear()

        try:
            qtd = int(self.qtd_var.get())
            if qtd <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        novos = gerar_jogos_6(qtd, self.jogos_existentes)

        for i, (tamanho, nums) in enumerate(novos):
            linha = "-".join(f"{n:02d}" for n in nums)
            tag = "even" if i % 2 == 0 else "odd"
            self.tree_novos.insert("", "end", values=(linha, "Novo"), tags=(tag,))
            self.jogos_novos.append((tamanho, nums))

    def salvar_novos(self):
        if not self.jogos_novos:
            messagebox.showwarning("Aviso", "Nenhum jogo novo para salvar.")
            return

        if not messagebox.askyesno("Confirmar", "Salvar novos jogos no arquivo existente?"):
            return

        novos_registros = [(None, j, "OK") for j in self.jogos_novos]
        salvar_existentes(self.jogos_existentes + novos_registros)

        self.jogos_novos.clear()
        self.tree_novos.delete(*self.tree_novos.get_children())
        self.refresh()

        messagebox.showinfo("Sucesso", "Jogos salvos com sucesso.")


if __name__ == "__main__":
    App().mainloop()
