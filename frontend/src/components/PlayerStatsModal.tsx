import { motion, AnimatePresence } from "motion/react";
import { X } from "lucide-react";

interface GameData {
  date: string;
  opponent: string;
  statValue: number;
}

interface PlayerStatsModalProps {
  isOpen: boolean;
  onClose: () => void;
  playerName: string;
  category: string;
  propLine: number;
  // For now, we'll use mock data. Later this will be replaced with real data
  lastFiveGames?: GameData[];
}

/**
 * PlayerStatsModal Component
 * Shows a modal with player's last 5 games performance
 * Left side: Bar graph
 * Top right: Prop line and category
 * Bottom right: Table of last 5 games
 */
export const PlayerStatsModal = ({
  isOpen,
  onClose,
  playerName,
  category,
  propLine,
  lastFiveGames = [],
}: PlayerStatsModalProps) => {
  // Mock data for now (will be replaced with real API data)
  const mockGames: GameData[] = lastFiveGames.length > 0 ? lastFiveGames : [
    { date: "12/08", opponent: "vs MIA", statValue: 28.0 },
    { date: "12/06", opponent: "@ BOS", statValue: 24.0 },
    { date: "12/04", opponent: "vs PHX", statValue: 31.0 },
    { date: "12/02", opponent: "@ GSW", statValue: 22.0 },
    { date: "11/30", opponent: "vs DEN", statValue: 27.0 },
  ];

  const maxValue = Math.max(...mockGames.map(g => g.statValue), propLine) * 1.1;

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 z-50 backdrop-blur-sm"
            onClick={onClose}
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50"
            style={{ width: "1000px" }}
          >
            <div className="bg-card-bg border-2 border-card-border rounded-lg shadow-2xl overflow-hidden">
              {/* Header */}
              <div className="bg-surface border-b border-card-border flex items-center justify-between" style={{ padding: "8px 12px" }}>
                <h2 className="text-base font-bold text-text">{playerName}</h2>
                <button
                  onClick={onClose}
                  className="p-1 hover:bg-card-bg rounded transition-colors"
                >
                  <X className="w-3 h-3 text-text" />
                </button>
              </div>

              {/* Content - Side by Side */}
              <div style={{ padding: "16px", display: "flex", gap: "40px", height: "320px" }}>
                {/* Left Side - Bar Graph */}
                <div style={{ flex: 1, position: "relative", paddingRight: "100px" }}>
                  {/* Y-axis */}
                  <div
                    className="absolute left-0 top-0 bg-text-muted"
                    style={{ width: "2px", height: "240px" }}
                  />
                  {/* X-axis */}
                  <div
                    className="absolute left-0 bg-text-muted"
                    style={{ width: "calc(100% - 100px)", height: "2px", top: "240px" }}
                  />

                  {/* Prop Line */}
                  <div
                    className="absolute left-0 border-t-2 border-dashed"
                    style={{
                      borderColor: "var(--color-accent1)",
                      width: "calc(100% - 100px)",
                      top: `${240 - ((propLine / maxValue) * 240)}px`,
                    }}
                  />

                  {/* Line Label - Always on the right */}
                  <div
                    className="absolute text-xs font-semibold px-2 py-0.5 rounded"
                    style={{
                      backgroundColor: "var(--color-accent1)",
                      color: "white",
                      right: "0",
                      top: `${240 - ((propLine / maxValue) * 240) - 12}px`,
                    }}
                  >
                    Line: {propLine.toFixed(1)}
                  </div>

                  {/* Bars */}
                  <div className="absolute flex items-end justify-around" style={{ left: "30px", right: "120px", top: "0", height: "240px", gap: "16px" }}>
                    {mockGames.map((game, index) => {
                      const barHeight = (game.statValue / maxValue) * 240;
                      const isAboveLine = game.statValue > propLine;

                      return (
                        <div
                          key={index}
                          className="flex flex-col items-center"
                          style={{ width: "40px" }}
                        >
                          {/* Bar */}
                          <div
                            className="w-full"
                            style={{
                              height: `${barHeight}px`,
                              backgroundColor: isAboveLine
                                ? "var(--btn-success)"
                                : "var(--btn-error)",
                            }}
                          />
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Right Side - Single Column */}
                <div style={{ width: "340px", display: "flex", flexDirection: "column" }}>
                  {/* Prop Info - Compact inline layout */}
                  <div className="bg-surface rounded-lg border border-card-border" style={{ padding: "10px 12px", marginBottom: "12px" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                      <div>
                        <div className="text-xs text-text-muted">Category</div>
                        <div className="text-sm font-bold text-text">{category}</div>
                      </div>
                      <div style={{ textAlign: "right" }}>
                        <div className="text-xs text-text-muted">Prop Line</div>
                        <div
                          className="text-xl font-bold"
                          style={{ color: "var(--color-accent1)" }}
                        >
                          {propLine.toFixed(1)}
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Game Table */}
                  <div className="bg-surface rounded-lg border border-card-border flex-1" style={{ padding: "10px 12px", overflow: "hidden" }}>
                    <h4 className="text-xs font-semibold text-text" style={{ marginBottom: "8px" }}>Last 5 Games</h4>
                    <div>
                      {/* Table Header */}
                      <div className="grid grid-cols-3 gap-2 text-xs font-semibold text-text-muted border-b border-card-border" style={{ paddingBottom: "6px" }}>
                        <div>Date</div>
                        <div>Opponent</div>
                        <div className="text-right">Result</div>
                      </div>
                      {/* Table Rows */}
                      {mockGames.map((game, index) => (
                        <div
                          key={index}
                          className="grid grid-cols-3 gap-2 text-xs"
                          style={{ paddingTop: "6px", paddingBottom: "6px" }}
                        >
                          <div className="text-text">{game.date}</div>
                          <div className="text-text">{game.opponent}</div>
                          <div
                            className="text-right font-semibold"
                            style={{
                              color: game.statValue > propLine
                                ? "#ffffff"
                                : "#ffffff",
                            }}
                          >
                            {game.statValue.toFixed(1)}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};
