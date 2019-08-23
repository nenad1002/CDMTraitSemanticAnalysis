# CDMTraitSemanticAnalysis project


The purpose of this project is to find traits for entities and attributes inside [CDM](https://docs.microsoft.com/en-us/common-data-model/) schema documents.
The schema documents folder can be found in the project.

The proposed traits are being found by running NLP analysis on the name and descriptions of every entity.

The Jaccard index between the set of generated and sample traits is above 0.7

The project uses both **NLTK** and **Spacy** as NLP processing libraries in order to tokenize, stem, lemma and do vector-based comparison of the description sencences.
In order to run it, just install the requirements and run main.py to follow additional instructions.

Example:

Attribute name: agingId
Description: Represents the Microsoft's subsidiary age ID that have positive ROI every year.
Proposed traits: ['means.demographic.age', 'means.measurement.age', 'means.identity', 'means.idea.company', 'means.idea.organization', 'means.idea.organization.unit', 'means.identity.company.name']

As it is clear from the proposed set of traits, the analyzer will try to find appropriate features inside the description while ignoring the ones that are not important to find the correct traits.
