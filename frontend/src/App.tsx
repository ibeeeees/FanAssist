import { useState, useEffect } from 'react'
import './App.css'
import { useTheme } from './context/ThemeContext'
import CategoryFilter from './components/CategoryFilter'
import PlayerCardComponent from './components/PlayerCardComponent'
import { ScrollTriggeredAnimation } from './components/ScrollTriggeredAnimation'
import { WelcomePopup } from './components/WelcomePopup'
import SelectedPlayersSummary from './components/SelectedPlayersSummary'
import playersData from './data/players.json'
import { Sun, Moon } from 'lucide-react'
import type { SelectedPlayer } from './types'

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
    <div className="min-h-screen bg-bg p-3">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-3">
        <div className="flex items-center justify-between mb-4 align-baseline">
          <div className="flex items-center gap-1">
            <img src="/FanAssist_Logo.png" alt="FanAssist Logo" className="w-5 h-5"/>
            <h1 className="text-4xl font-medium text-text">FanAssist</h1>
          </div>
          <div className="flex items-center gap-4">
            <button 
              onClick={toggleTheme}
              className={`theme-toggle ${theme}`}
              aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
            >
              {theme === 'dark' ? <Moon className="w-2 h-2" /> : <Sun className="w-2 h-2" />}
            </button>
          </div>
        </div>

        {/* Player Count */}
        <div className="flex items-center gap-1 text-text-muted">
          <span className="text-sm">
            {playersData.players.length} Players Available
          </span>
          <span className="text-sm">•</span>
          <span className="text-sm">NBA Season 2025-26</span>
        </div>
      </div>

      {/* Category Filter */}
      <div className="max-w-7xl">
        <CategoryFilter 
          selectedCategory={selectedCategory}
          onCategoryChange={setSelectedCategory}
        />
      </div>


      {/* Player Picks */}
      <div className="flex flex-row gap-1">
        {/* Left side */}
        <div className="">
        
          {/* Player Cards Grid */}
          <div className="max-w-7xl mx-auto relative">
            {/* Welcome Popup */}
            <WelcomePopup triggerDelay={2000} />

            <div className="flex flex-wrap justify-center gap-1">
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
                    selectedPlayers={selectedPlayers}
                    setSelectedPlayers={setSelectedPlayers}
                  />
                </ScrollTriggeredAnimation>
              ))}
            </div>
          </div>
        </div>
        {/* Right Side */}
        <div className="">
          {/* Selected Players Summary */}
          <SelectedPlayersSummary 
            selectedPlayers={selectedPlayers}
            setSelectedPlayers={setSelectedPlayers}
          />
        </div>
      </div>
    </div>
  )
}

export default App
