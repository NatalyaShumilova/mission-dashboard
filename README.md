# mission-dashboard

## Assumptions

### KML Format
I am assuming that all kml files uploaded will have the same structure as the example file provided. Any other structures or potential additional tags/details are out of scope.

### Waypoint Order
I am assuming that the <wpml:index> tag indicates the waypoint order.

## Challenges
- Initially, I started this project using Mistral Codestral as the model, but found that it overeager and inattentive (would jump into tasks without a plan, didn't read files before editing them). For this reason I have switched to Claude Sonnet, which hasn't caused me any problems yet. 
- As I am unfamiliar with any of our backend stack (SQLite, Flask API), it can be difficult for me to determine the quality of the generated code and whether it is following best practices within this framework. While I do my best to review and investigate any concerns I have, this would best be reviewed by someone with experience in this framework as well before going to Production.

## Decisions

### Claude over Mistral
While Mistral offers some of the cheapest models, the quality of its output can very easily lead to a hacky codebase full of duplicated and redundant code. Though we could attempt to remediate this through custom instructions and more thorough and explicit prompts (such as enforcing a ReACT thinking cycle), Claude offers a more intelligent model out of the box, which will ultimately save time on adding common sense instructions to every prompt, and simplify more complex tasks. Ultimately the price difference would need to be looked into if an AI first development approach is to be scaled, to consider whether the quality improvement fits the budget.

### AI-owned memory bank
So far I have left AI to own the memory bank, and automatically update it, interfering only to correct obvious inaccuracies. It works, but I am leaning towards a human-maintained memory bank as a better practice, as, while the memory bank itself provides some context, the LLM updates the memory bank with a slightly different perspective each time, and this causes some minor inconsistancies. In the interest of saving time for this project, I will continue to leave this with the AI unless it begins to cause larger issues.

### Unit Testing
Since I am new to the backend technologies used in this project, it resembles more of a spike for me, as I'm not sure how exactly to set things up in advance. For this reason, I am holding off on unit testing until I can see that the app is working and have a better understanding of what it will look like, even though the usual best practice would be to write tests in parallel with (if not in advance of) the features developed.