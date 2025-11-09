# 🏀 FanAssist - Next-Gen NBA Sports Engagement Platform

> **PrizePicks Hackathon 2025 Submission**  
> **Track:** Next-Gen Game Flow - Re-imagining Real-Time Sports Engagement

A revolutionary sports engagement platform that combines AI-powered player analysis, real-time game simulation, and innovative betting mechanics to create an immersive, beginner-friendly experience for NBA fans.

---

## 🎯 The Challenge

Traditional sports betting platforms can be intimidating for newcomers and lack the real-time insights needed to make informed decisions. We set out to solve this by building a platform that:

- **Democratizes Sports Betting**: Makes prop betting accessible to beginners with AI-powered explanations
- **Provides Real-Time Intelligence**: Uses machine learning to simulate games and predict player performance
- **Gamifies the Experience**: Introduces innovative "Demons & Goblins" modifier system for dynamic risk/reward
- **Offers Safe Practice**: Paper betting with virtual currency lets users learn without financial risk

---

## ✨ Key Features

### 🎲 Demons & Goblins Modifier System
Our flagship innovation that transforms traditional prop betting:

- **Demon Players** 🔥: High-risk, high-reward modifiers that boost projections and multiply payouts
  - Projected stat increases by 4.0-5.5 points
  - Payout multipliers: **10x to 2000x** (scales with lineup size)
  - Visual indicators: Red borders, badges, and stat highlights

- **Goblin Players** 👺: Conservative plays that lower projections but provide safer bets
  - Projected stat decreases by 3.0 points
  - Payout reductions: **0.5x to 0.2x** (compound multiplicatively)
  - Visual indicators: Green borders, badges, and stat highlights

- **Dynamic Toggle System**: One-click modifier activation with real-time payout calculations
- **Smart Restrictions**: Prevents conflicting selections (e.g., LESS disabled when demon modifier active)

### 🧠 AI-Powered Analysis
Leveraging AWS Bedrock and advanced ML models:

- **Beginner-Friendly Explanations**: AI breaks down complex stats into easy-to-understand insights
- **Game Simulation Engine**: Monte Carlo simulations predict player performance across 10,000+ game scenarios
- **Machine Learning Predictions**: ML models analyze historical data, matchups, and trends
- **Real-Time Odds Calculation**: Instantly see win probabilities for any prop or parlay

### 💰 Paper Betting System
Risk-free practice environment:

- **Virtual Currency**: Start with $10,000 in paper money
- **Full Betting Simulation**: Place Power Plays (2-6 legs) and Flex Plays with real payout structures
- **Live Result Tracking**: Simulate bet outcomes based on AI predictions
- **Leaderboards**: Compete with friends to build the best virtual bankroll

### 📊 Real-Time Data Integration
Powered by NBA stats and PrizePicks API:

- **Live Player Projections**: Up-to-date stat lines for Points, Rebounds, Assists, 3-Pointers, and more
- **Daily Props**: Curated props for popular players updated daily
- **Injury Tracking**: Automatic filtering and warnings for injured players
- **Schedule Integration**: Complete game schedules with matchup analysis

### 🎨 Immersive User Experience
Built with modern design principles:

- **Dark/Light Theme Toggle**: Personalized viewing experience
- **Smooth Animations**: Scroll-triggered reveals and falling confetti celebrations
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Real-Time Payout Calculator**: See potential winnings update as you build your lineup
- **Welcome Tutorial**: Guided onboarding for new users

---

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript for type-safe component architecture
- **Vite** for lightning-fast development and optimized builds
- **Tailwind CSS v4** for modern, utility-first styling
- **Lucide React** for beautiful iconography
- **LocalStorage** for persistent state management

### Backend
- **FastAPI** (Python) for high-performance REST API
- **NBA API** for real-time player stats and game data
- **AWS Bedrock** for AI-powered analysis and natural language generation
- **NumPy/Pandas** for statistical analysis and simulation
- **PrizePicks API** integration for prop lines

### Development Tools
- **Docker** for containerized deployment
- **ESLint** for code quality
- **Git** for version control

---

## 🚀 Getting Started

### Prerequisites
- **Node.js** 18+ and npm/yarn
- **Python** 3.9+
- **Docker** (optional, for containerized deployment)

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --reload
```

The backend API will be available at `http://localhost:8000`

### Docker Deployment (Optional)

```bash
# Build and run with Docker Compose
docker-compose up --build
```

---

## 📖 How It Works

### 1. **Browse Players**
- Filter by category (Popular, Guards, Forwards, Centers)
- View live projections for all major stat categories
- See injury status and game matchups

### 2. **Build Your Lineup**
- Select 2-6 players for a Power Play or Flex Play
- Choose OVER or UNDER for each stat projection
- Activate Demon or Goblin modifiers for dynamic gameplay

