

## 1. Project Overview & Timeline

- **Target Conference:** MASCOTS 2026
    
- **Submission Deadline:** May 17, 2026
    
- **Format Requirements:** IEEE double-column format
    
- **Target Length:** 9 to 10 pages maximum
    
- **Core Narrative Arc:** Problem (Assumption of transferability) $\rightarrow$ Proof (84 experiments proving transfer fails) $\rightarrow$ Solution (The Local Telemetry Blueprint).
    

## 2. The 9-Page Paper Outline

1. **Abstract (~250 words):** Hook the reader with the failure of cross-cluster transfer, then introduce the minimal telemetry blueprint for reliable local training.
    
2. **§1 Introduction (~1 Page):** Detail the HPC community's need for predictive models, the false assumption of naive transfer, and outline the paper's three contributions (Dataset, Negative Proof, Local Blueprint).
    
3. **§2 Background & Related Work (~1 Page):** Cover FRESCO v1's limitations (lack of provenance) and why standard domain adaptation fails in HPC hardware environments.
    
4. **§3 FRESCO Dataset & Measurement Provenance (~1.5 Pages):** Explain the dataset infrastructure (hardware normalization, explicit semantics) acting as the diagnostic tool to prove _why_ models fail.
    
5. **§4 The Illusion of Transfer: 84 Experiments (~2 Pages):** Summarize the setup and deliver the "sledgehammer" visual showing the total collapse of models ($-24$ $R^2$), detailing covariate, conditional, and era shifts as the culprits.
    
6. **§5 The Local Telemetry Blueprint (~2.5 Pages):** _[WORK IN PROGRESS]_ The actionable solution. Define the "subset of given conditions" (minimal telemetry) and the specific training strategy required for a cluster to build a successful local model.
    
7. **§6 Conclusion (~0.5 Pages):** Wrap up the narrative arc from the failure of the old assumption to the success of the new blueprint.
    

---

# Execution Guide: Completing Section 5

Section 5 is the "recipe" section of your paper. Since Section 4 proves you can't just share a chef (a model) between different kitchens (clusters), Section 5 must provide the exact list of ingredients and cooking instructions for a cluster to train their own chef successfully.

To write this section, you need to define two distinct things:

### Part A: The Subset of Given Conditions (The Ingredients)

You need to identify the absolute minimum telemetry data a supercomputer must collect. Logging everything is too expensive. Look at your 84 experiments: which features in FRESCO v2 carried the most weight when a model _was_ successful locally?

- **Action:** Group these features logically (e.g., "Hardware-Normalized Memory Metrics," "Job Topology," "User History").
    
- **Goal:** Create a definitive, standardized checklist. "If you want to predict memory, your cluster must log exactly these _N_ things."
    

### Part B: The Training Strategy (The Cooking Instructions)

Once they have the right data, how should they train the model so it doesn't fall victim to the traps you found in Section 4?

- **Action:** Define the exact steps. How should they handle data splits? How frequently do they need to retrain to avoid "era shift"? How should they handle new hardware partitions being added to the cluster (to avoid "covariate shift")?
    
- **Goal:** A step-by-step methodology that data engineers can implement to guarantee a robust, locally trained model.
    

---

### LLM Prompts to Accelerate Section 5

When you are ready to tackle this section, use these prompts with me (or your preferred local AI coding assistant) to do the heavy lifting. Just fill in the bracketed information with your actual FRESCO data.

**Prompt 1: Extracting the "Subset of Given Conditions"**

> "I am writing the 'Local Telemetry Blueprint' section of my HPC paper. Based on my local training runs, the following features had the highest feature importance scores for predicting memory usage: [Paste your top features/metrics here]. Help me categorize these into 3 to 4 logical 'Telemetry Pillars' (e.g., Hardware Context, Job Constraints). Write a clear, intuitive paragraph for each pillar explaining _why_ this specific data is absolutely critical to collect, using the context that missing this data causes conditional or covariate shifts."

**Prompt 2: Drafting the Training Strategy**

> "I need to draft a 'Local Training Strategy' for supercomputing clusters. My previous experiments proved that models fail over time due to 'era shift' (hardware aging/software updates) and 'covariate shift' (adding new node types). Draft a 3-step training and maintenance strategy that tells an HPC data engineer exactly how to train a model initially, and exactly what operational triggers should force them to retrain the model to avoid those shifts."

**Prompt 3: The Reviewer Stress-Test**

> "Act as a highly critical reviewer for the MASCOTS computing conference. Read my proposed 'Local Telemetry Blueprint' below. Attack it from the perspective of a cluster administrator who thinks logging this much data is too expensive, or a data scientist who thinks the training strategy is too basic. Give me the top 3 weaknesses in my argument and suggest how to patch them before I submit."
> 
> [Paste your drafted Section 5 here]
