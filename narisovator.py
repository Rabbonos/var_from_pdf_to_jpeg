from PIL import Image, ImageDraw, ImageFont

# Load the image where you want to add the table row (optional, can create a blank image)
image_path = "outputzakaz.jpg"
image = Image.open(image_path)

# Initialize ImageDraw object
draw = ImageDraw.Draw(image)

def draw_second_table_row(draw, json_data):

    balki=[]
    rows=len(json_data['комплектация(размеры)']['профиль/сечение каждой балки'])
    if rows>1:
        for i in range(rows):
                balki.append( [json_data['комплектация(размеры)']['длина каждой балки'][i], json_data['комплектация(размеры)']['профиль/сечение каждой балки'][i] , json_data['максимально допустимые нагрузки']['на каждую пару балок'][i]])
    else:
         balki.append( [json_data['комплектация(размеры)']['длина каждой балки'], json_data['комплектация(размеры)']['профиль/сечение каждой балки'] , json_data['максимально допустимые нагрузки']['на каждую пару балок']] )
    # Define the table row parameters (coordinates for the row)
    row_top = 1002  # Y coordinate for the top of the row
    row_bottom = 1052  # Y coordinate for the bottom of the row
    column_widths = [881, 1283, 1503, 1961]  # X coordinates of each column boundary, these are constant

    for row in range(rows):
        # Draw a single row (as a series of horizontal and vertical lines)
        for i in range(len(column_widths)):
            # Draw vertical lines between columns
            draw.line([(column_widths[i], row_top), (column_widths[i], row_bottom)], fill="black", width=2)

        # Draw top and bottom lines of the row
        draw.line([(column_widths[0], row_top), (column_widths[-1], row_top)], fill="black", width=2)
        draw.line([(column_widths[0], row_bottom), (column_widths[-1], row_bottom)], fill="black", width=2)

        # Add text in the cells
        font = ImageFont.truetype("arial.ttf", 30)
        draw.text((column_widths[0] + 10, row_top + 5), f"{str(balki[row][1])}", font=font, fill="black")
        draw.text((column_widths[1] + 10, row_top + 5), f"{str(balki[row][0])}", font=font, fill="black")
        draw.text((column_widths[2] + 10, row_top + 5), f"{str(balki[row][2])}", font=font, fill="black")

        row_top= row_top+50
        row_bottom=row_bottom+50

# draw_table_row(draw, 3)

#drawing other values   
#эксплуатирующая организация ( 1877 180)
#производитель (1877 295)
#расположение объекта контроля ( 1750  380)
#высота рамы  (1800 445)
# профиль стойки   (1800 520)
#количество уровней (1877 585)
# макс высота первого уровня (1800 650)
# макс нагрузка на секцию (1800 720)

def draw_first_table(draw, json_data):

        organisation=json_data['заказчик']
        producer=json_data['производитель стеллажа']
        location=json_data['адрес объекта контроля']
        height=json_data['комплектация(размеры)']['высота рамы']
        profile=json_data['комплектация(размеры)']['профиль/сечение стойки']
        #levels=json_data['количество уровней'] use vision model to extract this
        #max_height=json_data['макс высота первого уровня']  use vision model to extract this
        max_nagruzka_sekciya=json_data['максимально допустимые нагрузки']['на весь стеллаж']
        total_data=[ [ organisation,1750, 180] , [ producer,1860, 295] , [ location,1500, 380] ,[  height,1840, 445] , [ profile,1760, 513] , [ max_nagruzka_sekciya,1850, 713] ]

        for data in total_data:
            # Define the table row parameters (coordinates for the row)
            text=data[0]
            x=data[1]
            y=data[2]
            font = ImageFont.truetype("arial.ttf", size=30)  # Use a .ttf font, adjust size as needed
            # Add the text to the image
            draw.text((x, y), str(text), font=font, fill="black")


# Save the result
image.save("output_with_table.jpg")
image.show()