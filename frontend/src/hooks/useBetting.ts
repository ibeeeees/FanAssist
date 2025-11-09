/**
 * Custom hook for managing betting functionality
 */

import { useState, useCallback } from 'react';
import { placeBet, placeParlay, getBalance, resetBalance, type BetRequest, type ParlayRequest } from '../services/api';

const DEFAULT_USERNAME = import.meta.env.VITE_DEFAULT_USERNAME || 'demo_user';
const BALANCE_CACHE_KEY = `balance_${DEFAULT_USERNAME}`;
const CACHE_DURATION = 30000; // 30 seconds

interface CachedBalance {
  balance: number;
  timestamp: number;
}

export function useBetting() {
  const [balance, setBalance] = useState<number | null>(() => {
    // Initialize from cache if available and valid
    try {
      const cached = localStorage.getItem(BALANCE_CACHE_KEY);
      if (cached) {
        const { balance: cachedBalance, timestamp }: CachedBalance = JSON.parse(cached);
        if (Date.now() - timestamp < CACHE_DURATION) {
          return cachedBalance;
        }
      }
    } catch (e) {
      console.error('Failed to load cached balance:', e);
    }
    return null;
  });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Save balance to cache
  const cacheBalance = (newBalance: number) => {
    try {
      const cached: CachedBalance = {
        balance: newBalance,
        timestamp: Date.now(),
      };
      localStorage.setItem(BALANCE_CACHE_KEY, JSON.stringify(cached));
    } catch (e) {
      console.error('Failed to cache balance:', e);
    }
  };

  // Fetch current balance
  const fetchBalance = useCallback(async (forceRefresh = false) => {
    // Check cache first if not forcing refresh
    if (!forceRefresh && balance !== null) {
      try {
        const cached = localStorage.getItem(BALANCE_CACHE_KEY);
        if (cached) {
          const { balance: cachedBalance, timestamp }: CachedBalance = JSON.parse(cached);
          if (Date.now() - timestamp < CACHE_DURATION) {
            console.log('📦 Using cached balance');
            return { balance: cachedBalance };
          }
        }
      } catch (e) {
        console.error('Cache check failed:', e);
      }
    }

    setIsLoading(true);
    setError(null);
    try {
      const response = await getBalance(DEFAULT_USERNAME);
      setBalance(response.balance);
      cacheBalance(response.balance);
      return response;
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to fetch balance';
      setError(errorMsg);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, [balance]);

  // Place a single bet
  const submitBet = useCallback(async (betData: BetRequest) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await placeBet(betData);
      // Update balance after bet
      const newBalance = result.betting_summary.new_balance;
      setBalance(newBalance);
      cacheBalance(newBalance);
      return result;
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to place bet';
      setError(errorMsg);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Place a parlay bet
  const submitParlay = useCallback(async (parlayData: Omit<ParlayRequest, 'username'>) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await placeParlay({
        ...parlayData,
        username: DEFAULT_USERNAME,
      });
      // Update balance after parlay
      if (result.betting_summary?.new_balance) {
        const newBalance = result.betting_summary.new_balance;
        setBalance(newBalance);
        cacheBalance(newBalance);
      }
      return result;
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to place parlay';
      setError(errorMsg);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Reset balance to starting amount
  const resetUserBalance = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await resetBalance(DEFAULT_USERNAME);
      const newBalance = result.new_balance;
      setBalance(newBalance);
      cacheBalance(newBalance);
      return result;
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to reset balance';
      setError(errorMsg);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  return {
    balance,
    isLoading,
    error,
    fetchBalance,
    submitBet,
    submitParlay,
    resetUserBalance,
  };
}
