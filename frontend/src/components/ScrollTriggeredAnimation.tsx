import { useEffect, useRef, useState } from "react";
import { FallingAnimation } from "./FallingAnimation";
import type { ReactNode } from "react";

interface ScrollTriggeredAnimationProps {
  children: ReactNode;
  delay?: number;
  duration?: number;
  fallDistance?: number;
  className?: string;
  threshold?: number;
}

/**
 * ScrollTriggeredAnimation Component
 * Triggers the falling animation only when the element is scrolled into view
 */
export const ScrollTriggeredAnimation = ({
  children,
  delay = 0,
  duration = 0.5,
  fallDistance = 30,
  className = "",
  threshold = 0.1,
}: ScrollTriggeredAnimationProps) => {
  const [isVisible, setIsVisible] = useState(false);
  const elementRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          // Only trigger animation once when element comes into view
          if (entry.isIntersecting && !isVisible) {
            setIsVisible(true);
          }
        });
      },
      {
        threshold: threshold,
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
  }, [isVisible, threshold]);

  return (
    <div ref={elementRef}>
      {isVisible ? (
        <FallingAnimation
          delay={delay}
          duration={duration}
          fallDistance={fallDistance}
          className={className}
        >
          {children}
        </FallingAnimation>
      ) : (
        // Render invisible placeholder to maintain layout
        <div style={{ opacity: 0 }}>{children}</div>
      )}
    </div>
  );
};
