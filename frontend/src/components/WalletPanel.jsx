// src/components/WalletPanel.jsx
import { useState } from 'react'
import { useWallet } from '../hooks/useWallet'

const TX_ICONS = {
  'Deposit': <span className="material-symbols-outlined text-[18px] text-emerald-500">arrow_downward</span>,
  'Escrow Lock': <span className="material-symbols-outlined text-[18px] text-amber-500">lock</span>,
  'Fare Release': <span className="material-symbols-outlined text-[18px] text-blue-500">arrow_upward</span>,
  'Escrow Refund': <span className="material-symbols-outlined text-[18px] text-violet-500">replay</span>,
}

export default function WalletPanel() {
  const { wallet, loading, deposit, refresh } = useWallet()
  const [depositAmt, setDepositAmt] = useState('')
  const [depositing, setDepositing] = useState(false)
  const [showDeposit, setShowDeposit] = useState(false)
  const QUICK_AMOUNTS = [100, 250, 500, 1000]

  async function handleDeposit(amount) {
    setDepositing(true)
    try {
      await deposit(Number(amount))
      setDepositAmt('')
      setShowDeposit(false)
    } catch (_) {}
    finally { setDepositing(false) }
  }

  if (!wallet) {
    return (
      <div className="flex items-center justify-center h-40">
        <span className="material-symbols-outlined text-[24px] animate-spin text-secondary">sync</span>
      </div>
    )
  }

  const available = wallet.balance ?? 0
  const locked = wallet.escrow_locked ?? 0
  const txns = wallet.transactions ?? []

  // Progress budget calculation
  const totalSpend = txns
    .filter(tx => tx.type === 'Fare Release')
    .reduce((sum, tx) => sum + Number(tx.amount), 0)
  const monthlyLimit = 2000
  const pct = Math.min((totalSpend / monthlyLimit) * 100, 100)
  const progressColor = pct < 50 ? 'bg-emerald-500' : pct < 80 ? 'bg-amber-500' : 'bg-rose-500'

  return (
    <div className="flex flex-col gap-5 pb-20 animate-fade-in-up">

      {/* Balance Card / YatraWallet Widget Redesign */}
      <div className="glass-panel rounded-2xl p-4 flex flex-col gap-4 relative overflow-hidden bg-gradient-to-br from-surface to-surface-container-low select-none">
        
        {/* Top Header Row */}
        <div className="flex items-start justify-between w-full relative z-10">
          <div className="flex flex-col">
            <span className="text-[11px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider block">
              YatraWallet Balance
            </span>
            <span className="text-[24px] font-bold text-on-surface font-mono mt-1 leading-none select-all">
              ₹ {available.toFixed(2)}
            </span>
          </div>

          <div className="flex items-center gap-2">
            <button 
              onClick={refresh} 
              className="w-10 h-10 rounded-xl bg-surface-container-high border border-outline-variant text-slate-500 hover:text-secondary transition-colors flex items-center justify-center active:scale-95 duration-100"
              title="Refresh wallet"
            >
              <span className={`material-symbols-outlined text-[18px] ${loading ? 'animate-spin' : ''}`}>sync</span>
            </button>
            <button
              onClick={() => setShowDeposit(true)}
              className="h-10 px-3 bg-secondary hover:brightness-110 text-white font-bold rounded-xl text-[12px] transition-all flex items-center justify-center gap-1 active:scale-95 duration-100"
            >
              <span className="material-symbols-outlined text-[16px]">add</span> Top Up
            </button>
          </div>
        </div>

        {/* Escrow Indicator */}
        {locked > 0 && (
          <div className="flex items-center gap-1.5 bg-amber-50 dark:bg-amber-950/20 border border-amber-500/20 rounded-xl px-3 py-2 mt-1 relative z-10">
            <span className="material-symbols-outlined text-[16px] text-amber-500 shrink-0">lock</span>
            <p className="text-[12px] text-amber-600 dark:text-amber-400 font-bold">₹{locked.toFixed(2)} locked in escrow</p>
          </div>
        )}

        {/* Low Balance Warning (PDF requirement: alert when balance falls below Rs. 150) */}
        {available < 150 && (
          <div className="flex items-center gap-1.5 bg-rose-500/10 dark:bg-rose-950/20 border border-rose-500/20 rounded-xl px-3 py-2 mt-1 relative z-10 animate-pulse">
            <span className="material-symbols-outlined text-[16px] text-rose-500 shrink-0">warning</span>
            <p className="text-[12px] text-rose-600 dark:text-rose-400 font-bold">Low Balance: Below ₹150. Top up to prevent transit disruptions.</p>
          </div>
        )}

        {/* Spend Progress Bar */}
        <div className="flex flex-col gap-1.5 mt-1 relative z-10">
          <div className="flex justify-between text-[11px] font-bold text-slate-400 dark:text-slate-500">
            <span>Spend Allowance Limit</span>
            <span className="font-mono text-slate-600 dark:text-slate-300">₹{totalSpend.toFixed(0)} / ₹{monthlyLimit}</span>
          </div>
          <div className="h-1 bg-surface-container-highest rounded-full overflow-hidden">
            <div className={`h-full rounded-full transition-all duration-300 ${progressColor}`} style={{ width: `${pct}%` }} />
          </div>
        </div>

        {/* UPI Secured Badge */}
        <div className="flex items-center gap-1 text-[11px] text-slate-400 dark:text-slate-500 relative z-10 mt-1 select-none">
          <span className="material-symbols-outlined text-[14px] text-emerald-500" style={{ fontVariationSettings: "'FILL' 1" }}>verified_user</span>
          <span className="font-medium">UPI secured and encrypted</span>
        </div>
      </div>

      {/* Top Up Deposit Modal */}
      {showDeposit && (
        <div className="modal-overlay" onClick={() => setShowDeposit(false)}>
          <div className="modal-content animate-fade-in-up dark:bg-surface-container-high" onClick={e => e.stopPropagation()}
               style={{ border: '1px solid var(--outline-variant)' }}>
            <div className="uts-header border-b border-outline-variant/20 pb-3 flex items-center gap-3">
              <div className="uts-logo-circle bg-secondary text-white font-bold w-9 h-9 rounded-full flex items-center justify-center text-[16px]">
                ₹
              </div>
              <div>
                <p className="text-on-surface font-semibold text-[13.5px]">Add Funds</p>
                <p className="text-[12px] text-slate-400 dark:text-slate-500 font-medium">Top up securely via simulated UPI gate</p>
              </div>
            </div>

            <p className="text-[11px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider mt-1">Quick Select</p>
            <div className="grid grid-cols-4 gap-2">
              {QUICK_AMOUNTS.map(amt => (
                <button
                  key={amt}
                  onClick={() => handleDeposit(amt)}
                  className="bg-surface-container-low text-secondary font-bold rounded-xl h-11 text-[12px]
                             border border-outline-variant hover:bg-secondary/10 transition-all flex items-center justify-center active:scale-[0.97]"
                >
                  +₹{amt}
                </button>
              ))}
            </div>

            <div className="flex gap-2 mt-2">
              <input
                type="number"
                value={depositAmt}
                onChange={e => setDepositAmt(e.target.value)}
                placeholder="Enter custom amount"
                className="flex-1 bg-surface-container border border-outline-variant rounded-xl px-4 h-11
                           text-on-surface placeholder-slate-400 text-[12px] outline-none focus:border-secondary transition-colors"
              />
              <button
                onClick={() => depositAmt && handleDeposit(depositAmt)}
                disabled={!depositAmt || depositing}
                className="bg-secondary text-white font-medium px-5 rounded-xl text-[12px] h-11 flex items-center justify-center
                           disabled:opacity-30 hover:brightness-110 transition-all active:scale-95 shrink-0"
              >
                {depositing ? 'Paying…' : 'Deposit'}
              </button>
            </div>

            <button
              onClick={() => setShowDeposit(false)}
              className="text-[12px] text-slate-400 dark:text-slate-500 hover:text-on-surface transition-colors text-center mt-2 h-11 flex items-center justify-center w-full select-none"
            >
              Cancel Payment
            </button>
          </div>
        </div>
      )}

      {/* Transactions Statement */}
      <div className="bg-surface border border-outline-variant rounded-[16px] p-4 dark:bg-surface-container-low">
        <p className="text-[11px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider font-outfit mb-3 block">
          Statement History
        </p>
        {txns.length === 0 ? (
          <p className="text-[12px] text-slate-400 dark:text-slate-500 text-center py-8">No transaction activity logged</p>
        ) : (
          <div className="flex flex-col">
            {txns.slice(0, 20).map((tx, i) => (
              <div key={i} className="flex items-center gap-3 py-2.5 border-b border-outline-variant/10 last:border-0 hover:bg-surface-container/20 rounded-lg px-1 transition-colors duration-150">
                <div className="w-8 h-8 rounded-lg bg-surface-container border border-outline-variant flex items-center justify-center shrink-0">
                  {TX_ICONS[tx.type] ?? <span className="material-symbols-outlined text-[18px]">arrow_upward</span>}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-[12px] text-on-surface font-semibold truncate">{tx.type}</p>
                  <p className="text-[11px] text-slate-400 dark:text-slate-500 truncate mt-0.5 leading-none">{tx.details}</p>
                </div>
                <div className="text-right shrink-0">
                  <p className={`text-[12px] font-bold ${
                    tx.type === 'Deposit' || tx.type === 'Escrow Refund' ? 'text-emerald-600 dark:text-emerald-400' : 'text-on-surface'
                  }`}>
                    {tx.type === 'Deposit' || tx.type === 'Escrow Refund' ? '+' : '-'}₹{tx.amount}
                  </p>
                  <p className="text-[11px] text-slate-400 dark:text-slate-500 mt-0.5 leading-none">{tx.timestamp}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
