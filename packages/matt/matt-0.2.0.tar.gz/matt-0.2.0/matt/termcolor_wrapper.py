# This file is part of Matt

# Copyright © 2020 Noisytoot
# MATT - MATT Arithmetic Training Test: Another maths test, this time in Python!

# Matt is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Matt is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Matt.  If not, see <https://www.gnu.org/licenses/>

import os, termcolor
__ALL__ = ["colored", "cprint"]
if "NO_COLOR" in os.environ:
    os.environ["ANSI_COLORS_DISABLED"] = "1"
colored = termcolor.colored
cprint = termcolor.cprint
