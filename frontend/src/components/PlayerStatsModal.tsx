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
  const [isCollapsed, setIsCollapsed] = React.useState(false)
  
  if (!isOpen) return null

  // Calculate max value for chart scaling
  const maxValue = Math.max(...lastFiveGames.map(g => g.stat_value), lineValue) * 1.2

  console.log('🎯 Modal is OPEN!', { playerName, lastFiveGames })

  return (
    <div 
      className="fixed inset-0 flex items-center justify-center p-4" 
      style={{ 
        zIndex: 10000,
        backgroundColor: 'rgba(0, 0, 0, 0.80)'
      }}
      onClick={onClose}
    >
      <div 
        className="rounded-xl shadow-2xl w-full max-h-[85vh] overflow-hidden" 
        style={{
          backgroundColor: '#ffffff',
          border: '2px solid #e2e8f0',
          maxWidth: isCollapsed ? '500px' : '650px'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3" style={{ borderBottom: '2px solid #e2e8f0', backgroundColor: '#f7fafc' }}>
          <div className="flex items-center gap-3">
            <img src={playerImage} alt={playerName} className="w-10 h-10 rounded-full border-2" style={{ borderColor: '#cbd5e0' }} />
            <div>
              <h3 className="font-bold text-base" style={{ color: '#1a202c' }}>{playerName}</h3>
              <p className="text-xs" style={{ color: '#718096' }}>{statCategory}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsCollapsed(!isCollapsed)}
              className="p-1.5 hover:bg-gray-200 rounded transition-colors"
              style={{ color: '#4a5568' }}
              title={isCollapsed ? "Expand" : "Collapse"}
            >
              <span className="text-sm font-bold">{isCollapsed ? '▼' : '▲'}</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 hover:bg-gray-200 rounded transition-colors"
              style={{ color: '#4a5568' }}
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Line Value Indicator */}
        <div className="px-4 py-2" style={{ backgroundColor: '#edf2f7', borderBottom: '1px solid #e2e8f0' }}>
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium" style={{ color: '#4a5568' }}>Betting Line</span>
            <span className="text-base font-bold" style={{ color: '#10b981' }}>{lineValue.toFixed(1)}</span>
          </div>
        </div>

        {/* Chart */}
        {!isCollapsed && (
          <div className="px-4 py-4">
            <h4 className="text-xs font-semibold mb-3" style={{ color: '#2d3748' }}>Last 5 Games Performance</h4>
            <div className="relative h-40 flex items-end gap-3">
            {/* Bars */}
            {lastFiveGames.map((game, index) => {
              const heightPercent = (game.stat_value / maxValue) * 100
              const isOver = game.result === 'over'
              
              return (
                <div key={index} className="flex-1 flex flex-col items-center gap-2">
                  {/* Bar */}
                  <div className="relative w-full flex items-end" style={{ height: '100%' }}>
                    <div
                      className="w-full rounded-t-lg transition-all hover:opacity-90 cursor-pointer shadow-md"
                      style={{ 
                        height: `${Math.max(heightPercent, 5)}%`,
                        background: isOver 
                          ? 'linear-gradient(to top, #10b981, #34d399)' 
                          : 'linear-gradient(to top, #ef4444, #f87171)',
                        minHeight: '20px'
                      }}
                      title={`${game.stat_value.toFixed(1)} vs ${game.opponent}`}
                    >
                      {/* Value label */}
                      <div className="absolute -top-5 left-1/2 -translate-x-1/2 whitespace-nowrap">
                        <span className="text-[11px] font-bold px-1.5 py-0.5 rounded shadow" style={{ color: '#1a202c', backgroundColor: '#ffffff', border: '1px solid #e2e8f0' }}>
                          {game.stat_value.toFixed(1)}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Game info */}
                  <div className="text-center mt-1">
                    <div className="text-[10px] font-semibold" style={{ color: '#2d3748' }}>{game.opponent}</div>
                    <div className={`text-[9px] font-bold mt-0.5 px-1.5 py-0.5 rounded`} style={{ 
                      color: isOver ? '#10b981' : '#ef4444',
                      backgroundColor: isOver ? '#d1fae5' : '#fee2e2'
                    }}>
                      {isOver ? 'O' : 'U'}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
        )
        }

        {/* Summary Stats */}
        <div className="px-4 py-3" style={{ borderTop: '2px solid #e2e8f0', backgroundColor: '#f7fafc' }}>
          <div className="grid grid-cols-4 gap-2 text-center">
            <div className="p-2 rounded" style={{ backgroundColor: '#d1fae5' }}>
              <div className="text-[10px] font-medium mb-0.5" style={{ color: '#065f46' }}>Over</div>
              <div className="text-xl font-bold" style={{ color: '#10b981' }}>
                {lastFiveGames.filter(g => g.result === 'over').length}
              </div>
            </div>
            <div className="p-2 rounded" style={{ backgroundColor: '#fee2e2' }}>
              <div className="text-[10px] font-medium mb-0.5" style={{ color: '#991b1b' }}>Under</div>
              <div className="text-xl font-bold" style={{ color: '#ef4444' }}>
                {lastFiveGames.filter(g => g.result === 'under').length}
              </div>
            </div>
            <div className="p-2 rounded" style={{ backgroundColor: '#e0e7ff' }}>
              <div className="text-[10px] font-medium mb-0.5" style={{ color: '#3730a3' }}>Avg</div>
              <div className="text-xl font-bold" style={{ color: '#4f46e5' }}>
                {(lastFiveGames.reduce((sum, g) => sum + g.stat_value, 0) / lastFiveGames.length).toFixed(1)}
              </div>
            </div>
            <div className="p-2 rounded flex flex-col items-center justify-center" style={{ backgroundColor: '#fef3c7' }}>
              {lastFiveGames.filter(g => g.result === 'over').length >= 3 ? (
                <>
                  <TrendingUp className="w-4 h-4 mb-0.5" style={{ color: '#10b981' }} />
                  <span className="text-[9px] font-bold" style={{ color: '#10b981' }}>OVER</span>
                </>
              ) : lastFiveGames.filter(g => g.result === 'under').length >= 3 ? (
                <>
                  <TrendingDown className="w-4 h-4 mb-0.5" style={{ color: '#ef4444' }} />
                  <span className="text-[9px] font-bold" style={{ color: '#ef4444' }}>UNDER</span>
                </>
              ) : (
                <>
                  <span className="text-xl" style={{ color: '#718096' }}>•</span>
                  <span className="text-[9px] font-bold" style={{ color: '#718096' }}>MIXED</span>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PlayerStatsModal
