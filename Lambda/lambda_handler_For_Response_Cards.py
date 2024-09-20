import json

friedChickenSizes = ['small', 'medium', 'large', 'family size']
friedChicken_branch = ['kfc', 'jollipee', 'texas']
kfc_types = ['original', 'extra crispy', 'hot & spicy']
jollipee_types = ['classic', 'spicy', 'sweet chili']
texas_types = ['smoky bbq', 'cajun spice', 'honey butter']

def validate_order(slots):
    # Validate FriedChickenSizes
    if not slots['FriedChickenSizes']:
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
            'message': 'Please select a {} fried chicken size.'.format(", ".join(friedChickenSizes))
        }

    # Validate FriedChicken_branch
    if not slots['FriedChicken_branch']:
        print('Validating FriedChicken_branch Slot')

        return {
            'isValid': False,
            'invalidSlot': 'FriedChicken_branch'
        }

    if slots['FriedChicken_branch']['value']['originalValue'].lower() not in friedChicken_branch:
        print('Invalid FriedChickenSizes')

        return {
            'isValid': False,
            'invalidSlot': 'FriedChicken_branch',
            'message': 'Please select from {} fried chicken branch.'.format(", ".join(friedChicken_branch))
        }

    # Validate FriedChicken_Types
    if not slots['FriedChicken_Types']:
        print('Validating FriedChicken_Types Slot')

        return {
            'isValid': False,
            'invalidSlot': 'FriedChicken_Types',
            'invalidFranchise': ''
        }

    # Validate FriedChicken_Types for FriedChicken_branch
    if slots['FriedChicken_branch']['value']['originalValue'].lower() == 'kfc':
        if slots['FriedChicken_Types']['value']['originalValue'].lower() not in kfc_types:
            print('Invalid FriedChicken_Types for KFC')

            return {
                'isValid': False,
                'invalidSlot': 'FriedChicken_Types',
                'invalidFranchise': 'kfc',
                'message': 'Please select a KFC type of {}.'.format(", ".join(kfc_types))
            }

    if slots['FriedChicken_branch']['value']['originalValue'].lower() == 'jollipee':
        if slots['FriedChicken_Types']['value']['originalValue'].lower() not in jollipee_types:
            print('Invalid FriedChicken_Types for Jollipee')

            return {
                'isValid': False,
                'invalidSlot': 'FriedChicken_Types',
                'invalidFranchise': 'jollipee',
                'message': 'Please select a Jollipee type of {}.'.format(", ".join(jollipee_types))
            }

    if slots['FriedChicken_branch']['value']['originalValue'].lower() == 'texas':
        if slots['FriedChicken_Types']['value']['originalValue'].lower() not in texas_types:
            print('Invalid FriedChicken_Types for Texas')

            return {
                'isValid': False,
                'invalidSlot': 'FriedChicken_Types',
                'invalidFranchise': 'texas',
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
    print(order_validation_result)

    if event['invocationSource'] == 'DialogCodeHook':
        if not order_validation_result['isValid']:
            response_message = 'FriedChickenFriend'
            if 'message' in order_validation_result:
                response_message = order_validation_result['message']

            response_card_sub_title = ''
            response_card_buttons = []

            kfc_sub_title = 'Please select a Fried Chicken type'
            kfc_buttons = [
                {
                    "text": "Original",
                    "value": "original"
                },
                {
                    "text": "Extra Crispy",
                    "value": "extra crispy"
                },
                {
                    "text": "Hot & Spicy",
                    "value": "hot & spicy"
                }
            ]

            jollipee_sub_title = 'Please select a Jollipee type'
            jollipee_buttons = [
                {
                    "text": "Classic",
                    "value": "classic"
                },
                {
                    "text": "Spicy",
                    "value": "spicy"
                },
                {
                    "text": "Sweet Chili",
                    "value": "sweet chili"
                }
            ]
            
            texas_sub_title = 'Please select a Texas type'
            texas_buttons = [
                {
                    "text": "Smoky BBQ",
                    "value": "smoky bbq"
                },
                {
                    "text": "Cajun Spice",
                    "value": "cajun spice"
                },
                {
                    "text": "Honey Butter",
                    "value": "honey butter"
                }
            ]

            if order_validation_result['invalidSlot'] == "FriedChickenSizes":
                response_card_sub_title = "Please select a Fried Chicken size"
                response_card_buttons = [
                    {
                        "text": "Small",
                        "value": "small"
                    },
                    {
                        "text": "Medium",
                        "value": "medium"
                    },
                    {
                        "text": "Large",
                        "value": "large"
                    },
                    {
                        "text": "Family Size",
                        "value": "family size"
                    }
                ]

            if order_validation_result['invalidSlot'] == "FriedChicken_branch":
                response_card_sub_title = "Please select a Fried Chicken franchise"
                response_card_buttons = [
                    {
                        "text": "KFC",
                        "value": "kfc"
                    },
                    {
                        "text": "Jollipee",
                        "value": "jollipee"
                    },
                    {
                        "text": "Texas",
                        "value": "texas"
                    }
                ]

            if order_validation_result['invalidSlot'] == "FriedChicken_Types":
                if order_validation_result['invalidFranchise'] == "kfc":
                    response_card_sub_title = kfc_sub_title
                    response_card_buttons = kfc_buttons
                elif order_validation_result['invalidFranchise'] == "jollipee":
                    response_card_sub_title = jollipee_sub_title
                    response_card_buttons = jollipee_buttons 
                elif order_validation_result['invalidFranchise'] == "texas":
                    response_card_sub_title = texas_sub_title
                    response_card_buttons = texas_buttons
                else:
                    response_card_sub_title = 'Please select a fried chicken type'
                    response_card_buttons = [
                        {
                            "text": "Original",
                            "value": "original"
                        },
                        {
                            "text": "Extra Crispy",
                            "value": "extra crispy"
                        },
                        {
                            "text": "Hot & Spicy",
                            "value": "hot & spicy"
                        }
                        ,
                        {
                            "text": "Classic",
                            "value": "classic"
                        },
                        {
                            "text": "Spicy",
                            "value": "spicy"
                        }
                    ]

            response = {
                "sessionState": {
                    "dialogAction": {
                        "slotToElicit": order_validation_result['invalidSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots,
                    }
                },
                "messages": [
                    {
                        "contentType": "ImageResponseCard",
                        "content": response_message,
                        "imageResponseCard": {
                            "title": "FriedChickenFriend",
                            "subtitle": response_card_sub_title,
                            "buttons": response_card_buttons
                        }
                    }
                ]
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
