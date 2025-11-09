import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "motion/react";

interface WelcomePopupProps {
  onClose?: () => void;
  triggerDelay?: number;
}

/**
 * WelcomePopup Component
 * Displays a welcome message popup that appears after scrolling to cards section
 * with a backdrop blur effect
 */
export const WelcomePopup = ({
  onClose,
  triggerDelay = 2000,
}: WelcomePopupProps) => {
  const [showPopup, setShowPopup] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  const hasTriggeredRef = useRef(false);

  useEffect(() => {
    // Check scroll position to determine if user has scrolled down
    const handleScroll = () => {
      if (!hasTriggeredRef.current && window.scrollY > 300) {
        hasTriggeredRef.current = true;
        // Show popup after delay
        setTimeout(() => {
          setShowPopup(true);
        }, triggerDelay);
        // Remove listener after triggering
        window.removeEventListener('scroll', handleScroll);
      }
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [triggerDelay]);

  // Lock/unlock scroll when popup is shown/hidden
  useEffect(() => {
    if (showPopup && currentStep !== 3) {
      // Disable scrolling for steps 1 and 2
      document.body.style.overflow = 'hidden';
    } else {
      // Enable scrolling for step 3 or when popup is closed
      document.body.style.overflow = 'unset';
    }

    // Cleanup: ensure scrolling is re-enabled when component unmounts
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [showPopup, currentStep]);

  const handleClose = () => {
    setShowPopup(false);
    setCurrentStep(1);
    if (onClose) {
      onClose();
    }
  };

  const handleNext = () => {
    if (currentStep === 1) {
      // Scroll to top of page for step 2
      window.scrollTo({ top: 0, behavior: 'smooth' });
      // Delay showing the categories box
      setTimeout(() => {
        setCurrentStep(2);
      }, 300);
    } else if (currentStep === 2) {
      // Scroll down to cards for step 3
      window.scrollTo({ top: 400, behavior: 'smooth' });
      // Delay showing the player cards overlay
      setTimeout(() => {
        setCurrentStep(3);
      }, 300);
    }
  };

  return (
    <>
      {/* Popup with backdrop */}
      <AnimatePresence>
        {showPopup && currentStep === 1 && (
          <>
            {/* Blurred backdrop - only for step 1 */}
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="fixed inset-0 z-40"
              style={{
                backdropFilter: "blur(8px)",
                backgroundColor: "rgba(0, 0, 0, 0.3)",
              }}
              onClick={handleClose}
            />

            {/* Welcome popup - centered with falling animation */}
            <div className="fixed top-0 left-0 w-full h-full flex items-center justify-center z-50 p-4">
              <motion.div
                initial={{
                  y: -50,
                  opacity: 0,
                  scale: 0.8,
                }}
                animate={{
                  y: 0,
                  opacity: 1,
                  scale: 1,
                }}
                exit={{
                  y: -50,
                  opacity: 0,
                  scale: 0.8,
                }}
                transition={{
                  type: "spring",
                  damping: 15,
                  stiffness: 200,
                  duration: 0.5,
                }}
                className="relative max-w-md w-full p-3 rounded-lg shadow-2xl"
                style={{
                  backgroundColor: "#7f00ff",
                  color: "white",
                }}
              >
                {/* Content */}
                <div>
                  <h2 className="text-xl font-bold mb-3 text-left underline">Welcome to FanAssist!</h2>
                  <p className="text-sm leading-relaxed text-left mb-4">
                    We'll help get you started with PrizePicks and how it works, and at the end,
                    provide you with useful insights for you to use with PrizePicks!
                  </p>
                  <div className="flex justify-end">
                    <button
                      onClick={handleNext}
                      className="bg-white text-purple-700 rounded font-semibold text-sm hover:bg-gray-100 transition-colors"
                      style={{ padding: "6px 12px" }}
                    >
                      Next
                    </button>
                  </div>
                </div>
              </motion.div>
            </div>
          </>
        )}
      </AnimatePresence>

      {/* Categories popup - no blur, positioned at top pointing down */}
      <AnimatePresence>
        {showPopup && currentStep === 2 && (
          <motion.div
              initial={{
                y: -50,
                opacity: 0,
              }}
              animate={{
                y: 0,
                opacity: 1,
              }}
              exit={{
                y: -50,
                opacity: 0,
              }}
              transition={{
                type: "spring",
                damping: 15,
                stiffness: 200,
                duration: 0.5,
              }}
              className="fixed z-50 max-w-md w-full px-4"
              style={{
                top: "110px",
                left: "40%",
                transform: "translateX(-50%)",
              }}
            >
            <div
              className="relative rounded-lg shadow-2xl"
              style={{
                backgroundColor: "#7f00ff",
                color: "white",
                padding: "18px",
              }}
            >
              {/* Content */}
              <div>
                <h2 className="text-xl font-bold text-left underline" style={{ marginBottom: "8px" }}>Categories</h2>
                <p className="text-sm leading-relaxed text-left" style={{ marginBottom: "12px" }}>
                  Use the category filters below to view different lines. Select any stat you like!
                </p>
                <div className="flex justify-end">
                  <button
                    onClick={handleNext}
                    className="bg-white text-purple-700 rounded font-semibold text-sm hover:bg-gray-100 transition-colors"
                    style={{ padding: "6px 12px" }}
                  >
                    Next
                  </button>
                </div>
              </div>

              {/* Down arrow pointer */}
              <div
                className="absolute left-1/2"
                style={{
                  bottom: "-10px",
                  transform: "translateX(-50%)",
                  width: 0,
                  height: 0,
                  borderLeft: "10px solid transparent",
                  borderRight: "10px solid transparent",
                  borderTop: "10px solid #7f00ff",
                }}
              />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Player Cards Explanation - bottom-right overlay */}
      <AnimatePresence>
        {showPopup && currentStep === 3 && (
          <motion.div
            initial={{
              x: 50,
              opacity: 0,
            }}
            animate={{
              x: 0,
              opacity: 1,
            }}
            exit={{
              x: 50,
              opacity: 0,
            }}
            transition={{
              type: "spring",
              damping: 20,
              stiffness: 150,
              duration: 0.5,
            }}
            className="fixed bottom-6 right-6 z-50 w-full max-w-md"
            style={{
              maxHeight: "calc(100vh - 120px)",
            }}
          >
            <div
              className="relative rounded-lg shadow-2xl overflow-hidden"
              style={{
                backgroundColor: "#7f00ff",
                color: "white",
              }}
            >
              {/* Scrollable content */}
              <div
                style={{
                  maxHeight: "calc(100vh - 200px)",
                  overflowY: "auto",
                  padding: "18px",
                }}
              >
                <h2
                  className="text-xl font-bold text-left underline"
                  style={{
                    marginBottom: "8px",
                  }}
                >
                  Understanding Player Cards
                </h2>

                <div>
                  <p className="text-sm leading-relaxed text-left" style={{ marginBottom: "12px" }}>
                    Each player card displays information about the player and their line. 
                  </p>

                  <ul className="text-sm leading-relaxed text-left" style={{ marginBottom: "12px", paddingLeft: "20px" }}>
                    <li style={{ marginBottom: "8px" }}>
                      The player's name and position are located at the top of each card
                    </li>
                    <li style={{ marginBottom: "8px" }}>
                      The matchup info shows the opponent and game time
                    </li>
                    <li style={{ marginBottom: "8px" }}>
                      The large number displays the projected value for the selected category
                    </li>
                    <li style={{ marginBottom: "8px" }}>
                      Select whether you think the player will score more or less than the projection
                    </li>
                  </ul>

                  <p className="text-sm leading-relaxed text-left" style={{ marginBottom: "12px" }}>
                    When selecting players, you'll notice a demon or goblin icon in some of the cards. Demons and goblins are non-standard payouts, where demons pay more, but are riskier and less likely to win, and vice versa for goblins.
                  </p>
                </div>
              </div>

              {/* Navigation buttons */}
              <div
                className="flex justify-end items-center"
                style={{
                  padding: "0 18px 18px 18px",
                }}
              >
                <button
                  onClick={handleClose}
                  className="bg-white text-purple-700 rounded font-semibold text-sm hover:bg-gray-100 transition-colors"
                  style={{
                    padding: "6px 12px",
                  }}
                >
                  Next
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};
