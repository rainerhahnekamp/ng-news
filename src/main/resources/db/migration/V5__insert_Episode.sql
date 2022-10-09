INSERT INTO ngnews.Episode (Id, Name, PublishedDate, Content, ImageSrc) VALUES (6, 'Episode 22/39', '2022-10-03 00:00:00', '## Enea Jahollari: It''s ok to use function calls in Angular templates

Calling functions within a template is a known code smell. We shouldn''t do that. The function will unnecessarily run multiple times because the change detection triggers it.

As always, there are exceptions to the rule. One of them is the pipe. By default, it is a normal function with a built-in cache.

Enea Jahollari explains in his article how the pipe works and how we can apply the same principles to our own functions.

As a bonus, he explains the raw source code, the Angular compiler produces out of his example.

{% embed https://dev.to/eneajaho/its-ok-to-use-function-calls-in-angular-templates-4029 %}

## Tim Deschryver: Watch out what you expose with Angular Interceptors

In his latest article, Tim Deschryver points out potential security risks and how to deal with them when we use HTTP interceptors. especially when an interceptor adds authentication tokens to the HTTP headers.

By default, every endpoint receives this token which is surely not the best way.

https://timdeschryver.dev/blog/watch-out-what-you-expose-with-angular-interceptors

## Dany Paredes: How to build Compound Components in Angular

Another interesting article comes from Dany Parades. He discusses the compound component pattern.

Whenever a component should be flexible in terms of its usage or visualisation, you can split it up into multiple pieces, all working together using techniques like content projection or @ContentChild, etc.

https://www.danywalls.com/how-to-build-compound-components-in-angular

## TypeScript 10th year anniversary

As they say, time flies. TypeScript has already its 10-year anniversary. If you are in for history or nostalgia, you can read the anniversary blog post from Daniel Rosenwasser or watch Anders Hejlsberg at the GOTO conference where he presented TypeScript to the world for the first time.

Other than that, we have new minor versions. Jest, a testing framework, to 29.1 with improved support for types. Cypress, also a testing framework, to 10.9 with new features in the area of multi-domain switching. And nx, an alternative to the Angular CLI, to 14.8.

{% embed https://youtu.be/3dqZW_DqHIQ %}

{% embed https://devblogs.microsoft.com/typescript/ten-years-of-typescript/ %}

## Minor Version Releases

Jest was released in 29.1 with improved support for type inference.

[Release Notes](https://github.com/facebook/jest/blob/main/CHANGELOG.md#2910)

---

Cypress in 10.9 with new features for multi domain switching.

[Release Notes](https://docs.cypress.io/guides/references/changelog#10-9-0)

---

Nx 14.8: [Release Notes](https://github.com/nrwl/nx/releases/tag/14.8.0)', 'images/22-39.png');
INSERT INTO ngnews.Episode (Id, Name, PublishedDate, Content, ImageSrc) VALUES (7, 'Episode 22/38', '2022-10-03 00:00:00', '## Angular & Electron

Angular defines itself not as web framework but as a platform because it is not limited to the web only. To create mobile applications, we normally go with Ionic. For desktop applications, though, we can use Electron.

Aristeidis Bampakos gave a short introduction during the September Angular World Tour edition.

{% embed https://youtu.be/TNKE9TLTTto %}

## TypeScript Beta 4.9

Microsoft released the beta version of TypeScript 4.9.

It comes with a new satisfies operator. Until now, when you declared a union type to a variable and also assigned a specific value, the variable''s property was always a union type. With the new `satisfies` operator that union type is gone.

We can also expect an improvement for the `in` operator which can check if a certain object contains a particular property and is used for type narrowing in order to improve type safety.

{% embed https://devblogs.microsoft.com/typescript/announcing-typescript-4-9-beta/ %}

## Chrome DevTools 106

Chrome DevTools version 106 comes with improvements for bundled JavaScript files like Angular produces it.

The main feature is a much better stack trace and call stack because DevTools lists only our application files and excludes those from Angular or other third-party libraries.

This only works if the underlying framework adds special metadata to its bundles. Good for us because Angular does that already.

{% embed  https://youtu.be/5gBqTXctxO8 %}

## Minor Releases

Last but not least, we have a minor version of Playwright, an E2E testing framework, to 1.26.

https://github.com/microsoft/playwright/releases/tag/v1.26.0

And Spectator went up to 11.2.

https://github.com/ngneat/spectator/blob/master/CHANGELOG.md#1120-2022-09-23', 'images/22-38.png');
INSERT INTO ngnews.Episode (Id, Name, PublishedDate, Content, ImageSrc) VALUES (8, 'Episode 22/37', '2022-10-03 00:00:00', '## ng-conf Keynotes

The ng-conf keynote, held by Angular team members, is available on YouTube.

Sarah Drasner talked about how different frameworks incluenced each other over time, and Madleina Scheidegger talked about the future plans of Angular.

The main focus on the upcoming features will be a better developer experience. We can expect improvements in the areas of hydration and reactivity.

{% embed https://youtu.be/CABHcf1gCbg %}

The video of the community keynote is also online. It is a set of "mini presentations" about libraries, partners in the Angular ecosystem.

Like NgRx, nx, Ionic, etc.

{% embed https://youtu.be/3Mnp2WYGrVA %}

## AMA with Minko Gechev

On Twitter, Minko Gechev, also member of the Angular team, opened an Ask-me-anything session.

One of his interesting responses was that the Angular team doesn''t plan to set the change detection strategy to OnPush by default. It might introduce further bugs, especially if the implications are not well understood.

Minko also suggested a minimalistic design in terms of dependencies. For example, one could use the fetch method instead of the big HttpClient, or, one should not always jump directly to angular animations but try to use native CSS first.

{% embed https://twitter.com/mgechev/status/1569866924850556930 %}

## Cypress 10.8 with support for Safari/Webkit

Cypress, an E2E testing framework, comes with support for  Safari in version 10.8. It is a little bit of a compromise though. It doesn''t use the browser Safari itself.

Instead, it uses a wrapper, that acts as a minimal browser, around Safari''s engine, Webkit. That particular browser comes from Playwright, another E2E testing framework that had quite some traction in 2022.

Support for Safari/Webkit is still experimental.

{% embed https://www.cypress.io/blog/2022/09/13/cypress-10-8-experimental-run-tests-in-webkit/ %}

## Minor Releases

Prime Ng, was released in 14.1.

https://github.com/primefaces/primeng/tree/v14.1.0

Angular Nation released a video about the directive composition API which we can expect for Angular 15. It will improve use cases where a component needs to have multiple directives.

{% embed https://youtu.be/oC9Qd9yw3pE %}

', 'images/22-37.png');
