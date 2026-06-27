#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

import pandas as pd


def normalize_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    cols = {c.lower().strip(): c for c in df.columns}

    def pick(*names):
        for n in names:
            if n in cols:
                return cols[n]
        return None

    date_col = pick("date", "time", "timestamp", "datetime")
    open_col = pick("open", "o")
    high_col = pick("high", "h")
    low_col = pick("low", "l")
    close_col = pick("close", "c")
    volume_col = pick("volume", "vol", "v")

    missing = [name for name, col in {
        "open": open_col,
        "high": high_col,
        "low": low_col,
        "close": close_col,
    }.items() if col is None]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    out = pd.DataFrame()
    if date_col:
        out["date"] = pd.to_datetime(df[date_col], errors="coerce")
    else:
        out["date"] = pd.RangeIndex(len(df))

    out["open"] = pd.to_numeric(df[open_col], errors="coerce")
    out["high"] = pd.to_numeric(df[high_col], errors="coerce")
    out["low"] = pd.to_numeric(df[low_col], errors="coerce")
    out["close"] = pd.to_numeric(df[close_col], errors="coerce")
    out["volume"] = pd.to_numeric(df[volume_col], errors="coerce") if volume_col else 0

    out = out.dropna(subset=["open", "high", "low", "close"]).reset_index(drop=True)
    return out


def rsi(series: pd.Series, period: int) -> pd.Series:
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss.replace(0, math.nan)
    return 100 - (100 / (1 + rs))


def roc(series: pd.Series, period: int) -> pd.Series:
    return (series / series.shift(period) - 1) * 100


def momentum(series: pd.Series, period: int) -> pd.Series:
    return series - series.shift(period)


def cci(df: pd.DataFrame, period: int = 20) -> pd.Series:
    tp = (df["high"] + df["low"] + df["close"]) / 3
    sma = tp.rolling(period).mean()
    mad = (tp - sma).abs().rolling(period).mean()
    return (tp - sma) / (0.015 * mad.replace(0, math.nan))


