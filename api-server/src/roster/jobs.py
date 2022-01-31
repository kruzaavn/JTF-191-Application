import os

from django_rq import job
from wand.image import Image
from wand.drawing import Drawing
from cairosvg import svg2png
from azure.storage.blob import BlockBlobService
from io import BytesIO

from .models import CombatLog

@job
def create_aviator_lua(aviator, lua_sections, lua_path):

    lua_text = "livery = {\n"        
    for lua_section in lua_sections:
        lua_text += f"\n{lua_section.text}\n"
    lua_text += f"\n}}\nname = \"{aviator.squadron.designation} {aviator.callsign}\""

    azure_key = os.getenv('AZURE_STORAGE_KEY')
    account_name = 'jtf191blobstorage'
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
            with Image(blob=svg2png(bytestring=citation.award.ribbon_image.read())) as cit_img:
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


def get_killboard_subimage(icon_path, combat_log, min_kills):
    max_icons = 30
    y_offset = 0
    tmp_image = Image(width=210, height=65)
    with Image(filename=icon_path) as icon_img:
        icon_img.transform(resize="x20")
        to_show = min(int(combat_log.kills / min_kills), max_icons)
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


def get_killboard_image(aviator_id, prop):
    tmp_image = Image(width=210, height=200)
    draw = Drawing()

    min_air_kills = 20
    min_ground_kills = 100
    min_maritime_kills = 1

    sql_query = """
                select 
                    COUNT(category) as kills, 
                    category as target_category, 
                    1 as id 
                from 
                    roster_combatlog 
                inner join 
                    roster_target on roster_target.id = roster_combatlog.target_id 
                where 
                    aviator_id=%s and type='kill' 
                group by 
                    category; """

    combat_logs = CombatLog.objects.raw(sql_query, [aviator_id])

    y_offset = 0
    for combat_log in combat_logs:
        if combat_log.target_category in [0, 1] and combat_log.kills >= min_air_kills:
            icon = 'icons/jet.png'
            min_kills = min_air_kills
        elif combat_log.target_category in [2, 4] and combat_log.kills >= min_ground_kills:
            icon = 'icons/tank.png'
            min_kills = min_ground_kills
        elif combat_log.target_category == 3 and combat_log.kills >= min_maritime_kills:
            icon = 'icons/carrier.png'
            min_kills = min_maritime_kills
        else:
            continue

        sub_image = get_killboard_subimage(icon, combat_log, min_kills)
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


def get_callsign_image(aviator, prop):
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
        draw.text(text_offset_x, text_offset_y, f"{aviator.rank} {aviator.first_name} \"{aviator.callsign}\" {aviator.last_name}")
    else:
        draw.text(text_offset_x, text_offset_y, f"{aviator.rank} {aviator.first_name} {aviator.last_name}")
        draw.text(text_offset_x, text_offset_y + int(draw.font_size), f"{aviator.callsign}")

    draw(tmp_image)
    
    if "angle" in prop:
        tmp_image.rotate(prop["angle"])

    if "flip" in prop and prop["flip"]:
        tmp_image.flip()

    if "flop" in prop and prop["flop"]:
        tmp_image.flop()

    return tmp_image
    
@job
def create_aviator_dds(skin, aviator, blob_path):
    with Image(file=skin.dds_file.open(mode='rb')) as img:
        for prop in skin.json_description:
            if prop["prop"] == "callsign":
                img.composite(image=get_callsign_image(aviator, prop), left=prop["x"], top=prop["y"])

            citations = aviator.citations.all()[0:3] # only showing max 3 ribbons
            if prop["prop"] == "award" and citations:
                img.composite(image=get_ribbonrack_image(citations, prop), left=prop["x"], top=prop["y"])

            if prop["prop"] == "killboard" and citations:
                img.composite(image=get_killboard_image(aviator.id, prop), left=prop["x"], top=prop["y"])

        # Result into a buffer
        buf = BytesIO()
        img.compression = 'dxt1'
        img.save(file=buf)

        azure_key = os.getenv('AZURE_STORAGE_KEY')
        account_name = 'jtf191blobstorage'
        azure_container = 'static'
        block_blob_service = BlockBlobService(account_name=account_name, account_key=azure_key)

        block_blob_service.create_blob_from_bytes(container_name=azure_container, blob_name=blob_path, blob=buf.getvalue())