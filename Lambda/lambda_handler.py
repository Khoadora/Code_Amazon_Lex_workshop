import json

friedChickenSizes = ['small', 'medium', 'large', 'family size']
friedChicken_branch = ['kfc', 'jollipee', 'texas']
kfc_types = ['original', 'extra crispy', 'hot & spicy']
jollipee_types = ['classic', 'spicy', 'sweet chili']
texas_types = ['smoky bbq', 'cajun spice', 'honey butter']



def validate_order(slots):
    # Validate FriedChickenSizes
    if 'FriedChickenSizes' not in slots or not slots['FriedChickenSizes']:
        print('Validating FriedChickenSizes Slot')

        return {
            'isValid': False,
            'invalidSlot': 'FriedChickenSizes'
        }

    if slots['FriedChickenSizes']['value']['originalValue'].lower() not in friedChickenSizes:
        print('Invalid FriedChickenSizes')

        return {
            'isValid': False,
            'invalidSlot': 'FriedChickenSizes',
            'message': 'Please select a {} burger size.'.format(", ".join(friedChickenSizes))
        }

    # Validate FriedChicken_branch
    if 'FriedChicken_branch' not in slots or not slots['FriedChicken_branch']:
        print('Validating FriedChicken_branch Slot')

        return {
            'isValid': False,
            'invalidSlot': 'FriedChicken_branch'
        }

    if slots['FriedChicken_branch']['value']['originalValue'].lower() not in friedChicken_branch:
        print('Invalid FriedChicken_branch')

        return {
            'isValid': False,
            'invalidSlot': 'FriedChicken_branch',
            'message': 'Please select from {} burger franchises.'.format(", ".join(friedChicken_branch))
        }

    # Validate FriedChicken_Types
    if 'FriedChicken_Types' not in slots or not slots['FriedChicken_Types']:
        print('Validating FriedChicken_Types Slot')

        return {
            'isValid': False,
            'invalidSlot': 'FriedChicken_Types'
        }

    # Validate FriedChicken_Types for FriedChicken_branch
    branch_value = slots['FriedChicken_branch']['value']['originalValue'].lower()
    type_value = slots['FriedChicken_Types']['value']['originalValue'].lower()

    if branch_value == 'kfc':
        if type_value not in kfc_types:
            print('Invalid FriedChicken_Types for KFC')

            return {
                'isValid': False,
                'invalidSlot': 'FriedChicken_Types',
                'message': 'Please select a KFC type of {}.'.format(", ".join(kfc_types))
            }

    elif branch_value == 'jollipee':
        if type_value not in jollipee_types:
            print('Invalid FriedChicken_Types for Jollipee')

            return {
                'isValid': False,
                'invalidSlot': 'FriedChicken_Types',
                'message': 'Please select a Jollipee type of {}.'.format(", ".join(jollipee_types))
            }

    elif branch_value == 'texas':
        if type_value not in texas_types:
            print('Invalid FriedChicken_Types for Texas')

            return {
                'isValid': False,
                'invalidSlot': 'FriedChicken_Types',
                'message': 'Please select a Texas type of {}.'.format(", ".join(texas_types))
            }

    # Valid Order
    return {'isValid': True}



def lambda_handler(event, context):
    print(event)

    bot = event['bot']['name']
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    order_validation_result = validate_order(slots)

    if event['invocationSource'] == 'DialogCodeHook':
        if not order_validation_result['isValid']:
            if 'message' in order_validation_result:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    },
                    "messages": [
                        {
                            "contentType": "PlainText",
                            "content": order_validation_result['message']
                        }
                    ]
                }
            else:
                response = {
                    "sessionState": {
                        "dialogAction": {
                            "slotToElicit": order_validation_result['invalidSlot'],
                            "type": "ElicitSlot"
                        },
                        "intent": {
                            "name": intent,
                            "slots": slots
                        }
                    }
                }
        else:
            response = {
                "sessionState": {
                    "dialogAction": {
                        "type": "Delegate"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots
                    }
                }
            }

    if event['invocationSource'] == 'FulfillmentCodeHook':
        response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": slots,
                    "state": "Fulfilled"
                }

            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "I've placed your order."
                }
            ]
        }

    print(response)
    return response