def macd_histogram(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.Series:
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    sig = macd.ewm(span=signal, adjust=False).mean()
    return macd - sig


def stochastic_k(df: pd.DataFrame, period: int = 14) -> pd.Series:
    lowest_low = df["low"].rolling(period).min()
    highest_high = df["high"].rolling(period).max()
    return ((df["close"] - lowest_low) / (highest_high - lowest_low).replace(0, math.nan)) * 100


def williams_r(df: pd.DataFrame, period: int = 14) -> pd.Series:
    highest_high = df["high"].rolling(period).max()
    lowest_low = df["low"].rolling(period).min()
    return -100 * ((highest_high - df["close"]) / (highest_high - lowest_low).replace(0, math.nan))


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    prev_close = df["close"].shift(1)
    tr = pd.concat([
        df["high"] - df["low"],
        (df["high"] - prev_close).abs(),
        (df["low"] - prev_close).abs(),
    ], axis=1).max(axis=1)
    return tr.rolling(period).mean()


def detector_values(df: pd.DataFrame, detector: str) -> pd.Series:
    close = df["close"]
    if detector == "RSI7":
        return rsi(close, 7)
    if detector == "RSI14":
        return rsi(close, 14)
    if detector == "RSI21":
        return rsi(close, 21)
    if detector == "ROC5":
        return roc(close, 5)
    if detector == "ROC10":
        return roc(close, 10)
    if detector == "ROC14":
        return roc(close, 14)
    if detector == "MOM5":
        return momentum(close, 5)
    if detector == "MOM10":
        return momentum(close, 10)
    if detector == "MOM14":
        return momentum(close, 14)
    if detector == "CCI20":
        return cci(df, 20)
    if detector == "MACD_HIST":
        return macd_histogram(close)
    if detector == "STOCH14":
        return stochastic_k(df, 14)
    if detector == "WILLIAMS14":
        return williams_r(df, 14)
    if detector == "PRICE_BODY":
        return (df["close"] - df["open"]).abs()
    if detector == "PRICE_BODY_ATR":
        return (df["close"] - df["open"]).abs() / atr(df, 14).replace(0, math.nan)
    raise ValueError(f"Unknown detector: {detector}")


def opposite_candle_index(df: pd.DataFrame, momentum_idx: int, direction: str) -> int | None:
    if direction == "bullish":
        # آخر شمعة هابطة قبل شمعة الزخم
        for i in range(momentum_idx - 1, -1, -1):
            if df.loc[i, "close"] < df.loc[i, "open"]:
                return i
    else:
        # آخر شمعة صاعدة قبل شمعة الزخم
        for i in range(momentum_idx - 1, -1, -1):
            if df.loc[i, "close"] > df.loc[i, "open"]:
                return i
    return None


def ref_price(df: pd.DataFrame, idx: int, method: str) -> float:
    if method == "open":
        return float(df.loc[idx, "open"])
    if method == "close":
        return float(df.loc[idx, "close"])
    if method == "midpoint":
        return float((df.loc[idx, "open"] + df.loc[idx, "close"]) / 2)
    if method == "high":
        return float(df.loc[idx, "high"])
    if method == "low":
        return float(df.loc[idx, "low"])
    raise ValueError(method)


def evaluate_nmp(df: pd.DataFrame, nmp_idx: int, nmp_price: float, direction: str, lookahead: int = 30) -> dict:
    end = min(len(df), nmp_idx + lookahead + 1)
    future = df.iloc[nmp_idx + 1:end]

    if future.empty:
        return {"touch": 0, "bounce": 0, "false_break": 0, "max_reaction_pct": 0}

    tolerance = max(float(df.loc[nmp_idx, "close"]) * 0.002, 1e-9)

    touched = ((future["low"] <= nmp_price + tolerance) & (future["high"] >= nmp_price - tolerance)).any()

    if direction == "bullish":
        max_reaction = (future["high"].max() - nmp_price) / nmp_price * 100
        false_break = (future["close"] < nmp_price - tolerance).any()
    else:
        max_reaction = (nmp_price - future["low"].min()) / nmp_price * 100
        false_break = (future["close"] > nmp_price + tolerance).any()

    bounce = bool(touched and max_reaction > 0.5)

    return {
        "touch": int(bool(touched)),
        "bounce": int(bounce),
        "false_break": int(bool(false_break)),
        "max_reaction_pct": round(float(max_reaction), 4),
    }


def run_file(path: Path, outdir: Path):
    df_raw = pd.read_csv(path)
    df = normalize_ohlcv(df_raw)

    detectors = [
        "RSI7", "RSI14", "RSI21",
        "ROC5", "ROC10", "ROC14",
        "MOM5", "MOM10", "MOM14",
        "CCI20",
        "MACD_HIST", "STOCH14", "WILLIAMS14",
        "PRICE_BODY", "PRICE_BODY_ATR",
    ]
    refs = ["open", "close", "midpoint", "high", "low"]
    directions = ["bullish", "bearish"]

    rows = []

    for detector in detectors:
        values = detector_values(df, detector)
        for direction in directions:
            if direction == "bullish":
                idx = values.idxmax()
            else:
                idx = values.idxmin()

            if pd.isna(idx):
                continue

            idx = int(idx)
            opp_idx = opposite_candle_index(df, idx, direction)
            if opp_idx is None:
                continue

            for rp in refs:
                price = ref_price(df, opp_idx, rp)
                score = evaluate_nmp(df, opp_idx, price, direction)
                rows.append({
                    "file": path.name,
                    "detector": detector,
                    "direction": direction,
                    "momentum_index": idx,
                    "opposite_index": opp_idx,
                    "reference_price_type": rp,
                    "opposite_candle_rule": "last_opposite_candle_before_momentum",
                    "nmp_formula": f"{detector} + Opposite Candle + {rp}",
                    "nmp_price": price,
                    **score,
                })

    result = pd.DataFrame(rows)
    out_csv = outdir / f"{path.stem}_nmp_lab_results.csv"
    result.to_csv(out_csv, index=False)

    summary = (
        result
        .groupby(["detector", "reference_price_type"], as_index=False)
        .agg(
            tests=("file", "count"),
            touch_rate=("touch", "mean"),
            bounce_rate=("bounce", "mean"),
            false_break_rate=("false_break", "mean"),
            avg_reaction_pct=("max_reaction_pct", "mean"),
        )
    )

    summary["score"] = (
        summary["touch_rate"] * 0.30 +
        summary["bounce_rate"] * 0.35 -
        summary["false_break_rate"] * 0.20 +
        (summary["avg_reaction_pct"].clip(upper=5) / 5) * 0.15
    )

    summary = summary.sort_values("score", ascending=False)
    out_summary = outdir / f"{path.stem}_nmp_lab_summary.csv"
    summary.to_csv(out_summary, index=False)

    return out_csv, out_summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    outdir = Path(args.out_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    files = sorted(data_dir.glob("*.csv"))
    manifest = []

    for f in files:
        try:
            result, summary = run_file(f, outdir)
            manifest.append({"file": str(f), "result": str(result), "summary": str(summary), "ok": True})
        except Exception as e:
            manifest.append({"file": str(f), "ok": False, "error": str(e)})

    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
