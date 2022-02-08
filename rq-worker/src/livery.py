from fileinput import filename
import os
import json
from urllib.request import urlopen
from wand.image import Image
from wand.drawing import Drawing
from cairosvg import svg2png
from azure.storage.blob import BlockBlobService
from io import BytesIO


def create_aviator_lua(squadron_designation, aviator_callsign, lua_sections, lua_path):
    lua_text = "livery = {\n"        
    for lua_section in lua_sections:
        lua_text += f"\n{lua_section['text']}\n"
    lua_text += f"\n}}\nname = \"{squadron_designation} {aviator_callsign}\""
    azure_key = os.getenv('AZURE_STORAGE_KEY')
    account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME', 'jtf191blobstorage')
    azure_container = 'static'
    block_blob_service = BlockBlobService(account_name=account_name, account_key=azure_key)

    block_blob_service.create_blob_from_text(azure_container, lua_path, lua_text)


def get_ribbonrack_image(citations, prop):
    if citations:
        img_width = 100
        img_height = 28
        tmp_image = Image(width=len(citations)*img_width, height=img_height)
        draw = Drawing()
        for (idx, citation) in enumerate(citations):
            with Image(blob=svg2png(url=citation)) as cit_img:
                cit_img.resize(img_width)
                tmp_image.composite(image=cit_img, left=int(idx * (cit_img.width)), top=0)

        draw(tmp_image)
        
        if "angle" in prop:
            tmp_image.rotate(prop["angle"])

        if "flip" in prop and prop["flip"]:
            tmp_image.flip()

        if "flop" in prop and prop["flop"]:
            tmp_image.flop()
        
        if "scale" in prop and prop["scale"]:
            tmp_image.transform(resize=prop["scale"])

        return tmp_image


def get_killboard_subimage(icon_path, kills):
    max_icons = 30
    y_offset = 0
    tmp_image = Image(width=210, height=65)
    with Image(filename=icon_path) as icon_img:
        icon_img.transform(resize="x20")
        to_show = min(kills, max_icons)
        max_in_row = (tmp_image.width / icon_img.width) - 1
        x_offset = 0
        for _ in range(to_show):
            if x_offset >= max_in_row:
                x_offset = 0
                y_offset += 1

            tmp_image.composite(
                image=icon_img,
                left=int(x_offset * (icon_img.width)),
                top=int(y_offset * (icon_img.width))
            )
            x_offset += 1
        y_offset += 1

    return tmp_image


def get_killboard_image(combat_logs, prop):
    tmp_image = Image(width=210, height=200)
    draw = Drawing()

    air_kills_threshold = 20
    ground_kills_threshold = 100
    maritime_kills_threshold = 1

    y_offset = 0
    to_render = {
        "air": {
            "icon": "/usr/src/workers/src/icons/jet.png",
            "kills": 0
        },
        "ground": {
            "icon": "/usr/src/workers/src/icons/tank.png",
            "kills": 0
        },
        "maritime": {
            "icon": "/usr/src/workers/src/icons/carrier.png",
            "kills": 0
        }
    }
    for combat_log in combat_logs:
        if combat_log["target__category"] in [0, 1] and combat_log["kills"] >= air_kills_threshold:
            to_render["air"]["kills"] = int(combat_log["kills"] / air_kills_threshold)
        elif combat_log["target__category"] in [2, 4] and combat_log["kills"] >= ground_kills_threshold:
            to_render["ground"]["kills"] += int(combat_log["kills"] / ground_kills_threshold)
        elif combat_log["target__category"] == 3 and combat_log["kills"] >= maritime_kills_threshold:
            to_render["maritime"]["kills"] += int(combat_log["kills"] / maritime_kills_threshold)
        else:
            continue

    for log in to_render.values():
        if log["kills"] > 0:
            sub_image = get_killboard_subimage(log["icon"], log["kills"])
            tmp_image.composite(
                image=sub_image,
                left=0,
                top=int(y_offset * (sub_image.height))
            )
            y_offset += 1

    draw(tmp_image)
    
    if "angle" in prop:
        tmp_image.rotate(prop["angle"])

    if "flip" in prop and prop["flip"]:
        tmp_image.flip()

    if "flop" in prop and prop["flop"]:
        tmp_image.flop()
    
    if "scale" in prop and prop["scale"]:
        tmp_image.transform(resize=prop["scale"])

    return tmp_image


def get_callsign_image(aviator_props, prop):
    tmp_image = Image(width=prop["img_size"]["width"], height=prop["img_size"]["height"])
    draw = Drawing()

    if "font" in prop:
        draw.font = "fonts/" + prop["font"]

    if "font_size" in prop:
        draw.font_size = prop["font_size"]

    if "font_opacity" in prop:
        draw.fill_opacity = prop["font_opacity"]

    if "font_alignment" in prop:
        draw.text_alignment = prop["font_alignment"]

    text_offset_x = prop["text_offset_x"]
    text_offset_y = prop["text_offset_y"]

    if "type" in prop and prop["type"] == 2:
        draw.text(text_offset_x, text_offset_y, f'{aviator_props["rank"]} {aviator_props["first_name"]} "{aviator_props["callsign"]}" {aviator_props["last_name"]}')
    else:
        draw.text(text_offset_x, text_offset_y, f'{aviator_props["rank"]} {aviator_props["first_name"]} {aviator_props["last_name"]}')
        draw.text(text_offset_x, text_offset_y + int(draw.font_size), aviator_props["callsign"])

    draw(tmp_image)
    
    if "angle" in prop:
        tmp_image.rotate(prop["angle"])

    if "flip" in prop and prop["flip"]:
        tmp_image.flip()

    if "flop" in prop and prop["flop"]:
        tmp_image.flop()

    return tmp_image
    
def create_aviator_dds(aviator_props, skin_url, skin_description, citations, combat_logs, blob_path):
    response = urlopen(skin_url)
    with Image(file=response) as img:
        for prop in skin_description:
            if prop["prop"] == "callsign":
                img.composite(image=get_callsign_image(aviator_props, prop), left=prop["x"], top=prop["y"])

            if prop["prop"] == "award" and citations:
                img.composite(image=get_ribbonrack_image(citations, prop), left=prop["x"], top=prop["y"])

            if prop["prop"] == "killboard" and citations:
                img.composite(image=get_killboard_image(combat_logs, prop), left=prop["x"], top=prop["y"])

        # Result into a buffer
        buf = BytesIO()
        img.compression = 'dxt1'
        img.save(file=buf)

        azure_key = os.getenv('AZURE_STORAGE_KEY')
        account_name = os.getenv('AZURE_STORAGE_ACCOUNT_NAME', 'jtf191blobstorage')
        azure_container = 'static'
        block_blob_service = BlockBlobService(account_name=account_name, account_key=azure_key)

        block_blob_service.create_blob_from_bytes(container_name=azure_container, blob_name=blob_path, blob=buf.getvalue())