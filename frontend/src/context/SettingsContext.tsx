import React, { createContext, useContext, useEffect, useState } from 'react';

export interface Settings {
  // Colors
  colorPrimary?: string;
  colorSecondary?: string;
  colorAccent?: string;
  colorSuccess?: string;
  colorWarning?: string;
  colorError?: string;
  
  // Layout
  radius?: string;
  radiusSm?: string;
  radiusLg?: string;
  radiusXl?: string;
  
  spacing?: string;
  spacingXs?: string;
  spacingSm?: string;
  spacingLg?: string;
  spacingXl?: string;
  
  // Typography
  fontSans?: string;
  textBase?: string;
  
  // Any other custom CSS variable
  [key: string]: string | undefined;
}

interface SettingsContextValue {
  settings: Settings;
  setSetting: (key: string, value: string) => void;
  setSettings: (settings: Partial<Settings>) => void;
  resetDefaults: () => void;
}

const SettingsContext = createContext<SettingsContextValue | undefined>(undefined);

const STORAGE_KEY = 'fanassist:settings';

export const SettingsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [settings, setSettingsState] = useState<Settings>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : {};
    } catch (e) {
      console.warn('Failed to read settings from localStorage:', e);
      return {};
    }
  });

  useEffect(() => {
    const root = document.documentElement;

    // Apply each setting as a CSS variable
    Object.entries(settings).forEach(([key, value]) => {
      if (value === undefined || value === null) return;
      
      // Convert camelCase to kebab-case for CSS variable names
      // e.g., colorPrimary -> --color-primary
      const cssVarName = `--${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`;
      root.style.setProperty(cssVarName, value);
    });

    // Persist to localStorage
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
    } catch (e) {
      console.warn('Failed to save settings to localStorage:', e);
    }
  }, [settings]);

  const setSetting = (key: string, value: string) => {
    setSettingsState(prev => ({ ...prev, [key]: value }));
  };

  const setSettings = (newSettings: Partial<Settings>) => {
    setSettingsState(prev => ({ ...prev, ...newSettings }));
  };

  const resetDefaults = () => {
    // Clear all inline styles and state
    const root = document.documentElement;
    Object.keys(settings).forEach(key => {
      const cssVarName = `--${key.replace(/([A-Z])/g, '-$1').toLowerCase()}`;
      root.style.removeProperty(cssVarName);
    });
    
    setSettingsState({});
    
    try {
      localStorage.removeItem(STORAGE_KEY);
    } catch (e) {
      console.warn('Failed to remove settings from localStorage:', e);
    }
  };

  const value: SettingsContextValue = {
    settings,
    setSetting,
    setSettings,
    resetDefaults
  };

  return <SettingsContext.Provider value={value}>{children}</SettingsContext.Provider>;
};

export const useSettings = (): SettingsContextValue => {
  const context = useContext(SettingsContext);
  if (!context) {
    throw new Error('useSettings must be used within SettingsProvider');
  }
  return context;
};
