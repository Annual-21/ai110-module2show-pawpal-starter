# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
1. **Add and exclude a pet** - the user can create a pet profile with a name, species and age. When it is needed the user can include one more pet's profile or delete it. This is handled by the 'Pet' class, which stores pet attributes and belong to a 'User'.
2. **Schedule daily nutritions**- The user can schdule the nutrition intake for a specific pet at a chosen time everyday. This is managed by the 'Food' class, which holds schedule and nutrition details and a link to a 'User' to a 'Pet'.
3. **Schedule a Walk** — The user can schedule a walk for a specific pet at a chosen date and time. This is managed by the `Walk` class, which holds scheduling details and links a `User` to a `Pet`.

Classes include:
- 'User' -stores user credentials and owns a list of pets
- 'Pet' - holds pet profile data
- 'Food' - represents schedule nutritions data, and time
- 'Walk' - represents a scheduled walk with date, time, and duration

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
