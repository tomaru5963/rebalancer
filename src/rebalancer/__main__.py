import sys
from .cli import main

"""
rc = 1
try:
    main()
    rc = 0
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
sys.exit(rc)
"""

sys.exit(main())
