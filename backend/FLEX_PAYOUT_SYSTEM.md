# Flex Payout System

## Overview
The Flex bet mode allows players to win even if they miss 1 or 2 picks, with reduced payouts based on a fixed multiplier table.

## Payout Table

| Lineup Size | All Picks Correct | Miss One Pick | Miss Two Picks |
|-------------|-------------------|---------------|----------------|
| **6 Picks** | 25x               | 2x (5/6)      | 0.4x (4/6)     |
| **5 Picks** | 10x               | 2x (4/5)      | 0.4x (3/5)     |
| **4 Picks** | 6x                | 1.5x (3/4)    | N/A            |
| **3 Picks** | 3x                | 1x (2/3)      | N/A            |

## Examples

### 6-Leg Parlay - $50 Wager

- **All 6 correct**: $50 × 25 = **$1,250 payout** ($1,200 profit)
- **5 out of 6 correct**: $50 × 2 = **$100 payout** ($50 profit)
- **4 out of 6 correct**: $50 × 0.4 = **$20 payout** ($30 loss)
- **3 or fewer correct**: $0 payout ($50 loss)

### 5-Leg Parlay - $100 Wager

- **All 5 correct**: $100 × 10 = **$1,000 payout** ($900 profit)
- **4 out of 5 correct**: $100 × 2 = **$200 payout** ($100 profit)
- **3 out of 5 correct**: $100 × 0.4 = **$40 payout** ($60 loss)
- **2 or fewer correct**: $0 payout ($100 loss)

### 4-Leg Parlay - $75 Wager

- **All 4 correct**: $75 × 6 = **$450 payout** ($375 profit)
- **3 out of 4 correct**: $75 × 1.5 = **$112.50 payout** ($37.50 profit)
- **2 or fewer correct**: $0 payout ($75 loss)

### 3-Leg Parlay - $50 Wager

- **All 3 correct**: $50 × 3 = **$150 payout** ($100 profit)
- **2 out of 3 correct**: $50 × 1 = **$50 payout** ($0 profit/loss - push)
- **1 or fewer correct**: $0 payout ($50 loss)

## Rules

1. **Minimum legs**: 3
2. **Maximum legs**: 6
3. **Miss tolerance**:
   - 3-4 leg parlays: Can miss 1 pick
   - 5-6 leg parlays: Can miss up to 2 picks
4. **Fixed multipliers**: Payouts are predetermined and don't change based on odds

## Comparison: Flex vs Standard (Power)

### 6-Leg Parlay Example ($50 wager)

| Outcome | Standard Mode | Flex Mode |
|---------|---------------|-----------|
| 6/6 wins | ~$3,000+ | $1,250 |
| 5/6 wins | $0 | $100 |
| 4/6 wins | $0 | $20 |
| 3/6 wins | $0 | $0 |

**Key Difference**: 
- **Standard (Power)**: Higher potential payout but all-or-nothing
- **Flex**: Lower max payout but insurance against 1-2 losses

## When to Use Flex

✅ **Use Flex when:**
- You're confident in most picks but not 100% on all
- You want insurance against one bad call
- You prefer consistent smaller wins over rare big wins
- Building a 5-6 leg parlay (best value with miss-two option)

❌ **Avoid Flex when:**
- You're extremely confident in ALL picks
- You want maximum payout potential
- Betting small parlays (3 legs have low flex advantage)

## Backend Implementation

The flex payout logic is implemented in `backend/app/routes/daily_props.py`:

```python
flex_payouts = {
    6: {"all": 25.0, "miss_one": 2.0, "miss_two": 0.4},
    5: {"all": 10.0, "miss_one": 2.0, "miss_two": 0.4},
    4: {"all": 6.0, "miss_one": 1.5, "miss_two": 0.0},
    3: {"all": 3.0, "miss_one": 1.0, "miss_two": 0.0}
}
```

### Payout Calculation

```python
if num_losses == 0:
    # All correct
    payout = wager × full_win_multiplier
elif num_losses == 1:
    # Miss one
    payout = wager × flex_win_multiplier
elif num_losses == 2 and flex_miss_two_multiplier > 0:
    # Miss two (5-6 leg only)
    payout = wager × flex_miss_two_multiplier
else:
    # Lost
    payout = 0
```

## Testing

Test the flex system with different scenarios:

```bash
# Test 6-leg flex (all wins)
curl -X POST http://localhost:8000/api/daily-props/place-parlay \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "legs": [...],  # 6 legs
    "total_wager": 50,
    "bet_mode": "flex"
  }'

# Expected: bet_result = "full_win", payout = $1,250
```

## UI Display

In the frontend, show flex rules clearly:

```
Mode: 🎯 Flex
Rules: All correct: 25x | Miss 1: 2x | Miss 2: 0.4x
```

For 3-4 leg parlays (no miss-two):
```
Mode: 🎯 Flex  
Rules: All correct: 6x | Miss 1: 1.5x
```
