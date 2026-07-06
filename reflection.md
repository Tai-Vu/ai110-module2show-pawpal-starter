# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- My initial UML design centered on a simple pet-care planning system with four main classes: Owner, Pet, Task, and SchedulePlanner.
- The Owner class would hold basic owner information and preferences, the Pet class would represent the animal and its basic care needs, and the Task class would represent each care activity with attributes such as title, duration, priority, and optional frequency.
- The SchedulePlanner class would take the owner, pet, and list of tasks and generate a daily plan by selecting and ordering tasks based on constraints like time and importance.

**b. Design changes**

- Yes. During implementation, I simplified the design slightly by keeping the scheduling logic in one planner component rather than splitting it into separate sorting, filtering, and conflict-resolution classes.
- I made that change because the project is still fairly small, and a single planner made the system easier to understand, implement, and test without adding unnecessary complexity.

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
