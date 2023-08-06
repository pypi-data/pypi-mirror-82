# -*- coding: utf-8 -*-

from ....Classes.Arc1 import Arc1
from ....Classes.Arc3 import Arc3
from ....Classes.Segment import Segment
from ....Classes.SurfLine import SurfLine


def build_geometry_wind(self, Nrad, Ntan, is_simplified=False, alpha=0, delta=0):
    """Split the slot winding area in several zone

    Parameters
    ----------
    self : SlotW26
        A SlotW26 object
    Nrad : int
        Number of radial layer
    Ntan : int
        Number of tangentiel layer
    is_simplified : bool
        boolean to specify if coincident lines are considered as one or different lines (Default value = False)
    alpha : float
        Angle for rotation (Default value = 0) [rad]
    delta : Complex
        complex for translation (Default value = 0)

    Returns
    -------
    surf_list: list
        List of surface delimiting the winding zone

    """

    if self.get_is_stator():  # check if the slot is on the stator
        st = "S"
    else:
        st = "R"
    # getting all point coordinate
    [
        Z1,
        Z2,
        Z3,
        Z4,
        Z5,
        Z6,
        Z7,
        Z8,
        Ztan1,
        Ztan2,
        Zmid,
        Zrad1,
        Zrad2,
        rot_sign,
    ] = self._comp_point_coordinate()
    # We can split in rad only if Zrad1 is between Z6 and Z5
    is_rad_splittable = self.H1 > 0 and (
        (Z6.real < Zrad1.real and Zrad1.real < Z5.real)
        or (Z5.real < Zrad1.real and Zrad1.real < Z6.real)
    )

    # Creation of curve
    rot_sign = rot_sign * -1
    surf_list = list()
    if Nrad == 1 and Ntan == 2:
        if is_simplified:  # no doubling Line allowed
            # Part 1 (0,0)
            curve_list = list()
            curve_list.append(Segment(Z7, Ztan1))
            curve_list.append(Segment(Ztan1, Ztan2))
            point_ref = (Z7 + Ztan1 + Ztan2 + Z5 + Z6) / 5
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R0_T0_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
            # Part2 (0,1)
            curve_list = list()
            curve_list.append(Segment(Ztan1, Z2))
            point_ref = (Ztan1 + Z2 + Z3 + Z4 + Ztan2) / 5
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R0_T1_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
        else:

            # Part 1 (0,0)
            curve_list = list()
            curve_list.append(Segment(Z7, Ztan1))
            curve_list.append(Segment(Ztan1, Ztan2))
            curve_list.append(
                Arc1(
                    Ztan2,
                    Z5,
                    rot_sign * self.R2,
                    is_trigo_direction=not self.is_outwards(),
                )
            )
            curve_list.append(Segment(Z5, Z6))
            curve_list.append(
                Arc1(
                    Z6,
                    Z7,
                    rot_sign * self.R1,
                    is_trigo_direction=not self.is_outwards(),
                )
            )
            point_ref = (Z7 + Ztan1 + Ztan2 + Z5 + Z6) / 5
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R0_T0_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
            # Part2 (0,1)
            curve_list = list()
            curve_list.append(Segment(Ztan1, Z2))
            curve_list.append(
                Arc1(
                    Z2,
                    Z3,
                    rot_sign * self.R1,
                    is_trigo_direction=not self.is_outwards(),
                )
            )
            curve_list.append(Segment(Z3, Z4))
            curve_list.append(
                Arc1(
                    Z4,
                    Ztan2,
                    rot_sign * self.R2,
                    is_trigo_direction=not self.is_outwards(),
                )
            )
            curve_list.append(Segment(Ztan2, Ztan1))
            point_ref = (Ztan1 + Z2 + Z3 + Z4 + Ztan2) / 5
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R0_T1_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
    elif Nrad == 2 and Ntan == 1 and is_rad_splittable:
        if is_simplified:  # no doubling Line allowed
            # Part 1 (0,0)
            curve_list = list()
            curve_list.append(Segment(Z7, Z2))
            curve_list.append(Segment(Zrad2, Zrad1))
            point_ref = (Z7 + Z2 + Z3 + Zrad2 + Zrad1 + Z6) / 6
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R0_T0_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
            # Part2 (1,0)
            curve_list = list()
            point_ref = (Zrad1 + Zrad2 + Z4 + Z5) / 4
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R1_T0_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
        else:

            # Part 1 (0,0)
            curve_list = list()
            curve_list.append(Segment(Z7, Z2))
            curve_list.append(
                Arc1(
                    Z2,
                    Z3,
                    rot_sign * self.R1,
                    is_trigo_direction=not self.is_outwards(),
                )
            )
            curve_list.append(Segment(Z3, Zrad2))
            curve_list.append(Segment(Zrad2, Zrad1))
            curve_list.append(Segment(Zrad1, Z6))
            curve_list.append(
                Arc1(
                    Z6,
                    Z7,
                    rot_sign * self.R1,
                    is_trigo_direction=not self.is_outwards(),
                )
            )
            point_ref = (Z7 + Z2 + Z3 + Zrad2 + Zrad1 + Z6) / 6
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R0_T0_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
            # Part2 (1,0)
            curve_list = list()
            curve_list.append(Segment(Zrad1, Zrad2))
            curve_list.append(Segment(Zrad2, Z4))
            curve_list.append(Arc3(Z4, Z5, not self.is_outwards()))
            curve_list.append(Segment(Z5, Zrad1))
            point_ref = (Zrad1 + Zrad2 + Z4 + Z5) / 4
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R1_T0_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
    elif Nrad == 2 and Ntan == 2 and is_rad_splittable:
        if is_simplified:  # no doubling Line allowed
            # Part 1 (0,0)
            curve_list = list()
            curve_list.append(Segment(Z7, Ztan1))
            curve_list.append(Segment(Ztan1, Zmid))
            curve_list.append(Segment(Zmid, Zrad1))
            point_ref = (Z7 + Ztan1 + Zmid + Zrad1 + Z6) / 5
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R0_T0_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
            # Part2 (1,0)
            curve_list = list()
            curve_list.append(Segment(Zmid, Ztan2))
            point_ref = (Zrad1 + Zmid + Ztan2 + Z5) / 4
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R1_T0_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
            # Part 3 (0,1)
            curve_list = list()
            curve_list.append(Segment(Ztan1, Z2))
            curve_list.append(Segment(Zrad2, Zmid))
            point_ref = (Ztan1 + Z2 + Z3 + Zrad2 + Zmid) / 5
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R0_T1_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
            # Part4 (1,1)
            curve_list = list()
            point_ref = (Zmid + Zrad2 + Z4 + Ztan2) / 4
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R1_T1_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
        else:
            # Part 1 (0,0)
            curve_list = list()
            curve_list.append(Segment(Z7, Ztan1))
            curve_list.append(Segment(Ztan1, Zmid))
            curve_list.append(Segment(Zmid, Zrad1))
            curve_list.append(Segment(Zrad1, Z6))
            curve_list.append(
                Arc1(
                    Z6,
                    Z7,
                    rot_sign * self.R1,
                    is_trigo_direction=not self.is_outwards(),
                )
            )
            point_ref = (Z7 + Ztan1 + Zmid + Zrad1 + Z6) / 5
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R0_T0_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
            # Part2 (1,0)
            curve_list = list()
            curve_list.append(Segment(Zrad1, Zmid))
            curve_list.append(Segment(Zmid, Ztan2))
            curve_list.append(
                Arc1(
                    Ztan2,
                    Z5,
                    rot_sign * self.R2,
                    is_trigo_direction=not self.is_outwards(),
                )
            )
            curve_list.append(Segment(Z5, Zrad1))
            point_ref = (Zrad1 + Zmid + Ztan2 + Z5) / 4
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R1_T0_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
            # Part 3 (0,1)
            curve_list = list()
            curve_list.append(Segment(Ztan1, Z2))
            curve_list.append(
                Arc1(
                    Z2,
                    Z3,
                    rot_sign * self.R1,
                    is_trigo_direction=not self.is_outwards(),
                )
            )
            curve_list.append(Segment(Z3, Zrad2))
            curve_list.append(Segment(Zrad2, Zmid))
            curve_list.append(Segment(Zmid, Ztan1))
            point_ref = (Ztan1 + Z2 + Z3 + Zrad2 + Zmid) / 5

            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R0_T1_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
            # Part4 (1,1)
            curve_list = list()
            curve_list.append(Segment(Zmid, Zrad2))
            curve_list.append(Segment(Zrad2, Z4))
            curve_list.append(
                Arc1(
                    Z4,
                    Ztan2,
                    rot_sign * self.R2,
                    is_trigo_direction=not self.is_outwards(),
                )
            )
            curve_list.append(Segment(Ztan2, Zmid))
            point_ref = (Zmid + Zrad2 + Z4 + Ztan2) / 4
            surface = SurfLine(
                line_list=curve_list,
                label="Wind" + st + "_R1_T1_S0",
                point_ref=point_ref,
            )
            surf_list.append(surface)
    else:  # Default : only one zone
        # Only one zone for type 2_6 for now
        curve_list = self.build_geometry()
        # Remove the isthmus part
        curve_list = curve_list[1:-1]
        curve_list = [Segment(curve_list[-1].end, curve_list[0].begin)] + curve_list
        surface = SurfLine(
            line_list=curve_list, label="Wind" + st + "_R0_T0_S0", point_ref=Zmid
        )
        surf_list.append(surface)

    for surf in surf_list:
        surf.rotate(alpha)
        surf.translate(delta)
    return surf_list


class Slot26_H1(Exception):
    """ """

    pass
