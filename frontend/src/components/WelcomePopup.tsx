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
  const [isVisible, setIsVisible] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const elementRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          // Only trigger once when element comes into view
          if (entry.isIntersecting && !isVisible) {
            setIsVisible(true);
            // Show popup after delay
            setTimeout(() => {
              setShowPopup(true);
            }, triggerDelay);
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: "0px",
      }
    );

    if (elementRef.current) {
      observer.observe(elementRef.current);
    }

    return () => {
      if (elementRef.current) {
        observer.unobserve(elementRef.current);
      }
    };
  }, [isVisible, triggerDelay]);

  const handleClose = () => {
    setShowPopup(false);
    if (onClose) {
      onClose();
    }
  };

  return (
    <>
      {/* Invisible trigger element */}
      <div ref={elementRef} style={{ position: "absolute", top: 0, left: 0, width: 1, height: 1 }} />

      {/* Popup with backdrop */}
      <AnimatePresence>
        {showPopup && (
          <>
            {/* Blurred backdrop */}
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

            {/* Popup box with falling animation */}
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
                {/* Close button - positioned from edge of box, not padding */}
                <button
                  onClick={handleClose}
                  className="absolute w-5 h-5 flex items-center justify-center hover:opacity-70 transition-opacity z-10"
                  aria-label="Close"
                  style={{
                    color: "white",
                    top: "4px",
                    right: "4px"
                  }}
                >
                  <span className="text-lg leading-none font-bold">&times;</span>
                </button>

                {/* Content */}
                <div>
                  <h2 className="text-xl font-bold mb-3 text-left underline">Welcome to FanAssist!</h2>
                  <p className="text-sm leading-relaxed text-left">
                    We'll help get you started with PrizePicks and how it works, and at the end,
                    provide you with useful insights for you to use with PrizePicks!
                  </p>
                </div>
              </motion.div>
            </div>
          </>
        )}
      </AnimatePresence>
    </>
  );
};
