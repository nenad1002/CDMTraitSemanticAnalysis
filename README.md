# TraitSemanticAnalysis

The file account.cdm.json.out has suggested traits for attributes inside the applicationCommon/Account entity as an example. While it is still not perfect, thanks to NLP processing some of the traits are easily discovered such as for the aging30 attribute:

**aging30**
means.demographic.age
means.measurement.age

where it find the common root of words age and aging.

Work that will be done during hackathon:
- Find a way to reduce noise
- Find a way to incoporate description into the equation (content of the is.localized.described as and is.localized.displayedAs trait) by executing POS and named entity recognition on top of it, also checking hypernym-hyponym relationship might be useful
- Rank traits for suggestions based on how important they appear
- Build better UX for users
- Find a way to resolve entities with Python to have a full set of attributes
- Anything else that might be interesting to do or anaylize.

