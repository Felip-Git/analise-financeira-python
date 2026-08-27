import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / "data" / "vendas.csv", parse_dates=["data"])

df["mes"] = df["data"].dt.to_period("M").astype(str)
df["margem"] = df["lucro"] / df["receita"]

print("=== RESUMO FINANCEIRO ===")
print(f"Receita: R$ {df['receita'].sum():,.2f}")
print(f"Custo:   R$ {df['custo_total'].sum():,.2f}")
print(f"Lucro:   R$ {df['lucro'].sum():,.2f}")
print(f"Margem:  {df['lucro'].sum()/df['receita'].sum():.2%}")

mensal = df.groupby("mes")[["receita", "custo_total", "lucro"]].sum()
produto = df.groupby("produto")[["receita", "lucro"]].sum().sort_values("lucro", ascending=False)
cliente = df.groupby("cliente")["receita"].sum().sort_values(ascending=False)

print("\n=== TOP PRODUTOS POR LUCRO ===")
print(produto.head(5))
print("\n=== TOP CLIENTES POR RECEITA ===")
print(cliente.head(5))

ROOT.joinpath("outputs").mkdir(exist_ok=True)

plt.figure(figsize=(10, 5))
mensal["receita"].plot(kind="line", marker="o")
plt.title("Evolução da Receita Mensal")
plt.xlabel("Mês")
plt.ylabel("Receita (R$)")
plt.grid(alpha=.25)
plt.tight_layout()
plt.savefig(ROOT / "outputs" / "receita_mensal.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 5))
produto.head(8)["lucro"].sort_values().plot(kind="barh")
plt.title("Lucro por Produto — Top 8")
plt.xlabel("Lucro (R$)")
plt.tight_layout()
plt.savefig(ROOT / "outputs" / "lucro_produtos.png", dpi=150)
plt.close()
