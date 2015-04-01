'''
lib.views.utils
Utilities for view code.
'''

def remove_objects_from_serialized(serialized):
    serialized = serialized.replace('<object type="hash">', '')
    serialized = serialized.replace('</object>', '')
    serialized = serialized.replace('<objects>', '')
    serialized = serialized.replace('</objects>', '')
    return serialized
    
def remove_objects(parent):
    """
    Function to clean out object elements created by the tasty-pie serializer.
    """
    objects = parent.findall('object')
    if objects:
        children = [o.getchildren()[0] for o in objects]
        for object in objects:
            parent.remove(object)
        for child in children:
            parent.append(child)
    for child in parent.getchildren():
        remove_objects(child)
