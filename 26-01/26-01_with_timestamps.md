# Ng-Poland Outtakes: Keynote and Q&A Highlights

In this episode, we cover news from around Christmas until New Year's Eve. The next episode will focus solely on events from 2026.

<segment topic="Ng-Poland">
Ng-Poland took place in November, and videos from both the keynote and the Q&A session with the Angular team are now available on YouTube. Here are the main takeaways.

<card>
type: event
title: Ng-Poland 2025
date: November 2025
location: Warsaw
video: https://www.youtube.com/watch?v=bxrl6Xf03JM
items:
  - Keynote
  - Q&A Session
</card>
</segment>

## [00:17] Keynote Highlights

The keynote primarily discussed features introduced in Angular 21, which we covered in a previous episode. The keynote, however, was mainly about AI.

<segment topic="MCP Server Workflow">
First, Jeremy Elbourn explained an AI-supported workflow that we can expect. With the help of Angular's MCP Server, the LLM would first generate modern Angular code. It would also start the application and test the produced code via Playwright's MCP Server. If there was a bug, the Angular MCP could connect to the running browser and collect the context of the running application—its state, so to speak—to find the error and fix it.

<card>
type: concept
title: MCP Server
subtitle: Model Context Protocol
description: Enables LLMs to interact with development tools
workflow:
  - Generate Angular code
  - Start application
  - Test with Playwright MCP
  - Debug in browser context
</card>
</segment>

<segment topic="AI as End User">
Second, Alex Rickabaugh, tech lead of the Angular framework, discussed what changes the framework requires to be prepared for what might come. In the past, they have been doing user studies with real developers, where they showed them certain APIs that they wanted to introduce and then observed how those developers were dealing with them. Nowadays, they also see AI as an end-user and have a similar approach.

[Audio clip at 52: ...trying to change the framework instead of the model...]

<card>
type: person-quote
person: Alex Rickabaugh
role: Angular Framework Tech Lead
quote: trying to change the framework instead of the model...
timestamp: 52:00
</card>
</segment>

<segment topic="Dynamic UIs">
Alex also mentioned that they have to prepare for more dynamic UIs. They don't have anything concrete yet, but they recommend checking out community solutions like Hashbrown.

<card>
type: library
name: Hashbrown
description: Community solution for dynamic UIs
status: community
recommended-by: Alex Rickabaugh
</card>
</segment>

**Keynote video:** https://www.youtube.com/watch?v=bxrl6Xf03JM

## [01:41] Q&A Session

Next, there was also the Q&A. Here are three interesting takeaways:

<segment topic="Security">
There was a question on how to protect your codebase from malicious libraries, especially from those kinds of attacks which we have seen in the second half of 2025. Here, we can just take a look at the measures Angular does for its own project.

[Security measures mentioned by Googlers]

<card>
type: topic
title: Security
subtitle: Protecting against malicious libraries
context: Angular's security measures for their own project
timeline: Second half of 2025 attacks
</card>
</segment>

There was also a question about `@angular/aria` and how it fits together with Angular Material. Here, Jeremy said that the days of having full-blown UI libraries which might be a little hard to customize are over.

[Jeremy mentioning that people moved away from Angular Material]

<segment topic="Signal Forms Migration">
And there were, of course, also a few questions about Signal Forms. The migration from Reactive or Template-Driven Forms is also important. At the moment, we do have the possibility to reuse `FormControl` or `FormGroup` from Reactive Forms in Signal Forms, but Alex also announced that there will be a path towards the other direction: Reactive Forms will be able to run Signal Forms.

<card>
type: migration
title: Signal Forms Migration
current: Signal Forms → Reactive Forms (FormControl/FormGroup reusable)
future: Reactive Forms → Signal Forms [Coming Soon]
legacy: Template-Driven Forms
announced-by: Alex Rickabaugh
</card>
</segment>

**Q&A video:** https://www.youtube.com/watch?v=OpprrzvyqEc

## [02:52] Dynamic Forms

<segment topic="Dynamic Forms Concept">
There is this idea of having dynamic forms. So you provide a certain set of metadata, which includes the value, the validation rules, but also the UI type (select box, input field, radio button, or checkbox), and then the form could be generated dynamically.

<card>
type: concept
title: Dynamic Forms
description: Forms generated from metadata configuration
metadata-includes:
  - Value
  - Validation rules
  - UI type (select, input, radio, checkbox)
</card>
</segment>

<segment topic="@ng-forge/dynamic-forms">
For the old form system, there were some libraries which did that. A prominent one was ngx-formly. Now, at the moment, it is not clear if ngx-formly will and, if so, how it will provide support for Signal Forms. But there is a new library, built from the beginning for Signal Forms. Its name is `@ng-forge/dynamic-forms`. It comes with an integration of common UI libraries: Angular Material, Bootstrap, but also PrimeNG and Ionic.

<card>
type: library
name: "@ng-forge/dynamic-forms"
built-for: Signal Forms
url: https://www.ng-forge.com/dynamic-forms/what-is-dynamic-forms
ui-libraries:
  - Angular Material
  - Bootstrap
  - PrimeNG
  - Ionic
legacy-alternative: ngx-formly (Signal Forms support unclear)
</card>
</segment>

**Learn more:** https://www.ng-forge.com/dynamic-forms/what-is-dynamic-forms

## [03:42] NgRx 21

<segment topic="NgRx 21 Release">
NgRx, the most used library for state management in Angular, was released in version 21. It brings a new website, the events plugin for the SignalStore went stable, and further improvements.

<card>
type: release
name: NgRx
version: 21
milestone: 10 Years Celebration
description: Most used library for state management in Angular
url: https://dev.to/ngrx/announcing-ngrx-21-celebrating-a-10-year-journey-with-a-fresh-new-look-and-ngrxsignalsevents-5ekp
features:
  - SignalStore Events Plugin (Stable)
  - New Website
  - Further Improvements
</card>
</segment>

**Announcement:** https://dev.to/ngrx/announcing-ngrx-21-celebrating-a-10-year-journey-with-a-fresh-new-look-and-ngrxsignalsevents-5ekp
