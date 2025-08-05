# Prompt Engineering Principles

This document contains 26 proven principles for crafting effective prompts for Large Language Models (LLMs). Each principle includes a description, examples, and practical applications.

## The 26 Principles

### 1. Be Concise
**Description:** No need for polite phrases; get straight to the point.

**Bad Example:** "Could you kindly describe the structure of a human cell, please?"

**Good Example:** "Describe the structure of a human cell."

**When to Use:** Always. Conciseness improves clarity and reduces token usage.

---

### 2. Specify Audience
**Description:** Integrate the intended audience in the prompt.

**Example:** "Construct an overview of how smartphones work, intended for seniors who have never used one before."

**When to Use:** When the complexity level or terminology needs to match a specific group's understanding.

---

### 3. Break Down Tasks
**Description:** Break complex tasks into simpler, sequential prompts in an interactive conversation.

**Example Sequence:**
- P1: "Distribute the negative sign to each term inside the parentheses of the following equation: 2x + 3y - (4x - 5y)"
- P2: "Combine like terms for 'x' and 'y' separately."
- P3: "Provide the simplified expression after combining the terms."

**When to Use:** For multi-step problems, calculations, or complex analyses.

---

### 4. Use Affirmative Directives
**Description:** Employ affirmative directives such as "do," while steering clear of negative language like "don't".

**Example:** "How do buildings remain stable during earthquakes?"

**When to Use:** Always. Positive framing leads to more focused responses.

---

### 5. Request Clarity at the Right Level
**Description:** Adjust the complexity of explanations to match your needs.

**Common Phrases:**
- "Explain [topic] in simple terms."
- "Explain to me like I'm 11 years old."
- "Explain to me as if I'm a beginner in [field]."
- "Explain to me as if I'm an expert in [field]."
- "Write the [essay/text/paragraph] using simple English like you're explaining something to a 5-year-old."

**Example:** "Explain to me like I'm 11 years old: how does encryption work?"

**When to Use:** When you need explanations tailored to specific knowledge levels.

---

### 6. Use Incentives for Better Solutions
**Description:** Add "I'm going to tip $xxx for a better solution" to motivate comprehensive responses.

**Example:** "I'm going to tip $300K for a better solution! Explain the concept of dynamic programming and provide an example use case."

**When to Use:** For complex problems requiring extra effort or creativity.

---

### 7. Example-Driven Prompting (Few-Shot)
**Description:** Provide examples to guide the model's response format and style.

**Example:**
```
Example 1: Translate the following English sentence to French: "The sky is blue." (Response: "Le ciel est bleu.")
Example 2: Translate the following English sentence to Spanish: "I love books." (Response: "Amo los libros.")
Task: Translate the following English sentence to German: "Good morning."
```

**When to Use:** For tasks requiring specific formats, translations, or patterns.

---

### 8. Use Delimiters and Structure
**Description:** Start with '###Instruction###', followed by '###Example###' or '###Question###' if relevant.

**Example:**
```
###Instruction###
Translate a given word from English to French.

###Question###
What is the French word for "book"?
```

**When to Use:** For complex prompts with multiple components.

---

### 9. Use Explicit Directives
**Description:** Incorporate phrases like "Your task is" and "You MUST".

**Example:** "Your task is to explain the water cycle to your friend. You MUST use simple language."

**When to Use:** When specific requirements are non-negotiable.

---

### 10. State Penalties for Non-Compliance
**Description:** Incorporate phrases like "You will be penalized" to emphasize requirements.

**Example:** "Your task is to explain the water cycle to your friend. You will be penalized if you fail to use simple language."

**When to Use:** For critical requirements that must be followed.

---

### 11. Request Human-Like Answers
**Description:** Use the phrase "Answer a question given in a natural, human-like manner".

**Example:** "Write a paragraph about healthy food. Answer a question given in a natural, human-like manner."

**When to Use:** When you want conversational, relatable responses.

---

### 12. Encourage Step-by-Step Reasoning
**Description:** Use leading words like "think step by step" or "let's work through this systematically".

**Example:** "Write a Python code to loop through 10 numbers and sum all of them. Let's think step by step."

**When to Use:** For problems requiring logical progression or debugging.

---

### 13. Request Unbiased Answers
**Description:** Add "Ensure that your answer is unbiased and avoids relying on stereotypes."

**Example:** "How do cultural backgrounds influence the perception of mental health? Ensure that your answer is unbiased and avoids relying on stereotypes."

**When to Use:** For sensitive topics or when objectivity is crucial.

---

### 14. Elicit Details by Asking Questions
**Description:** Allow the model to ask you questions until it has enough information.

**Example:** "From now on, ask me questions until you have enough information to create a personalized fitness routine."

**When to Use:** For personalized or highly specific tasks.

---

### 15. Teach and Test Understanding
**Description:** Request teaching followed by testing without revealing answers.

**Example:** "Teach me about the KVL law and include a test at the end, and let me know if my answers are correct after I respond, without providing the answers beforehand."

