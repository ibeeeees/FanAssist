import { useState, useEffect } from 'react'
import './App.css'
import { useTheme } from './context/ThemeContext'
import CategoryFilter from './components/CategoryFilter'
import PlayerCardComponent from './components/PlayerCardComponent'
import { ScrollTriggeredAnimation } from './components/ScrollTriggeredAnimation'
import playersData from './data/players.json'

interface SelectedPlayer {
  playerId: string;
  playerName: string;
  category: string;
  selection: 'more' | 'less';
  statValue: number;
}

function App() {
  const [selectedCategory, setSelectedCategory] = useState('Popular')
  const { theme, toggleTheme } = useTheme()
  const [selectedPlayers, setSelectedPlayers] = useState<SelectedPlayer[]>([])

  // Load selected players from localStorage on mount
  useEffect(() => {
    const savedPlayers = localStorage.getItem('selectedPlayers')
    if (savedPlayers) {
      try {
        setSelectedPlayers(JSON.parse(savedPlayers))
      } catch (error) {
        console.error('Failed to load selected players:', error)
      }
    }
  }, [])

  // Save selected players to localStorage whenever it changes
  useEffect(() => {
    localStorage.setItem('selectedPlayers', JSON.stringify(selectedPlayers))
  }, [selectedPlayers])


  return (
    <div className="min-h-screen bg-bg p-6">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="flex items-center justify-between mb-6">
          <h1 className="text-4xl font-bold text-text">FanAssist</h1>
          <div className="flex items-center gap-4">
            <button 
              onClick={toggleTheme}
              className="px-4 py-2 rounded-lg font-semibold transition-all"
              style={{
                backgroundColor: 'var(--btn-default)',
                color: 'var(--btn-default-text)'
              }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'var(--btn-default-hover)'}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'var(--btn-default)'}
            >
              {theme === 'dark' ? '🌙 Dark' : '☀️ Light'} Mode
            </button>
          </div>
        </div>

        {/* Player Count */}
        <div className="flex items-center gap-4 text-text-muted">
          <span className="text-sm">
            {playersData.players.length} Players Available
          </span>
          <span className="text-sm">•</span>
          <span className="text-sm">NBA Season 2025-26</span>
        </div>
      </div>

      {/* Category Filter */}
      <div className="max-w-7xl mx-auto">
        <CategoryFilter 
          selectedCategory={selectedCategory}
          onCategoryChange={setSelectedCategory}
        />
      </div>

      {/* Player Cards Grid */}
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {playersData.players.map((player, index) => (
            <ScrollTriggeredAnimation
              key={player.id}
              delay={index * 0.05}
              duration={0.5}
              fallDistance={30}
            >
              <PlayerCardComponent
                player={player}
                selectedCategory={selectedCategory}
                setSelectedPlayers={setSelectedPlayers}
              />
            </ScrollTriggeredAnimation>
          ))}
        </div>
      </div>

      {/* Selected Players Summary */}
      {selectedPlayers.length > 0 && (
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
      )}

    </div>
  )
}

export default App
