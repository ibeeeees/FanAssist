import React from 'react'
import { X, TrendingUp, TrendingDown } from 'lucide-react'

interface GameLog {
  game_date: string
  opponent: string
  stat_value: number
  line_value: number
  result: 'over' | 'under'
}

interface PlayerStatsModalProps {
  isOpen: boolean
  onClose: () => void
  playerName: string
  playerImage: string
  statCategory: string
  lineValue: number
  lastFiveGames: GameLog[]
}

const PlayerStatsModal: React.FC<PlayerStatsModalProps> = ({
  isOpen,
  onClose,
  playerName,
  playerImage,
  statCategory,
  lineValue,
  lastFiveGames,
}) => {
  if (!isOpen) return null

  // Calculate max value for chart scaling
  const maxValue = Math.max(...lastFiveGames.map(g => g.stat_value), lineValue) * 1.2

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4" onClick={onClose}>
      <div className="bg-surface rounded-xl border border-card-border shadow-2xl max-w-lg w-full" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-card-border">
          <div className="flex items-center gap-3">
            <img src={playerImage} alt={playerName} className="w-10 h-10 rounded-full border-2 border-card-border" />
            <div>
              <h3 className="font-bold text-text text-sm">{playerName}</h3>
              <p className="text-xs text-text-muted">{statCategory} - Last 5 Games</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-text-muted hover:text-text transition-colors p-1"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Line Value Indicator */}
        <div className="px-4 py-2 bg-card-bg/30 border-b border-card-border">
          <div className="flex items-center justify-between">
            <span className="text-xs text-text-muted">Line</span>
            <span className="text-sm font-bold text-accent1">{lineValue.toFixed(1)}</span>
          </div>
        </div>

        {/* Chart */}
        <div className="p-4">
          <div className="relative h-48 flex items-end gap-2">
            {/* Line indicator */}
            <div 
              className="absolute left-0 right-0 border-t-2 border-dashed border-accent1/50 z-10"
              style={{ bottom: `${(lineValue / maxValue) * 100}%` }}
            >
              <span className="absolute -top-3 right-0 text-[10px] font-bold text-accent1 bg-surface px-1 rounded">
                {lineValue.toFixed(1)}
              </span>
            </div>

            {/* Bars */}
            {lastFiveGames.map((game, index) => {
              const heightPercent = (game.stat_value / maxValue) * 100
              const isOver = game.result === 'over'
              
              return (
                <div key={index} className="flex-1 flex flex-col items-center gap-1">
                  {/* Bar */}
                  <div className="relative w-full flex items-end" style={{ height: '100%' }}>
                    <div
                      className={`w-full rounded-t transition-all hover:opacity-80 cursor-pointer ${
                        isOver ? 'bg-gradient-to-t from-green-500 to-green-400' : 'bg-gradient-to-t from-red-500 to-red-400'
                      }`}
                      style={{ height: `${heightPercent}%` }}
                      title={`${game.stat_value.toFixed(1)} vs ${game.opponent}`}
                    >
                      {/* Value label */}
                      <div className="absolute -top-5 left-1/2 -translate-x-1/2 whitespace-nowrap">
                        <span className="text-[10px] font-bold text-text bg-surface px-1 rounded shadow-sm">
                          {game.stat_value.toFixed(1)}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Game info */}
                  <div className="text-center mt-1">
                    <div className="text-[9px] font-medium text-text-muted">vs {game.opponent}</div>
                    <div className="text-[8px] text-text-muted/70">{game.game_date}</div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Summary Stats */}
        <div className="px-4 py-3 border-t border-card-border bg-card-bg/20">
          <div className="grid grid-cols-3 gap-3 text-center">
            <div>
              <div className="text-xs text-text-muted mb-0.5">Over</div>
              <div className="text-lg font-bold text-green-500">
                {lastFiveGames.filter(g => g.result === 'over').length}
              </div>
            </div>
            <div>
              <div className="text-xs text-text-muted mb-0.5">Under</div>
              <div className="text-lg font-bold text-red-500">
                {lastFiveGames.filter(g => g.result === 'under').length}
              </div>
            </div>
            <div>
              <div className="text-xs text-text-muted mb-0.5">Avg</div>
              <div className="text-lg font-bold text-text">
                {(lastFiveGames.reduce((sum, g) => sum + g.stat_value, 0) / lastFiveGames.length).toFixed(1)}
              </div>
            </div>
          </div>
        </div>

        {/* Trend Indicator */}
        <div className="px-4 py-2 border-t border-card-border">
          <div className="flex items-center justify-center gap-2 text-xs">
            {lastFiveGames.filter(g => g.result === 'over').length >= 3 ? (
              <>
                <TrendingUp className="w-4 h-4 text-green-500" />
                <span className="text-green-500 font-medium">Trending Over</span>
              </>
            ) : lastFiveGames.filter(g => g.result === 'under').length >= 3 ? (
              <>
                <TrendingDown className="w-4 h-4 text-red-500" />
                <span className="text-red-500 font-medium">Trending Under</span>
              </>
            ) : (
              <span className="text-text-muted">Mixed Results</span>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default PlayerStatsModal
