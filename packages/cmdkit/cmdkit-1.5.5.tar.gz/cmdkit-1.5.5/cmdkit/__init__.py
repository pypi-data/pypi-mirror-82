# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Package initialization for CmdKit."""


from .__meta__ import (__pkgname__, __version__, __authors__, __contact__,\
                       __license__, __copyright__, __description__)

import sys
if sys.version_info < (3, 7):
    raise SystemError('cmdkit requires at least Python 3.7 to run.')

