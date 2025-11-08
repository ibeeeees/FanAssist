import { useState } from 'react'
import './App.css'
import { useTheme } from './context/ThemeContext'
import CategoryFilter from './components/CategoryFilter'
import PlayerCardComponent from './components/PlayerCardComponent'
import playersData from './data/players.json'

function App() {
  const [showShowcase, setShowShowcase] = useState(false)
  const [selectedCategory, setSelectedCategory] = useState('Popular')
  const { theme, toggleTheme } = useTheme()


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
            <button 
              onClick={() => setShowShowcase(!showShowcase)}
              className="px-4 py-2 rounded-lg font-semibold transition-all"
              style={{
                backgroundColor: 'var(--btn-secondary)',
                color: 'var(--btn-secondary-text)'
              }}
              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'var(--btn-secondary-hover)'}
              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'var(--btn-secondary)'}
            >
              {showShowcase ? 'Hide' : 'Show'} Showcase
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
          {playersData.players.map((player) => (
            <PlayerCardComponent 
              key={player.id} 
              player={player}
              selectedCategory={selectedCategory}
            />
          ))}
        </div>
      </div>

    </div>
  )
}

export default App
