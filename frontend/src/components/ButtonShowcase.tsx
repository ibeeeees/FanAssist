import React, { useState } from 'react';

/**
 * Button Showcase Component
 * Demonstrates all button variants with their states (normal, hover, active)
 */
export const ButtonShowcase: React.FC = () => {
  const [activeButton, setActiveButton] = useState<string | null>(null);

  const buttonVariants = [
    { name: 'Default', bg: 'btn-default', hover: 'btn-default-hover', active: 'btn-default-active', text: 'btn-default-text' },
    { name: 'Primary', bg: 'btn-primary', hover: 'btn-primary-hover', active: 'btn-primary-active', text: 'btn-primary-text', highlight: 'btn-primary-highlight' },
    { name: 'Secondary', bg: 'btn-secondary', hover: 'btn-secondary-hover', active: 'btn-secondary-active', text: 'btn-secondary-text', highlight: 'btn-secondary-highlight' },
    { name: 'Accent', bg: 'btn-accent', hover: 'btn-accent-hover', active: 'btn-accent-active', text: 'btn-accent-text', highlight: 'btn-accent-highlight' },
    { name: 'Success', bg: 'btn-success', hover: 'btn-success-hover', active: 'btn-success-active', text: 'btn-success-text', highlight: 'btn-success-highlight' },
    { name: 'Warning', bg: 'btn-warning', hover: 'btn-warning-hover', active: 'btn-warning-active', text: 'btn-warning-text', highlight: 'btn-warning-highlight' },
    { name: 'Error', bg: 'btn-error', hover: 'btn-error-hover', active: 'btn-error-active', text: 'btn-error-text', highlight: 'btn-error-highlight' },
  ];

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-text">Button Variants</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {buttonVariants.map((variant) => (
          <div key={variant.name} className="p-4 rounded-lg border border-border bg-surface">
            <h3 className="text-sm font-semibold mb-2 text-text-muted">{variant.name}</h3>
            
            {/* Normal Button */}
            <button
              onClick={() => setActiveButton(variant.name)}
              className="w-full px-4 py-2 rounded-lg font-medium transition-all duration-200"
              style={{
                backgroundColor: activeButton === variant.name 
                  ? `var(--${variant.active})` 
                  : `var(--${variant.bg})`,
                color: `var(--${variant.text})`
              }}
              onMouseEnter={(e) => {
                if (activeButton !== variant.name) {
                  e.currentTarget.style.backgroundColor = `var(--${variant.hover})`;
                }
              }}
              onMouseLeave={(e) => {
                if (activeButton !== variant.name) {
                  e.currentTarget.style.backgroundColor = `var(--${variant.bg})`;
                }
              }}
            >
              {variant.name} Button
            </button>

            {/* Highlight Badge (if available) */}
            {variant.highlight && (
              <div className="mt-2 flex items-center gap-2">
                <span className="text-xs text-text-muted">Highlight:</span>
                <span
                  className="px-2 py-1 rounded text-xs font-medium"
                  style={{
                    backgroundColor: `var(--${variant.highlight})`,
                    color: `var(--${variant.text})`
                  }}
                >
                  Badge
                </span>
              </div>
            )}
          </div>
        ))}

        {/* Ghost Button */}
        <div className="p-4 rounded-lg border border-border bg-surface">
          <h3 className="text-sm font-semibold mb-2 text-text-muted">Ghost</h3>
          <button
            className="w-full px-4 py-2 rounded-lg font-medium transition-all duration-200 border"
            style={{
              backgroundColor: activeButton === 'Ghost' 
                ? 'var(--btn-ghost-active)' 
                : 'var(--btn-ghost)',
              color: 'var(--btn-ghost-text)',
              borderColor: 'var(--btn-ghost-border)'
            }}
            onClick={() => setActiveButton('Ghost')}
            onMouseEnter={(e) => {
              if (activeButton !== 'Ghost') {
                e.currentTarget.style.backgroundColor = 'var(--btn-ghost-hover)';
              }
            }}
            onMouseLeave={(e) => {
              if (activeButton !== 'Ghost') {
                e.currentTarget.style.backgroundColor = 'var(--btn-ghost)';
              }
            }}
          >
            Ghost Button
          </button>
        </div>
      </div>

      {activeButton && (
        <p className="text-sm text-text-muted">
          Active: <strong className="text-text">{activeButton}</strong> (click another to change)
        </p>
      )}
    </div>
  );
};

