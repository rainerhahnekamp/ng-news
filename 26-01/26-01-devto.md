The Angular team reveals their vision for AI-powered development workflows using MCP Servers, where LLMs generate, test, and debug Angular applications autonomously. Plus, learn about <a href="https://angular.io/guide/forms" target="_blank" rel="noopener">Signal Forms</a> migration paths, the new `@ng-forge/dynamic-forms` library, and <a href="https://ngrx.io/" target="_blank" rel="noopener">NgRx</a> 21.

📺 **Watch the full episode on YouTube:**

{% embed https://youtu.be/AO2KtDkLA6c %}

This episode covers news from around Christmas until New Year's Eve. The next episode will focus solely on events from 2026.

## Ng-Poland Keynote

Ng-Poland took place in November, and videos from both the keynote and the Q&A session with the Angular team are now available on YouTube. Here are the main takeaways.

The keynote discussed features introduced in Angular 21, which we covered in a previous episode. The keynote, however, was mainly about AI.

### MCP Server Workflow

First, Jeremy Elbourn explained an AI-supported workflow that we can expect.

With the help of Angular's MCP Server (Model Context Protocol), the LLM would first generate modern Angular code. It would also start the application and test the produced code via <a href="https://playwright.dev/" target="_blank" rel="noopener">Playwright's</a> MCP Server.

If there was a bug, the Angular MCP could connect to the running browser and collect the context of the running application—its state, so to speak—to find the error and fix it.

### AI as User

Second, Alex Rickabaugh, tech lead of the Angular framework, discussed what changes the framework requires to be prepared for what might come. In the past, they have been doing user studies with real developers, where they showed them certain APIs that they wanted to introduce and then observed how those developers were dealing with them. Nowadays, they also see AI as an end-user and have a similar approach.

> "trying to change the framework instead of the model..." - Alex Rickabaugh, Angular Framework Tech Lead

Alex also mentioned that they have to prepare for more dynamic UIs. They don't have anything concrete yet, but they recommend checking out community solutions like <a href="https://hashbrown.dev/" target="_blank" rel="noopener">Hashbrown</a>.

**Keynote video:**

{% embed https://www.youtube.com/watch?v=bxrl6Xf03JM %}

## Q&A Session

Next, there was also the Q&A. Here are three interesting takeaways:

### Security

There was a question on how to protect your codebase from malicious libraries, especially from those kinds of attacks which we have seen in the second half of 2025. Here, we can just take a look at the measures Angular does for its own project.

1. They use <a href="https://pnpm.io/" target="_blank" rel="noopener">`pnpm`</a>, which has a lot of advantages over <a href="https://www.npmjs.com/" target="_blank" rel="noopener">`npm`</a>. For example it doesn't automatically execute post-install scripts.
2. <a href="https://docs.renovatebot.com/" target="_blank" rel="noopener">Renovate</a> is responsible for managing the upgrades and it has a setting which doesn't install packages until they've been published for a certain period of time, for example 2 days.

Generally speaking, studying the Angular repo itself will show further measures for improving security.

### Angular Material and UI Libraries

There was also a question about `@angular/aria` and how it fits together with <a href="https://material.angular.io/" target="_blank" rel="noopener">Angular Material</a>. Jeremy said that the days of having full-blown UI libraries which might be a little hard to customize are over.

The current trend is more towards customizable individual design systems, and this is why `@angular/aria` is strong. It only provides the behavior, the visual is completely up to the developers.

### Signal Forms Migration

And there were, of course, also a few questions about Signal Forms.

The migration from Reactive Forms or Template-Driven Forms is also important. At the moment, we do have the possibility to reuse `FormControl` or `FormGroup` from Reactive Forms in Signal Forms, but Alex also announced that there will be a path towards the other direction: Reactive Forms will be able to run Signal Forms.

**Q&A video:**

{% embed https://www.youtube.com/watch?v=OpprrzvyqEc %}

## Dynamic Forms

There is this idea of having dynamic forms. So you provide a certain set of metadata, which includes the value, the validation rules, but also the UI type (select box, input field, radio button, or checkbox), and then the form could be generated dynamically.

For the old form system, there were some libraries which did that. A prominent one was <a href="https://formly.dev/" target="_blank" rel="noopener">ngx-formly</a>. At the moment, it is not clear if ngx-formly will provide support for Signal Forms and, if so, how it will do so.

But there is a new library, built from the beginning for Signal Forms. Its name is `@ng-forge/dynamic-forms`. It comes with an integration of common UI libraries: <a href="https://material.angular.io/" target="_blank" rel="noopener">Angular Material</a>, <a href="https://getbootstrap.com/" target="_blank" rel="noopener">Bootstrap</a>, but also <a href="https://primeng.org/" target="_blank" rel="noopener">PrimeNG</a> and <a href="https://ionicframework.com/" target="_blank" rel="noopener">Ionic</a>.

{% embed https://www.ng-forge.com/dynamic-forms/what-is-dynamic-forms %}

## NgRx 21

<a href="https://ngrx.io/" target="_blank" rel="noopener">NgRx</a>, the most used library for state management in Angular, was released in version 21. It brings a new website, the events plugin for the <a href="https://ngrx.io/guide/signals/signal-store" target="_blank" rel="noopener">SignalStore</a> went stable, and further improvements.

{% embed https://dev.to/ngrx/announcing-ngrx-21-celebrating-a-10-year-journey-with-a-fresh-new-look-and-ngrxsignalsevents-5ekp %}
