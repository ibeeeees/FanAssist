import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { useTheme } from './context/ThemeContext'
import { useSettings } from './context/SettingsContext'
import { ButtonShowcase, CardShowcase } from './components/ButtonShowcase'

function App() {
  const [count, setCount] = useState(0)
  const [showShowcase, setShowShowcase] = useState(false)
  const { theme, toggleTheme } = useTheme()
  const { setSetting, resetDefaults } = useSettings()

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1 className="">Vite + React</h1>
      
      {/* Theme Controls Demo */}
      <div className="card">
        <div className="space-y-4">
          <div className="flex items-center gap-4 flex-wrap">
            <button onClick={toggleTheme} className="px-4 py-2 rounded-lg bg-primary text-white">
              {theme === 'dark' ? '🌙 Dark' : '☀️ Light'} Mode
            </button>
            <button onClick={() => setCount((count) => count + 1)} className="px-4 py-2 rounded bg-surface border border-border">
              count is {count}
            </button>
            <button 
              onClick={() => setShowShowcase(!showShowcase)}
              className="px-4 py-2 rounded-lg"
              style={{
                backgroundColor: 'var(--btn-accent)',
                color: 'var(--btn-accent-text)'
              }}
            >
              {showShowcase ? 'Hide' : 'Show'} Button & Card Showcase
            </button>
          </div>

          {/* Color Customization Demo */}
          <div className="p-4 rounded-lg bg-surface border border-border">
            <h3 className="text-lg font-semibold mb-3">Customize Colors</h3>
            <div className="grid grid-cols-2 gap-3">
              <div className="flex items-center gap-2">
                <label className="text-sm text-text-muted">Primary:</label>
                <input
                  type="color"
                  onChange={(e) => setSetting('colorPrimary', e.target.value)}
                  className="w-10 h-8 rounded cursor-pointer"
                  defaultValue="#0ea5e9"
                />
              </div>
              <div className="flex items-center gap-2">
                <label className="text-sm text-text-muted">Accent:</label>
                <input
                  type="color"
                  onChange={(e) => setSetting('colorAccent', e.target.value)}
                  className="w-10 h-8 rounded cursor-pointer"
                  defaultValue="#f97316"
                />
              </div>
            </div>
            <button 
              onClick={resetDefaults}
              className="mt-3 px-3 py-1 text-sm rounded bg-error text-white"
            >
              Reset to Defaults
            </button>
          </div>

          {/* Demo of Tailwind classes using CSS variables */}
          <div className="p-4 rounded-lg bg-surface border border-border">
            <p className="text-text mb-2">Using Tailwind + CSS Variables:</p>
            <div className="flex gap-2 flex-wrap">
              <span className="px-3 py-1 rounded bg-primary text-white">Primary</span>
              <span className="px-3 py-1 rounded bg-secondary text-white">Secondary</span>
              <span className="px-3 py-1 rounded bg-accent text-white">Accent</span>
              <span className="px-3 py-1 rounded bg-success text-white">Success</span>
              <span className="px-3 py-1 rounded bg-warning text-white">Warning</span>
              <span className="px-3 py-1 rounded bg-error text-white">Error</span>
            </div>
          </div>
        </div>
        
        <p className="mt-4 text-text-muted">
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>

      {/* Button & Card Showcase */}
      {showShowcase && (
        <div className="w-full max-w-6xl mx-auto space-y-8 p-6">
          <ButtonShowcase />
          <hr className="border-border my-8" />
          <CardShowcase />
        </div>
      )}

      <p className="read-the-docs text-text-subtle">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App
