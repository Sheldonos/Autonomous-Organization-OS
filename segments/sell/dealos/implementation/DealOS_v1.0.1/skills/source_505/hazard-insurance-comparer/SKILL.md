---
name: hazard-insurance-comparer
description: Compares hazard (homeowners) insurance quotes for US properties by collecting detailed property data from the user, dynamically finding available insurance providers in the user's state, programmatically scraping or navigating online quote tools, and generating a ranked comparison table with a best-pick recommendation. Use when a user asks to compare home or hazard insurance quotes.
---

# Hazard Insurance Comparer

This skill enables the agent to act as a digital insurance broker, guiding users through the collection of necessary property details, dynamically identifying top homeowners insurance providers in their specific state, fetching quotes using web browsing or scraping, and presenting a comprehensive comparison table to find the best deal.

## Core Workflow

Comparing hazard insurance quotes involves these sequential steps:

1. **Intake and Discovery**

1. **Provider Identification**

1. **Quote Retrieval Execution**

1. **Analysis and Presentation**

### 1. Intake and Discovery

To provide accurate quotes, you must collect the necessary information from the user.Ask the user for the following details if not already provided:

- **Property Address** (Full street address, city, state, ZIP)

- **Property Details** (Year built, square footage, number of stories/bathrooms, roof age/material, exterior wall material)

- **Occupancy** (Primary residence, secondary, rental, number of full-time residents)

- **Coverage Preferences** (Estimated home replacement cost or market value, desired deductible amount)

- **History** (Any home insurance claims in the past 3 years? Credit score range: Excellent/Good/Fair/Poor)

- **Safety Features** (Presence of smoke detectors, burglar alarms, security cameras, deadbolts)

*Note: You can use property record search tools (like Zillow or Redfin via the browser) to automatically find public details like year built and square footage based on the address to save the user time.*

### 2. Provider Identification

Once the state is known, dynamically identify the top insurance providers operating in that state.

- Use the `search` tool to find the largest and most highly-rated homeowners insurance companies available in the user's state (e.g., State Farm, Allstate, USAA, Liberty Mutual, Farmers, Progressive, Travelers).

- Identify at least 3 to 5 viable providers to compare.

- Prioritize providers that offer online quoting tools (e.g., "Get a Quote" buttons on their websites).

### 3. Quote Retrieval Execution

Use the `browser` tool to navigate to the identified insurance providers' websites or major comparison marketplaces (like Policygenius, The Zebra, or Insurify).

- Navigate to the "Homeowners Insurance Quote" section of each provider.

- Methodically fill out the quote forms using the data collected in Step 1.

- If a site blocks automated access or requires a phone call, skip it and move to the next provider on your list.

- Extract the final quoted premiums, coverage limits (Dwelling, Personal Property, Liability), and deductibles.

- Take screenshots of the final quote pages if possible to verify the data.

*Note: Since real-time quoting often requires PII (Personally Identifiable Information) like name, email, or phone number, ask the user if they want you to use dummy/placeholder contact info to avoid spam, or if they prefer to provide their actual contact info. If using placeholder info, ensure it passes basic validation (e.g., John Doe, 555-0199).*

### 4. Analysis and Presentation

Compile the retrieved quotes into a clear, ranked comparison table and provide a final recommendation.

Generate a final Markdown report containing:

#### A. Executive Summary

A brief overview of the property being insured and the requested coverage parameters.

#### B. Quote Comparison Table

Format the data into a Markdown table with the following columns:

- **Insurance Provider**

- **Annual Premium**

- **Monthly Premium**

- **Dwelling Coverage (Coverage A)**

- **Deductible**

- **Notable Features / Discounts Applied**

#### C. Best Pick Recommendation

Provide a clear recommendation on which policy offers the "best deal." Consider not just the lowest price, but the balance of premium cost, deductible, and company reputation/financial strength. Explain the reasoning behind the recommendation.

#### D. Next Steps

Provide direct links to the quoted policies (if available) or instructions on how the user can bind the recommended policy.

## Best Practices

- **Accuracy:** Insurance quotes are highly sensitive to input data. Ensure you use the exact address and property details.

- **Privacy:** Handle the user's address and personal details securely. Do not share them outside the context of retrieving these specific quotes.

- **Transparency:** If a quote is an "estimate" rather than a final bound rate, explicitly state this in the presentation.

- **Fallback:** If individual carrier sites are too difficult to navigate due to captchas, fall back to comparison aggregator sites (like The Zebra or NerdWallet's quote tools) as a proxy, secondary option.

---

## ibm-aes-line-function-presenter

