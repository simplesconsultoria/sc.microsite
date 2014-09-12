# -*- coding: utf-8 -*-
from sc.microsite.config import ADD_PERMISSION


def change_add_permission(object, event):
    """Remove all roles from 'sc.microsite: Add Microsite' permission inside
    a Microsite. We do that to avoid having a Microsite inside a Microsite.
    """
    object.manage_permission(
        ADD_PERMISSION,
        roles=[]
    )
