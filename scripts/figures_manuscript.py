"""Figures for the accompanying manuscript (Figures 1-2, Supplementary Figures 1-2). Output: figures_out/.
All text 8 pt (panel letters 8 pt bold, uppercase); thinnest lines 1 pt; RGB; vector PDF plus
600-dpi PNG and TIFF. Values are the study's computed outputs (Supplementary Table 3)."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

MM = 1 / 25.4
FS = 8
LW = 1.0
plt.rcParams.update({
    "font.family": ["Arial", "Liberation Sans"], "font.size": FS,
    "axes.linewidth": LW, "xtick.major.width": LW, "ytick.major.width": LW,
    "xtick.major.size": 3, "ytick.major.size": 0, "lines.linewidth": LW,
    "pdf.fonttype": 42, "svg.fonttype": "none", "hatch.linewidth": LW,
})
INK, INK2, MUTED = "#0b0b0b", "#4a4946", "#8a8984"
BLUE, BLUE_L = "#1c5cab", "#e8f0fb"
GRAY_F, GUIDE = "#ecebe7", "#dcdbd6"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures_out") + os.sep
os.makedirs(OUT, exist_ok=True)
N = 943


def save(fig, name):
    fig.savefig(OUT + name + ".pdf")
    fig.savefig(OUT + name + ".png", dpi=600)
    fig.savefig(OUT + name + ".tif", dpi=600, pil_kwargs={"compression": "tiff_lzw"})
    from PIL import Image  # flatten RGBA to RGB on white for journal upload
    im = Image.open(OUT + name + ".tif"); bg = Image.new("RGB", im.size, "white")
    bg.paste(im, mask=im.split()[-1] if im.mode == "RGBA" else None)
    bg.save(OUT + name + ".tif", compression="tiff_lzw", dpi=(600, 600))
    plt.close(fig)


def box(ax, x, y, w, h, text, fc="white", ec=INK2, lw=LW, color=INK, weight="normal", ls="-", ha="center", zorder=2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.012",
                                fc=fc, ec=ec, lw=lw, ls=ls, zorder=zorder))
    tx = x + w / 2 if ha == "center" else x + 0.012
    ax.text(tx, y + h / 2, text, ha=ha, va="center", fontsize=FS, color=color,
            fontweight=weight, linespacing=1.15, zorder=zorder + 1)


def arrow(ax, x1, y1, x2, y2, color=INK2, ls="-", lw=LW, zorder=3):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=8,
                                 color=color, lw=lw, ls=ls, shrinkA=0, shrinkB=0, zorder=zorder))


def cross(ax, x, y, r, color=INK2, lw=1.4):
    ax.add_line(Line2D([x - r, x + r], [y - r, y + r], color=color, lw=lw, zorder=5))
    ax.add_line(Line2D([x - r, x + r], [y + r, y - r], color=color, lw=lw, zorder=5))


def tick(ax, x, y, r, color=BLUE, lw=1.6):
    ax.add_line(Line2D([x - r, x - 0.3 * r, x + r], [y, y - 0.7 * r, y + 0.9 * r], color=color, lw=lw,
                       zorder=5, solid_capstyle="round"))


# ------------------------------------------------------------------ Fig. 1
def fig1():
    W, H = 180, 104
    fig = plt.figure(figsize=(W * MM, H * MM))
    # ---- panel a (left 47%)
    ax = fig.add_axes([0, 0, 0.47, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.01, 0.975, "A", fontsize=FS, fontweight="bold", va="top")
    ax.text(0.06, 0.975, "Two directions of aggregation", fontsize=FS, va="top")
    # vertical grouping field (product 1 and its records)
    ax.add_patch(FancyBboxPatch((0.035, 0.155), 0.30, 0.47, boxstyle="round,pad=0,rounding_size=0.02",
                                fc=GRAY_F, ec="none", zorder=0))
    # horizontal grouping outline (products)
    ax.add_patch(FancyBboxPatch((0.025, 0.475), 0.955, 0.145, boxstyle="round,pad=0,rounding_size=0.02",
                                fc="none", ec=BLUE, lw=1.3, zorder=1))
    # component
    box(ax, 0.20, 0.80, 0.60, 0.11, "Upstream component c\n(for example, a foundation model)", fc=BLUE_L, ec=BLUE)
    # products
    pc = [0.185, 0.50, 0.815]
    for i, x in enumerate(pc):
        box(ax, x - 0.125, 0.49, 0.25, 0.115, f"Product {i + 1}\nfirm {'ABC'[i]}")
        arrow(ax, x, 0.605, 0.50 + (i - 1) * 0.12, 0.80, color=BLUE, ls=(0, (3, 2)))
    # event records
    groups = {0: [0.105, 0.185, 0.265], 1: [0.46, 0.54], 2: [0.735, 0.815, 0.895]}
    for o, xs in groups.items():
        for x in xs:
            box(ax, x - 0.032, 0.225, 0.064, 0.085, "e")
            arrow(ax, x, 0.31, pc[o] + (x - pc[o]) * 0.3, 0.49, color=INK2)
    # hop labels
    ax.text(0.985, 0.705, "hop 3", fontsize=FS, color=BLUE, ha="right", va="center")
    ax.text(0.985, 0.40, "hop 1", fontsize=FS, color=INK2, ha="right", va="center")
    ax.text(0.045, 0.19, "event records", fontsize=FS, color=INK2, va="center")
    # captions
    ax.text(0.035, 0.105, "Vertical (grey field): records of one product", fontsize=FS, color=INK, va="center")
    ax.text(0.035, 0.050, "Horizontal (blue): products that share c", fontsize=FS, color=BLUE, va="center")

    # ---- panel b (right 53%)
    bx = fig.add_axes([0.49, 0, 0.51, 1]); bx.set_xlim(0, 1); bx.set_ylim(0, 1); bx.axis("off")
    bx.text(0.0, 0.975, "B", fontsize=FS, fontweight="bold", va="top")
    bx.text(0.05, 0.975, "Where the traversal breaks", fontsize=FS, va="top")
    cols = [(0.02, "US device surveillance"), (0.52, "Vaccine Safety Datalink\n(positive control)")]
    bw, bh = 0.44, 0.13
    ys = {"top": 0.70, "mid": 0.405, "bot": 0.11}
    for x0, head in cols:
        bx.text(x0 + bw / 2, 0.895, head, fontsize=FS, ha="center", va="center", fontweight="bold",
                linespacing=1.1)
    # device column
    x0 = cols[0][0]
    box(bx, x0, ys["top"], bw, bh, "", fc="white", ec=MUTED, ls=(0, (3, 2)))
    cross(bx, x0 + 0.045, ys["top"] + bh / 2, 0.02)
    bx.text(x0 + 0.08 + (bw - 0.08) / 2, ys["top"] + bh / 2,
            "Upstream component:\nno field in any of the\nseven audited systems",
            ha="center", va="center", fontsize=FS, color=INK2, linespacing=1.15, zorder=4)
    box(bx, x0, ys["mid"], bw, bh, "Product\n510(k) database or GUDID\nrecord (hop 2)")
    box(bx, x0, ys["bot"], bw, bh, "Event record\nMDR master record\nand DEVICE file")
    ax_x = x0 + 0.06
    arrow(bx, ax_x, ys["bot"] + bh, ax_x, ys["mid"], color=INK2)
    bx.text(ax_x + 0.025, (ys["bot"] + bh + ys["mid"]) / 2, "hop 1: submission\nnumber or UDI-DI",
            fontsize=FS, va="center", color=INK2, linespacing=1.1)
    arrow(bx, ax_x, ys["mid"] + bh, ax_x, ys["top"], color=MUTED, ls=(0, (3, 2)))
    bx.text(ax_x + 0.025, (ys["mid"] + bh + ys["top"]) / 2, "hop 3: no structured\nfield",
            fontsize=FS, va="center", color=INK2, linespacing=1.1)
    # vaccine column
    x1 = cols[1][0]
    box(bx, x1, ys["top"], bw, bh, "", fc=BLUE_L, ec=BLUE)
    tick(bx, x1 + 0.045, ys["top"] + bh / 2, 0.02)
    bx.text(x1 + 0.08 + (bw - 0.08) / 2, ys["top"] + bh / 2,
            "Shared technology\n(mRNA): pooled weekly\nanalyses; C1–C3 present",
            ha="center", va="center", fontsize=FS, color=INK, linespacing=1.15, zorder=4)
    box(bx, x1, ys["mid"], bw, bh, "Vaccine product\n(CVX code)")
    box(bx, x1, ys["bot"], bw, bh, "Vaccination record")
    vx = x1 + 0.06
    arrow(bx, vx, ys["bot"] + bh, vx, ys["mid"], color=INK2)
    bx.text(vx + 0.025, (ys["bot"] + bh + ys["mid"]) / 2, "CVX code", fontsize=FS, va="center", color=INK2)
    arrow(bx, vx, ys["mid"] + bh, vx, ys["top"], color=BLUE)
    bx.text(vx + 0.025, (ys["mid"] + bh + ys["top"]) / 2, "prespecified list\nof CVX codes",
            fontsize=FS, va="center", color=BLUE, linespacing=1.1)
    bx.text(0.5, 0.04, "C1, query key; C2, signal definition; C3, scheduled review",
            fontsize=FS, color=INK2, ha="center", va="center")
    save(fig, "Fig1_directions_traversal")


# ------------------------------------------------------------------ Fig. 2
def dotpanel(fig, rect, rows, xmax=135):
    ax = fig.add_axes(rect)
    n = len(rows)
    ys = list(range(n))[::-1]
    for (lab, val, kind, note, grp), y in zip(rows, ys):
        ax.plot([0, 100], [y, y], color=GUIDE, lw=LW, zorder=0, solid_capstyle="butt")
        if kind == "dot":
            ax.plot(val, y, "o", ms=6, mfc=BLUE, mec=BLUE, mew=LW, zorder=3)
        elif kind == "open":
            ax.plot(val, y, "o", ms=6.5, mfc="white", mec=BLUE, mew=1.3, zorder=3)
        elif kind == "diamond":
            ax.plot(val, y, "D", ms=5.5, mfc=INK, mec=INK, mew=LW, zorder=3)
        elif kind == "cross":
            ax.plot(0, y, "x", ms=7, mec=INK2, mew=1.6, zorder=3, clip_on=False)
        ax.text((val if kind != "cross" else 0) + 3.2, y, note, va="center", ha="left", fontsize=FS,
                color=INK if kind != "cross" else INK2, zorder=4,
                bbox=dict(boxstyle="square,pad=0.12", fc="white", ec="none"))
        ax.text(-4, y, lab, va="center", ha="right", fontsize=FS, color=INK)
        if grp:
            ax.text(-102, y, grp, va="center", ha="left", fontsize=FS, fontweight="bold", color=INK)
    ax.set_xlim(0, xmax); ax.set_ylim(-0.7, n - 0.3)
    ax.set_yticks([]); ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0", "25", "50", "75", "100"], fontsize=FS, color=INK)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_bounds(0, 100); ax.spines["bottom"].set_color(INK2)
    ax.tick_params(axis="x", colors=INK2, labelcolor=INK)
    return ax, ys


def fig2():
    W, H = 180, 76
    fig = plt.figure(figsize=(W * MM, H * MM))
    L, Wd = 0.43, 0.555
    rows_a = [
        ("Submission number, sample", 100.0, "open", "943 (100%)", "Hop 1"),
        ("Submission number, population 2013–2023", 75.05, "diamond", "75% of 15,463,770 reports", ""),
        ("Agrees with source-study attribution", 100 * 913 / N, "dot", "913 (96.8%)", ""),
        ("UDI-DI recorded in DEVICE file", 100 * 446 / N, "dot", "446 (47.3%)", ""),
        ("UDI-DI resolves in GUDID", 100 * 445 / N, "dot", "445 (47.2%)", "Hop 2"),
        ("GUDID names a submission", 100 * 382 / N, "dot", "382 (40.5%)", ""),
        ("Agrees with master record", 100 * 366 / N, "dot", "366 (38.8%)", ""),
        ("Upstream component identified", 0, "cross", "no structured field", "Hop 3"),
    ]
    axa, ysa = dotpanel(fig, [L, 0.17, Wd, 0.80], rows_a)
    for yb in [ysa[3] - 0.5, ysa[6] - 0.5]:
        axa.plot([-102, 135], [yb, yb], color=GUIDE, lw=LW, clip_on=False, zorder=0)
    axa.set_xlabel("Reports (%)", fontsize=FS, color=INK)
    axa.xaxis.set_label_coords(100 / 270, -0.13)
    save(fig, "Fig2_joinability")


def figS1_identity():
    W, H = 180, 52
    fig = plt.figure(figsize=(W * MM, H * MM))
    L, Wd = 0.43, 0.555
    rows_b = [
        ("Designated software-version field (I3)", 0, "cross", "no field in any layout", ""),
        ("No UDI-DI recorded", 100 * 497 / N, "dot", "497 (52.7%)", ""),
        ("Dominant identifier: hardware model", 100 * 250 / N, "dot", "250 (26.5%)", ""),
        ("Other identifiers: could designate a version (I2)", 100 * 196 / N, "dot", "196 (20.8%), upper bound", ""),
    ]
    axb, ysb = dotpanel(fig, [L, 0.26, Wd, 0.70], rows_b)
    axb.plot([-102, 135], [ysb[0] - 0.5, ysb[0] - 0.5], color=GUIDE, lw=LW, clip_on=False, zorder=0)
    axb.set_xlabel("Reports (%)", fontsize=FS, color=INK)
    axb.xaxis.set_label_coords(100 / 270, -0.24)
    save(fig, "FigS1_identity")


# ------------------------------------------------------------------ Supplementary Fig. 1
def figS1():
    W, H = 180, 112
    fig = plt.figure(figsize=(W * MM, H * MM))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.015, 0.97, "Configuration commitment registry: one implementation of the design requirement",
            fontsize=FS, va="top")
    box(ax, 0.015, 0.685, 0.56, 0.235,
        "Node table\nkey: hiding commitment to a manifest (one commitment over per-element\n"
        "commitments: model, prompts, retrieval sources, guardrails, orchestration,\n"
        "interface); assurance grade: declaration, attestation or proof")
    box(ax, 0.015, 0.435, 0.56, 0.20,
        "Edge table\nsigned relations between commitments (composed-of, derived-from);\n"
        "append-only log with verifiable inclusion and consistency")
    box(ax, 0.64, 0.685, 0.345, 0.235, "Conformity query\nis the running manifest in\nthe authorized set?",
        fc=BLUE_L, ec=BLUE)
    box(ax, 0.64, 0.435, 0.345, 0.20, "Surveillance query\nrecursive traversal from an ancestor\nto all registered descendants",
        fc=BLUE_L, ec=BLUE)
    arrow(ax, 0.575, 0.8025, 0.64, 0.8025); arrow(ax, 0.575, 0.535, 0.64, 0.535)
    ax.text(0.015, 0.385, "Connection points to existing systems", fontsize=FS, color=INK, va="center")
    conn = ["MDR DEVICE record:\nupstream-model\nfield (supplies\nhop 3)",
            "UDI and GUDID:\narticle identity;\nversion via the\nproduction identifier",
            "Foundation Model\nMaster File keyed\nto the commitment\n(converse query)",
            "Section 524B SBOM\nor ML-BOM: component\nlist carried into\nevent records"]
    for i, t in enumerate(conn):
        box(ax, 0.015 + i * 0.245, 0.12, 0.225, 0.23, t, fc="#f4f3f0", ec=MUTED)
    ax.text(0.015, 0.07, "The regulator holds commitments and signatures, not model weights or patient data.",
            fontsize=FS, color=INK2, va="center")
    ax.text(0.015, 0.03, "Commitments are salted; access to the edge table is governed because dependency "
            "structure can be commercially sensitive.", fontsize=FS, color=INK2, va="center")
    save(fig, "FigS2_registry")


fig1(); fig2(); figS1_identity(); figS1()
print("figures written:", sorted(os.listdir(OUT)))