**When to Use:** For learning and verifying understanding.

---

### 16. Assign a Role to the Model
**Description:** Give the LLM a specific expertise or perspective.

**Example:** "If you were an expert economist, how would you answer this: What are the key differences between a capitalist and a socialist economic system?"

**When to Use:** When you need domain-specific expertise or perspectives.

---

### 17. Use Delimiters for Clarity
**Description:** Use delimiters to separate sections or highlight key content.

**Example:** "Compose a persuasive essay discussing the importance of 'renewable energy sources' in reducing greenhouse gas emissions."

**When to Use:** To emphasize specific terms or separate different parts of complex prompts.

---

### 18. Repeat Key Words or Phrases
**Description:** Repeat important terms to maintain focus throughout the response.

**Example:** "Evolution, as a concept, has shaped the development of species. What are the main drivers of evolution, and how has evolution affected modern humans?"

**When to Use:** To ensure consistent focus on the main topic.

---

### 19. Combine Chain-of-Thought with Few-Shot
**Description:** Use both reasoning steps and examples together.

**Example:**
```
Example 1: "Divide 10 by 2. First, take 10 and divide it by 2. The result is 5."
Example 2: "Divide 20 by 4. First, take 20 and divide it by 4. The result is 5."
Main Question: "Divide 30 by 6. First, take 30 and divide it by 6. The result is...?"
```

**When to Use:** For mathematical or logical problems requiring specific methodology.

---

### 20. Use Output Primers
**Description:** Start the desired output format at the end of your prompt.

**Example:** "Describe the principle behind Newton's First Law of Motion. Explanation:"

**When to Use:** To ensure responses begin with the right format or tone.

---

### 21. Request Detailed Content
**Description:** Explicitly ask for comprehensive information.

**Example:** "Write a detailed paragraph for me on the evolution of smartphones in detail by adding all the information necessary."

**When to Use:** When you need thorough, comprehensive responses.

---

### 22. Request Style-Preserving Corrections
**Description:** Maintain original writing style while improving grammar and vocabulary.

**Example:** "Try to revise every text sent by users. You should only improve the user's grammar and vocabulary and make sure it sounds natural. You should maintain the original writing style, ensuring that a formal paragraph remains formal. Paragraph: Renewable energy is really important for our planet's future..."

**When to Use:** For editing and proofreading tasks.

---

### 23. Automate Multi-File Code Generation
**Description:** Request scripts that generate multiple files automatically.

**Example:** "Generate code that spans more than one file, and generate a Python script that can be run to automatically create the specified files for a Django project with two basic apps for different functionalities."

**When to Use:** For complex coding projects with multiple components.

---

### 24. Continue Text with Specific Starters
**Description:** Provide beginning text and request consistent continuation.

**Example:** "I'm providing you with the beginning of a fantasy tale: 'The misty mountains held secrets no man knew.' Finish it based on the words provided. Keep the flow consistent."

**When to Use:** For creative writing or maintaining specific styles.

---

### 25. State Explicit Requirements
**Description:** List specific keywords, regulations, or instructions that must be included.

**Example:** "Create a packing list for a beach vacation, including the following keywords 'sunscreen,' 'swimsuit,' and 'beach towel' as essential items."

**When to Use:** When specific elements must be included in the response.

---

### 26. Mimic Provided Language Style
**Description:** Match the style of a given sample in new content.

**Example:** "'The gentle waves whispered tales of old to the silvery sands, each story a fleeting memory of epochs gone by.' Use the same language based on the provided text to portray a mountain's interaction with the wind."

**When to Use:** For maintaining consistent tone or style across content.

---

## Quick Reference Guide

### For Clarity and Structure:
- Principles 1, 4, 8, 17: Basic clarity
- Principles 3, 12: Breaking down complexity
- Principles 20, 21: Output formatting

### For Specific Requirements:
- Principles 9, 10, 25: Enforcing requirements
- Principles 2, 5, 16: Audience targeting
- Principles 13, 22, 26: Style and bias control

### For Learning and Examples:
- Principles 7, 19: Example-based learning
- Principles 14, 15: Interactive learning
- Principle 6: Motivation for quality

### For Natural Responses:
- Principles 11, 24: Human-like output
- Principle 18: Maintaining focus
- Principle 23: Complex implementations

## Best Practices

1. **Combine Principles:** Many principles work well together. For example, combine Principle 7 (few-shot) with Principle 12 (step-by-step) for complex tasks.

2. **Match Principle to Task:** Choose principles based on your specific needs:
   - Technical tasks: Use principles 3, 7, 12, 19
   - Creative tasks: Use principles 11, 24, 26
   - Learning tasks: Use principles 5, 14, 15

3. **Start Simple:** Begin with principles 1 and 4, then add others as needed.

4. **Iterate:** If a prompt doesn't work well, try applying different principles or combining them differently.

5. **Context Matters:** Some principles (like 6, 10) work better for complex, high-stakes tasks, while others (like 1, 4) should be used universally.