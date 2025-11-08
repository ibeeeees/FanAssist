import React from 'react'

interface CategoryFilterProps {
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
}

const categories = [
  // Row 1
  { name: 'Popular', icon: '🔥' },
  { name: 'Points', icon: null },
  { name: 'Rebounds', icon: null },
  { name: '3-PT Made', icon: null },
  { name: 'Assists', icon: null },
  { name: 'Pts+Asts', icon: null },
  { name: 'Pts+Rebs+Asts', icon: null },
  { name: 'FG Made', icon: null },
  { name: 'Defensive Rebounds', icon: null },
  // Row 2
  { name: 'Fantasy Score', icon: null },
  { name: 'Offensive Rebounds', icon: null },
  { name: 'Rebs+Asts', icon: null },
  { name: '3-PT Attempted', icon: null },
  { name: 'Points (Combo)', icon: null },
  { name: '3-PT Made (Combo)', icon: null },
  { name: 'Assists (Combo)', icon: null },
  // Row 3
  { name: 'Rebounds (Combo)', icon: null },
  { name: 'Free Throws Made', icon: null },
  { name: 'FG Attempted', icon: null },
  { name: 'Dunks', icon: null },
  { name: 'Pts+Rebs', icon: null },
  { name: 'Blocked Shots', icon: null },
  { name: 'Steals', icon: null },
  { name: 'Free Throws Attempted', icon: null },
  // Row 4
  { name: 'Personal Fouls', icon: null },
  { name: 'Blks+Stls', icon: null },
  { name: 'Turnovers', icon: null },
  { name: 'Assists - 1st 3 Minutes', icon: null },
  { name: 'Points - 1st 3 Minutes', icon: null },
  { name: 'Quarters with 3+ Points', icon: null },
  { name: 'Rebounds - 1st 3 Minutes', icon: null },
  // Row 5
  { name: 'Quarters with 5+ Points', icon: null },
  { name: 'Two Pointers Attempted', icon: null },
  { name: 'Two Pointers Made', icon: null },
];

const CategoryFilter: React.FC<CategoryFilterProps> = ({ selectedCategory, onCategoryChange }) => {
  return (
    <div className="mb-6 overflow-x-auto">
      {/* Row 1 */}
      <div className="flex gap-3 mb-3 pb-2">
        {categories.slice(0, 9).map((category) => (
          <button
            key={category.name}
            onClick={() => onCategoryChange(category.name)}
            className="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all flex items-center gap-2"
            style={{
              backgroundColor: selectedCategory === category.name ? 'var(--btn-default)' : 'var(--surface)',
              color: selectedCategory === category.name ? 'var(--btn-default-text)' : 'var(--text-muted)',
              border: `1px solid ${selectedCategory === category.name ? 'var(--card-border-hover)' : 'var(--card-border)'}`,
            }}
          >
            {category.icon && <span>{category.icon}</span>}
            {category.name}
          </button>
        ))}
      </div>

      {/* Row 2 */}
      <div className="flex gap-3 mb-3 pb-2">
        {categories.slice(9, 16).map((category) => (
          <button
            key={category.name}
            onClick={() => onCategoryChange(category.name)}
            className="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all"
            style={{
              backgroundColor: selectedCategory === category.name ? 'var(--btn-default)' : 'var(--surface)',
              color: selectedCategory === category.name ? 'var(--btn-default-text)' : 'var(--text-muted)',
              border: `1px solid ${selectedCategory === category.name ? 'var(--card-border-hover)' : 'var(--card-border)'}`,
            }}
          >
            {category.name}
          </button>
        ))}
      </div>

      {/* Row 3 */}
      <div className="flex gap-3 mb-3 pb-2">
        {categories.slice(16, 24).map((category) => (
          <button
            key={category.name}
            onClick={() => onCategoryChange(category.name)}
            className="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all"
            style={{
              backgroundColor: selectedCategory === category.name ? 'var(--btn-default)' : 'var(--surface)',
              color: selectedCategory === category.name ? 'var(--btn-default-text)' : 'var(--text-muted)',
              border: `1px solid ${selectedCategory === category.name ? 'var(--card-border-hover)' : 'var(--card-border)'}`,
            }}
          >
            {category.name}
          </button>
        ))}
      </div>

      {/* Row 4 */}
      <div className="flex gap-3 mb-3 pb-2">
        {categories.slice(24, 31).map((category) => (
          <button
            key={category.name}
            onClick={() => onCategoryChange(category.name)}
            className="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all"
            style={{
              backgroundColor: selectedCategory === category.name ? 'var(--btn-default)' : 'var(--surface)',
              color: selectedCategory === category.name ? 'var(--btn-default-text)' : 'var(--text-muted)',
              border: `1px solid ${selectedCategory === category.name ? 'var(--card-border-hover)' : 'var(--card-border)'}`,
            }}
          >
            {category.name}
          </button>
        ))}
      </div>

      {/* Row 5 */}
      <div className="flex gap-3 pb-2">
        {categories.slice(31).map((category) => (
          <button
            key={category.name}
            onClick={() => onCategoryChange(category.name)}
            className="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all"
            style={{
              backgroundColor: selectedCategory === category.name ? 'var(--btn-default)' : 'var(--surface)',
              color: selectedCategory === category.name ? 'var(--btn-default-text)' : 'var(--text-muted)',
              border: `1px solid ${selectedCategory === category.name ? 'var(--card-border-hover)' : 'var(--card-border)'}`,
            }}
          >
            {category.name}
          </button>
        ))}
      </div>
    </div>
  )
}

export default CategoryFilter
