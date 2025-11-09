import type { ReactNode } from "react";
import { motion } from "motion/react";

interface FallingAnimationProps {
  children: ReactNode;
  delay?: number;
  duration?: number;
  fallDistance?: number;
  className?: string;
}

/**
 * FallingAnimation Component
 * Creates a "falling into place" animation where elements appear from above and fall into position
 */
export const FallingAnimation = ({
  children,
  delay = 0,
  duration = 0.6,
  fallDistance = 50,
  className = "",
}: FallingAnimationProps) => {
  return (
    <motion.div
      initial={{
        y: -fallDistance,
        opacity: 0,
        scale: 0.8,
      }}
      animate={{
        y: 0,
        opacity: 1,
        scale: 1,
      }}
      transition={{
        type: "spring",
        damping: 15,
        stiffness: 200,
        delay: delay,
        duration: duration,
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
};

/**
 * FallingAnimationSequence Component
 * Renders multiple elements that fall into place in sequence
 */
interface FallingAnimationSequenceProps {
  items: string[];
  className?: string;
  itemClassName?: string;
  staggerDelay?: number;
}

export const FallingAnimationSequence = ({
  items,
  className = "",
  itemClassName = "",
  staggerDelay = 0.1,
}: FallingAnimationSequenceProps) => {
  return (
    <div className={`flex flex-wrap gap-2 ${className}`}>
      {items.map((item, index) => (
        <FallingAnimation
          key={index}
          delay={index * staggerDelay}
          className={itemClassName}
        >
          <span>{item}</span>
        </FallingAnimation>
      ))}
    </div>
  );
};