### 3. **Calculate Payouts**
- Real-time payout display updates as you build
- Power Play multipliers: **3x to 37.5x**
- Flex Play multipliers: **0.4x to 25x**
- Demon/Goblin modifiers apply additional multipliers

### 4. **Simulate & Analyze**
- Run AI simulations to see win probabilities
- Get beginner-friendly explanations of each pick
- View Monte Carlo simulation results (10,000+ game scenarios)

### 5. **Place Paper Bets**
- Submit bets using virtual currency
- Track your balance and betting history
- Compete on leaderboards

---

## 🎨 Design Philosophy

### User-Centric Design
- **Beginner-Friendly**: No jargon, AI explains everything in plain English
- **Visual Clarity**: Color-coded modifiers (red for demons, green for goblins)
- **Instant Feedback**: Real-time payout calculations and stat updates

### Innovation in Engagement
- **Gamification**: Demons & Goblins add strategic depth beyond traditional betting
- **Risk Management**: Flexible play styles from conservative (goblins) to aggressive (demons)
- **Social Competition**: Leaderboards and shareable results encourage community

---

## 📊 API Documentation

### Core Endpoints

#### Daily Props
```
GET  /api/daily-props/today          # Today's props for popular players
GET  /api/daily-props/tomorrow       # Tomorrow's props
POST /api/daily-props/simulate-bet   # Simulate single prop outcome
POST /api/daily-props/place-bet      # Place paper bet
POST /api/daily-props/place-parlay   # Place multi-leg parlay
GET  /api/daily-props/balance/:user  # Check balance
```

#### Simulation
```
POST /api/simulation/single-game     # Simulate one game
POST /api/simulation/bet-outcome     # Simulate bet result
POST /api/simulation/multi-leg-ticket # Simulate parlay
GET  /api/simulation/quick-odds/:player # Get quick odds
```

#### Beginner Analysis
```
GET  /api/beginner/players/:name/beginner-analysis # Get AI explanation
POST /api/beginner/analyze-prop/beginner          # Analyze single prop
POST /api/beginner/analyze-ticket/beginner        # Analyze full ticket
```

Full API documentation available at `http://localhost:8000/docs` (Swagger UI)

---

## 🏆 What Makes This Special

### Technical Innovation
✅ **Hybrid Simulation Engine**: Combines Monte Carlo methods with ML predictions  
✅ **Real-Time Multiplier Calculations**: Complex payout logic with modifier stacking  
✅ **Type-Safe Architecture**: Full TypeScript implementation prevents runtime errors  
✅ **Optimized Performance**: Lazy loading, code splitting, and efficient state management

### User Experience Innovation
✅ **One-Click Modifiers**: Toggle demons/goblins without complexity  
✅ **Smart Validation**: Prevents invalid selections (e.g., LESS with active demons)  
✅ **Visual Storytelling**: Borders, badges, and colors communicate game state instantly  
✅ **Progressive Disclosure**: Advanced features accessible but not overwhelming

### Business Innovation
✅ **Lower Barrier to Entry**: Paper betting removes financial risk for newcomers  
✅ **Educational Value**: AI explanations teach users about sports analytics  
✅ **Engagement Hooks**: Modifiers and simulations keep users coming back  
✅ **Scalable Architecture**: FastAPI + React ready for production deployment

---

## 👥 Team

This project was built by a team of 4 passionate developers for the PrizePicks Hackathon 2025.

---

## 🔮 Future Enhancements

### Phase 1 (Post-Hackathon)
- [ ] User authentication and profile management
- [ ] Historical bet tracking and analytics dashboard
- [ ] Social features (share lineups, follow friends)
- [ ] Push notifications for game starts and bet outcomes

### Phase 2
- [ ] Live in-game stat tracking and mid-game betting
- [ ] Expanded modifier system (Wizards, Trolls, etc.)
- [ ] Tournament mode with prize pools
- [ ] Mobile app (React Native)

### Phase 3
- [ ] Multi-sport support (NFL, MLB, NHL)
- [ ] Advanced AI: Personalized prop recommendations
- [ ] Blockchain integration for provably fair simulations
- [ ] API marketplace for third-party integrations

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **PrizePicks** for hosting the hackathon and inspiring this project
- **NBA.com** for comprehensive player statistics
- **AWS** for Bedrock AI capabilities
- **Open Source Community** for the amazing tools and libraries

---

## 📞 Contact

Built with ❤️ for the PrizePicks "Next-Gen Game Flow" Hackathon

**Live Demo**: [Coming Soon]  
**Documentation**: See `/frontend` and `/backend` directories for detailed guides

---

## 🎮 Try It Out!

```bash
# Quick Start (from project root)
npm install --prefix frontend
pip install -r backend/requirements.txt
npm run dev --prefix frontend &
python3 run.py
```


