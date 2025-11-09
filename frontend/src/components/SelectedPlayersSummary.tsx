import React from 'react'

interface SelectedPlayer {
  playerId: string;
  playerName: string;
  category: string;
  selection: 'more' | 'less';
  statValue: number;
}

interface SelectedPlayersSummaryProps {
  selectedPlayers: SelectedPlayer[];
}

const SelectedPlayersSummary: React.FC<SelectedPlayersSummaryProps> = ({ selectedPlayers }) => {
  if (selectedPlayers.length === 0) {
    return null;
  }

  return (
    <div className="max-w-7xl mx-auto mt-8">
      <div className="bg-surface p-6 rounded-lg border border-card-border">
        <h2 className="text-2xl font-bold text-text mb-4">
          Your Lineup ({selectedPlayers.length})
        </h2>
        <div className="space-y-2">
          {selectedPlayers.map((sp, index) => (
            <div 
              key={`${sp.playerId}-${index}`}
              className="flex items-center justify-between p-3 bg-card-bg rounded border border-card-border"
            >
              <div className="flex items-center gap-3">
                <span className="font-semibold text-text">{sp.playerName}</span>
                <span className="text-text-muted text-sm">•</span>
                <span className="text-sm text-text-muted">{sp.category}</span>
              </div>
              <div className="flex items-center gap-3">
                <span 
                  className="text-lg font-bold" 
                  style={{ color: 'var(--color-accent1)' }}
                >
                  {sp.statValue.toFixed(1)}
                </span>
                <span 
                  className={`px-3 py-1 rounded text-sm font-semibold ${
                    sp.selection === 'more' 
                      ? 'bg-btn-success text-btn-success-text' 
                      : 'bg-btn-error text-btn-error-text'
                  }`}
                >
                  {sp.selection === 'more' ? 'More' : 'Less'}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default SelectedPlayersSummary
