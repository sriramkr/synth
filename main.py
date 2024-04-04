import estimate
import extract
import synth
import pprint
import flags
from evalloop import *
from anonymizers import *
from estimate import *
from extract import *
from predict import *
from synth import *
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_community.llms import Ollama
from langchain.schema.output_parser import StrOutputParser
import random
import json
import time
from faker import Faker
from estimate import is_identifiable_gpt4
from evalloop import evalloop
fake = Faker()

property_loader()
pp = pprint.PrettyPrinter(indent=4)
flags.debug = False


# To generate more stories run
synth.generate_stories()

# To generate generic stories, run
synth.generate_generic_stories()

# To run extraction tests, run
extract.extract_test()

# To run estimation tests, run
estimate.estimate_test()

# To run extraction + estimation tests, run
estimate.extract_estimate_test()

# To run the main loop, run
evalloop()

txt = "I saw a Lamborghini on my walk to the beach."

out = anonymize_gpt4(txt)
print(out)

estimate_test(10)
extract_estimate_test()

evalloop()