# 🏀 FanAssist - Next-Gen NBA Sports Engagement Platform

> **PrizePicks Hackathon 2025 Submission**  
> **Track:** Next-Gen Game Flow - Re-imagining Real-Time Sports Engagement

A revolutionary sports engagement platform that combines AI-powered player analysis, real-time game simulation, and innovative betting mechanics to create an immersive, beginner-friendly experience for NBA fans.

---

## 🎯 The Challenge

Traditional sports betting platforms can be intimidating for newcomers and lack the real-time insights needed to make informed decisions. We set out to solve this by building a platform that:

- **Democratizes Sports Betting**: Makes prop betting accessible to beginners with AI-powered explanations
- **Provides Real-Time Intelligence**: Uses machine learning to simulate games and predict player performance
- **Gamifies the Experience**: Introduces innovative "Demons & Goblins" modifier system for dynamic risk/reward
- **Offers Safe Practice**: Paper betting with virtual currency lets users learn without financial risk

---

## ✨ Key Features

### 🎲 Demons & Goblins Modifier System
Our flagship innovation that transforms traditional prop betting:

- **Demon Players** 🔥: High-risk, high-reward modifiers that boost projections and multiply payouts
  - Projected stat increases by 4.0-5.5 points
  - Payout multipliers: **10x to 2000x** (scales with lineup size)
  - Visual indicators: Red borders, badges, and stat highlights

- **Goblin Players** 👺: Conservative plays that lower projections but provide safer bets
  - Projected stat decreases by 3.0 points
  - Payout reductions: **0.5x to 0.2x** (compound multiplicatively)
  - Visual indicators: Green borders, badges, and stat highlights

- **Dynamic Toggle System**: One-click modifier activation with real-time payout calculations
- **Smart Restrictions**: Prevents conflicting selections (e.g., LESS disabled when demon modifier active)

### 🧠 AI-Powered Analysis
Leveraging AWS Bedrock and advanced ML models:

- **Beginner-Friendly Explanations**: AI breaks down complex stats into easy-to-understand insights
- **Game Simulation Engine**: Monte Carlo simulations predict player performance across 10,000+ game scenarios
- **Machine Learning Predictions**: ML models analyze historical data, matchups, and trends
- **Real-Time Odds Calculation**: Instantly see win probabilities for any prop or parlay

### 💰 Paper Betting System
Risk-free practice environment:

- **Virtual Currency**: Start with $10,000 in paper money
- **Full Betting Simulation**: Place Power Plays (2-6 legs) and Flex Plays with real payout structures
- **Live Result Tracking**: Simulate bet outcomes based on AI predictions
- **Leaderboards**: Compete with friends to build the best virtual bankroll

### 📊 Real-Time Data Integration
Powered by NBA stats and PrizePicks API:

- **Live Player Projections**: Up-to-date stat lines for Points, Rebounds, Assists, 3-Pointers, and more
- **Daily Props**: Curated props for popular players updated daily
- **Injury Tracking**: Automatic filtering and warnings for injured players
- **Schedule Integration**: Complete game schedules with matchup analysis

### 🎨 Immersive User Experience
Built with modern design principles:

- **Dark/Light Theme Toggle**: Personalized viewing experience
- **Smooth Animations**: Scroll-triggered reveals and falling confetti celebrations
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Real-Time Payout Calculator**: See potential winnings update as you build your lineup
- **Welcome Tutorial**: Guided onboarding for new users

---

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript for type-safe component architecture
- **Vite** for lightning-fast development and optimized builds
- **Tailwind CSS v4** for modern, utility-first styling
- **Lucide React** for beautiful iconography
- **LocalStorage** for persistent state management

### Backend
- **FastAPI** (Python) for high-performance REST API
- **NBA API** for real-time player stats and game data
- **AWS Bedrock** for AI-powered analysis and natural language generation
- **NumPy/Pandas** for statistical analysis and simulation
- **PrizePicks API** integration for prop lines

### Development Tools
- **Docker** for containerized deployment
- **ESLint** for code quality
- **Git** for version control

---

## 🚀 Getting Started

### Prerequisites
- **Node.js** 18+ and npm/yarn
- **Python** 3.9+
- **Docker** (optional, for containerized deployment)

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --reload
```

The backend API will be available at `http://localhost:8000`

### Docker Deployment (Optional)

```bash
# Build and run with Docker Compose
docker-compose up --build
```

---

## 📖 How It Works

### 1. **Browse Players**
- Filter by category (Popular, Guards, Forwards, Centers)
- View live projections for all major stat categories
- See injury status and game matchups

### 2. **Build Your Lineup**
- Select 2-6 players for a Power Play or Flex Play
- Choose OVER or UNDER for each stat projection
- Activate Demon or Goblin modifiers for dynamic gameplay

