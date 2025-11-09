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
    if (showPopup) {
      // Disable scrolling
      document.body.style.overflow = 'hidden';
    } else {
      // Enable scrolling
      document.body.style.overflow = 'unset';
    }

    // Cleanup: ensure scrolling is re-enabled when component unmounts
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [showPopup]);

  const handleClose = () => {
    setShowPopup(false);
    setCurrentStep(1);
    if (onClose) {
      onClose();
    }
  };

  const handleNext = () => {
    // Scroll to top of page
    window.scrollTo({ top: 0, behavior: 'smooth' });
    // Delay showing the categories box
    setTimeout(() => {
      setCurrentStep(2);
    }, 300);
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
                top: "140px",
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
                    onClick={handleClose}
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
    </>
  );
};
