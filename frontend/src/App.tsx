import { useState, useEffect } from 'react'
import './App.css'
import { useTheme } from './context/ThemeContext'
import CategoryFilter from './components/CategoryFilter'
import PlayerCardComponent from './components/PlayerCardComponent'
import { ScrollTriggeredAnimation } from './components/ScrollTriggeredAnimation'
import { WelcomePopup } from './components/WelcomePopup'
import SelectedPlayersSummary from './components/SelectedPlayersSummary'
import playersDataRaw from './data/players.json'
import { Sun, Moon, RefreshCw } from 'lucide-react'
import type { SelectedPlayer } from './types'
import { getTodaysPlayers, transformBackendPlayer } from './services/api'

// Type assertion for players data
interface PlayerData {
  id: string;
  name: string;
  image: string;
  team: string;
  teamAbbr: string;
  position: string[];
  gameLocation: string;
  opponent: string;
  opponentAbbr: string;
  gameDay: string;
  gameTime: string;
  gameDate: string;
  projections: any; // Using any to match JSON import
  specialModifier?: 'demon' | 'goblin';
  modifierMultiplier?: number;
  isInjured: boolean;
  injuryStatus: string | null;
}

const playersData = playersDataRaw as { players: PlayerData[] };

function App() {
  const [selectedCategory, setSelectedCategory] = useState('Popular')
  const { theme, toggleTheme } = useTheme()
  const [selectedPlayers, setSelectedPlayers] = useState<SelectedPlayer[]>([])
  const [players, setPlayers] = useState<any[]>([]) // Start with empty array - load live data on mount
  const [isLoading, setIsLoading] = useState(true) // Start loading immediately
  const [useBackendData, setUseBackendData] = useState(true) // Live data enabled
  const [lastFetchTime, setLastFetchTime] = useState<Date | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLineupCollapsed, setIsLineupCollapsed] = useState(false)

  // Fetch players from backend - LIVE DATA ONLY
  const fetchPlayersFromBackend = async () => {
    setIsLoading(true)
    setError(null)
    try {
      console.log('🔄 Fetching TODAY\'S players from backend...')
      const response = await getTodaysPlayers()
      console.log('📊 Backend response:', response)
      
      if (response.players && response.players.length > 0) {
        const transformedPlayers = response.players.map((player, index) => 
          transformBackendPlayer(player, index)
        )
        setPlayers(transformedPlayers)
        setLastFetchTime(new Date())
        console.log(`✅ Loaded ${transformedPlayers.length} LIVE players playing today`)
      } else {
        console.warn('⚠️ No players returned from backend')
        setError('No games scheduled for today. Check back later!')
        setPlayers([])
      }
    } catch (error) {
      console.error('❌ Error fetching from backend:', error)
      setError('Failed to load live data. Please refresh or check your connection.')
      setPlayers([])
    } finally {
      setIsLoading(false)
    }
  }

  // Load data on mount
  useEffect(() => {
    if (useBackendData) {
      fetchPlayersFromBackend()
      
      // Auto-refresh every 5 minutes
      const interval = setInterval(() => {
        fetchPlayersFromBackend()
      }, 5 * 60 * 1000)
      
      return () => clearInterval(interval)
    } else {
      setPlayers(playersData.players)
    }
  }, [useBackendData])

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
            <img src="/FanAssist_Logo.png" alt="FanAssist Logo" className="w-5 h-5 drop-shadow-lg"/>
            <h1 className="text-4xl font-medium text-text">FanAssist</h1>
          </div>
          <div className="flex items-center gap-4">
            {/* Live Data Toggle */}
            <button
              onClick={() => setUseBackendData(!useBackendData)}
              className={`py-0.5 px-1 rounded-lg text-sm font-medium transition-colors ${
                useBackendData 
                  ? 'bg-accent1 text-white' 
                  : 'bg-gray-300 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
              }`}
              title={useBackendData ? 'Using Live Backend Data' : 'Using Static Data'}
            >
              {useBackendData ? '🟢 Live' : '⚫ Static'}
            </button>
            
            {/* Refresh Button */}
            {useBackendData && (
              <button
                onClick={fetchPlayersFromBackend}
                disabled={isLoading}
                className="py-0.5 px-1 rounded-lg bg-accent2 text-white text-sm font-medium hover:bg-accent2/80 cursor-pointer transition-colors flex items-center gap-1"
                title="Refresh player data"
              >
                <RefreshCw className={` ${isLoading ? 'animate-spin' : ''}`} />
                {isLoading ? 'Loading...' : 'Refresh'}
              </button>
            )}
            
            <button 
              onClick={toggleTheme}
              className={`theme-toggle ${theme}`}
              aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
            >
              {theme === 'dark' ? <Moon className="w-2 h-2" /> : <Sun className="w-2 h-2" />}
            </button>
          </div>
        </div>

        {/* Player Count & Status */}
        <div className="flex items-center gap-1 text-text-muted">
          <span className="text-sm">
            {players.length} Players Available
          </span>
          <span className="text-sm">•</span>
          <span className="text-sm">NBA Season 2025-26</span>
          {useBackendData && lastFetchTime && (
            <>
              <span className="text-sm">•</span>
              <span className="text-sm">
                Updated: {lastFetchTime.toLocaleTimeString()}
              </span>
            </>
          )}
        </div>
        
        {/* Error Message */}
        {error && (
          <div className="mt-2 px-4 py-2 bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 rounded-lg text-sm">
            ⚠️ {error}
          </div>
        )}
      </div>

      {/* Category Filter */}
      <div className="max-w-7xl">
        <CategoryFilter 
          selectedCategory={selectedCategory}
          onCategoryChange={setSelectedCategory}
        />
      </div>


      {/* Responsive Layout: Dynamic based on lineup collapse state */}
      <div className={`flex flex-col gap-4 max-w-[1920px] mx-auto ${isLineupCollapsed ? '' : 'md:flex-row'}`}>
        {/* Left side - Player Cards (full width when collapsed, otherwise side-by-side) */}
        <div className={`order-2 md:order-1 ${isLineupCollapsed ? 'w-full' : 'flex-1'}`}>
          {/* Player Cards Grid */}
          <div className="relative">
            {/* Welcome Popup */}
            <WelcomePopup triggerDelay={2000} />

            <div className="flex flex-wrap justify-center gap-1">
              {isLoading && players.length === 0 ? (
                <div className="text-center py-20">
                  <RefreshCw className="w-12 h-12 animate-spin mx-auto mb-4 text-blue-500" />
                  <p className="text-text-muted">Loading players from backend...</p>
                </div>
              ) : (
                players.map((player, index) => (
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
                ))
              )}
            </div>
          </div>
        </div>

        {/* Right Side - Lineup Panel (full width when collapsed) */}
        <aside className={`order-1 md:order-2 ${isLineupCollapsed ? 'w-full' : 'w-full md:w-64 lg:w-72 xl:w-80'}`}>
          <SelectedPlayersSummary 
            selectedPlayers={selectedPlayers}
            setSelectedPlayers={setSelectedPlayers}
            onCollapseChange={setIsLineupCollapsed}
          />
        </aside>
      </div>
    </div>
  )
}

export default App
