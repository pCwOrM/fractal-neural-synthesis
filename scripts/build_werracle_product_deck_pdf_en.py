import os
import shutil
from playwright.sync_api import sync_playwright

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>WERRACLE: Zero-Storage On-Chain AI Decision Oracle - Investor Pitch Deck</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    @page {
      size: 1920px 1080px;
      margin: 0;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: #070a12;
      color: #f8fafc;
      -webkit-font-smoothing: antialiased;
    }

    .slide {
      width: 1920px;
      height: 1080px;
      page-break-after: always;
      position: relative;
      overflow: hidden;
      background: radial-gradient(circle at 85% 15%, rgba(56, 189, 248, 0.08) 0%, transparent 45%),
                  radial-gradient(circle at 15% 85%, rgba(16, 185, 129, 0.06) 0%, transparent 45%),
                  #070a12;
      padding: 70px 100px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }

    .header-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 22px;
    }

    .brand-wrap {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .brand-badge {
      background: linear-gradient(135deg, #38bdf8 0%, #10b981 100%);
      color: #070a12;
      font-weight: 800;
      font-size: 17px;
      padding: 6px 16px;
      border-radius: 8px;
      letter-spacing: 0.05em;
    }

    .brand-title {
      font-size: 21px;
      font-weight: 700;
      letter-spacing: -0.02em;
      color: #e2e8f0;
    }

    .category-tag {
      font-family: 'JetBrains Mono', monospace;
      font-size: 14px;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      background: rgba(255, 255, 255, 0.04);
      padding: 7px 16px;
      border-radius: 20px;
      border: 1px solid rgba(255, 255, 255, 0.08);
    }

    .footer-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding-top: 20px;
      font-size: 14px;
      color: #64748b;
    }

    .content-area {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      margin: 35px 0;
    }

    .slide-title {
      font-size: 46px;
      font-weight: 800;
      letter-spacing: -0.03em;
      line-height: 1.15;
      margin-bottom: 12px;
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .slide-subtitle {
      font-size: 21px;
      color: #94a3b8;
      margin-bottom: 35px;
      max-width: 1400px;
      line-height: 1.45;
    }

    .grid-2 {
      display: grid;
      grid-template-columns: 1.1fr 0.9fr;
      gap: 50px;
      align-items: center;
    }

    .grid-3 {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 30px;
    }

    .grid-4 {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 24px;
    }

    .card {
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 18px;
      padding: 32px;
      box-shadow: 0 16px 36px rgba(0, 0, 0, 0.35);
      backdrop-filter: blur(12px);
    }

    .card-highlight {
      border: 1px solid rgba(56, 189, 248, 0.35);
      background: rgba(15, 23, 42, 0.85);
    }

    .card-accent-green {
      border: 1px solid rgba(16, 185, 129, 0.35);
    }

    .card-accent-purple {
      border: 1px solid rgba(168, 85, 247, 0.35);
    }

    .card-title {
      font-size: 22px;
      font-weight: 700;
      margin-bottom: 14px;
      color: #f1f5f9;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .card-desc {
      font-size: 16px;
      color: #94a3b8;
      line-height: 1.6;
    }

    .metric-hero {
      font-family: 'JetBrains Mono', monospace;
      font-size: 52px;
      font-weight: 800;
      line-height: 1;
      margin-bottom: 8px;
    }

    .metric-sub {
      font-size: 15px;
      color: #94a3b8;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      font-weight: 600;
    }

    .color-cyan { color: #38bdf8; }
    .color-green { color: #34d399; }
    .color-purple { color: #c084fc; }
    .color-rose { color: #fb7185; }
    .color-gold { color: #fbbf24; }

    .chart-container {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 20px;
      padding: 16px;
      display: flex;
      justify-content: center;
      align-items: center;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }

    .chart-container img {
      max-width: 100%;
      height: auto;
      border-radius: 12px;
    }

    table.data-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 17px;
      margin-top: 10px;
    }

    table.data-table th {
      background: rgba(30, 41, 59, 0.7);
      color: #38bdf8;
      padding: 16px 20px;
      text-align: left;
      font-weight: 700;
      border-bottom: 2px solid rgba(56, 189, 248, 0.2);
    }

    table.data-table td {
      padding: 18px 20px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      color: #cbd5e1;
    }

    table.data-table tr:hover td {
      background: rgba(255, 255, 255, 0.02);
    }

    .pill-list {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 16px;
    }

    .pill-item {
      font-family: 'JetBrains Mono', monospace;
      font-size: 13px;
      padding: 6px 14px;
      border-radius: 20px;
      background: rgba(56, 189, 248, 0.1);
      color: #38bdf8;
      border: 1px solid rgba(56, 189, 248, 0.2);
    }

    .pill-item.green {
      background: rgba(16, 185, 129, 0.1);
      color: #34d399;
      border-color: rgba(16, 185, 129, 0.2);
    }

    .pill-item.purple {
      background: rgba(168, 85, 247, 0.1);
      color: #c084fc;
      border-color: rgba(168, 85, 247, 0.2);
    }

    /* Cover specific styling */
    .cover-title {
      font-size: 68px;
      font-weight: 800;
      letter-spacing: -0.04em;
      line-height: 1.08;
      margin-bottom: 24px;
      background: linear-gradient(135deg, #ffffff 10%, #38bdf8 50%, #34d399 90%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      max-width: 1400px;
    }

    .cover-sub {
      font-size: 26px;
      color: #94a3b8;
      line-height: 1.45;
      max-width: 1300px;
      margin-bottom: 50px;
    }

    .portal-badges {
      display: flex;
      gap: 16px;
      margin-top: 25px;
    }

    .portal-badge {
      display: flex;
      align-items: center;
      gap: 10px;
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 12px;
      padding: 12px 20px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 15px;
      font-weight: 600;
    }

    .portal-badge .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }
  </style>
</head>
<body>

  <!-- SLIDE 1: COVER -->
  <div class="slide">
    <div class="header-bar">
      <div class="brand-wrap">
        <span class="brand-badge">WERRACLE</span>
        <span class="brand-title">Zero-Storage On-Chain AI Decision Oracle</span>
      </div>
      <div class="category-tag">SEED ROUND &bull; $1.5M TARGET &bull; OCT 2026</div>
    </div>

    <div class="content-area">
      <div class="cover-title">Sub-Cent Intra-Block Reflex Intelligence & Real-Time Risk Defense for Web3</div>
      <div class="cover-sub">
        The first production-grade On-Chain AI Oracle executing directly inside EVM and Starknet smart contracts at ~20.7k gas with zero neural storage footprints, powered by Lean 4 machine-verified procedural escape dynamics.
      </div>

      <div class="grid-4" style="margin-top: 20px;">
        <div class="card card-highlight">
          <div class="metric-hero color-cyan">~20.7k</div>
          <div class="metric-sub">EVM Execution Gas</div>
          <p style="font-size: 14px; color: #94a3b8; margin-top: 8px;">Sub-cent cost (<$0.001) per intra-block classification</p>
        </div>
        <div class="card card-accent-green">
          <div class="metric-hero color-green">0 Bytes</div>
          <div class="metric-sub">On-Chain Model Footprint</div>
          <p style="font-size: 14px; color: #94a3b8; margin-top: 8px;">Zero VRAM/DRAM weights. Single bytes32 storage slot</p>
        </div>
        <div class="card card-accent-purple">
          <div class="metric-hero color-purple">&lt; 12 ms</div>
          <div class="metric-sub">Intra-Block Latency</div>
          <p style="font-size: 14px; color: #94a3b8; margin-top: 8px;">Synchronous execution halts flash-loans mid-transaction</p>
        </div>
        <div class="card">
          <div class="metric-hero color-gold">$2.20B+</div>
          <div class="metric-sub">Active Debt Surveilled</div>
          <p style="font-size: 14px; color: #94a3b8; margin-top: 8px;">Live across 38 verified Morpho, Aave & Euler markets</p>
        </div>
      </div>

      <div class="portal-badges">
        <div class="portal-badge"><span class="dot" style="background:#38bdf8;"></span> werracle.io &bull; On-Chain Protocol & Hooks</div>
        <div class="portal-badge"><span class="dot" style="background:#34d399;"></span> radar.werracle.com &bull; B2B Risk Telemetry DaaS</div>
        <div class="portal-badge"><span class="dot" style="background:#fbbf24;"></span> werracle.com &bull; Enterprise & Curator SLA</div>
        <div class="portal-badge"><span class="dot" style="background:#c084fc;"></span> werr.io &bull; Lean 4 Formal Proofs & Academic</div>
      </div>
    </div>

    <div class="footer-bar">
      <span>ITOUCH BİLİŞİM SİSTEMLERİ MÜH. DAN. SAN. VE TİC. LTD. ŞTİ. &bull; Cukurova University Science Park</span>
      <span>Confidential &bull; Seed Investment Pitch Deck</span>
      <span>Slide 01 / 14</span>
    </div>
  </div>

  <!-- SLIDE 2: THE PROBLEM -->
  <div class="slide">
    <div class="header-bar">
      <div class="brand-wrap">
        <span class="brand-badge">WERRACLE</span>
        <span class="brand-title">Market Need & Problem Statement</span>
      </div>
      <div class="category-tag">THE $3.8B+ LATENCY GAP</div>
    </div>

    <div class="content-area">
      <div class="slide-title">DeFi Smart Contracts Are Static & Blind to Intra-Block Exploits</div>
      <div class="slide-subtitle">
        Decentralized protocols handle billions in high-velocity capital with static state rules. Existing solutions fail to provide real-time, intra-block decision intelligence.
      </div>

      <div class="grid-3">
        <div class="card">
          <div class="card-title color-rose">
            <span style="font-size: 26px;">⚠️</span> The Intra-Block Exploit Gap
          </div>
          <div class="card-desc">
            Atomic flash loans, sandwich attacks, and price-oracle front-running happen within a single block before state finalization. Over <b>$3.8B has been lost</b> to atomic exploits because contracts cannot react dynamically mid-execution.
          </div>
          <div class="pill-list">
            <span class="pill-item">Flash Loan Drains</span>
            <span class="pill-item">Toxic MEV Sandwiching</span>
            <span class="pill-item">Loss Versus Rebalancing (LVR)</span>
          </div>
        </div>

        <div class="card">
          <div class="card-title color-rose">
            <span style="font-size: 26px;">⏱️</span> Asynchronous Oracle Delay
          </div>
          <div class="card-desc">
            Traditional push/pull oracles (Chainlink, Pyth) update once every block or cross-chain roundtrip (seconds to minutes). They are completely blind to transactional state changes occurring inside the same block and callstack.
          </div>
          <div class="pill-list">
            <span class="pill-item">Heartbeat Thresholds</span>
            <span class="pill-item">Price Feed Stale Windows</span>
            <span class="pill-item">Zero Intra-Block Visibility</span>
          </div>
        </div>

        <div class="card">
          <div class="card-title color-rose">
            <span style="font-size: 26px;">🛑</span> ZK-ML & Storage Bottlenecks
          </div>
          <div class="card-desc">
            Zero-Knowledge Machine Learning (ZK-ML) is too slow and expensive for synchronous defense. Proof generation requires 15–60 seconds, and on-chain verification consumes 350k–1M+ gas, making intra-block circuit breaking impossible.
          </div>
          <div class="pill-list">
            <span class="pill-item">Heavy Off-Chain Provers</span>
            <span class="pill-item">Massive Gas Overhead</span>
            <span class="pill-item">Storage/DRAM Exhaustion</span>
          </div>
        </div>
      </div>

      <div class="card card-highlight" style="margin-top: 30px;">
        <div style="font-size: 18px; color: #cbd5e1;">
          <b>The Institutional Dilemma:</b> Vault curators (managing $10B+ TVL in Morpho, Aave, and Euler) fly completely blind without granular, real-time borrower liquidation telemetry and automated, sub-cent circuit breakers.
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <span>Werracle: Procedural On-Chain AI</span>
      <span>Confidential &bull; Seed Investment Pitch Deck</span>
      <span>Slide 02 / 14</span>
    </div>
  </div>

  <!-- SLIDE 3: THE BREAKTHROUGH -->
  <div class="slide">
    <div class="header-bar">
      <div class="brand-wrap">
        <span class="brand-badge">WERRACLE</span>
        <span class="brand-title">Proprietary Technology & Architecture</span>
      </div>
      <div class="category-tag">PATENT PENDING &bull; TR 2026/016285</div>
    </div>

    <div class="content-area">
      <div class="slide-title">Procedural Escape Dynamics: AI Reflex Without Heavy Weights</div>
      <div class="slide-subtitle">
        Eliminating the Von Neumann storage bottleneck: synthesizing real-time decision surfaces from deterministic polynomial trajectories (<span style="font-family:'JetBrains Mono';">z<sub>n+1</sub> = z<sub>n</sub><sup>2</sup> + c</span>) in a single storage slot.
      </div>

      <div class="grid-2">
        <div style="display: flex; flex-direction: column; gap: 20px;">
          <div class="card card-highlight">
            <div class="card-title color-cyan">Zero-Storage Synaptic Synthesis</div>
            <div class="card-desc">
              Instead of loading megabytes of static weight matrices into memory, Werracle dynamically computes high-dimensional decision boundaries using procedural Mandelbrot escape velocities. Decision model footprint is strictly <b>0 Bytes on-chain</b>.
            </div>
          </div>

          <div class="card card-accent-green">
            <div class="card-title color-green">Single Packed 32-Byte Slot (bytes32 / felt252)</div>
            <div class="card-desc">
              The entire runtime state—seed coordinates, zoom exponent, nonce, escape threshold, sensitivity mode, and emergency breaker flag—fits compactly into a single storage slot. Maximum read/write efficiency on EVM and Starknet Cairo.
            </div>
          </div>

          <div class="card card-accent-purple">
            <div class="card-title color-purple">Sub-12ms Synchronous Execution</div>
            <div class="card-desc">
              Executes within the exact same EVM transaction callstack (<span style="font-family:'JetBrains Mono'; color:#38bdf8;">decideNoul</span> consuming 20.7k gas). If abnormal price divergence or liquidity drain is detected, the transaction reverts atomically before funds exit.
            </div>
          </div>
        </div>

        <div class="card" style="padding: 30px; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <div style="font-size: 20px; font-weight: 700; color: #f8fafc; margin-bottom: 15px;">Key Technical Specifications</div>
            <table class="data-table">
              <tr>
                <td><b>Gas Consumption</b></td>
                <td style="color:#38bdf8; font-weight:700;">20,700 Gas (solc 0.8.20)</td>
              </tr>
              <tr>
                <td><b>Starknet CairoVM</b></td>
                <td style="color:#34d399; font-weight:700;">~1,420 Steps (STARK-Native)</td>
              </tr>
              <tr>
                <td><b>Storage Footprint</b></td>
                <td style="color:#c084fc; font-weight:700;">1 x bytes32 (EVM) / felt252 (Cairo)</td>
              </tr>
              <tr>
                <td><b>Fixed-Point Precision</b></td>
                <td style="color:#f8fafc; font-weight:700;">Q16.16 Arithmetic (No Overflow)</td>
              </tr>
              <tr>
                <td><b>Execution Speed</b></td>
                <td style="color:#fbbf24; font-weight:700;">9.3 ms Engine / &lt;12 ms RPC</td>
              </tr>
              <tr>
                <td><b>Patent Application</b></td>
                <td style="color:#fb7185; font-weight:700;">TÜRKPATENT TR 2026/016285</td>
              </tr>
            </table>
          </div>
          <div style="background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 15px; margin-top: 20px; font-size: 14px; color: #cbd5e1;">
            <b>Formal Verification Guarantee:</b> 100% of mathematical escape bounds verified in Lean 4 without axioms (<span style="font-family:'JetBrains Mono';">zero sorry</span>). Provably safe against infinite execution loops.
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <span>Werracle Core Engine: Procedural Escape Dynamics</span>
      <span>Confidential &bull; Seed Investment Pitch Deck</span>
      <span>Slide 03 / 14</span>
    </div>
  </div>

  <!-- SLIDE 4: BENCHMARK & COMPARISON -->
  <div class="slide">
    <div class="header-bar">
      <div class="brand-wrap">
        <span class="brand-badge">WERRACLE</span>
        <span class="brand-title">Competitive Benchmarks & Gas Profiling</span>
      </div>
      <div class="category-tag">1000x FASTER &bull; 15x CHEAPER THAN ZK-ML</div>
    </div>

    <div class="content-area">
      <div class="slide-title">Unrivaled Asymmetry in Cost, Latency & Storage</div>
      <div class="slide-subtitle">
        Empirical comparison across EVM execution gas and decision latency demonstrates why Werracle is the only viable intra-block defense engine for smart contracts.
      </div>

      <div class="grid-2">
        <div class="chart-container">
          <img src="chart_latency_gas_comparison_en.png" alt="Execution Gas & Latency Comparison">
        </div>

        <div style="display: flex; flex-direction: column; gap: 18px;">
          <div class="card card-highlight">
            <div class="card-title color-cyan">15x to 25x Lower Gas than ZK-ML</div>
            <div class="card-desc">
              ZK-ML verifiers (Modulus, EZKL) consume <b>350k to 1,200k gas</b> per inference check, making active per-swap or per-loan checks economically prohibitive on mainnets. Werracle uses only <b>20.7k gas</b>.
            </div>
          </div>

          <div class="card card-accent-green">
            <div class="card-title color-green">1000x Faster Latency (<12ms vs 35s)</div>
            <div class="card-desc">
              ZK-ML provers require 15 to 60 seconds of off-chain proving before publishing an on-chain receipt. By that time, flash-loan exploiters have already completed their arbitrage and transferred funds off-chain.
            </div>
          </div>

          <div class="card card-accent-purple">
            <div class="card-title color-purple">Synchronous Intra-Block Execution</div>
            <div class="card-desc">
              Unlike push/pull oracles (Chainlink/Pyth) that require cross-block asynchronous updates, Werracle sits inside the contract’s internal callstack, evaluating liquidity and price volatility <b>before</b> funds move.
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <span>Benchmarked with solc 0.8.20 and Cairo 2.8+</span>
      <span>Confidential &bull; Seed Investment Pitch Deck</span>
      <span>Slide 04 / 14</span>
    </div>
  </div>

  <!-- SLIDE 5: PILLAR 1 - WERRACLE.IO -->
  <div class="slide">
    <div class="header-bar">
      <div class="brand-wrap">
        <span class="brand-badge">WERRACLE</span>
        <span class="brand-title">Product Pillar 1: werracle.io</span>
      </div>
      <div class="category-tag">ON-CHAIN PROTOCOL & HOOKS</div>
    </div>

    <div class="content-area">
      <div class="slide-title">werracle.io: The Web3 Protocol & Autonomous Hook Layer</div>
      <div class="slide-subtitle">
        Providing ready-to-deploy smart contract hooks, flash-loan circuit breakers, and AMM dynamic fee modules across major EVM chains, Starknet, and NEAR.
      </div>

      <div class="grid-3">
        <div class="card card-highlight">
          <div class="card-title color-cyan">
            <span>🛡️</span> Intra-Block Circuit Breakers
          </div>
          <div class="card-desc">
            Embeds directly into lending pools, liquid staking vaults, and collateral managers. Synchronously samples volatility in the execution transaction, automatically halting hostile flash-loan cascades before debt settlement.
          </div>
          <div class="pill-list" style="margin-top:20px;">
            <span class="pill-item">Morpho Vault Wrap</span>
            <span class="pill-item">Aave v3 Protection</span>
            <span class="pill-item">Atomic Reverts</span>
          </div>
        </div>

        <div class="card card-accent-green">
          <div class="card-title color-green">
            <span>⚡</span> Uniswap v4 Dynamic Fee Hook
          </div>
          <div class="card-desc">
            Intercepts incoming swaps via <span style="font-family:'JetBrains Mono'; font-size:14px; color:#34d399;">beforeSwap</span>. Dynamically adjusts liquidity pool fees during abrupt volatility surges, mitigating toxic MEV flow and protecting passive LPs against Loss Versus Rebalancing (LVR).
          </div>
          <div class="pill-list" style="margin-top:20px;">
            <span class="pill-item">Uniswap v4 Hook</span>
            <span class="pill-item">LVR Mitigation</span>
            <span class="pill-item">LP Fee Capture</span>
          </div>
        </div>

        <div class="card card-accent-purple">
          <div class="card-title color-purple">
            <span>🌐</span> Multi-Chain Architecture
          </div>
          <div class="card-desc">
            Production contracts verified across multiple virtual machines:
            <ul style="margin-left: 20px; margin-top: 10px; font-size: 14.5px; color:#cbd5e1; line-height: 1.6;">
              <li><b>EVM:</b> Live on Aurora testnet (<span style="font-family:'JetBrains Mono'; font-size:12px;">0x1d7Ae9...</span>)</li>
              <li><b>Starknet:</b> Cairo 2.8+ Sierra (Ekubo extension)</li>
              <li><b>NEAR:</b> Toxic intent filtering and routing</li>
            </ul>
          </div>
          <div class="pill-list" style="margin-top:15px;">
            <span class="pill-item">Solidity 0.8.20</span>
            <span class="pill-item">Cairo 2.8 Sierra</span>
            <span class="pill-item">NEAR Intents</span>
          </div>
        </div>
      </div>

      <div class="card" style="margin-top: 25px; padding: 22px 30px; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <span style="font-size: 18px; font-weight: 700; color: #f8fafc;">Interactive Browser Simulator & Live Contract Explorer:</span>
          <span style="font-size: 16px; color: #94a3b8; margin-left: 15px;">Developers can test and verify decision boundaries in browser with 100% bit-exact equivalence to deployed EVM bytecode.</span>
        </div>
        <span class="category-tag" style="color: #38bdf8; border-color: rgba(56, 189, 248, 0.3);">werracle.io/#simulator</span>
      </div>
    </div>

    <div class="footer-bar">
      <span>werracle.io &bull; Web3 Protocol & Smart Contract Defense</span>
      <span>Confidential &bull; Seed Investment Pitch Deck</span>
      <span>Slide 05 / 14</span>
    </div>
  </div>

  <!-- SLIDE 6: PILLAR 2 - RADAR.WERRACLE.COM -->
  <div class="slide">
    <div class="header-bar">
      <div class="brand-wrap">
        <span class="brand-badge">WERRACLE</span>
        <span class="brand-title">Product Pillar 2: radar.werracle.com</span>
      </div>
      <div class="category-tag">REAL-TIME RISK TELEMETRY & B2B DAAS</div>
    </div>

    <div class="content-area">
      <div class="slide-title">radar.werracle.com: Empirical Liquidation & OEV Observatory</div>
      <div class="slide-subtitle">
        Surveilling over $2.20 Billion in lending debt across Morpho, Aave, and Euler with automated bad debt tracking, SVR verification, and programmatic USDC API key delivery.
      </div>

      <div class="grid-4" style="margin-bottom: 25px;">
        <div class="card">
          <div class="metric-hero color-cyan">38</div>
          <div class="metric-sub">Verified Lending Markets</div>
          <p style="font-size: 14px; color: #94a3b8; margin-top: 8px;">Morpho Blue, Aave v3, Euler v2 (45 unlisted/synthetic spam markets isolated)</p>
        </div>
        <div class="card">
          <div class="metric-hero color-green">$2.20B</div>
          <div class="metric-sub">Clean Borrow Debt Tracked</div>
          <p style="font-size: 14px; color: #94a3b8; margin-top: 8px;">68,735 active borrower positions monitored in real-time</p>
        </div>
        <div class="card">
          <div class="metric-hero color-gold">94.38%</div>
          <div class="metric-sub">SVR Value Recaptured</div>
          <p style="font-size: 14px; color: #94a3b8; margin-top: 8px;">$179.8k of $190.5k gross incentive returned to depositors on Base</p>
        </div>
        <div class="card">
          <div class="metric-hero color-purple">95.94%</div>
          <div class="metric-sub">Top 22 L1 Fat-Tail Leak</div>
          <p style="font-size: 14px; color: #94a3b8; margin-top: 8px;">22 transactions account for $351.3k of $366.1k builder bribes on L1</p>
        </div>
      </div>

      <div class="grid-2">
        <div class="card card-highlight">
          <div class="card-title color-cyan">Autonomous B2B Micro-Settlement (USDC on Base)</div>
          <div class="card-desc">
            Developers and funds subscribe seamlessly using native USDC on Base. Zero manual invoicing: on-chain transactions verify ECDSA signatures, deliver cryptographically bound API keys, and enforce atomic rate limits across distributed Uvicorn workers.
          </div>
          <div class="pill-list">
            <span class="pill-item">Developer ($149/mo)</span>
            <span class="pill-item">Professional ($499/mo)</span>
            <span class="pill-item">Institutional ($2,499/mo)</span>
          </div>
        </div>

        <div class="card card-accent-green">
          <div class="card-title color-green">Continuous Macro Risk Classification</div>
          <div class="card-desc">
            Categorizes live positions into <span style="color:#fb7185; font-weight:700;">Bad Debt (HF &lt; 0.95)</span> and <span style="color:#fbbf24; font-weight:700;">Near-Liquidation Distress (0.95 &le; HF &lt; 1.10)</span>. Provides DeFi protocols and risk curators with immediate warning flags before systemic insolvency occurs.
          </div>
          <div class="pill-list">
            <span class="pill-item">Instant Websocket Alerts</span>
            <span class="pill-item">Curator Vault Sync</span>
            <span class="pill-item">Historical Trace Replays</span>
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <span>radar.werracle.com &bull; Live Telemetry API: api.werracle.com/v1/radar</span>
      <span>Confidential &bull; Seed Investment Pitch Deck</span>
      <span>Slide 06 / 14</span>
    </div>
  </div>

  <!-- SLIDE 7: PILLAR 3 - WERRACLE.COM -->
  <div class="slide">
    <div class="header-bar">
      <div class="brand-wrap">
        <span class="brand-badge">WERRACLE</span>
        <span class="brand-title">Product Pillar 3: werracle.com</span>
      </div>
      <div class="category-tag">ENTERPRISE, CURATOR SLA & LICENSING</div>
    </div>

    <div class="content-area">
      <div class="slide-title">werracle.com: Enterprise Licensing & Institutional Curator SLA</div>
      <div class="slide-subtitle">
        Providing tier-1 vault risk curators and institutional lending protocols with dedicated collateral stress simulation engines and custom fractal seed models.
      </div>

      <div class="grid-3">
        <div class="card card-highlight">
          <div class="card-title color-cyan">
            <span>🏛️</span> Vault Curator Stress Modeling
          </div>
          <div class="card-desc">
            Tailored analytics engine built for premier risk managers: <b>Steakhouse Financial, Gauntlet, and Re7 Capital</b>. Dynamically simulates black-swan collateral shocks (0% to -30%) across specific vault allocations to predict bad debt exposure and liquidation premiums.
          </div>
          <div class="pill-list" style="margin-top:15px;">
            <span class="pill-item">Steakhouse USDC Vault</span>
            <span class="pill-item">Gauntlet Prime Core</span>
            <span class="pill-item">Re7 WETH Morpho</span>
          </div>
        </div>

        <div class="card card-accent-green">
          <div class="card-title color-green">
            <span>🔑</span> Custom Institutional Seed Synthesis
          </div>
          <div class="card-desc">
            Institutional subnets, permissioned rollups, and private liquidity pools require specialized risk sensitivity parameters. We formulate, calibrate, and cryptographically seal custom fractal seeds matching specific real-world asset (RWA) and institutional risk profiles.
          </div>
          <div class="pill-list" style="margin-top:15px;">
            <span class="pill-item">RWA Debt Parameters</span>
            <span class="pill-item">Institutional Subnets</span>
            <span class="pill-item">Private Oracles</span>
          </div>
        </div>

        <div class="card card-accent-purple">
          <div class="card-title color-purple">
            <span>📜</span> Business Source License (BSL 1.1)
          </div>
          <div class="card-desc">
            Core execution intellectual property is protected under BSL 1.1 with a guaranteed transition date to <b>Apache 2.0 on 2030-01-01</b>. Ensures proprietary monetization during commercialization while providing full public transparency and verifiable trust to the ecosystem.
          </div>
          <div class="pill-list" style="margin-top:15px;">
            <span class="pill-item">BSL 1.1 Commercial</span>
            <span class="pill-item">Change Date 2030-01-01</span>
            <span class="pill-item">Apache 2.0 Transition</span>
          </div>
        </div>
      </div>

      <div class="card" style="margin-top: 25px; padding: 22px 30px;">
        <div style="font-size: 17px; color: #cbd5e1; line-height: 1.6;">
          <b>Active Pilot Engagement:</b> Dedicated 30-day evaluation keys are currently active in production for Steakhouse Financial, Gauntlet, and Re7 Capital (<span style="font-family:'JetBrains Mono'; color:#38bdf8;">/v1/radar/curator/steakhouse</span>). Modeling shows Steakhouse's worst-case TVL loss under a severe 20% collateral flash crash is contained to just <b>0.13% of TVL</b> ($146k).
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <span>werracle.com &bull; Enterprise Headquarters & Commercial Hub</span>
      <span>Confidential &bull; Seed Investment Pitch Deck</span>
      <span>Slide 07 / 14</span>
    </div>
  </div>

  <!-- SLIDE 8: UNIFIED PRODUCT FLYWHEEL -->
  <div class="slide">
    <div class="header-bar">
      <div class="brand-wrap">
        <span class="brand-badge">WERRACLE</span>
        <span class="brand-title">Ecosystem Synergy & The Flywheel</span>
      </div>
      <div class="category-tag">END-TO-END DEFENSE ARCHITECTURE</div>
    </div>

    <div class="content-area">
      <div class="slide-title">The Unified Flywheel: How Every Portal Reinforces Value</div>
      <div class="slide-subtitle">
        Telemetry feeds the on-chain hooks; on-chain volume drives enterprise SLA contracts; formal proofs guarantee protocol trust.
      </div>

      <div class="grid-2">
        <div class="chart-container">
          <img src="chart_werracle_ecosystem_en.png" alt="Unified Werracle Product Stack">
        </div>

        <div style="display: flex; flex-direction: column; gap: 20px;">
          <div class="card card-highlight">
            <div class="card-title color-cyan">1. Telemetry Ingestion (radar.werracle.com)</div>
            <div class="card-desc">
              Continuous live surveillance over $2.20B+ in debt provides the real-time volatility indices and liquidation risk signals required to tune on-chain circuit breakers.
            </div>
          </div>

          <div class="card card-accent-green">
            <div class="card-title color-green">2. On-Chain Reflex Execution (werracle.io)</div>
            <div class="card-desc">
              Protocol hooks execute within the transaction callback at 20.7k gas, halting toxic flow, collecting dynamic AMM swap fees, and preventing multi-million dollar flash-loan drain.
            </div>
          </div>

          <div class="card card-accent-purple">
            <div class="card-title color-purple">3. Enterprise Monetization (werracle.com)</div>
            <div class="card-desc">
              Institutional curators and DeFi protocols convert into high-value enterprise SLA and custom seed licensing clients, driving sustainable ARR and long-term moat.
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <span>Synergistic Multi-Product Defensibility</span>
      <span>Confidential &bull; Seed Investment Pitch Deck</span>
      <span>Slide 08 / 14</span>
    </div>
  </div>

  <!-- SLIDE 9: FORMAL PROOFS & ACADEMIC -->
  <div class="slide">
    <div class="header-bar">
      <div class="brand-wrap">
        <span class="brand-badge">WERRACLE</span>
        <span class="brand-title">Academic Foundation & Lean 4 Proofs</span>
      </div>
      <div class="category-tag">ZERO AXIOMS &bull; 40 THEOREMS &bull; ZERO SORRY</div>
    </div>

    <div class="content-area">
      <div class="slide-title">Mathematically Proven Safety: Eliminating Smart Contract Liability</div>
      <div class="slide-subtitle">
        Unlike probabilistic deep neural networks that hallucinate, Werracle’s procedural escape dynamics are formally machine-verified in Lean 4.
      </div>

      <div class="grid-3">
        <div class="card card-highlight">
          <div class="card-title color-purple">
            <span>📜</span> Lean 4 Formal Verification
          </div>
          <div class="card-desc">
            A comprehensive suite of <b>40 machine-verified theorems</b> across Rungs 1 to 6 in <span style="font-family:'JetBrains Mono'; font-size:13px; color:#c084fc;">WerracleProof.lean</span>. Zero unproven assumptions (<span style="font-family:'JetBrains Mono'; font-weight:700;">zero sorry</span>).
          </div>
          <ul style="margin-left: 20px; margin-top: 10px; font-size: 14px; color:#cbd5e1; line-height: 1.6;">
            <li>Guaranteed termination of procedural escape loops</li>
            <li>Provable bounded Q16.16 arithmetic (no int64 overflow)</li>
            <li>Deterministic gas consumption ceilings</li>
          </ul>
        </div>

        <div class="card card-accent-green">
          <div class="card-title color-green">
            <span>🔬</span> Peer-Reviewed Academic Corpus
          </div>
          <div class="card-desc">
            Published across leading open-science and peer-reviewed international repositories:
          </div>
          <ul style="margin-left: 20px; margin-top: 10px; font-size: 14px; color:#cbd5e1; line-height: 1.6;">
            <li><b>arXiv: 2609.30719</b> [cs.CR, cs.AI, cs.DC]</li>
            <li><b>Elsevier SSRN: 7626279</b> (Liquidation Monograph)</li>
            <li><b>arXiv: 2609.33066</b> (Lean 4 Formal Proofs)</li>
            <li><b>CERN Zenodo Concept DOI: 10.5281/zenodo.22942598</b></li>
          </ul>
        </div>

        <div class="card">
          <div class="card-title color-cyan">
            <span>🔒</span> 1,000 Sealed Test Vectors
          </div>
          <div class="card-desc">
            Cryptographically sealed in SHA-256 test manifests: <b>1,000 rigorous edge-case vectors</b> evaluated across both EVM and CairoVM compilers with a 100% pass rate.
          </div>
          <div class="pill-list" style="margin-top: 20px;">
            <span class="pill-item">100% Pass Rate</span>
            <span class="pill-item">Bit-Exact Simulation</span>
            <span class="pill-item">Zero Compiling Variance</span>
          </div>
        </div>
      </div>

      <div class="card" style="margin-top: 25px; padding: 22px 30px;">
        <div style="font-size: 17px; color: #cbd5e1;">
          <b>The Academic Distinction:</b> While competing Web3 oracles rely on multi-sig trust assumptions, Werracle’s algorithmic defense is mathematically guaranteed by the Lean 4 interactive theorem prover.
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <span>werr.io &bull; Academic Portal & Formal Proof Repository</span>
      <span>Confidential &bull; Seed Investment Pitch Deck</span>
      <span>Slide 09 / 14</span>
    </div>
  </div>

  <!-- SLIDE 10: BUSINESS MODEL & FINANCIALS -->
  <div class="slide">
    <div class="header-bar">
      <div class="brand-wrap">
        <span class="brand-badge">WERRACLE</span>
        <span class="brand-title">Financial Model & Revenue Engines</span>
      </div>
      <div class="category-tag">TRIPLE-TIER RECURRING REVENUE</div>
    </div>

    <div class="content-area">
      <div class="slide-title">Multi-Engine Monetization: Scaling to $7.4M ARR by 2029</div>
      <div class="slide-subtitle">
        Combining predictable B2B DaaS recurring revenue with protocol volume fee capture and enterprise SLA licensing.
      </div>

      <div class="grid-2">
        <div class="chart-container">
          <img src="chart_product_arr_projection_en.png" alt="Consolidated ARR Projections">
        </div>

        <div style="display: flex; flex-direction: column; gap: 18px;">
          <div class="card card-highlight">
            <div class="card-title color-cyan">Engine 1: Radar DaaS Subscriptions ($149 – $2,499/mo)</div>
            <div class="card-desc">
              Paid in native USDC on Base. Developers, searchers, and risk desks pay for high-frequency liquidation signals, bad debt alerts, and raw historical traces. Reaches <b>$3.20M ARR</b> at maturity.
            </div>
          </div>

          <div class="card card-accent-green">
            <div class="card-title color-green">Engine 2: Protocol Hook Royalties (0.5 – 1.5 bps)</div>
            <div class="card-desc">
              Protocols implementing Werracle Uniswap v4 fee hooks and flash loan circuit breakers share in the recaptured value and fee volume. Reaches <b>$2.70M ARR</b> with 15 major protocols.
            </div>
          </div>

          <div class="card card-accent-purple">
            <div class="card-title color-purple">Engine 3: Curator SLA & Enterprise Licensing</div>
            <div class="card-desc">
              Institutional vault curators (Steakhouse, Gauntlet, Re7) pay $10k–$25k/mo for bespoke stress simulation APIs, private oracle seeds, and enterprise SLA uptime. Reaches <b>$1.50M ARR</b>.
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <span>Financial Projections & Monetization Model</span>
      <span>Confidential &bull; Seed Investment Pitch Deck</span>
      <span>Slide 10 / 14</span>
    </div>
  </div>

  <!-- SLIDE 11: MARKET OPPORTUNITY & TRACTION -->
  <div class="slide">
    <div class="header-bar">
      <div class="brand-wrap">
        <span class="brand-badge">WERRACLE</span>
        <span class="brand-title">Market Opportunity & Current Traction</span>
      </div>
      <div class="category-tag">MASSIVE ADDRESSABLE MARKET</div>
    </div>

    <div class="content-area">
      <div class="slide-title">Capturing Value Across a $140B+ DeFi Landscape</div>
      <div class="slide-subtitle">
        Web3 capital requires institutional-grade security infrastructure. Werracle is uniquely positioned at the intersection of on-chain AI, oracle infrastructure, and DeFi risk management.
      </div>

      <div class="grid-3" style="margin-bottom: 25px;">
        <div class="card">
          <div class="metric-hero color-cyan">$140B+</div>
          <div class="metric-sub">Total Addressable Market (TAM)</div>
          <p style="font-size: 14.5px; color: #94a3b8; margin-top: 8px;">Total capital locked across global DeFi protocols and lending vaults</p>
        </div>
        <div class="card">
          <div class="metric-hero color-green">$15B+</div>
          <div class="metric-sub">Serviceable Addressable Market (SAM)</div>
          <p style="font-size: 14.5px; color: #94a3b8; margin-top: 8px;">Lending and AMM liquidity exposed to MEV and flash-loan risk</p>
        </div>
        <div class="card">
          <div class="metric-hero color-gold">$1.8B</div>
          <div class="metric-sub">Serviceable Obtainable Market (SOM)</div>
          <p style="font-size: 14.5px; color: #94a3b8; margin-top: 8px;">Annual expenditure on oracles, risk audits, and telemetry tooling</p>
        </div>
      </div>

      <div class="card card-highlight">
        <div class="card-title color-cyan">Current Operational Traction & Milestones</div>
        <div class="grid-3" style="margin-top: 15px;">
          <div>
            <div style="font-size: 16px; font-weight: 700; color: #f8fafc;">Live On-Chain Deployments</div>
            <p style="font-size: 14px; color: #94a3b8; margin-top: 6px;">
              Contracts live on Aurora testnet; Base L2 production telemetry active; Starknet Cairo 2.8 Sierra codebase verified.
            </p>
          </div>
          <div>
            <div style="font-size: 16px; font-weight: 700; color: #f8fafc;">Institutional Evaluation Keys</div>
            <p style="font-size: 14px; color: #94a3b8; margin-top: 6px;">
              Live pilot evaluation keys generated and active for Steakhouse Financial, Gauntlet, and Re7 Capital risk desks.
            </p>
          </div>
          <div>
            <div style="font-size: 16px; font-weight: 700; color: #f8fafc;">Intellectual Property & Grants</div>
            <p style="font-size: 14px; color: #94a3b8; margin-top: 6px;">
              TÜRKPATENT TR 2026/016285 filed; academic monographs published; Teknokent R&D approval and Base nomination ready.
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <span>Market Sizing & Operational Footprint</span>
      <span>Confidential &bull; Seed Investment Pitch Deck</span>
      <span>Slide 11 / 14</span>
    </div>
  </div>

  <!-- SLIDE 12: THE TEAM -->
  <div class="slide">
    <div class="header-bar">
      <div class="brand-wrap">
        <span class="brand-badge">WERRACLE</span>
        <span class="brand-title">Executive Team & Academic Governance</span>
      </div>
      <div class="category-tag">ENGINEERING & ACADEMIC RIGOR</div>
    </div>

    <div class="content-area">
      <div class="slide-title">Executive Leadership, Engineering Force & Academic Rigor</div>
      <div class="slide-subtitle">
        Operated commercially by our 8-person team at ITouch Systems (Cukurova University Science Park) alongside an independent academic research & patent layer.
      </div>

      <div class="grid-3">
        <div class="card card-highlight">
          <div class="card-title color-cyan">
            <span>💻</span> Executive Leadership (Partners)
          </div>
          <div class="card-desc" style="font-size: 14.5px; line-height: 1.55;">
            <b>Volkan Dağlı — Founder & CTO</b><br>
            Physicist, MIS Specialist & M.Sc. in IT. Lead architect of the WERR Engine, Lean 4 formal proof suite, and EVM/Cairo runtime.<br><br>
            <b>Bekirhan Dağlı — Partner & CEO</b><br>
            Environmental Engineer. Leads corporate strategy, enterprise partnerships, and institutional operations at ITouch Systems.
          </div>
        </div>

        <div class="card card-accent-green">
          <div class="card-title color-green">
            <span>⚙️</span> Engineering, Finance & Operations
          </div>
          <div class="card-desc" style="font-size: 14px; line-height: 1.55;">
            &bull; <b>Burak Salar</b> — Mechatronics Engineer, MBA<br>
            &bull; <b>Fatih İlkin Sercan</b> — Economist & M.Sc. in Capital Markets and Stock Exchange<br>
            &bull; <b>Mustafa Kalender</b> — Computer Engineer<br>
            &bull; <b>Mustafa Ünal</b> — Software Development Specialist & Master Instructor<br>
            &bull; <b>Prenses Metin</b> — Computer Programmer<br>
            &bull; <b>Semih Salar</b> — Business Administration Specialist
          </div>
        </div>

        <div class="card card-accent-purple">
          <div class="card-title color-purple">
            <span>🎓</span> Academic Research & Patents
          </div>
          <div class="card-desc" style="font-size: 14px; line-height: 1.55;">
            &bull; <b>Volkan Dağlı</b> — Principal Investigator (Anadolu University)<br>
            &bull; <b>Dr. Zerrin Dağlı</b> — Academic Advisor, Co-Author & Co-Inventor (Mersin University)<br>
            &bull; <b>Dağhan Dağlı</b> — Co-Author & Co-Inventor (Toros University — Toros Science High School)<br><br>
            <b>Patents TR 2026/016285 & TR 2026/016633:</b> Licensed exclusively to ITouch Systems.
          </div>
        </div>
      </div>

      <div class="card" style="margin-top: 25px; padding: 20px 28px; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <span style="font-size: 17px; font-weight: 700; color: #f8fafc;">ITouch Bilişim Sistemleri Ltd. Şti. (Cukurova University Science Park):</span>
          <span style="font-size: 15px; color: #94a3b8; margin-left: 12px;">Trademarks: Werr™, Werracle™, Answerr™</span>
        </div>
        <span class="category-tag" style="color: #34d399; border-color: rgba(16, 185, 129, 0.3);">contact@werracle.com</span>
      </div>
    </div>

    <div class="footer-bar">
      <span>The Werracle Team & Institutional Heritage</span>
      <span>Confidential &bull; Seed Investment Pitch Deck</span>
      <span>Slide 12 / 14</span>
    </div>
  </div>

  <!-- SLIDE 13: THE ASK & USE OF FUNDS -->
  <div class="slide">
    <div class="header-bar">
      <div class="brand-wrap">
        <span class="brand-badge">WERRACLE</span>
        <span class="brand-title">Seed Investment Ask & Fund Allocation</span>
      </div>
      <div class="category-tag">$1,500,000 USD SEED ROUND</div>
    </div>

    <div class="content-area">
      <div class="slide-title">Fueling Global Protocol Expansion & Tier-1 Audits</div>
      <div class="slide-subtitle">
        Securing an 18 to 24-month runway to finalize multi-chain protocol hooks, onboard top DeFi curators, and scale recurring DaaS revenue to cashflow break-even.
      </div>

      <div class="grid-2">
        <div class="chart-container">
          <img src="chart_fund_allocation_werracle_en.png" alt="Use of Funds Pie Chart">
        </div>

        <div style="display: flex; flex-direction: column; gap: 16px;">
          <div class="card card-highlight">
            <div class="card-title color-cyan">40% ($600,000) &bull; Core Protocol & Multi-Chain Engineering</div>
            <div class="card-desc">
              Production deployment of Uniswap v4 fee hooks, Starknet Ekubo LVR extension, and high-throughput adaptors for Monad, Sei, and Solana.
            </div>
          </div>

          <div class="card card-accent-green">
            <div class="card-title color-green">25% ($375,000) &bull; DeFi BD & Institutional Curator Partnerships</div>
            <div class="card-desc">
              Direct integration into top 15 lending markets and AMMs. Onboarding vault managers (Steakhouse, Gauntlet, Re7) with dedicated SLA support.
            </div>
          </div>

          <div class="card card-accent-purple">
            <div class="card-title color-purple">20% ($300,000) &bull; Security Audits & Low-Latency Bare-Metal Infra</div>
            <div class="card-desc">
              Tier-1 smart contract audits (OpenZeppelin / Trail of Bits), ongoing Lean 4 formal proof extensions, and distributed RPC node clusters.
            </div>
          </div>

          <div class="card">
            <div class="card-title color-gold">15% ($225,000) &bull; Global IP, Legal & US Corporate Structuring</div>
            <div class="card-desc">
              PCT international patent filings, establishing US corporate subsidiary, and W-8BEN-E / regulatory compliance infrastructure.
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <span>Seed Round Capital Allocation (18–24 Month Runway)</span>
      <span>Confidential &bull; Seed Investment Pitch Deck</span>
      <span>Slide 13 / 14</span>
    </div>
  </div>

  <!-- SLIDE 14: CONCLUSION & CONTACT -->
  <div class="slide">
    <div class="header-bar">
      <div class="brand-wrap">
        <span class="brand-badge">WERRACLE</span>
        <span class="brand-title">The Future of Autonomous Web3 Defense</span>
      </div>
      <div class="category-tag">JOIN US IN REDEFINING ORACLES</div>
    </div>

    <div class="content-area" style="text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center;">
      <div class="brand-badge" style="font-size: 22px; padding: 10px 28px; margin-bottom: 25px;">WERRACLE PROTOCOL & DAAS</div>
      
      <div class="cover-title" style="max-width: 1400px; font-size: 60px; margin-bottom: 25px;">
        Smart Contracts Can No Longer Afford to Be Passive. The Future of Web3 is Reflexive.
      </div>

      <div style="font-size: 24px; color: #94a3b8; max-width: 1100px; line-height: 1.5; margin-bottom: 50px;">
        Partner with Werracle as we build the sub-cent, machine-verified reflex intelligence layer securing the next trillion dollars in decentralized finance.
      </div>

      <div class="grid-4" style="width: 100%; max-width: 1500px; text-align: left;">
        <div class="card card-highlight">
          <div style="font-size: 14px; text-transform: uppercase; color: #38bdf8; font-weight: 700; margin-bottom: 6px;">Protocol & dApp</div>
          <div style="font-size: 19px; font-weight: 700; color: #f8fafc;">https://werracle.io</div>
          <p style="font-size: 14px; color: #94a3b8; margin-top: 8px;">Interactive Simulator & Uniswap v4 Hook</p>
        </div>

        <div class="card card-accent-green">
          <div style="font-size: 14px; text-transform: uppercase; color: #34d399; font-weight: 700; margin-bottom: 6px;">Risk Telemetry DaaS</div>
          <div style="font-size: 19px; font-weight: 700; color: #f8fafc;">https://radar.werracle.com</div>
          <p style="font-size: 14px; color: #94a3b8; margin-top: 8px;">Live API & $2.20B Debt Surveillance</p>
        </div>

        <div class="card card-accent-purple">
          <div style="font-size: 14px; text-transform: uppercase; color: #c084fc; font-weight: 700; margin-bottom: 6px;">Corporate & Enterprise</div>
          <div style="font-size: 19px; font-weight: 700; color: #f8fafc;">https://werracle.com</div>
          <p style="font-size: 14px; color: #94a3b8; margin-top: 8px;">Licensing & Institutional Curator SLA</p>
        </div>

        <div class="card">
          <div style="font-size: 14px; text-transform: uppercase; color: #fbbf24; font-weight: 700; margin-bottom: 6px;">Executive Contact</div>
          <div style="font-size: 19px; font-weight: 700; color: #f8fafc;">ask@answerr.me</div>
          <p style="font-size: 14px; color: #94a3b8; margin-top: 8px;">Volkan Dağlı (Founder & CTO) • Bekirhan Dağlı (Partner & CEO)</p>
        </div>
      </div>
    </div>

    <div class="footer-bar">
      <span>ITOUCH BİLİŞİM SİSTEMLERİ MÜH. DAN. SAN. VE TİC. LTD. ŞTİ. &bull; Cukurova University Science Park, Adana / Turkey</span>
      <span>Confidential &bull; Seed Investment Pitch Deck</span>
      <span>Slide 14 / 14</span>
    </div>
  </div>

</body>
</html>
"""

html_path = os.path.abspath('deck_assets/werracle_product_deck_en.html')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"HTML presentation written: {html_path}")

pdf_local_path = os.path.abspath('Werracle_Product_Investor_Pitch_Deck_EN.pdf')
pdf_artifact_path = os.path.abspath('C:/Users/maat/.gemini/antigravity/brain/9cfb8917-acbb-4be8-8bb2-995d94af3274/Werracle_Product_Investor_Pitch_Deck_EN.pdf')

print("Rendering English Werracle Product PDF via Playwright Chromium...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    file_url = f"file:///{html_path.replace(os.sep, '/')}"
    page.goto(file_url, wait_until="networkidle")
    page.pdf(
        path=pdf_local_path,
        width="1920px",
        height="1080px",
        print_background=True,
        prefer_css_page_size=True
    )
    browser.close()

print(f"SUCCESS: Rendered local English PDF -> {pdf_local_path}")
shutil.copy2(pdf_local_path, pdf_artifact_path)
print(f"SUCCESS: Copied artifact English PDF -> {pdf_artifact_path}")
print("PDF Size:", f"{os.path.getsize(pdf_local_path):,} bytes")
