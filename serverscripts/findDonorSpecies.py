
import sys

import os

freq = os.system("cut -f 1 {} | cut -d ':' -f 2 | cut -d '(' -f 1 | sort | uniq -c | sort -n".format(sys.argv[1]))

print(freq)