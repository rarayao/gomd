// +build !xtc

/*
 * charges.go, part of Bartender
 *
 *
 * Copyright 2020 Raul Mera <rmera{at}usach(dot)cl>
 *
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License along
 *  with this program; if not, write to the Free Software Foundation, Inc.,
 *  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 *
 */

/*To the long life of the Ven. Khenpo Phuntzok Tenzin Rinpoche*/

package main

import (
	"fmt"

	chem "github.com/rmera/gochem"
)

func OpenXTC(name string) (chem.Traj, error) {
	return nil, fmt.Errorf("XTC not supported! recompile Bartender with the xtc compilation tag")
}