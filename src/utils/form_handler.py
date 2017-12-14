"""Form handler util -- Used to handle form from the request"""

from exceptions.BadFormData import BadFormData

def extract_attribute(request, attribute):
    try:
        return request.form[attribute]
    except Exception as e:
        raise BadFormData(attribute + ' field is missing')