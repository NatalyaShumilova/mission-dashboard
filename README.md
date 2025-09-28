# mission-dashboard

## Assumptions

### KML Format
I am assuming that all kml files uploaded will have the same structure as the example file provided. Any other structures or potential additional tags/details are out of scope.

### Waypoint Order
I am assuming that the <wpml:index> tag indicates the waypoint order.

### Mission editing
I am assuming that features around editing the waypoints themselves is out of scope, and any additional changes within this prototype (annotations, ect), do not need to be exported as part of a new kml file. In other words, the assumption is that the mission itself stays as-is, and any layers added on top of it live separately and only within the prototype for now.

## Challenges
- Initially, I started this project using Mistral Codestral as the model, but found that it overeager and inattentive (would jump into tasks without a plan, didn't read files before editing them). For this reason I have switched to Claude Sonnet, which hasn't caused me any problems yet. 
- As I am unfamiliar with any of our backend stack (SQLite, Flask API), it can be difficult for me to determine the quality of the generated code and whether it is following best practices within this framework. While I do my best to review and investigate any concerns I have, this would best be reviewed by someone with experience in this framework as well before going to Production.
- I have found that since AI is capable of generating a huge amount of code in a very short timeframe, and all of that code needs to be read through and reviewed, it can actually get quite overwhelming to keep up with the sheer volume of code. It's like reviewing large PRs all day.

## Decisions

### Claude over Mistral
While Mistral offers some of the cheapest models, the quality of its output can very easily lead to a hacky codebase full of duplicated and redundant code. Though we could attempt to remediate this through custom instructions and more thorough and explicit prompts (such as enforcing a ReACT thinking cycle), Claude offers a more intelligent model out of the box, which will ultimately save time on adding common sense instructions to every prompt, and simplify more complex tasks. Ultimately the price difference would need to be looked into if an AI first development approach is to be scaled, to consider whether the quality improvement fits the budget.

- Update: So far this project (using Claude) has taken me ~14 hours and ~$36 (NZD). This would be a significant cost to scale, but it has allowed me to build an application in a timeframe that would not have been possible if I was doing it manually, escpecially taking into account that I am unfamiliar with the entire backend stack, and the Mapbox component (I could easily see this being no less than a week's work without AI assistance). I likely would have spent a significant amount of time on google searches and trial and error alone. It would be worth investigating what options Anthropic (or other providers with similar quality models) offer in terms of larger-scale usage costs.

### AI-owned memory bank
So far I have left AI to own the memory bank, and automatically update it, interfering only to correct obvious inaccuracies. It works, but I am leaning towards a human-maintained memory bank as a better practice, as, while the memory bank itself provides some context, the LLM updates the memory bank with a slightly different perspective each time, and this causes some minor inconsistancies. In the interest of saving time for this project, I will continue to leave this with the AI unless it begins to cause larger issues.

### Unit Testing
Since I am new to the backend technologies used in this project, it resembles more of a spike for me, as I'm not sure how exactly to set things up in advance. For this reason, I am holding off on unit testing until I can see that the app is working and have a better understanding of what it will look like, even though the usual best practice would be to write tests in parallel with (if not in advance of) the features developed.

### SQLite
As I don't have experience with docker, I have decided to set up with SQLite instead. This seems to be the simpler of the two approaches, and is sufficient for this POC.

### Styling
AI seems to be doing a decent job at styling the UI - as proper UI/UX design is out of scope for this POC, I will keep the AI generated styles as is, outside of perhaps refactoring if needed.

## Production-readiness

*Interestingly, I have observed that Claude actually defaults to fully fledged production patterns for things like observability, testing, configuration, ect. I've actually had to tell it to simplify some of it, as this is still a prototype and does not need a lot of these capabilities at this stage.*

These are some considerations and work items that would need to be done before this protoype is production ready:
- As I have run out of time, some core features (such as annotations) have not been implemented - presumably these would need to be completed before this piece can go to production. Additionally, there may be extra functionality required for production that was not brought up for the prototype (such as login capabilities, along with account management, the ability for full CRUD operations on Missions and Waypoints, ect.)
- Definition of Done and Quality requirements - to bring this to a production ready state, it will need to meet the organisation's definition of done, including but not limited to considerations in areas such as:
    - Security (access management, not logging full error traces, ect.)
    - Accessibility (screen reader, keyboard navigation, contrast, UI scaling, ect)
    - Localization if applicable, including translations
    - Testing and QA (we have unit tests, but there may be requirements for other forms of testing and quality assurance gates)
- Non-local environment setup and configuration. This will also include setting up an actual database, as in memory storage will not suffice for a production environment.
- Proper UX/UI design, as the current one was jointly created by a developer and an AI, and was not given the necessary attention and consideration
