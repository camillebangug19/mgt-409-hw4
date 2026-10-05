# Campus Customs Usability Improvements

This document records the four Problem 9 improvements and explains how each one benefits a Campus Customs shopper or the business.

## Frontend improvements

### 1. Save products with “Woofs”

- Improvement: Add a paw-print “Woof” control for logged-in shoppers on both the Products page and each individual product page. A shopper can use it to save an item, then revisit those products on a page titled “Your Woofs.”
- Why it helps a Campus Customs shopper or business: Shoppers can quickly return to products they are considering instead of searching again. The saved-item list also creates a clearer path back to future purchases and gives the business a useful signal of shopper interest.

### 2. Reposition authentication controls

- Improvement: Place the “Log In” and “Create Account” buttons in the upper-right header next to “Shop the collection.”
- Why it helps a Campus Customs shopper or business: Grouping account actions with the primary shopping action makes the navigation easier to understand and helps shoppers find account access when they are ready to browse or purchase.

## Backend improvements

### 3. Improve short-term conversational context

- Improvement: Give the agent recent conversation turns and the current product-page context so it can resolve references such as “this,” “that one,” and “the other one.” When the reference is ambiguous, the agent should ask for clarification and continue using exact catalogue data rather than guessing.
- Why it helps a Campus Customs shopper or business: Shoppers can speak naturally without repeating product names, while clarification safeguards keep product recommendations, prices, and availability accurate and protect the business from misleading answers.

### 4. Add robust backend error handling

- Improvement: Add clear handling for database failures, invalid product IDs, malformed requests, and agent or tool failures. The assistant should return a helpful explanation when something goes wrong and must never invent product information to compensate for a failed lookup.
- Why it helps a Campus Customs shopper or business: Shoppers receive actionable feedback instead of confusing failures, and the business gets safer, more predictable behavior when services or data are unavailable.