/**
 * Card Showcase Component
 * Demonstrates card variants with different states and highlights
 */
export const CardShowcase: React.FC = () => {
  const [hoveredCard, setHoveredCard] = useState<string | null>(null);
  const [selectedCard, setSelectedCard] = useState<string | null>(null);

  const cardHighlights = [
    { name: 'Primary', highlight: 'card-highlight-primary' },
    { name: 'Secondary', highlight: 'card-highlight-secondary' },
    { name: 'Accent', highlight: 'card-highlight-accent' },
    { name: 'Success', highlight: 'card-highlight-success' },
    { name: 'Warning', highlight: 'card-highlight-warning' },
    { name: 'Error', highlight: 'card-highlight-error' },
  ];

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-text">Card Variants</h2>

      {/* Default Card with States */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-text">Default Card States</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {['Normal', 'Hover', 'Active'].map((state) => (
            <div
              key={state}
              className="p-4 rounded-lg border transition-all duration-200"
              style={{
                backgroundColor: state === 'Normal' ? 'var(--card-bg)' : 
                                state === 'Hover' ? 'var(--card-bg-hover)' : 
                                'var(--card-bg-active)',
                borderColor: state === 'Hover' ? 'var(--card-border-hover)' : 'var(--card-border)',
                boxShadow: state === 'Hover' ? 'var(--card-shadow-hover)' : 'var(--card-shadow)'
              }}
            >
              <h4 className="font-semibold text-text mb-2">{state} State</h4>
              <p className="text-sm text-text-muted">Card content goes here</p>
            </div>
          ))}
        </div>
      </div>

      {/* Interactive Cards with Highlights */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-text">Highlight Colors (Click to Select)</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {cardHighlights.map((card) => (
            <div
              key={card.name}
              className="p-4 rounded-lg border cursor-pointer transition-all duration-200"
              style={{
                backgroundColor: selectedCard === card.name 
                  ? `var(--${card.highlight})` 
                  : hoveredCard === card.name 
                    ? 'var(--card-bg-hover)' 
                    : 'var(--card-bg)',
                borderColor: selectedCard === card.name 
                  ? `var(--color-${card.name.toLowerCase()})` 
                  : hoveredCard === card.name 
                    ? 'var(--card-border-hover)' 
                    : 'var(--card-border)',
                boxShadow: hoveredCard === card.name || selectedCard === card.name 
                  ? 'var(--card-shadow-hover)' 
                  : 'var(--card-shadow)',
                borderWidth: selectedCard === card.name ? '2px' : '1px'
              }}
              onClick={() => setSelectedCard(selectedCard === card.name ? null : card.name)}
              onMouseEnter={() => setHoveredCard(card.name)}
              onMouseLeave={() => setHoveredCard(null)}
            >
              <div className="flex items-center justify-between mb-2">
                <h4 className="font-semibold text-text">{card.name} Card</h4>
                {selectedCard === card.name && (
                  <span className="text-xs px-2 py-1 rounded" style={{
                    backgroundColor: `var(--btn-${card.name.toLowerCase()})`,
                    color: `var(--btn-${card.name.toLowerCase()}-text)`
                  }}>
                    Selected
                  </span>
                )}
              </div>
              <p className="text-sm text-text-muted">
                {selectedCard === card.name ? 'Highlighted state' : 'Click to highlight'}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
