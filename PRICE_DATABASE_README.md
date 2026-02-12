# BIO Ingredient Price Database

This file documents the BIO ingredient price database used for cost estimation in recipes.

## File Location

`ingredient_prices.yaml`

## Purpose

Provides estimated costs for BIO/organic ingredients in EUR (€) to calculate:
- Individual recipe costs
- Shopping list total costs
- Budget planning

## Price Sources

Prices are estimates based on typical German BIO supermarket prices (REWE Bio, Edeka Bio, Bio Company, etc.).

**Important:** Prices are approximations and actual costs may vary by:
- Location/region
- Season
- Retailer
- Product brand
- Package size

## Updating Prices

### When to Update

- **Quarterly** - Check prices every 3 months
- **After major inflation** - When general food prices change significantly
- **When adding new ingredients** - Research current BIO prices

### How to Update

1. Open `ingredient_prices.yaml`
2. For each ingredient, check current BIO prices at:
   - REWE Bio online shop (https://www.rewe.de/bio)
   - Edeka Bio (https://www.edeka.de)
   - Bio Company
   - Local BIO supermarkets
3. Update the `price` field with average price
4. Run `python main.py` to regenerate costs
5. Commit changes to git

### Format

```yaml
Ingredient_Name: {price: XX.XX, unit: "kg/L/piece/bunch", notes: "optional"}
```

**Units:**
- `kg` - Kilograms (for solid items)
- `L` - Liters (for liquids)
- `piece` - Individual items (eggs, garlic cloves, cucumbers)
- `bunch` - Bunches (herbs like parsley, basil)

**Examples:**
```yaml
Tomaten: {price: 5.00, unit: "kg"}
Milch: {price: 1.50, unit: "L"}
Eier: {price: 0.50, unit: "piece"}
Petersilie: {price: 0.80, unit: "bunch"}
```

## Coverage

The database includes ~100+ common ingredients. For ingredients not in the database:
- Cost will show as 0 or "partially estimated"
- Add missing ingredients with researched BIO prices
- Use similar items as price reference

## Calculation Method

Costs are calculated by:
1. Parsing ingredient amounts from recipes
2. Converting to standard units (kg, L, pieces)
3. Multiplying by price from database
4. Scaling based on recipe servings

## Last Major Update

**Date:** February 12, 2026
**Source:** Initial estimates based on typical German BIO prices
**Next Review:** May 2026

## Notes

- Prices assume **BIO/organic quality**
- Some items (spices, herbs in small amounts) may show as "negligible cost"
- Canned items are priced per can/unit
- Prices include average quality BIO products (not premium brands)

## Contributing Price Updates

When updating prices, please:
1. Use BIO/organic sources only
2. Take average of 2-3 retailers
3. Document source in git commit message
4. Round to reasonable precision (usually 2 decimal places)

## Disclaimer

These are **estimated costs** for planning purposes only. Actual shopping costs will vary based on individual shopping habits, retailers, and current market conditions.
