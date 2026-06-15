// src/constants/modes.js

export const MODE_CONFIG = {
  Suburban_Train: {
    color: '#f59e0b',
    bg: '#FFFBEB',
    label: 'Suburban Rail',
    icon: '🚆',
    passType: 'uts',
  },
  Intercity_Train: {
    color: '#f59e0b',
    bg: '#FFFBEB',
    label: 'Intercity Express',
    icon: '🚄',
    passType: 'uts',
  },
  Metro: {
    color: '#06b6d4',
    bg: '#ECFEFF',
    label: 'CMRL Metro',
    icon: '🚇',
    passType: 'cmrl_qr',
  },
  MTC_Bus: {
    color: '#ef4444',
    bg: '#FEF2F2',
    label: 'MTC Bus',
    icon: '🚌',
    passType: 'upi_scan',
  },
  SETC_Bus: {
    color: '#ef4444',
    bg: '#FEF2F2',
    label: 'SETC Bus',
    icon: '🚌',
    passType: 'upi_scan',
  },
  Town_Bus: {
    color: '#ef4444',
    bg: '#FEF2F2',
    label: 'Town Bus',
    icon: '🚌',
    passType: 'upi_scan',
  },
  Rapido_Bike: {
    color: '#10b981',
    bg: '#ECFDF5',
    label: 'Rapido Bike',
    icon: '🛵',
    passType: 'pin',
  },
  Ola_Auto: {
    color: '#10b981',
    bg: '#ECFDF5',
    label: 'Ola Auto',
    icon: '🛺',
    passType: 'pin',
  },
  Walk: {
    color: '#64748b',
    bg: 'transparent',
    label: 'Walk',
    icon: '🚶',
    passType: 'walk',
  },
}

export const MOOD_CONFIG = {
  cheapest: {
    label: 'Cheapest',
    icon: 'payments',
    color: '#10B981',
    bg: '#ECFDF5',
    border: 'rgba(16,185,129,0.3)',
    desc: 'Lowest cost route',
  },
  fastest: {
    label: 'Fastest',
    icon: 'bolt',
    color: '#3B82F6',
    bg: '#EEF2FF',
    border: 'rgba(59,130,246,0.3)',
    desc: 'Minimum travel time',
  },
  greenest: {
    label: 'Greenest',
    icon: 'eco',
    color: '#0D9488',
    bg: '#F0FDFA',
    border: 'rgba(13,148,136,0.3)',
    desc: 'Lowest carbon footprint',
  },
  safest: {
    label: 'Safest',
    icon: 'verified_user',
    color: '#7C3AED',
    bg: '#F5F3FF',
    border: 'rgba(124,58,237,0.3)',
    desc: 'Maximum safety routing',
  },
}

export const TRANSIT_MODES_LIST = [
  'Suburban_Train',
  'Metro',
  'MTC_Bus',
  'SETC_Bus',
  'Rapido_Bike',
  'Ola_Auto',
  'Intercity_Train',
]
