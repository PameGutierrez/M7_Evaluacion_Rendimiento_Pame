# -*- coding: utf-8 -*-
import sys, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def read_jmeter_csv(path):
    df = pd.read_csv(path)
    cols = df.columns.str.lower().tolist()
    if 'elapsed' in cols:
        df['elapsed_ms'] = df[[c for c in df.columns if c.lower()=='elapsed'][0]]
        label_col = [c for c in df.columns if c.lower()=='label']
        df['label'] = df[label_col[0]] if label_col else 'request'
        success_col = [c for c in df.columns if c.lower()=='success']
        if success_col:
            df['success'] = df[success_col[0]].astype(str).str.lower().isin(['true','1','t'])
        else:
            df['success'] = True
    elif 'average' in cols and 'label' in cols:
        df = df.rename(columns={'Average':'elapsed_ms','Label':'label'})
        df['elapsed_ms'] = pd.to_numeric(df['elapsed_ms'], errors='coerce')
        df['success'] = np.nan
    else:
        raise ValueError("Formato de CSV no reconocido: columnas " + str(df.columns))
    return df

def pct(series, p):
    return float(np.percentile(series, p))

def main():
    if len(sys.argv) < 2:
        print("Uso: python generar_informe_jmeter_solo.py <JMETER_CSV>")
        sys.exit(1)
    jm_path = sys.argv[1]
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "3_Ejecuciones", "informes"))
    graphs_dir = os.path.join(out_dir, "graficos")
    os.makedirs(graphs_dir, exist_ok=True)

    jm = read_jmeter_csv(jm_path)
    overall = {
        "jmeter_samples": int(len(jm)),
        "avg_ms": float(jm['elapsed_ms'].mean()),
        "p90_ms": pct(jm['elapsed_ms'], 90),
        "p95_ms": pct(jm['elapsed_ms'], 95),
        "p99_ms": pct(jm['elapsed_ms'], 99),
    }
    if 'success' in jm and jm['success'].notna().any():
        overall["error_rate_pct"] = float(100.0*(1 - jm['success'].mean()))

    # Gráficos
    if len(jm) > 0:
        plt.figure()
        jm['elapsed_ms'].plot(kind='hist', bins=30)
        plt.title('Histograma de tiempos de respuesta (JMeter)')
        plt.xlabel('ms'); plt.ylabel('frecuencia'); plt.grid(True)
        plt.savefig(os.path.join(graphs_dir, 'histograma_jmeter.png'), bbox_inches='tight')
        plt.close()

    by_label = None
    if 'label' in jm:
        def agg(gr):
            d = {
                'count': len(gr),
                'avg_ms': gr['elapsed_ms'].mean(),
                'p90_ms': pct(gr['elapsed_ms'], 90),
                'p95_ms': pct(gr['elapsed_ms'], 95),
                'p99_ms': pct(gr['elapsed_ms'], 99),
            }
            if 'success' in gr:
                d['error_rate_pct'] = 100.0*(1 - gr['success'].mean())
            return pd.Series(d)
        by_label = jm.groupby('label').apply(agg).reset_index()
        by_label.to_csv(os.path.join(out_dir, 'resumen_por_label_jmeter.csv'), index=False)
        # gráfico promedio por label
        import matplotlib.pyplot as plt
        plt.figure()
        plt.bar(by_label['label'], by_label['avg_ms'])
        plt.title('Promedio por sampler (JMeter)')
        plt.xlabel('Sampler'); plt.ylabel('Promedio (ms)')
        plt.xticks(rotation=20, ha='right'); plt.grid(True, axis='y')
        plt.savefig(os.path.join(graphs_dir, 'avg_por_sampler_jmeter.png'), bbox_inches='tight')
        plt.close()

    # CSV overall
    pd.DataFrame([overall]).to_csv(os.path.join(out_dir, 'resumen_overall_jmeter.csv'), index=False)

    # Informe Markdown
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    md = []
    md.append("# Informe de Resultados (JMeter)")
    md.append("")
    md.append(f"_Generado automáticamente el {ts}_")
    md.append("")
    md.append("## Resumen Ejecutivo")
    md.append(f"- Muestras (JMeter): **{overall['jmeter_samples']}**")
    md.append(f"- Promedio: **{overall['avg_ms']:.1f} ms**")
    md.append(f"- p95: **{overall['p95_ms']:.1f} ms**")
    if 'error_rate_pct' in overall:
        md.append(f"- Error rate: **{overall['error_rate_pct']:.2f}%**")
    md.append("")
    md.append("## Resultados Detallados")
    md.append("- CSV overall: `resumen_overall_jmeter.csv`")
    if by_label is not None:
        md.append("- CSV por sampler: `resumen_por_label_jmeter.csv`")
        md.append("![Promedio por sampler](./graficos/avg_por_sampler_jmeter.png)")
    md.append("![Histograma](./graficos/histograma_jmeter.png)")
    md.append("")
    md.append("## Conclusiones y Recomendaciones")
    md.append("- Verificar que el p95 cumpla el umbral objetivo (ej. 800 ms).")
    md.append("- Vigilar tasa de errores bajo carga.")
    md.append("- Priorizar optimización de endpoints con peor promedio/percentiles.")

    with open(os.path.join(out_dir, "Informe_Resultados_JMeter.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(md))

    print("Informe generado en:", os.path.join(out_dir, "Informe_Resultados_JMeter.md"))

if __name__ == "__main__":
    main()
