from PIL import Image, ImageDraw, ImageFont
import string, random 

# generate thr random captcha string
def random_string():
    # hash length
    N = 8
    s = string.ascii_uppercase + string.ascii_lowercase + string.digits
    random_string = ''.join(random.choices(s, k=N))
    return random_string
def random_name():
    # hash length
    N = 7
    s = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # generate a random string of length 5
    random_string = ''.join(random.choices(s, k=N))
    return random_string


# lambda function - used to pick a random loaction in image
getit = lambda : (random.randrange(5, 305),random.randrange(5, 55))

# pick a random colors for points
colors = ["black","red","blue","green",(64, 107, 76),(0, 87, 128),(0, 3, 82)]

# fill_color = [120,145,130,89,58,50,75,86,98,176,]
# pick a random colors for lines
fill_color = [(64, 107, 76),(0, 87, 128),(0, 3, 82),(191, 0, 255),(72, 189, 0),(189, 107, 0),(189, 41, 0)]

# generate the captcha image
def gen_captcha_img():
    # create a img object
    img = Image.new('RGB', (300,50), color="#e9ecef")
    draw = ImageDraw.Draw(img)
    # get the random string
    captcha_str = random_string()
    # get the text color
    text_colors = random.choice(colors)
    font_name = "./demo/fonts/SansitaSwashed-SemiBold.ttf"
    font = ImageFont.truetype(font_name, 100)
    draw.text((120,20), captcha_str, fill=text_colors)
    # draw some random lines
    for i in range(5,random.randrange(6, 10)):
        draw.line((getit(), getit()), fill=random.choice(fill_color), width=random.randrange(1,3))
    print("le font marche ")
    # draw some random points
    for i in range(1,random.randrange(11, 20)):
        draw.point((getit(), getit(), getit(), getit(), getit(), getit(), getit(), getit(),getit(), getit(), getit(), getit(), getit(), getit()), fill=random.choice(colors))
    name = random_name()
    # save image in captcha_img directory
    img.save("./demo/captcha_img/"+name +".png")
    print("limage marche")
    return {"name" : name, "cap_text" : captcha_str}
    


