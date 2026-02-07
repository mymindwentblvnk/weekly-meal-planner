# Future Ideas & Enhancements

This document tracks potential features and improvements for the recipe manager.

## High Priority

### Firebase Sync for localStorage
**Goal:** Sync user data (weekly plan, stats, views) across devices

**Benefits:**
- Data persists across devices (phone, tablet, computer)
- Survives browser cache clears
- Could share weekly plans with family/roommates
- Automatic backup
- Aggregate anonymous stats across all users

**Technical Approach:**
- Firebase Realtime Database or Firestore
- Firebase Authentication (anonymous auth to start)
- Hybrid storage: localStorage (primary/fast) + Firebase (sync/backup)
- Data structure:
  ```
  users/{userId}/
    weeklyMealPlan/
      recipes: [...]
      lastModified: timestamp
    recipeAddToPlanCount/
      {recipeName}: count
    recipeViews/
      {recipeName}: count
  ```

**Considerations:**
- Privacy notice and opt-in required
- Firebase free tier should cover traffic
- Add Firebase SDK (~50KB)
- Offline handling and merge conflicts
- Could make it optional feature

**Intermediate Step:**
- Export/import functionality (download/upload JSON)
- No backend needed, user controls data
- Works cross-device with manual transfer

## Medium Priority

### Recipe Images
- Add optional image field to YAML
- Display images on overview and detail pages
- Store in media folder or use external URLs
- Optimize for web (WebP, lazy loading)

### Advanced Search & Filtering
- Full-text search across ingredients, instructions, tags
- Filter by prep time range (quick: <30min, medium: 30-60min, slow: >60min)
- Filter by dietary restrictions (vegetarian, vegan, low-carb, etc.)
- Filter by ingredients you have
- "What can I cook?" feature - suggest recipes based on available ingredients

### Shopping List Integration
- Beyond Bring! widget: custom shopping list
- Add multiple recipes to list
- Combine duplicate ingredients
- Mark items as purchased
- Sync with weekly plan

### Meal Planning Enhancements
- Calendar view (assign recipes to specific dates)
- Drag-and-drop interface
- Meal prep mode (batch cooking suggestions)
- Leftovers tracking
- Portion calculator (scale servings up/down)

### Recipe Collections
- Create custom collections/folders
- "Favorites" collection
- "Quick weeknight dinners" collection
- "Batch cooking" collection
- Share collections via link

### Nutrition Information
- Add optional nutrition field to YAML
- Display calories, protein, carbs, fats
- Daily nutrition summary in weekly plan
- Track nutrition goals

### User Accounts
- Optional login (Firebase Auth)
- Save preferences (theme, default servings)
- Recipe notes and modifications
- Rating system for recipes

## Low Priority

### Print Styling
- Printer-friendly recipe pages
- Clean layout without navigation
- Include only essential information
- Checkbox list for ingredients/steps

### Progressive Web App (PWA)
- Install as app on mobile
- Offline support with service worker
- Push notifications for meal prep reminders

### Voice Commands
- Read recipe steps aloud while cooking
- Hands-free navigation
- Timer integration

### Recipe Scaling
- Automatic ingredient scaling based on servings
- Unit conversion (metric ↔ imperial)
- Batch cooking multipliers

### Social Features
- Share recipes via link
- Comments on recipes
- User-submitted recipes
- Recipe ratings and reviews

### Multi-Language Support
- i18n for interface
- Recipe translations
- Language switcher

### Theme Customization
- Dark mode (already have)
- Custom color schemes
- Font size adjustments
- Layout preferences

### Recipe Import Enhancements
- Support more recipe sites (HelloFresh, Chefkoch, allrecipes, etc.)
- Import from image (OCR)
- Import from PDF
- Bulk import

### Analytics & Insights
- Most cooked recipes over time
- Cooking frequency trends
- Average cook time per week
- Ingredient usage patterns
- Cost tracking per recipe

### Integration Ideas
- Calendar integration (Google Calendar, iCal)
- Grocery delivery APIs
- Kitchen timer integration
- Meal subscription box imports

## Technical Improvements

### Performance
- Lazy load recipe cards on overview
- Image optimization
- Code splitting
- Caching strategies

### Testing
- Add more test coverage
- E2E tests with Playwright/Cypress
- Visual regression tests

### CI/CD
- Automated testing on PR
- Deploy previews for branches
- Automated recipe validation

### Code Quality
- TypeScript migration
- Linting and formatting
- Pre-commit hooks
- Documentation improvements

## Notes

- Prioritize features that enhance core functionality (meal planning, recipe discovery)
- Keep the app lightweight and fast
- Maintain privacy-first approach
- Consider mobile-first design for all new features
- User data should always be exportable (no lock-in)

---

*Last updated: February 2026*
