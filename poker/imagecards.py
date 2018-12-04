from PIL import Image

route = 'poker/cartas/{}.jpg'

offset = 130
card_size = 178
card_height = 315


def get_image_card(player_name, card_codes):
    length = card_codes.__len__()
    removal = 0
    if length > 2:
        removal = 5 * length * length
    background = Image.new('RGBA', (card_size * length - removal, card_height), (255, 255, 255, 255))
    for index, card_code in enumerate(card_codes):
        card = Image.open(route.format(card_code)).convert('RGBA')
        background.paste(card, (offset * index, 0), card)
    card_route = 'poker/players/{}.png'.format(player_name)
    background.save(card_route)
    return card_route
