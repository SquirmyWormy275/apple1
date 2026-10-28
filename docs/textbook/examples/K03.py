from tools.card_image import rehearse_reader

result = rehearse_reader()
for action, text in result.items():
    print(action + ":", repr(text))
