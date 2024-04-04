# Synth: An Anonymization and Data Minimization Testbed

When training models on user data, it is important to remove information and context that can be tied back to the user.
This is a broad open-ended problem, and the solutions range from simple techniques like PII detection and removal
all the way to full anonymization, as defined by GDPR.

This is a simple prototype testbed for testing different anonymization solutions to understand how effective they are. We are 
interested in two things: how good is the solution at removing actual sensitive information about the user, and what is the 
overall loss in data quality by applying this solution. If a solution is close to optimal we would expect that it is 
particularly good at getting rid of identifying information while minmizing collateral damage to the rest of the content.

### Setting
The setting is here is that we have an anonymizer candidate. This could be a simple regex
based setup, or something that uses complex ML techniques under the hood. But the interface is fixed - it should take in a blob of text and return another blob of text.

``` output =  anonymizer(input)```

We are interested in how well this anonymizer works in practice. Specifically, is it actually good at detecting and removing identifying information, and is it good at 
preserving the information contained in the rest of input. We are going to evaluate the
anonymizer by trying it on different inputs and coming up with an aggregate score.

### Prereqs
The testbed uses various LLMs: GPT 3.5, GPT 4, Mistral, Neural Chat, etc. You need
access to providers that can run these models, such as OpenAI and Replicate, or run them 
locally where possible, with Ollama. The code actually uses Ollama but it can be easily 
configured to use Replicate instead. The code also needs `langchain` and `faker` along
with the client libraries of the model providers.


### The Testbed setup
A single run of the testbed works as follows: 
1. We start by defining a bunch of properties that we are likely to find in user generated content.
2. We then use a _synthesizer_ to generate a story with a subset of these properties.
3. We use the _anonymizer_ under consideration to process this story.
4. We use an _extractor_ to pull out properties from this processed story and compare with the properties we picked in Step 1.
5. We use a _estimator_ to evaluate if the processed story can be considered 'anonymized'. 
6. We assign a score for this run based on whether the anonymizer did a good job at actually anonymizing (step 4), and how well it preserved the non-sensitive parts of the
input (step 5).

We repeat this on multiple inputs and aggregate all the scores. This main evaluation loop is defined in `evalloop.py`. Let's look at the these components in more detail.

#### Property Definitions
The properties is defined in `properties.json` and includes things like where a user worked, what their car is, etc. Each property has
an associated sensitivity, in the form of the `identifying` and `weight` fields. The 
properties that are more likely to contain sensitive PII will have heigher weights.

#### Synthesizer
The synthesizer, defined in `synth.py` picks a set of properties and uses Mistral to generate a story blurb based on them.

#### Anonymizers
This is the component we are actually trying to test. There are couple of example anonymizer candidates already in the code, including one based on GPT-4 and one based on Microsoft Presidio. Feel free to try out other candidates.

#### Extractor
This component parses a unstructured text story and extracts a dictionary of key-value pairs representing the properties of the author of the story. There are a few implementations of this, but the best one seems to be based on Intel's Neural Chat LLM.
These are defined in `extractor.py`.

#### Estimator
This component takes as input a set of key value pairs representing the properties
of a user and estimates whether this information can be used to _identify_ the user.
Here, _identify_ determining how many unique people fall into the bucket defined 
by all these properties, and then checking if this bucket is smaller/larger than a set
threshold, defaulting to a million.

#### Scoring
We use a simple formula to compute the score for a run. The score is a tuple `(anon_score, match_score)`. `anon_score` is `1` if the estimator outputs that the story
is not identifiable; it's `0` otherwise. `match_score` is the fraction of properties from
the original story that are preserved in the anonymizer's output. Here we use fuzzy matching to ensure that we capture information that has been slightly modified but still
contains the original context.