### 3. **Calculate Payouts**
- Real-time payout display updates as you build
- Power Play multipliers: **3x to 37.5x**
- Flex Play multipliers: **0.4x to 25x**
- Demon/Goblin modifiers apply additional multipliers

### 4. **Simulate & Analyze**
- Run AI simulations to see win probabilities
- Get beginner-friendly explanations of each pick
- View Monte Carlo simulation results (10,000+ game scenarios)

### 5. **Place Paper Bets**
- Submit bets using virtual currency
- Track your balance and betting history
- Compete on leaderboards

---

## 🎨 Design Philosophy

### User-Centric Design
- **Beginner-Friendly**: No jargon, AI explains everything in plain English
- **Visual Clarity**: Color-coded modifiers (red for demons, green for goblins)
- **Instant Feedback**: Real-time payout calculations and stat updates

### Innovation in Engagement
- **Gamification**: Demons & Goblins add strategic depth beyond traditional betting
- **Risk Management**: Flexible play styles from conservative (goblins) to aggressive (demons)
- **Social Competition**: Leaderboards and shareable results encourage community

---

## 📊 API Documentation

### Core Endpoints

#### Daily Props
```
GET  /api/daily-props/today          # Today's props for popular players
GET  /api/daily-props/tomorrow       # Tomorrow's props
POST /api/daily-props/simulate-bet   # Simulate single prop outcome
POST /api/daily-props/place-bet      # Place paper bet
POST /api/daily-props/place-parlay   # Place multi-leg parlay
GET  /api/daily-props/balance/:user  # Check balance
```

#### Simulation
```
POST /api/simulation/single-game     # Simulate one game
POST /api/simulation/bet-outcome     # Simulate bet result
POST /api/simulation/multi-leg-ticket # Simulate parlay
GET  /api/simulation/quick-odds/:player # Get quick odds
```

#### Beginner Analysis
```
GET  /api/beginner/players/:name/beginner-analysis # Get AI explanation
POST /api/beginner/analyze-prop/beginner          # Analyze single prop
POST /api/beginner/analyze-ticket/beginner        # Analyze full ticket
```

Full API documentation available at `http://localhost:8000/docs` (Swagger UI)

---

## 🏆 What Makes This Special

### Technical Innovation
✅ **Hybrid Simulation Engine**: Combines Monte Carlo methods with ML predictions  
✅ **Real-Time Multiplier Calculations**: Complex payout logic with modifier stacking  
✅ **Type-Safe Architecture**: Full TypeScript implementation prevents runtime errors  
✅ **Optimized Performance**: Lazy loading, code splitting, and efficient state management

### User Experience Innovation
✅ **One-Click Modifiers**: Toggle demons/goblins without complexity  
✅ **Smart Validation**: Prevents invalid selections (e.g., LESS with active demons)  
✅ **Visual Storytelling**: Borders, badges, and colors communicate game state instantly  
✅ **Progressive Disclosure**: Advanced features accessible but not overwhelming

### Business Innovation
✅ **Lower Barrier to Entry**: Paper betting removes financial risk for newcomers  
✅ **Educational Value**: AI explanations teach users about sports analytics  
✅ **Engagement Hooks**: Modifiers and simulations keep users coming back  
✅ **Scalable Architecture**: FastAPI + React ready for production deployment

---

## 👥 Team

This project was built by a team of 4 passionate developers for the PrizePicks Hackathon 2025.

---

## 🔮 Future Enhancements

### Phase 1 (Post-Hackathon)
- [ ] User authentication and profile management
- [ ] Historical bet tracking and analytics dashboard
- [ ] Social features (share lineups, follow friends)
- [ ] Push notifications for game starts and bet outcomes

### Phase 2
- [ ] Live in-game stat tracking and mid-game betting
- [ ] Expanded modifier system (Wizards, Trolls, etc.)
- [ ] Tournament mode with prize pools
- [ ] Mobile app (React Native)

### Phase 3
- [ ] Multi-sport support (NFL, MLB, NHL)
- [ ] Advanced AI: Personalized prop recommendations
- [ ] Blockchain integration for provably fair simulations
- [ ] API marketplace for third-party integrations

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **PrizePicks** for hosting the hackathon and inspiring this project
- **NBA.com** for comprehensive player statistics
- **AWS** for Bedrock AI capabilities
- **Open Source Community** for the amazing tools and libraries

---

## 📞 Contact

Built with ❤️ for the PrizePicks "Next-Gen Game Flow" Hackathon

**Live Demo**: [Coming Soon]  
**Documentation**: See `/frontend` and `/backend` directories for detailed guides

---

## 🎮 Try It Out!

```bash
# Quick Start (from project root)
npm install --prefix frontend
pip install -r backend/requirements.txt
npm run dev --prefix frontend &
python3 run.py
```


