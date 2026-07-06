# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- My initial UML design used four main classes: Owner, Pet, Task, and SchedulePlanner.
- The Owner class represents the person managing the pet care routine. Its responsibility is to store basic owner information, availability, and preferences that influence how tasks are scheduled.
- The Pet class represents the animal being cared for. Its responsibility is to store the pet’s identity, species, and care needs so the scheduler can account for what the pet requires.
- The Task class represents an individual care activity such as a walk, feeding, medication, or grooming. Its responsibility is to hold details like the task title, duration, priority, and optional frequency.
- The SchedulePlanner class coordinates the whole system. Its responsibility is to take the owner, pet, and list of tasks and generate a daily plan by sorting, filtering, and arranging tasks around the available time.

**b. Design changes**

- Yes. Based on the feedback, I adjusted the design so the relationships between the main classes are clearer and the scheduling logic is more realistic.
- I added the idea that an Owner can be associated with one or more Pets, and that Tasks should be connected more directly to the pet-care context rather than existing as isolated items.
- I also refined the planner so it should consider owner availability, task time windows, and potential conflicts when building a schedule, instead of treating the plan as a simple priority-based list.
- These changes were made because they make the system easier to extend later and better reflect how a real pet care assistant would behave.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- My scheduler considers scheduled time, task priority, completion status, and pet ownership.
- I prioritized time and priority because they are the clearest signals for building a usable daily plan: users need to see what should happen first and when.
- Completion status matters because the plan should focus on pending tasks rather than already finished ones.

**b. Tradeoffs**

- One tradeoff my scheduler makes is that it only checks for exact time matches when detecting conflicts, rather than trying to reason about overlapping durations or task lengths.
- That is reasonable for this project because the app is a lightweight pet-care planner, and exact time matching keeps the logic simple, predictable, and easy to explain while still catching obvious scheduling overlaps.

---

## 3. AI Collaboration

**a. How you used AI**

- I used my AI coding assistant for three main phases. First was designing the class structure. Second, I used my AI assistent in implementing the scheduler methods. Then, I used the AI assistant in polishing the Streamlit interface.
- The most effective features were code generation for the core class methods, quick debugging help when tests failed, and iterative refactoring suggestions that made the code cleaner.
- Prompts that asked for specific behavior, such as “implement recurring-task creation” or “add conflict warning logic,” worked especially well because they gave the assistant a narrow goal.

**b. Judgment and verification**

- One AI suggestion I rejected was a proposal to make the scheduler handle recurrence in a more complex way than the project needed. I modified it to keep the logic simple and aligned with the existing `Task` and `Scheduler` structure.
- I verified suggestions by testing them against the existing behavior and by checking whether they matched the project’s simple class model rather than overengineering the solution.
- I also relied on the test suite to confirm that new logic actually worked instead of assuming the AI-generated code was correct.

**c. AI Strategy Reflection**

- Using separate chat sessions for different phases helped me stay organized because each session could focus on a single concern, such as backend logic, UI design, or testing.
- That separation made it easier to avoid mixing ideas and to revisit earlier decisions when I needed to refine the implementation.
- It also helped me stay the lead architect, because I could review each suggestion in context and decide whether it improved the system or introduced unnecessary complexity.

**d. What I learned**

- I learned that being the lead architect means guiding the AI with clear goals, validating every important change, and keeping the system design simple enough to understand and maintain.
- Powerful AI tools are very helpful, but they work best when the human partner defines the structure, makes the tradeoff decisions, and ensures the final solution remains coherent.

---

## 4. Testing and Verification

**a. What you tested**

- I tested task completion, recurring-task creation, task ordering, conflict detection, pet specific filtering, and the scheduler’s warning behavior.
- These tests were important because they cover the core behaviors users rely on when planning a daily pet-care routine.
- They also helped catch edge cases such as duplicate times and recurring tasks creating duplicate or missing follow-up tasks.

**b. Confidence**

- I am fairly confident that the scheduler works correctly for the core scenarios in this project because the test suite passes and the app behavior is consistent with those tests. The streamlit app also works properly when ran. 
- If I had more time, I would test more complex edge cases such as invalid time input, multiple overlapping tasks, and more advanced recurrence scenarios. I would also like to do the extra extensions as well.

---

## 5. Reflection

**a. What went well**

- I am most satisfied with how the scheduler became clear and testable once the core behaviors were implemented.
- I also feel good about the polished UI, because it makes the app feel more approachable and friendly for pet owners.

**b. What you would improve**

- If I had another iteration, I would add more realistic scheduling features such as task duration, owner availability windows, and more detailed conflict handling.
- I would also make the UI more interactive by allowing users to edit or remove tasks directly from the app.

**c. Key takeaway**

- One important lesson I learned is that strong system design comes from choosing the right abstractions and keeping the implementation aligned with them, even when AI tools can generate code very quickly.
- The best results come from using AI as a collaborator while still thinking like the architect of the system.
