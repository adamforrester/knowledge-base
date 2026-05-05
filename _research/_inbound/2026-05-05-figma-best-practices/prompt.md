You are researching Figma-specific best practices for design systems work, intended for a senior design systems practitioner at a digital agency. The output is a structured knowledge document covering how to architect, organize, govern, and maintain a design system within Figma at a professional level. This is not an introductory guide — assume the reader knows Figma and knows what a design system is.

Research scope — cover all of the following:

1. Library architecture and organization

Single library vs. multi-library strategies — when to split (foundations, components, patterns, brand-specific) and when consolidation is better
Folder and page structure conventions within a Figma library
Naming conventions: components, variants, properties, layers — current best practices and the conventions that have become de facto standards
Published vs. unpublished libraries and when each is appropriate

2. Component architecture

Variant construction: when to use variants vs. component properties vs. nested components
Component properties (boolean, instance swap, text, variant) — how to use them effectively and common misuse patterns
Nesting strategy: how deep is too deep, performance implications of deep nesting
Base component / composition patterns — abstracting primitive components that specialized components build from
Slots and content override patterns in Figma
Detaching: when it's appropriate and how to design components that minimize the need to detach

3. Figma Variables and token architecture

Variable collections: how to structure primitive and semantic token layers in Figma Variables
Mode support: light/dark, brand themes, density — how Variables handle multi-mode and where the limits are
Variable scoping: restricting variable visibility to appropriate properties
Figma Variables vs. Tokens Studio: current state of each, when to use which, migration considerations
Connecting Figma Variables to a code token pipeline (W3C DTCG format, Style Dictionary)
Known gaps and limitations of Figma Varia5/2026

4. Design-to-development handoff

What a well-prepared Figma library enables for developers vs. what it doesn't
Annotation approaches: native Figma annotations vs. third-party plugins
Figma's Dev Mode: what it provides, its limits, and how DS teams should structure components to maximize Dev Mode utility
Code Connect: what it is, how it works, current maturity and limitations
Handoff documentation that lives inside Figma vs. documentation that needs to be external

5. Multi-platform design in Figma

Managing web and mobile (iOS, Android, Flutter) component libraries from a single Figma workspace
Shared token foundations with platform-specific component pages or libraries
Figma conventions for representing platform-specific interaction patterns

6. Governance of Figma libraries

Branching and versioning in Figma — current capabilities and their limits
Library update management: how to push and communicate updates to consumers
Contribution workflows within Figma: proposal, review, publish
Audit and coverage tracking: how teams assess what's in the library vs. what the product needs

7. Performance and maintenance

Component count and library performance — at what scale do Figma libraries become unwieldy
Techniques for keeping libraries performant (hidden vs. published components, page organization)
Deprecation patterns: how to retire components without breaking consumer files

Output format: Structured markdown. Synthesize findings — do not list sources mechanically. Where there is genuine debate or context-dependence (e.g., single vs. multi-library), name the trade-offs rather than declaring a winner. Flag where Figma's native capabilities have known gaps that practitioners work around. Include a references section with links to primary sources (Figma documentation, Config talks, practitioner blogs).

Depth: Expert audience. Do not explain what variants are — explain when not to use them and why.
